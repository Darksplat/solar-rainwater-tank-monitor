# Engineering status report — revision0.2 development

The project now includes a complete editable electrical schematic and routed custom PCB, four-layer fabrication exports, three-monitor firmware with battery/solar reporting, two independently named builds, HA dashboard/alerts, calculation tools, CAD packaging/mounting studies and reproduction documentation. It is an engineering development snapshot; the finished outdoor monitoring system has not achieved physical acceptance.

## Completed and executed

Twelve Python tests, actual shared C++ water/battery helpers, actual INA228 driver fault tests and24 HA template scenarios pass. Both ESPHome images compile. KiCad ERC/DRC report zero violations and zero unconnected pads. Exported netlist/board/source parity and fabrication structure checks pass. Four saved FreeCAD documents,38 STEP exports and35 closed STL meshes pass geometry checks. Test reports and hashes identify the evidence and its limits.

## Designed or simulated

Worst-case DC loop compliance/current limiting, processor/radio/monitor/charger/disconnect/BMS/converter power allocations, seven-day+25% reserve, regional NASA winter radiation, cold panel voltage and estimated hot startup headroom are calculated. They are not measured system performance. Tank calibration/grid/fault simulations exercise real calculation code; they do not simulate the physical pressure transmitter, RF environment or battery chemistry. The outdoor±20mm depth target remains unverified and is not supported as an unconditional temperature-range claim.

## Awaiting hardware and supplied information

The97-component board requires independent circuit/layout review, assembler land/stencil/DC-bias confirmation, current-limited prototype bring-up and stability/thermal/surge tests. The exact probe configuration and battery cold-charge/BMS version require supplier confirmation. Discontinued20W panel stock must be secured or the PV protection redesigned for a qualified replacement. Procurement is a consolidated list with explicit unpriced/unqualified entries, not a completed purchasing quotation.

The cabinet and equipment CAD includes actual board geometry and stated commercial envelopes, a metal shelf/straps, spacers, exploded assembly and solar/post study. Vendor fixing patterns, cable diameters, probe dimensions, site wind/soil and load/ingress/condensation tests remain open. The cabinet manufacturer currently statesIP65; the assembled cabinet has no demonstrated rating. No tank drilling is authorized.

Owner measurements are needed for internal tank dimensions, outlet/diaphragm/max-fill datums, cable route, shade. Real HA/Thread border-router access and physical devices are required for commissioning, RF/OTA/restart/alert tests. Real network credentials must remain local. No manufactured board, installed sensor, validated battery autonomy, calibrated litre measurement or live HA modification is claimed.

## Reproduction entry points

Start with README, assembly-guide, electrical-design, solar-power-design, mechanical-design, installation-guide, calibration-guide and testing-report. The progress register preserves open gates. Historical0.1 wiring/binaries are incompatible. The0.2 release directory contains only explicitly marked test-fixture images; build new images with independent owner secrets before use. GitHub publication and hosted validation are recorded separately with actual commit/run links.

Owner configuration: both tanks supply the garden, one has secondary fire use, and no minimum-reserve display is requested. Catalogue height is 2.32 m; original 4 m height assumptions are superseded. The existing Raspberry Pi Zero2W/PoE/Sonoff radio already runs Thread and is to be retained. See site-configuration.md.
