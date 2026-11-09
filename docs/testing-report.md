# Verification report — revision0.2, 9 November 2026

No PCB manufacture, physical flashing, water-depth measurement, RF-range, battery-autonomy or ingress test is recorded as passed. Reports below are reproducible software/geometry evidence.

| Test | Procedure / expected result | Actual result | Status / limit |
|---|---|---|---|
| Water core | C++17 warnings-as-errors, actual shared header; depth grid/volume/filter/fault boundaries | Assertions pass; synthetic CSV saved | PASS calculation/simulation only |
| Python suite | unittest calibration/power/cold-PV/input bounds |12 tests pass | PASS software only |
| INA228 driver | Compile actual production driver against controlled I²C stub; inject each read failure, reset, overflow, not-ready, wrong identity, signed decoding and recovery | Assertions pass | PASS software driver, not analog/I²C hardware |
| Battery guard/SOC | Actual shared helper: unknown/low/high supply; verified-full guard, discharge/charge, counter gap/reset, changed capacity, NaN and timer wrap | Assertions pass | PASS software; no capacity measurement |
| HA examples | YAML parsing and actual shipped Jinja expressions against day/night/full/charging/missing/fault fixtures |24 scenarios pass;22 distinct automation IDs | PASS expressions, not HA engine/timers/notifications |
| Tank1 firmware | Pinned ESPHome/ESP-IDF build, independently named node | Factory and OTA images produced | PASS compilation; public fixtures only |
| Tank2 firmware | Same toolchain, independent node/config | Factory and OTA images produced | PASS compilation; public fixtures only |
| Schematic ERC | Native KiCad10 electrical rules |0 violations | PASS rule check, not component qualification |
| PCB DRC | Native KiCad10 with declared0.15mm minima |0 violations,0 unconnected pads | PASS connectivity/geometry, not circuit behavior |
| Source/net parity | Exported schematic versus manifest; independent critical-pin checks; board pad nets versus source |97 components /101 footprints match | PASS source consistency |
| DC bounds | Worst-case feedback/shunt/limiter tolerances and cable allowance |≥11.300V probe at24mA;≤81.23mA bounded DC short;≤0.742W each limiter | PASS conditional calculation, not transient survival |
| Fabrication exports | Four copper layers, mask/paste/silk/outline, separated drill syntax/maps, placement table, content hashes | Export audit passes;77 SMD placement rows | PASS structure; external CAM/stencil review not performed |
| CAD saved sources | Reopen all native FreeCAD documents; validate every non-null shape |4 documents pass | PASS saved geometry only |
| CAD exports | Independently reopen STEP and STL |38 STEP files valid;35 STL meshes closed | PASS export geometry; no structural/fit/IP approval |
| CAD assembly | Eight commercial-envelope intersection checks plus STEP volume round trips | No intersections in the tested pairs; volume round trips pass | PASS packaging study only |
| Power/solar | Component allocations, winter sensitivity,25% reserve margin, cold-Voc/hot-Vmp checks |163.84Wh model usable vs144.09Wh required;40W winter model surplus | PASS assumptions; actual current/cold capacity/shading unmeasured |
| Accuracy | Conditional source/temperature/density contributors |±20mm not guaranteed by the full outdoor budget | ANALYSIS only; physical calibration missing |
| Hosted GitHub CI | Calculation/source audits, fault tests, both ESPHome builds | See publication-validation.md for the exact revised run | Separate remote execution evidence |
| Physical/HA/Thread/BMS/OTA | Matrix in hardware-validation.md | Hardware and owner environment unavailable | NOT RUN |

Important corrections: the original low-side ADS1115/100Ω interface was replaced by high-side INA228 measurement with explicit current limiting; the buck symbol pin map and exposed MINI module GPIO were corrected against source data; nonexistent inductor variants were replaced with actual Bourns4R7/100 parts; PV protection was coordinated with the cold array; PV return was separated and independent high-side load disconnect selected. Battery SOC no longer invents a percentage from voltage or an assumed reboot state. Failed I²C reads invalidate measurements. Six Kelvin branches keep power-track resistance out of shunt voltage sensing. Routing clearance/hole/stub defects were corrected and native DRC rerun to zero; design minima were retained.

Evidence resides in `tests/test-results/*-v02.*`, `hardware/pcb/reports/`, `hardware/cad/all-export-validation.json` and `assembly-validation.json`. `manufacturing-validation.json` binds native-check evidence to source hashes and export hashes. CI verifies those hashes; it does not rerun proprietary installed desktop CAD tools on Ubuntu.

Remaining qualification is explicit: exact configured transmitter and battery BMS documentation, effective capacitor/assembler review, analog startup/settling/stability/surge/thermal tests, traceable depth/current calibration, site shade/structural/cable review, actual HA/Thread/recovery and assembled-enclosure/weather testing. Manufacturer and supplier descriptions are not substituted for measured acceptance.
