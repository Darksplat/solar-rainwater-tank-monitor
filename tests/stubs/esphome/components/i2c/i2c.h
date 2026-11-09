#pragma once
#include <map>
#include <cstdint>
#include <cstddef>
namespace esphome {namespace i2c {
enum ErrorCode {ERROR_OK,ERROR_UNKNOWN};
class I2CDevice {public:
 std::map<uint8_t,uint64_t> registers;
 int failed_register=-1;bool fail_write=false;
 ErrorCode read_register(uint8_t r,uint8_t *b,size_t n){if(r==failed_register)return ERROR_UNKNOWN;uint64_t v=registers[r];for(size_t i=0;i<n;i++)b[n-1-i]=uint8_t(v>>(i*8));return ERROR_OK;}
 bool write_byte_16(uint8_t r,uint16_t v){if(fail_write)return false;registers[r]=v;return true;}
};
}}
