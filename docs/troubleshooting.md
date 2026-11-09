# Troubleshooting

| Symptom | Check |
|---|---|
| Uncalibrated | Enter verified geometry or verified reference-volume method, then enable calibration |
| Below probe unresolved | Water may be below diaphragm; confirm physically; do not force zero litres |
| Loop low | Probe supply off/faulted, broken wire, insufficient compliance or disconnected sensor |
| Loop high | Wrong transmitter range/output, loop fault or overrange; isolate power before probing |
| ADC fault | 3.3 V, I2C pullups/address, bus continuity; no 24 V on ADC inputs |
| Unstable | Bubbles/turbulence, settling, grounding, reference tube moisture or supply noise |
| Above max | Check actual operating level, range, zero/span and diaphragm datum |
| API connects but measurements stale | Sequence counter, ADC task and sensor switching; connectivity alone is insufficient |
| Thread attaches but HA unreachable | IPv6 route/firewall and border-router path |
| OTA unavailable | Enable ten-minute maintenance window (poll period 0) and keep USB recovery available |
| Night charging off | Normal; diagnose solar failure only with daylight and battery/temperature context |
| Implausible tank volume | Do not equate rated label to measured usable volume; verify dimensions and datums |

Service atmospheric reference desiccant/filter, inspect glands and corrosion, clean cage and verify probe elevation without blocking pressure openings. Annual repeat calibration establishes drift. Component replacement procedure awaits released PCB BOM and approved enclosure assembly.
