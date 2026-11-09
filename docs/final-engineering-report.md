# Development handover report — 0.1.0-dev

The requested finished hardware product is **not complete**. This revision preserves actual source work and test evidence; it is not a manufacturing release.

Fully completed and tested within limited software scope: shared depth/volume calculation core, calibration regression tool, power sensitivity model, fault-input tests, C++ host compilation, Python tests and syntax checks. Both ESPHome configurations compile as recorded in build-summary.json. FreeCAD concept solids and STEP/STL exports were generated and roundtrip-checked.

Completed as examples/simulations only: sensor input scenario CSV, conservative seven-day energy model, HA dashboard/templates/water alerts (YAML parsing, not HA runtime validation). No measured electrical consumption or verified site winter solar yield exists.

Designed as preliminary concepts awaiting engineering and physical validation: two-node architecture, loop measurement interface, tray/standoffs/probe cage, pressure candidate and solar/battery capacity candidates. Fit, protection coordination, wind loading, ingress and accuracy are not established.

Incomplete engineering deliverables: full production schematic and PCB, verified footprints, Gerber/drill/CPL/assembly files, final PCB 3D model, protected power/analog implementation, hardware-supported battery SOC and solar telemetry, battery/solar alert logic, final enclosure and panel mounts, complete qualified BOM/costs, final reproducible assembly manual and full hardware/system tests. These are not merely waiting to be manufactured.

External dependencies: configured sensor quote/order drawing, owner/site geometry and operating levels, current supplier availability and component quotations, real hardware and traceable test instruments, HA/Thread commissioning environment and repository-creation access. Owner created the GitHub repository and supplied its URL; existence verified through the connector: https://github.com/Darksplat/solar-rainwater-tank-monitor (public). The owner explicitly approved public upload on 9 November 2026. Hosted validation evidence is recorded separately from local test evidence.

Resume using progress.md. The next engineering gate is a fully selected protected circuit and approved component drawings, followed by complete KiCad schematic/PCB review. Do not purchase unqualified candidate parts from the partial BOM or represent prototype CAD as an IP-rated enclosure.
