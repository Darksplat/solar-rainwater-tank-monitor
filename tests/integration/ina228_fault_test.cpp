#include "../../firmware/components/tank_ina228/tank_ina228.h"
#include <cassert>
#include <iostream>
using namespace esphome;
int main(){
 tank_ina228::Monitor m;sensor::Sensor v,i,p,q,t;text_sensor::TextSensor status;
 m.set_voltage(&v);m.set_current(&i);m.set_power(&p);m.set_charge(&q);m.set_die_temperature(&t);m.set_diagnostic(&status);
 m.registers={{0x3E,0x5449},{0x3F,0x2281},{0x0B,3},{0x05,0x100000},{0x07,0x100000},{0x0A,7372800},{0x06,3200}};
 m.setup();assert(status.state=="initializing");m.update();assert(status.state=="ok");
 assert(std::abs(v.state-12.8f)<1e-5 && i.state==1 && std::abs(q.state-.5f)<1e-6 && t.state==25);
 m.registers[0x07]=0xF00000;m.registers[0x0A]=(1ULL<<40)-7372800;m.update();assert(i.state==-1 && q.state==-.5f && p.state<0);
 for(int reg:{0x02,0x0B,0x05,0x07,0x0A,0x06}){
  m.failed_register=reg;m.update();assert(status.state=="i2c_fault");
  for(float x:{v.state,i.state,p.state,q.state,t.state})assert(std::isnan(x));
  m.failed_register=-1;m.update();m.update();assert(status.state=="ok");
 }
 m.registers[0x02]=0;m.update();assert(status.state=="device_reset" && std::isnan(q.state));m.update();m.update();
 for(uint64_t diag:{0ULL,512ULL,1024ULL}){
  m.registers[0x0B]=diag;m.update();assert(status.state=="conversion_fault" && std::isnan(i.state));m.registers[0x0B]=3;m.update();m.update();
 }
 m.registers[0x0B]=1;m.update();assert(status.state=="not_ready" && std::isnan(q.state));
 m.registers[0x0B]=3;m.update();assert(status.state=="ok");
 m.registers[0x3F]=0x2190;m.setup();assert(status.state=="identity_fault" && std::isnan(i.state));
 assert(tank_ina228::signed20(0x800000)==-524288);
 assert(tank_ina228::signed40(1ULL<<39)==-549755813888LL);
 std::cout<<"PASS: real INA228 driver, register decoding, every I2C read failure, reset, overflow, readiness, identity and recovery\n";
}
