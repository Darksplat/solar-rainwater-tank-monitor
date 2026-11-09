#pragma once
#include <cmath>
#include <cstdint>
#include <algorithm>
#include <limits>
namespace tank {
inline bool can_measure_loop(float voltage,bool input_fault=false){return !input_fault && std::isfinite(voltage) && voltage>=12.0f && voltage<=15.0f;}
class CoulombSoc {
 public:
  bool valid() const {return valid_;}
  void invalidate(){valid_=false;}
  bool confirm_full(double capacity,double counter,float voltage,float current,uint32_t now){
   if(!std::isfinite(capacity)||capacity<=0||!std::isfinite(counter)||!std::isfinite(voltage)||!std::isfinite(current)||voltage<13.8f||voltage>14.7f||std::abs(current)>capacity*.02){invalidate();return false;}
   capacity_=capacity;remaining_=capacity;previous_=counter;time_=now;valid_=true;return true;
  }
  float observe(double counter,uint32_t now,double capacity){
   if(!std::isfinite(counter)||!std::isfinite(capacity)||capacity<=0){invalidate();return unknown();}
   if(!valid_)return unknown();
   uint32_t elapsed=now-time_;
   double delta=counter-previous_;
   if(std::abs(capacity-capacity_)>1e-6||elapsed>10000||std::abs(delta)>8.0*elapsed/3600000.0+.00002){invalidate();return unknown();}
   remaining_=std::clamp(remaining_-(delta<0?delta*.99:delta),0.0,capacity_);
   previous_=counter;time_=now;return float(100*remaining_/capacity_);
  }
  static float unknown(){return std::numeric_limits<float>::quiet_NaN();}
 private:
  bool valid_=false;double capacity_=20,remaining_=0,previous_=0;uint32_t time_=0;
};
inline CoulombSoc battery_soc;
}
