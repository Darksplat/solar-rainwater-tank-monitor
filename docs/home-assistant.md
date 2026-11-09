# Home Assistant setup

Add each node through the ESPHome integration using its IPv6 address and independent encryption key. Confirm actual entity IDs in Developer Tools; supplied dashboard assumes tank_1 / tank_2 prefixes and may need renaming. Thread is transport, so do not add these nodes through Matter.

Merge templates/tanks.yaml under `template:`, helpers/net-change.yaml under `sensor:`, and both automations/water-alerts.yaml and automations/power-alerts.yaml under `automation:`. Do not duplicate top-level keys in configuration.yaml. Copy dashboard YAML into a new manual dashboard. Back up HA first; run HA configuration validation before restarting. All examples parse, and 24 controlled scenarios execute the shipped Jinja expressions. HA runtime, timers, entity registration and notifications remain untested.

Record water and net-change entities for at least 30 days. Native measurement state class supports statistics where applicable. The derivative estimates signed net change in L/h; simultaneous rainfall and consumption cannot be separated using level alone. Actual consumption requires inlet and outlet metering or an independently verified no-inflow interval. Thresholds of 300 L/h are examples requiring site tuning; refill jitter and unavailable transitions need field testing.

Revision 0.2 supplies battery voltage, signed current, power, hardware charge counter, synchronized SOC, monitor diagnostics, solar input voltage/current/power after the PV reverse-blocking diode, Thread parent RSSI/link quality and charging state. Positive battery current means discharge; charging is sustained negative net current, not merely nonzero PV voltage. The dashboard has daily/weekly water and battery histories plus PV power/net-current history.

SOC is unavailable after boot and faults. Set actual battery capacity, fully charge using the approved charger, independently verify full charge and a low tail current, then press the verified-full synchronization button. The firmware also checks 13.8–14.7 V and ≤2% capacity tail current; these checks do not prove cell balance or full capacity. The hardware BMS/disconnect protects the battery independently of this estimate.

Power alerts include low voltage, low synchronized SOC, monitor faults and possible low daytime solar input. The latter requires solar elevation >10°, voltage <13.2 V, discharge >20 mA and PV <1 W for two hours. Its message explicitly asks the owner to consider clouds, shade and cold-charge inhibition; it does not diagnose a failed charger. Actual irradiance and battery temperature are not measured.

Stale-measurement alert watches the sequence entity, not just API connectivity. At five-minute reporting, the example warns after 15 min stale plus 5 min persistence. Validate detection with a frozen sensor task, border-router outage and HA restart. Alert thresholds crossing during HA downtime are a remaining startup-reconciliation improvement.

The owner requests no minimum tank-reserve display. Garden/fire use is recorded as context only; neither outlet is controlled. Battery-presence/protection faults invalidate battery SOC and stop pressure acquisition. The shunt omits controller/presence/BMS upstream drain and self-discharge, so synchronized SOC remains an estimate and needs periodic independent full-charge resynchronisation.
