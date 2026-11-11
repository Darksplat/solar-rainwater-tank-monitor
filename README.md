**Fabrication correction — 11 November 2026.** Review found that LOOP_P named both the pressure-probe terminal and the filtered positive measurement input in revision 0.2. This can bypass part of the current-limiting network through a sense resistor. The revision 0.2 PCB and manufacturing exports are superseded and require correction before fabrication. Revision 0.3 development separates the input as LOOP_SENSE_P and adds an explicit netlist check.

# Solar rainwater tank monitor

Development revision 0.2, 9 November 2026. **Engineering prototype; not released for manufacture or installation.** Two independent solar nodes; ESP32-C6, Thread MTD, pressure-loop measurement, ESPHome API to Home Assistant.

The revision includes a routed four-layer KiCad board, ERC/DRC reports, fabrication exports, FreeCAD assembly study, three-monitor firmware and battery/solar alerts. Start with [progress register](docs/progress.md), [architecture](docs/project-overview.md), [research evidence](docs/research.md) and [test report](docs/testing-report.md). Outstanding approvals, missing measurements and physical validation are explicit there. No live Home Assistant system has been modified.

Run `python3 -m unittest discover -s tests/unit -v`, then `python3 tools/power_budget.py`. Compile the shared C++ calculation tests with `c++ -std=c++17 -Wall -Wextra -Werror tests/integration/core_test.cpp -o /tmp/tank-core-test && /tmp/tank-core-test`.

Firmware: copy `firmware/secrets-example.yaml` to ignored `firmware/tank_1/secrets.yaml` and `firmware/tank_2/secrets.yaml`, setting independent real API keys and OTA passwords plus your Thread dataset, then `esphome config firmware/tank_1/tank.yaml` and `esphome compile firmware/tank_1/tank.yaml`; repeat for tank_2. Example secrets are deliberately not deployable credentials. See the installation guide before connecting any transmitter.

No rated capacity is treated as measured usable capacity. Configuration is initially uncalibrated and litres/percentage remain unavailable until calibration is enabled.

Build hardware with the [assembly guide](docs/assembly-guide.md), [electrical connection table](docs/electrical-design.md) and [manufacturing notes](hardware/pcb/manufacturing/README.md). Revision 0.1 binaries and wiring are historical and incompatible with revision 0.2.

Owner configuration is recorded in [site settings](docs/site-configuration.md): garden water, secondary fire use, no minimum-reserve display, catalogue tank height2.32m and the existing Raspberry Pi Zero2W/PoE/Sonoff Thread network. Internal geometry and operating datums remain unverified.

[Revision0.2 test images and checksums](releases/0.2.0-dev/) and [successful hosted validation](docs/publication-validation.md) are available. These are development artifacts; physical hardware and installation acceptance remain pending.
