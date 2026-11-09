#include "../../firmware/common/battery_core.h"
#include <cassert>
#include <cmath>
#include <iostream>
int main(){
 assert(!tank::can_measure_loop(12.8f,true));
 assert(!tank::can_measure_loop(NAN));assert(!tank::can_measure_loop(11.9f));assert(!tank::can_measure_loop(15.1f));assert(tank::can_measure_loop(12.0f));assert(tank::can_measure_loop(15.0f));
 tank::CoulombSoc s;assert(std::isnan(s.observe(0,0,20)));
 assert(!s.confirm_full(20,0,12.8,0,0));
 assert(!s.confirm_full(20,0,14.2,1,0));
 assert(s.confirm_full(20,0,14.2,0.1,0));
 double q=0;
 for(uint32_t now=1000;now<=3600000;now+=1000){q+=1.0/3600;s.observe(q,now,20);}
 assert(std::abs(s.observe(q,3600000,20)-95)<.001);
 assert(std::isnan(s.observe(q,3620000,20))); // unobserved interval invalidates SOC
 assert(s.confirm_full(20,0,14.2,0,0));assert(std::isnan(s.observe(-1,1000,20))); // reset/discontinuity
 assert(s.confirm_full(20,0,14.2,0,0));assert(std::isnan(s.observe(0,1000,10))); // capacity changed
 assert(s.confirm_full(20,0,14.2,0,0));assert(std::isnan(s.observe(NAN,1000,20)));
 assert(s.confirm_full(20,0,14.2,0,0xFFFFFF00));assert(std::isfinite(s.observe(0,0x000002E8,20))); // millis wrap
 std::cout<<"PASS: coulomb SOC, verified-full guard, 1Ah discharge, gaps, resets, capacity changes and timer wrap\n";
}
