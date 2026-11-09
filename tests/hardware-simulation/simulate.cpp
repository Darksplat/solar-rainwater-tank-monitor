#include "../../firmware/common/tank_core.h"
#include <iostream>
int main(){
 tank::Calibration c;c.enabled=true;c.length=2;c.width=1.3;
 std::cout<<"scenario,reference_depth_m,current_ma,status,reported_depth_m,usable_litres\n";
 for(float d:{0.0f,0.25f,0.5f,1.f,1.5f,2.f,2.5f,3.f,3.5f,3.85f}){
  float ma=4+std::max(0.f,d-c.diaphragm)*c.density*c.gravity/c.pressure_pa*16;
  auto r=tank::calculate(ma,c);
  std::cout<<"synthetic_depth,"<<d<<","<<ma<<","<<tank::status_text(r.status)<<","<<r.depth<<","<<r.usable_litres<<"\n";
 }
 for(float ma:{0.f,3.5f,21.1f,24.f,tank::nan}){
  auto r=tank::calculate(ma,c);
  std::cout<<"injected_current_fault,nan,"<<ma<<","<<tank::status_text(r.status)<<","<<r.depth<<","<<r.usable_litres<<"\n";
 }
}
