# Footprint and component review record — 9 November 2026

Critical pin mappings are independently asserted in `tools/validate_circuit.py`; exported source-to-board pad/net parity is checked in `tools/validate_manufacturing.py`. KiCad's library is not treated as proof of a manufacturer's package selection.

| Part | Manufacturer check | KiCad implementation | Remaining qualification |
|---|---|---|---|
| AP63203WU-7 | Diodes DS41326 rev3, TSOT26: 0.95mm pitch, 2.8mm nominal total lead span; FB/EN/VIN/GND/SW/BST pins1–6 | TSOT-23-6, 0.95mm pitch; pads1.325×0.6mm at x±1.1375 | IPC-style land differs from vendor's suggested pad widths; verify stencil/reflow with assembler |
| TPS61170DRVR | TI DRV WSON6 2×2mm, pitch0.65mm; EP ground | WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm; 6 leads and EP7 | Final mechanical overlay/stencil review and exposed-pad joint inspection |
| INA228AIDGSR | TI DGS0010A VSSOP10 body3×3mm, pitch0.5mm; example pad1.45×0.3mm | TSSOP-10_3x3mm_P0.5mm has1.45×0.3mm pads, centre rows4.3mm vs TI example4.4mm | Assembler land acceptance; similar INA226 package is not an electrical substitute |
| Phoenix1715721 | Primary page specifies5.08mm pitch,0.9mm square pins and1.3mm PCB holes; width10.16mm, length9.8mm, installed height13.8mm | Named MKDS1.5-2-5.08 footprint,5.08mm pitch,1.3mm drills,2.6mm pads | Dry fit and support terminal block while tightening; obey0.22–0.25Nm current product instructions after verification |
| SRP5030TA-4R7M / -100M | Manufacturer drawing visually checked; 5×5×3mm family, land centres±2.25mm, pads2×1.8mm | L_Bourns_SRP5030T matches those pad dimensions | Solder fillet and actual clearance inspection; 4R7 Isat6A/Irms4.6A,100 Isat3.5A/Irms2.75A |
| DMP2035U-7 | Diodes pin1 gate,2 source,3 drain; SOT23 | SOT-23 with explicit custom symbol matching pin map | Supplier order package and polarity inspection |
| ESP32-C6-MINI-1-N4 | Espressif v1.5,13.2×16.6mm module,48 peripheral0.8×0.4mm lands plus ground pattern | Actual MINI footprint; signal pin names resolved against library and independently checked; local copy removes only antenna-notch silk | Copper overlay, RF keepout/metal clearance and cabinet/tank range test |

The passive MPN table is a nominal selection, not blanket qualification. Manufacturer resistor records were retrieved; automated TDK retrieval was blocked while browser checks verified several exact records. Do not interpret a network failure as a failed part. Before manufacture obtain current characterization sheets and check C1 at actual input voltage, C4/C5 at3.3V, C6 at3.3V and C7 at17.64V for effective capacitance and temperature. Voltage ratings alone do not establish loop stability. Record assembler acceptance of stencil, land patterns and soldermask tolerances.

Sources: [AP63203 package and layout](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf), [INA228 package drawings](https://www.ti.com/lit/ds/symlink/ina228.pdf), [TPS61170](https://www.ti.com/lit/ds/symlink/tps61170.pdf), [Phoenix1715721](https://www.phoenixcontact.com/en-pc/products/pcb-terminal-block-mkds-15-2-508-1715721), [BournsSRP5030TA](https://www.bourns.com/docs/product-datasheets/srp5030ta.pdf?sfvrsn=f08a91f1_28), [EspressifMINI](https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf).

## Added protection parts

LTC4365ITS8#TRMPBF uses TSOT-23-8 with independently checked VIN/UV/OV/GND/SHDN/FAULT/VOUT/GATE pin mapping. Two IPD50N06S4L12ATMA2 DPAK MOSFETs use pins1 gate,2 drain/tab,3 source and a common-source connection. Confirm manufacturer land overlays/stencil and thermal rise before assembly approval. BC847B-7-F uses SOT-23 pins1 base,2 emitter,3 collector; 1N4148W-7-F uses SOD-123 cathode1/anode2.

D9's local DO-201AD footprint is based on maximum 9.5×5.3 mm body, 1.32 mm lead, 20.32 mm lead pitch, 1.6 mm drills and 3.2 mm lands; cathode pin1 follows the body stripe. Verify actual forming/height and bend clearance with the assembler. B360A-13-F is SMA for D1/D3; a Vishay SS36 SMC package is not interchangeable. R12/R13 CRCW2512-HP current datasheet rates 1.5 W at70°C; the DC calculation uses that rating and temperature derating. No supplier substitution or solder-process qualification is inferred from native DRC.
