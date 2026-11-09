#include "tank_ina228.h"
#include "esphome/core/hal.h"
#include <initializer_list>
namespace esphome { namespace tank_ina228 {
bool Monitor::read_(uint8_t reg,uint8_t count,uint64_t &v){
 uint8_t b[5]{};
 if(count>5 || this->read_register(reg,b,count)!=i2c::ERROR_OK)return false;
 v=0;for(uint8_t i=0;i<count;i++)v=(v<<8)|b[i];return true;
}
void Monitor::fail_(const char *reason,bool reinitialize){
 // Invalidate the complete sample; never publish an I2C failure as a fresh zero.
 for(auto *s:{voltage_,current_,power_,charge_,temperature_})if(s)s->publish_state(NAN);
 if(diagnostic_)diagnostic_->publish_state(reason);
 this->status_set_warning();if(reinitialize)initialized_=false;
}
bool Monitor::initialize_(){
 uint64_t manufacturer=0,device=0;
 if(!read_(0x3E,2,manufacturer)||!read_(0x3F,2,device)){fail_("i2c_fault");return false;}
 if(manufacturer!=0x5449 || (device>>4)!=0x228){fail_("identity_fault");return false;}
 current_lsb_=max_current_/524288.0f;
 double cal=13107200000.0*current_lsb_*shunt_;
 if(!std::isfinite(cal)||cal<1||cal>32767||max_current_*shunt_>0.16384){fail_("invalid_config");return false;}
 calibration_=uint16_t(std::lround(cal));
 if(!this->write_byte_16(0x00,0x8000)){fail_("i2c_fault");return false;}
 delay(2);
 // ADCRANGE=0, continuous all channels, 1052 us/channel, 16 averages (~50.5ms).
 if(!this->write_byte_16(0x00,0)||!this->write_byte_16(0x02,calibration_)||!this->write_byte_16(0x01,0xFB6A)){
  fail_("i2c_fault");return false;
 }
 initialized_=true;
 // Resetting the charge accumulator invalidates any prior SOC reference.
 fail_("initializing",false);
 return true;
}
void Monitor::setup(){initialize_();}
void Monitor::update(){
 if(!initialized_){initialize_();return;}
 uint64_t cal=0,diag=0,bus=0,current=0,charge=0,temp=0;
 if(!read_(0x02,2,cal)||!read_(0x0B,2,diag)||!read_(0x05,3,bus)||!read_(0x07,3,current)||!read_(0x0A,5,charge)||!read_(0x06,2,temp)){
  fail_("i2c_fault");return;
 }
 if(cal!=calibration_){fail_("device_reset");return;}
 if(!(diag&1)||diag&0x600){fail_("conversion_fault");return;}
 if(!(diag&2)){fail_("not_ready",false);return;}
 float v=float(bus>>4)*0.0001953125f;
 float a=float(signed20(current))*current_lsb_;
 float ah=float(double(signed40(charge))*16.0*current_lsb_/3600.0);
 float t=float(int16_t(temp))*0.0078125f;
 if(!std::isfinite(v)||v<0||v>85||!std::isfinite(a)||!std::isfinite(ah)) {fail_("invalid_data");return;}
 // Publish only after every required register and diagnostic check has succeeded.
 if(voltage_)voltage_->publish_state(v);
 if(current_)current_->publish_state(a);
 if(power_)power_->publish_state(v*a);
 if(temperature_)temperature_->publish_state(t);
 if(charge_)charge_->publish_state(ah);
 if(diagnostic_)diagnostic_->publish_state("ok");
 this->status_clear_warning();
}
}}
