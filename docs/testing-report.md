# Verification report — 9 November 2026

This report distinguishes actual software execution from physical hardware behavior. No water-depth measurement, RF-range test, battery-autonomy test, ingress test or manufactured PCB test was performed.

| Test | Procedure | Expected | Actual | Status |
|---|---|---|---|---|
| Calculation core | Compile C++17 with warnings as errors and execute assertions | Depth grid, volume, independent method and faults correct | All assertions passed | PASS software only |
| Python unit suite | unittest discovery | Power/calibration validity and boundaries pass | 10 tests passed | PASS software only |
| Synthetic sensor scenarios | Compile/run simulator against same C++ header | Valid grid plus invalid faults | CSV saved, including unresolved empty region | PASS simulation only |
| Python static syntax | compileall for tools/tests/CAD generator | No syntax errors | Completed successfully | PASS syntax only |
| HA/dashboard/workflow YAML | safe-load five files | Parse without syntax errors | Five parsed | PASS parsing only; no HA runtime schema check |
| Tank 1 ESPHome | ESPHome 2026.10.2, ESP-IDF 5.5.6, esp32-c6-devkitc-1, compile | Produce app and factory/OTA images | See build-summary.json | Compiler evidence only |
| Tank 2 ESPHome | Same toolchain, distinct device name | Independent images | See build-summary.json | Compiler evidence only |
| CAD solid validation | FreeCAD 1.1.4 generator | Positive-volume valid solids | Seven checked | PASS geometry only |
| CAD reopen/STEP roundtrip | Reopen FCStd and read STEP, compare volume | One solid and unchanged volume | Differences below 1e-4 mm³ | PASS export geometry only |
| STL roundtrip | Load exported meshes | Closed meshes | Seven closed meshes | PASS mesh closure only |
| Electrical/PCB | Complete schematic ERC/board DRC/export audit | Reviewed and passing | Complete circuit/layout absent | NOT RUN / INCOMPLETE |
| Physical acceptance | Procedures in hardware-validation.md | Measured evidence | Hardware unavailable | NOT RUN |
| HA runtime/network/OTA | Actual HA and Thread network | Reconnect, alerts and OTA verified | No device/network session supplied | NOT RUN |
| GitHub Actions | Push to actual GitHub repository | Hosted validation run | Repository created by owner; hosted run pending | NOT RUN |

Corrective actions during this work:

- Initial 15 Ah autonomy check failed: 122.88 Wh usable <130.82 Wh required. Increased provisional battery to 20 Ah (163.84 Wh usable). No load assumption was reduced to make the test pass.
- 20 W panel restores the margin-inclusive reserve too slowly under the assumed 1.5 PSH / 60% yield; provisional 40 W candidate retained for compatibility review.
- Initial C++ host test hit ambiguous `nan` identifier; qualified it as `tank::nan` and reran successfully.
- Initial ESPHome configuration rejected public test API key formatting; fixed the test fixture and validated. Production credentials remain owner-local.
- Initial device compilation failed from ambiguous empty-array initialization; changed to explicitly typed std::array initialization and compiled successfully.
- Shared package originally resolved secrets beside common YAML; moved secret references to each tank configuration so each device can use independent credentials. Both final builds must pass before recording release checksums.
- FreeCAD initially failed because its normal cache path was inaccessible. Authorized run with normal cache access succeeded; models were then reopened and exports roundtrip-checked.

Evidence files: tests/test-results/unit-tests.txt, firmware-core.txt, synthetic-pressure.csv, power-budget.json and build-summary.json; hardware/cad/validation.json and roundtrip-validation.json. Binary images are compilation fixtures with public test network/key: DO NOT DEPLOY.

Limits: the simulator covers calculation inputs, not analog transient response, sensor warmup, network recovery, BMS behavior or solar charging. Passing firmware compilation does not prove any hardware behavior. Accuracy target ±20 mm remains unverified and is not guaranteed by the present worst-case error budget.
