# Electrical design — revision 0.2 development

The editable KiCad schematic contains 97 components. The routed 130 × 110 mm four-layer PCB includes four M3 mounting holes and an antenna cutout. Native KiCad 10 ERC and DRC reports are in `hardware/pcb/reports/`; both report zero violations. These checks establish connectivity and geometric rules, not power stability, EMC or field reliability.

## Power and measurement

Battery positive passes through an external 5 A DC fuse, LTC4365 U7 and two back-to-back IPD50N06S4L12ATMA2 MOSFETs before R1 (10 mΩ). Common-source Q2/Q3 allow normal charge and discharge while blocking a reversed battery. U7 nominal thresholds are 5.07 V UV and 17.99 V OV; tolerance/TCR/leakage bounds are 4.768–5.396 V and 16.916–19.112 V. These wide windows protect connection polarity/overvoltage; normal battery cutoff is the external BatteryProtect. U3 INA228 at 0x40 measures protected battery voltage, signed discharge current and accumulated charge. Normal charger/load current passes R1. U7, the raw-positive detector and battery BMS draw upstream of R1 and are absent from coulomb counting; self-discharge also requires periodic verified-full SOC resynchronisation.

GPIO19 receives U7's active-low fault and GPIO20 receives an independent, clamped BC847B raw-positive presence detector. A solar-powered bus cannot establish battery presence. Missing/reversed/faulted battery input invalidates SOC and water readings and stops loop power. GPIO inputs are not precision voltage measurements. Fully latched-off BMS recovery is not automatic: the off back-to-back path cannot pass a wake-up charge. Use the battery maker's approved recovery charger directly at the raw battery only after verifying polarity. The BatteryProtect should normally disconnect the load first.

The external Smart BatteryProtect BPR065022000 carries load current from the system positive to J3; charger BAT is connected separately at J2. Charger LOAD terminals are unused. Its GND lead returns to battery negative; configure voltage mode A, not external-BMS-only mode C.

The PV positive path is J4 → D9 (1N5408-E3/54) → R2 (20 mΩ) → J5 → charger PV+. J4/J5 negative terminals share **PV_NEG only**, routed separately from board GND, and connect to charger PV−. Never bridge PV− to battery− externally: the charger manual identifies this as bypassing current measurement on some models. D9 is rated 1000 V and blocks reversed array polarity, including a charged charger input. Its 1.2 V forward-drop allowance is included in harvest/startup calculations; heat must be measured. U4 INA228 at 0x41 measures this positive-side path after D9 (solar input, not raw panel voltage) relative to battery ground; the charger establishes the working relationship between its returns.

J3 feeds B360A-13-F reverse-polarity diode D1, SMBJ15A D2 and AP63203WU-7 buck U1, producing 3.3 V. U1 pins are FB=1, EN=2, IN=3, GND=4, SW=5, BST=6. L1 is Bourns SRP5030TA-4R7M. The 3.3 V regulator has continuous radio and sensor-conversion headroom; actual ripple, temperature and transient tests remain required.

GPIO4 drives a P-channel DMP2035U input switch, active low. Its pullup defaults the loop supply off during reset. TPS61170DRVR U2 boosts switched 3.3 V to nominal 17.206 V, using SRP5030TA-100M, B360A-13-F, 130 kΩ/10 kΩ 0.1% feedback, 4.99 kΩ/10 nF compensation and 4.7 µF output capacitor. The boost is deliberately supplied from regulated 3.3 V because its input rating is 18 V. Its switch rating is 40 V. Compensation is a manufacturer starting point, requiring measured loop stability and startup qualification.

The pressure current path is LOOP_SUPPLY → 2 Ω precision R11 → 110 Ω/1.5 W R12 → 110 Ω/1.5 W R13 → J6+ → transmitter → J6−/GND. U5 INA228 at 0x42 senses R11 high-side. Its VBUS channel measures J6+ voltage, so the firmware “Transmitter voltage” is the terminal voltage before cable drop. INA228 allows 0–85 V common mode, independently of its 3.3 V digital supply. This replaces the preliminary ADS1115 low-side design completely; revision 0.1 wiring and binaries are incompatible.

## Independently checked bounds

`tools/validate_circuit.py` compares the exported schematic netlist with the circuit manifest and separately checks critical IC pin functions. Feedback reference, resistor tolerance and a conservative 60°C TCR excursion give 16.778–17.638 V. At 24 mA, including limiter/shunt tolerance and a 1.4 Ω cable allowance, transmitter voltage is at least 11.300 V against its 10 V requirement. Substitute actual cable resistance from the configured quote.

A DC short is bounded to 81.22 mA with both limiting resistors intact. Each CRCW2512-HP limiter dissipates at most 0.742 W, below its current datasheet's 1.5 W P70 rating derated to 85°C (1.235 W). R11 dissipates 13.23 mW. This electronics stress calculation is not a whole-system 85°C operating rating, demonstrated single-fault survival or transient qualification. Shorted limiter, feedback fault and external surges require current-limited tests.

SMBJ18A maximum specified clamp is 29.2 V, below the boost switch’s 40 V absolute limit at the stated datasheet pulse condition. This does not guarantee the probe’s 30 V limit under hot or other surges. PV sense inputs have 47 Ω series resistors and SMBJ51A TVSs; their 51 V standoff exceeds the selected series array’s calculated −10°C Voc of 50.737 V, and the 82.4 V published clamp is below INA228’s 85 V absolute limit. This narrow transient margin requires surge-waveform verification. It is **not lightning protection**. No enclosure earth or sensor shield bond is assumed; establish the installation bonding method separately.

INA228 differential input impedance loads the shunt sense filters slightly: two 10 Ω resistors versus about 92 kΩ introduces approximately 0.022%; two 47 Ω PV filters approximately 0.102%. Calibrate the full chain. The loop shunt gives 8–40 mV at 4–20 mA; quantization is far smaller than transmitter accuracy. The practical ±20 mm goal still depends on sensor thermal accuracy, water density, calibration and mounting.

## Controller connections

ESP32-C6-MINI-1-N4 uses its actual 53-pad module footprint, not DevKit pin numbering. GPIO6/7 are I²C SDA/SCL, GPIO4 is active-low boost enable, GPIO18 sinks the status LED; GPIO19/20 monitor protection fault/raw battery presence. GPIO8/9 have defined strap pullups; EN has 10 kΩ/1 µF reset conditioning. RESET and BOOT buttons plus 3.3 V UART support recovery. The local footprint adaptation removes only silkscreen over the board cutout; copper geometry is retained. RF range and cabinet/tank detuning remain untested.

| Connector | Pin 1 | Pin 2 |
|---|---|---|
| J1 | Fused battery positive | Battery negative / GND |
| J2 | System positive after R1; charger BAT+ and BatteryProtect IN via external distribution | Charger BAT− / GND |
| J3 | BatteryProtect OUT | GND; not charger LOAD− |
| J4 | Series PV array positive | Array negative / PV_NEG |
| J5 | Charger PV+ | Charger PV− / PV_NEG |
| J6 | Transmitter positive | Transmitter negative / GND |

J7 pins 1–6: GND, 3.3 V, controller TXD, controller RXD, BOOT, EN. Cross TX/RX to a **3.3 V** UART adapter. Do not apply 5 V or backfeed a powered 3.3 V rail.

Sources: [INA228](https://www.ti.com/lit/ds/symlink/ina228.pdf), [TPS61170](https://www.ti.com/lit/ds/symlink/tps61170.pdf), [AP63203](https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf), [DMP2035U](https://www.diodes.com/datasheet/download/DMP2035U.pdf), [Bourns inductors](https://www.bourns.com/docs/product-datasheets/srp5030ta.pdf?sfvrsn=f08a91f1_28), [charger manual](https://www.victronenergy.com/media/pg/Manual_SmartSolar_MPPT_75-10_up_to_100-20/en/index.html), [BatteryProtect manual](https://www.victronenergy.com/upload/documents/Smart_BatteryProtect_12V_24V/114439-Smart_BatteryProtect-pdf-en.pdf).

Protection sources: [LTC4365](https://www.analog.com/media/en/technical-documentation/data-sheets/4365fa.pdf), [Infineon MOSFET](https://www.infineon.com/assets/row/public/documents/10/49/infineon-ipd50n06s4l-12-datasheet-en.pdf), [1N5408](https://www.vishay.com/docs/88516/1n5400.pdf), [CRCW-HP ratings](https://www.vishay.com/docs/20115/crcwhp.pdf). One low-current BAT_RAW detector via uses 0.56 mm copper /0.25 mm drill; ordinary vias are 0.6/0.3 mm and power vias 1.2/0.6 mm. Native DRC retains declared clearance/annulus minima.
