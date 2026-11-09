import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, i2c, text_sensor
from esphome.const import CONF_ID
DEPENDENCIES=['i2c']
AUTO_LOAD=['text_sensor']
ns=cg.esphome_ns.namespace('tank_ina228')
Monitor=ns.class_('Monitor',cg.PollingComponent,i2c.I2CDevice)
CONFIG_SCHEMA=cv.Schema({
 cv.GenerateID():cv.declare_id(Monitor),
 cv.Required('shunt_resistance'):cv.All(cv.resistance,cv.Range(min=.0001,max=10)),
 cv.Required('max_current'):cv.All(cv.current,cv.Range(min=.001,max=100)),
 cv.Optional('voltage'):sensor.sensor_schema(unit_of_measurement='V',device_class='voltage',state_class='measurement',accuracy_decimals=3),
 cv.Optional('current'):sensor.sensor_schema(unit_of_measurement='A',device_class='current',state_class='measurement',accuracy_decimals=6),
 cv.Optional('power'):sensor.sensor_schema(unit_of_measurement='W',device_class='power',state_class='measurement',accuracy_decimals=3),
 cv.Optional('charge'):sensor.sensor_schema(unit_of_measurement='Ah',state_class='measurement',accuracy_decimals=6),
 cv.Optional('die_temperature'):sensor.sensor_schema(unit_of_measurement='°C',device_class='temperature',state_class='measurement',accuracy_decimals=1),
 cv.Optional('diagnostic'):text_sensor.text_sensor_schema(),
}).extend(cv.polling_component_schema('1s')).extend(i2c.i2c_device_schema(0x40))
async def to_code(config):
 var=cg.new_Pvariable(config[CONF_ID]);await cg.register_component(var,config);await i2c.register_i2c_device(var,config)
 cg.add(var.set_shunt(config['shunt_resistance']));cg.add(var.set_max_current(config['max_current']))
 for name in ['voltage','current','power','charge','die_temperature']:
  if name in config:cg.add(getattr(var,'set_'+name)(await sensor.new_sensor(config[name])))
 if 'diagnostic' in config:cg.add(var.set_diagnostic(await text_sensor.new_text_sensor(config['diagnostic'])))
