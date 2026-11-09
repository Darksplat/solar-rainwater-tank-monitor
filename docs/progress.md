# Progress register — 9 November 2026

Status is development, not acceptance. No production release, manufacture, purchase, physical installation or live HA changes claimed.

| Phase | Status | Evidence / next action |
|---|---|---|
| 1 Research | partial | Primary sources checked; configured sensor order code, full parts qualification and winter site data outstanding |
| 2 Engineering | partial | Tested geometry/power math; final load current and panel/charger compatibility unresolved |
| 3 Electronics | incomplete | Proposed interface and fault analysis; complete protected circuit, schematic, footprints, layout and ERC/DRC absent |
| 4 Mechanical | prototype | Editable FreeCAD tray/cage/standoffs and exports; fit, enclosure, mounts and environmental tests pending |
| 5 Firmware | prototype | Shared calculation core, two-node ESPHome; see testing-report for actual build state; battery/solar telemetry absent |
| 6 Home Assistant | examples | Dashboard and water alerts; parse validation only; battery/solar functions pending |
| 7 Simulation | partial | Calculation and power tests; no RF/network/BMS or physical claims |
| 8 Manufacturing | blocked by design maturity | No Gerbers/drills/CPL or assembly-ready BOM |
| 9 Documentation | development manual | Instructions explicitly distinguish missing final assembly details |
| 10 Validation | partial | Automated evidence report; physical matrix pending |

External inputs needed: measured tank geometry/outlet/max level, probe cable route and water-use classification; supplier quote with configured order code/current drawings; hardware and traceable current/depth references; actual solar shading/winter data; Thread border-router/site coverage; GitHub repository creation access. The owner created https://github.com/Darksplat/solar-rainwater-tank-monitor and supplied its URL. Connector verification confirms the repository exists and is PUBLIC. The owner explicitly approved public upload on 9 November 2026. Upload and hosted validation results are checked separately; no account visibility settings have been changed.

Engineering backlog remains independent of these external inputs: finish protected receiver and power selection, complete production KiCad design and BOM, implement battery/solar telemetry and alerts, finalize enclosure/solar mount design and complete documentation. Do not mark these as merely awaiting physical tests.

Resume from this register and tests, never restart from the initial prompt. Next release gate is component qualification and a reviewed complete schematic, followed by prototype PCB manufacture and bring-up.
