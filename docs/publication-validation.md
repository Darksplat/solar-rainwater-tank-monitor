# Public publication verification — 9 November 2026

Owner explicitly approved public upload to [Darksplat/solar-rainwater-tank-monitor](https://github.com/Darksplat/solar-rainwater-tank-monitor).

## Revision 0.2 engineering package

Verified engineering commit: [b0488ada47bff8b3b8d8a9ba1fb985d7d36acffa](https://github.com/Darksplat/solar-rainwater-tank-monitor/commit/b0488ada47bff8b3b8d8a9ba1fb985d7d36acffa). The published Git tree contains 253 files; every blob hash matches the local engineering snapshot exactly. Binary CAD, manufacturing outputs and test-only firmware were transferred without text conversion. Deployment secrets, build caches and local Git history were excluded.

Hosted validation: [run 42574612013](https://github.com/Darksplat/solar-rainwater-tank-monitor/actions/runs/42574612013).

| Job | Observed final result |
|---|---|
| calculations | Completed, success: 12 Python tests, production C++ water/battery helpers, actual INA228 driver fault injection, 24 HA template scenarios, synthetic Kingspan geometry and source/manufacturing evidence audits |
| firmware (tank_1) | Completed, success: ESPHome configuration validation and compilation |
| firmware (tank_2) | Completed, success: ESPHome configuration validation and compilation |

The subsequent documentation-only follow-up records this result and corrects commissioning wording. It changes no circuit, firmware, HA configuration, manufacturing or CAD source. The native KiCad/FreeCAD evidence was executed locally and its recorded hashes checked by hosted CI; those desktop applications were not run on the Linux runner.

`releases/0.2.0-dev/` is a versioned development directory with test-fixture images and exact firmware source hashes, not a GitHub tag or production release. No public fixture image has been physically flashed or commissioned. Build with owner-local credentials before deployment.

## Historical revision 0.1

[Run 42549543964](https://github.com/Darksplat/solar-rainwater-tank-monitor/actions/runs/42549543964) passed at commit 7f9897994c87a630d14c01c278581503f21c4c54. That older wiring and firmware are incompatible with the revision0.2 board.

These results establish build/software and file-transfer evidence, not physical accuracy, hardware stability, outdoor reliability, structural approval or manufacturing readiness. See final-engineering-report.md and hardware-validation.md for remaining gates. Publication used the connected GitHub service; local author history and tags were not pushed.
