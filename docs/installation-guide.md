# Installation and prototype bring-up

This is a development manual; final PCB assembly and installation instructions depend on the unresolved power/protection design. Do not order a production PCB or permanently connect a pressure probe from this revision.

## Bench firmware work

1. Install Python 3.13 and requirements.txt in an isolated environment.
2. Run tools/prepare_test_secrets.py only for compilation tests. For deployment replace every generated secrets.yaml locally with independent device API encryption keys, OTA passwords and your existing Thread dataset. Never deploy the public CI test dataset/key.
3. Validate and compile both tank configs. Initially power the DevKit from USB with no loop or battery connected. Flash via ESPHome serial upload using the detected port; retain USB recovery access.
4. Confirm Thread attachment, HA IPv6 connectivity and native API discovery. Configure each tank independently. Tank litres must remain unavailable while calibration is disabled.
5. Test with a calibrated current source and protected receiver. Do not apply 24 V to ADC pins. Confirm 0.4/2.0 V correspond to 4/20 mA at the shunt, actual shunt tolerance and ADC scale, open-loop and overload diagnostics.
6. Confirm transmitter voltage, supply switching, startup transient, settling at all temperatures and nine-sample acquisition. Until measured, the 5 s delay is provisional.
7. Complete the calibration procedure and physical acceptance matrix before tank installation.

## Solar and outdoor work

Configure the charger for the exact battery before connection. Verify battery polarity, approved charge profile and temperature cutoff. Battery fuse and wiring must be sized from selected component faults and wire ampacity. Use the charger manufacturer's connection/disconnection order. Ensure PV isolation, cold-Voc and hot-Vmp checks, short-circuit current limits and weather-rated strain relief. Panel faces north with site-specific tilt and shade survey. Prototype power model is not a commissioned solar system.

Suspend probe without tank entry or structural drilling. Keep away from inlet turbulence and sediment, verify diaphragm height and provide dry, breathable reference termination. Complete enclosure spray/condensation, RF range and winter autonomy tests. Attach device ID and calibration record. Replacing electronics must not disturb probe position.
