#include "../../firmware/common/tank_core.h"
#include <iostream>
#include <cassert>
int main(){
 tank::Calibration c;c.enabled=true;c.length=4;c.width=1.15f;c.corner_radius=.575f;
 c.max_level=2.17f;c.usable_depth=2.12f;c.pressure_pa=40000;
 // These are synthetic catalogue-envelope inputs, not measured tank geometry.
 std::cout<<"scenario,reference_depth_m,loop_mA,status,calculated_depth_m,total_litres,usable_litres,percent\n";
 for(float depth:{0.f,.25f,.5f,1.f,1.5f,2.f,2.17f,2.32f}){
  float ma=depth<=c.diaphragm?4:4+(depth-c.diaphragm)*c.density*c.gravity/c.pressure_pa*16;
  auto r=tank::calculate(ma,c);
  if(depth>c.diaphragm&&depth<=c.max_level){assert(r.status==tank::Status::ok);assert(std::abs(r.depth-depth)<1e-5);}
  std::cout<<"synthetic_rounded_catalogue,"<<depth<<','<<ma<<','<<int(r.status)<<','<<r.depth<<','<<r.total_litres<<','<<r.usable_litres<<','<<r.percent<<'\n';
 }
}
