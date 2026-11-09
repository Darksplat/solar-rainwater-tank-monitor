#pragma once
#include <limits>
namespace esphome {namespace sensor {class Sensor {public:float state=std::numeric_limits<float>::quiet_NaN();void publish_state(float v){state=v;}};}}
