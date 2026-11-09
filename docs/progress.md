# Progress register — revision 0.2, 9 November 2026

Development continues from the original prototype; no physical acceptance or production release is claimed.

| Work | Current evidence | Remaining gate |
|---|---|---|
| Architecture / calculations | Two independent nodes, protected power paths, calibrated geometry and battery/PV/loop telemetry | Real tank geometry, outlet and diaphragm datum |
| Electronics | 97-component KiCad schematic and 101-footprint four-layer PCB; native ERC/DRC reports and exported netlist checks | Independent hardware review, effective capacitor/thermal/stability/surge qualification |
| Current sensing | Three INA228s, high-side precision shunts, six dedicated Kelvin branches | Traceable current-source calibration and measured drift |
| Solar | Full component allowances, NASA regional climatology, cold-Voc/hot-Vmp model, seven-day +25% energy margin | Site shading, actual draw/cold capacity, exact battery BMS confirmation and panel stock |
| Firmware | Tank1/Tank2 compile; real-driver fault injection, battery SOC and water-core assertions pass | Serial flash, analog readings, power cycling, watchdog/OTA/Thread soak on hardware |
| Home Assistant | Dashboard, water/power automations and histories;24 Jinja scenarios and YAML parsing pass | Owner's HA entity IDs, configuration/runtime validation, alerts and reconnection |
| Mechanical | Editable cabinet packaging, actual board body, battery shelf/straps, exploded assembly and solar/post study; valid solids and STEP checks | Vendor fixing patterns, sensor configured drawing, cable diameters, structural/site review and dry fit |
| Manufacturing | Gerbers, separated drills/maps, BOM, SMD positions, assembly illustration, board STEP | Assembler/fabricator CAM and stencil review, prototype manufacture/bring-up |
| Purchasing |73 consolidated two-unit lines; PCB candidate MPNs and identified major equipment | Exact configured sensor order, outstanding quotes/direct offers, shipping and site cut lengths |
| Documentation | Revision2 electrical, power, assembly, installation, calibration, HA, sourcing and validation instructions | Incorporate measured commissioning results |
| GitHub | Public repository authorized by owner; initial0.1 source/builds previously published | Publish and verify this revised development package and its CI run |

External dependencies: hardware and traceable test instruments; actual internal tank measurements; sensor/battery supplier confirmations; remaining discontinued-panel stock; current bought-part fixing drawings; site cable/shade/wind/soil information; access to the existing Thread border router and HA environment. No private credentials or physical measurements have been fabricated.

Open engineering/procurement work is not automatically classified as physical testing: outstanding exact supplier offers, capacitor characterization and vendor mounting patterns remain explicit. The rack is a packaging study, not a structural design. The cabinet manufacturer currently specifies IP65; the assembled enclosure has not passed ingress testing. Keep all production gates open until evidence closes them.
