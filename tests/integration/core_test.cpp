#include "../../firmware/common/tank_core.h"
#include <cassert>
#include <iostream>
int main(){
 using namespace tank;
 Calibration c; c.enabled=true;c.length=2;c.width=1.3;
 auto current=[&](float depth){return 4+(depth-c.diaphragm)*c.density*c.gravity/c.pressure_pa*16;};
 for(float depth: {0.25f,0.5f,1.0f,1.5f,2.0f,2.5f,3.0f,3.5f,3.85f}){
   auto r=calculate(current(depth),c);assert(r.status==Status::ok);
   assert(std::abs(r.depth-depth)<0.00001f);
   assert(std::abs(r.total_litres-depth*2600)<0.01f);
 }
 assert(calculate(4,c).status==Status::blind_region);
 assert(calculate(0,c).status==Status::loop_low);
 assert(calculate(24,c).status==Status::loop_high);
 assert(calculate(tank::nan,c).status==Status::adc_fault);
 assert(calculate(current(4),c).status==Status::above_max);
 auto full=calculate(current(3.85),c); assert(std::abs(full.percent-100)<0.001);
 assert(std::abs(full.usable_litres-9880)<0.1);
 c.enabled=false;assert(calculate(10,c).status==Status::uncalibrated);c.enabled=true;
 c.width=0;assert(calculate(10,c).status==Status::invalid_calibration);
 c.manufacturer_method=true;c.verified_litres=10000;c.reference_depth=3.85;
 assert(std::abs(calculate(current(3.85),c).total_litres-10000)<0.1);
 c.density=tank::nan;assert(!c.valid());
 std::array<float,9> a={10,10,10,10,10,10,10,10,11};
 assert(robust_current(a)==10);a[0]=3;assert(!std::isfinite(robust_current(a)));
 a={8,9,10,11,12,13,14,15,16};assert(!std::isfinite(robust_current(a)));
 std::cout<<"PASS: shared firmware core depth grid, volume, faults, blind zone, calibration and filtering\n";
}
