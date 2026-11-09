#pragma once
#include "esphome/core/component.h"
#include "esphome/components/i2c/i2c.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/text_sensor/text_sensor.h"
#include <cmath>
#include <cstdint>
namespace esphome { namespace tank_ina228 {
class Monitor : public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void update() override;
  float get_setup_priority() const override {return setup_priority::DATA;}
  void set_shunt(float v){shunt_=v;}
  void set_max_current(float v){max_current_=v;}
  void set_voltage(sensor::Sensor *s){voltage_=s;}
  void set_current(sensor::Sensor *s){current_=s;}
  void set_power(sensor::Sensor *s){power_=s;}
  void set_charge(sensor::Sensor *s){charge_=s;}
  void set_die_temperature(sensor::Sensor *s){temperature_=s;}
  void set_diagnostic(text_sensor::TextSensor *s){diagnostic_=s;}
 protected:
  bool initialize_();
  bool read_(uint8_t reg,uint8_t count,uint64_t &v);
  void fail_(const char *reason,bool reinitialize=true);
  float shunt_=0.01f,max_current_=8,current_lsb_=0;
  uint16_t calibration_=0;
  bool initialized_=false;
  sensor::Sensor *voltage_=nullptr,*current_=nullptr,*power_=nullptr,*charge_=nullptr,*temperature_=nullptr;
  text_sensor::TextSensor *diagnostic_=nullptr;
};
inline int32_t signed20(uint64_t v){uint32_t n=uint32_t(v>>4)&0xFFFFF;return (n&0x80000)?int32_t(n)-0x100000:int32_t(n);}
inline int64_t signed40(uint64_t v){return (v&(1ULL<<39))?int64_t(v)-int64_t(1ULL<<40):int64_t(v);}
}}
