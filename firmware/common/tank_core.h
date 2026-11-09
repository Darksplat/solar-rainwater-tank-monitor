#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include <cstddef>
#include <limits>
namespace tank {
constexpr float nan = std::numeric_limits<float>::quiet_NaN();
enum class Status { ok, uncalibrated, adc_fault, loop_low, loop_high, unstable, blind_region, above_max, invalid_calibration };
struct Calibration {
 bool enabled=false, manufacturer_method=false;
 float length=0, width=0, corner_radius=0, usable_depth=3.8f, diaphragm=0.05f, rated_litres=10000,
       max_level=3.85f, verified_litres=0, reference_depth=0,
       zero_ma=4, span_ma=16, pressure_pa=60000, density=998.2f, gravity=9.80665f;
 bool valid() const {
  const float vals[]={length,width,corner_radius,usable_depth,diaphragm,rated_litres,max_level,verified_litres,reference_depth,zero_ma,span_ma,pressure_pa,density,gravity};
  for(float v:vals) if(!std::isfinite(v)) return false;
  return corner_radius>=0 && diaphragm>=0 && usable_depth>0 && max_level>diaphragm && usable_depth<=max_level &&
    rated_litres>0 && span_ma>0 && pressure_pa>0 && density>900 && density<1100 && gravity>9 && gravity<10 &&
    (manufacturer_method ? verified_litres>0 && reference_depth>0 : length>0 && width>0 && 2*corner_radius<=std::min(length,width));
 }
 float litres_per_m() const {return manufacturer_method ? verified_litres/reference_depth : (length*width-(4.0f-3.14159265358979323846f)*corner_radius*corner_radius)*1000;}
};
struct Result {Status status; float depth=nan, total_litres=nan, usable_litres=nan, capacity=nan, percent=nan;};
inline Status loop_status(float ma) {
 if(!std::isfinite(ma)) return Status::adc_fault;
 if(ma<3.6f) return Status::loop_low;
 if(ma>21.0f) return Status::loop_high;
 return Status::ok;
}
inline Result calculate(float ma,const Calibration &c) {
 Status s=loop_status(ma); if(s!=Status::ok) return {s};
 if(!c.enabled) return {Status::uncalibrated};
 if(!c.valid()) return {Status::invalid_calibration};
 float head=(ma-c.zero_ma)/c.span_ma*c.pressure_pa/(c.density*c.gravity);
 // The probe cannot observe the water surface below its diaphragm.
 if(head<=0) return {Status::blind_region};
 float depth=head+c.diaphragm;
 if(depth>c.max_level+0.02f) return {Status::above_max};
 depth=std::min(depth,c.max_level);
 float usable=std::max(0.0f,depth-(c.max_level-c.usable_depth));
 float k=c.litres_per_m();
 return {Status::ok,depth,depth*k,usable*k,c.usable_depth*k,100*usable/c.usable_depth};
}
inline float robust_current(std::array<float,9> a,float max_spread=0.08f) {
 for(float v:a) if(loop_status(v)!=Status::ok) return nan;
 std::sort(a.begin(),a.end());
 // Central seven must agree; one extreme at either end may be rejected.
 if(a[7]-a[1]>max_spread) return nan;
 return a[4];
}
inline const char *status_text(Status s) {
 switch(s){
 case Status::ok:return "ok";case Status::uncalibrated:return "uncalibrated";
 case Status::adc_fault:return "adc_fault";case Status::loop_low:return "loop_low";
 case Status::loop_high:return "loop_high";case Status::unstable:return "unstable";
 case Status::blind_region:return "below_probe_unresolved";case Status::above_max:return "above_max";
 default:return "invalid_calibration";
 }
}
}
