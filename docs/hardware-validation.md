# Physical acceptance procedures — ALL PENDING

Record date, unit serial, calibrated instrument ID, setup photographs, actual readings, pass/fail and corrective action for each test. The following are procedures, not evidence of success.

| Test | Procedure and required result |
|---|---|
| Water depth grid | Empty and measured points up to the actual tank maximum (e.g.250,500,1000,1500,2000 mm and maximum); ascending/descending ten samples; report mm, %FS and L errors; empty below diaphragm remains unresolved |
| Accuracy/temperature | Repeat grid at expected water temperatures; quantify sensor temp error and density contribution; establish whether ±20 mm can be met |
| Startup | Power-cycle loop 100 times at low/full depth; determine time to stable result and recovery from failed conversion |
| Loop disconnection/short | Current-limited bench supply; unplug/short appropriate loop terminals; receiver survives faults and invalidates water quantities |
| Miswire/overvoltage | Validate protection analytically then current-limited bench injection; all protected IC pins remain within their manufacturer limits, including powered-off states |
| ADC failure | Remove an INA228 monitor, force I2C timeout/stuck bus; no fresh valid water reading; task recovery documented |
| Battery low/overvoltage | Programmable supply sweep; hardware disconnect precedes damaging cell discharge; reconnect hysteresis avoids oscillation |
| Cold charge | Qualified temperature fixture verifies charging inhibit and restart; do not intentionally charge cells below permitted temperature |
| Solar failure | Daylight PV loss while battery not full; correct alert; no false night/full/cold inhibit alarms |
| Network loss | Parent loss, border-router restart, IPv6 firewall interruption; independent nodes recover within defined 15 min target |
| Power interruption | 100 randomized interruptions including sensor acquisition; calibration preserved and GPIO4 starts high/off; loop power remains off |
| Firmware recovery | Watchdog, interrupted OTA and 3.3 V UART recovery; no uncontrolled permanent loop power |
| Battery energy | Measure current in idle, poll, transmit, acquisition, startup and OTA; integrated 24 h Wh below design budget |
| Seven-day autonomy | Fully charged conditioned pack, no PV, normal reporting for 168 h; preserve specified margin and cell limits |
| Solar recovery | Site winter irradiance and measured charge series; verify acceptable replenishment after seven-day deficit |
| Environmental | Qualified spray/condensation/UV/thermal tests on completed enclosure; no IP65/66 claim from CAD |
| Mechanical | Probe/cage fit, vent and bubble purge, suspension load, panel wind mount and service access |
| Consumption | Compare level change against independently metered inflow/outflow; never label net decline as actual consumption |

Procurement release also requires complete schematic ERC, copper DRC, unconnected-net audit, official footprint drawing comparison, fabrication export inspection and independent design review. Native ERC/DRC, source/net parity and fabrication structure checks now pass for the complete routed development design; independent component/land-pattern/CAM review and physical qualification remain pending.

Reverse-input acceptance: current-limited fixtures must exercise J1 normal/reversed/absent battery with charger off and on, verify U7/Q2/Q3 isolation and normal bidirectional battery current, and check GPIO19/20 fault handling. Test reversed PV at J4 with the charger input discharged and precharged; verify D9 leakage, forward heating and surviving pin voltages. Never reverse a live battery or live array for an informal test. Verify maker-approved fully-off BMS recovery separately; no automatic wake-through path is provided.
