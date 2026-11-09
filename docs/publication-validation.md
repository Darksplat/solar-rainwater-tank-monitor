# Public publication verification — 9 November 2026

Owner explicitly approved public upload. Repository: https://github.com/Darksplat/solar-rainwater-tank-monitor

Verified source commit: 7f9897994c87a630d14c01c278581503f21c4c54. All 76 tracked files were uploaded through the connected GitHub service and fetched back. The only byte difference from the local package was CSV CRLF-to-LF normalization. Deployment secrets and build-cache directories were excluded.

Hosted run: https://github.com/Darksplat/solar-rainwater-tank-monitor/actions/runs/42549543964

- calculations: completed, success (10 Python tests plus C++ core assertions).
- firmware (tank_1): completed, success (ESPHome configuration validation and device compilation).
- firmware (tank_2): completed, success (ESPHome configuration validation and device compilation).

This evidence proves software build reproducibility on the hosted Linux runners. It does not establish physical accuracy, electrical safety, outdoor reliability or manufacturing readiness. See final-engineering-report.md for incomplete work. Publication was through the connector because local Git has no saved GitHub sign-in; local stage history and local tag were not pushed.
