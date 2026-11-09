# Electrical design review — preliminary, release blocked

At 100 ohm shunt: 4 mA = 0.4 V; 20 mA = 2 V; 24 mA = 2.4 V; dissipation at 24 mA = 57.6 mW. Specify 0.05%, <=10 ppm/K, >=0.25 W. ADS1115 3.3 V supply, +/-4.096 V PGA, single-ended A0 to ground. PGA range is NOT permission to exceed either supply rail. ADC resolution at this gain is 125 uV = 1.25 uA = ~0.48 mm for 60 kPa span, before noise/errors.

24 V loop at minimum 22.8 V: at 24 mA, shunt drops 2.4 V; 10 m cable using catalog 0.14 ohm/m drops 0.0336 V. Available transmitter voltage exceeds 20 V before protection drops, above 10 V requirement. A 12.8 V direct loop is rejected near battery discharge due to insufficient compliance.

A normal-current calculation is NOT an overvoltage protection design. A loop-return short to 24 V can put 24 V across the shunt (5.76 W) and destroy an ADC. Final PCB needs validated current limiting, shunt overload behavior, series ADC resistance, precision input clamps with a sink-capable rail, RC filtering, reverse input blocking and power-off backfeed protection. Do not wire loop return directly to A0 on an unprotected production PCB. TVS alone is insufficient. Ground-loop/shield strategy and surge testing remain open.

Proposed signals: GPIO6 SDA, GPIO7 SCL (confirm board pin use); GPIO10 sensor enable to driver, with hardware pulldown; ADS1115 ADDR low at 0x48; A0 protected loop signal; A1 divided protected battery; A2 divided protected PV; A3 spare. ESP32 pins must never directly switch 24 V. Test points: battery, 3V3, 24V, ground, shunt, SDA, SCL, enable, UART TX/RX, BOOT and EN. Antenna must project away from metal tank and battery; verify module keepout from Espressif drawing.

Battery and PV dividers, charger interface and current telemetry are NOT finalized. Firmware does not fabricate readings for unimplemented hardware. No schematic/PCB is released: exact sensor order drawing, regulator/charger choices, protection coordination and official footprints must be resolved first. Manufacturing files must not be generated from an electrically incomplete board.
