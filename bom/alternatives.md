# Substitution rules

Revision 0.1 DevKit/WROOM/ADS1115/100Ω/24V parts are historical and are not substitutes for revision 0.2. The selected module is ESP32-C6-MINI-1-N4 and three INA228AIDGSR monitors are required.

INA229 uses SPI and is not a drop-in. INA226 has lower input-voltage and different register capabilities; do not fit it in the similar package. TPS61170, AP63203 and the inductors require their specified pinouts, saturation/current ratings, compensation and capacitance. Verify effective capacitor values under DC bias and temperature, not just printed nominal capacitance. TVSs must retain standoff/clamp coordination over the actual waveform; a higher-voltage TVS is not automatically safer.

Two current-series Victron 30 W panels exceed the SMBJ51A standoff in the cold-Voc model and require protection redesign. A single nominal 12 V 40 W panel can fail the MPPT's battery+5 V startup condition in heat. Equivalent wattage does not establish voltage compatibility.

A substitute LiFePO4 pack needs independently confirmed cell-level BMS, cold-charge inhibit, current/capacity/temperature specifications, dimensions and matching charge profile. BatteryProtect is load-only and must not carry reverse charge current. Another disconnect must preserve both safe cutoff and a recharge path.

WIKA pressure-range substitutions require new calibration/span settings and accuracy calculations. Do not substitute an unvented absolute-pressure transmitter or an unapproved cable/diaphragm for consumed water. Sensor current limits and minimum loop voltage must satisfy the bounded circuit calculations.
