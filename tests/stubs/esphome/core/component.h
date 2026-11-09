#pragma once
namespace esphome {
namespace setup_priority {constexpr float DATA=600;}
class PollingComponent {public:virtual ~PollingComponent()=default;virtual void setup(){};virtual void update(){};virtual float get_setup_priority()const{return 0;}void status_set_warning(){warning=true;}void status_clear_warning(){warning=false;}bool warning=false;};
}
