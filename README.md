# Solar rainwater tank monitor

Development revision 0.1, 9 November 2026. **Engineering prototype; not released for manufacture or installation.** Two independent solar nodes; ESP32-C6, Thread MTD, pressure-loop measurement, ESPHome API to Home Assistant.

Start with [progress register](docs/progress.md), [architecture](docs/project-overview.md), [research evidence](docs/research.md) and [test report](docs/testing-report.md). Outstanding approvals, missing measurements and physical validation are explicit there. No live Home Assistant system has been modified.

Run `python3 -m unittest discover -s tests/unit -v`, then `python3 tools/power_budget.py`. Compile the shared C++ calculation tests with `c++ -std=c++17 -Wall -Wextra -Werror tests/integration/core_test.cpp -o /tmp/tank-core-test && /tmp/tank-core-test`.

Firmware: copy `firmware/secrets-example.yaml` to ignored `firmware/tank_1/secrets.yaml` and `firmware/tank_2/secrets.yaml`, setting independent real API keys and OTA passwords plus your Thread dataset, then `esphome config firmware/tank_1/tank.yaml` and `esphome compile firmware/tank_1/tank.yaml`; repeat for tank_2. Example secrets are deliberately not deployable credentials. See the installation guide before connecting any transmitter.

No rated capacity is treated as measured usable capacity. Configuration is initially uncalibrated and litres/percentage remain unavailable until calibration is enabled.
