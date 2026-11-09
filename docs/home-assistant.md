# Home Assistant setup

Add each node through the ESPHome integration using its IPv6 address and independent encryption key. Confirm actual entity IDs in Developer Tools; supplied dashboard assumes tank_1 / tank_2 prefixes and may need renaming. Thread is transport, so do not add these nodes through Matter.

Merge templates/tanks.yaml under `template:`, helpers/net-change.yaml under `sensor:`, and automations/water-alerts.yaml under `automation:`. Do not duplicate top-level keys in configuration.yaml. Copy dashboard YAML into a new manual dashboard. Back up HA first; run HA configuration validation before restarting. These examples have YAML parse checks only, not a live HA runtime test.

Record water and net-change entities for at least 30 days. Native measurement state class supports statistics where applicable. The derivative estimates signed net change in L/h; simultaneous rainfall and consumption cannot be separated using level alone. Actual consumption requires inlet and outlet metering or an independently verified no-inflow interval. Thresholds of 300 L/h are examples requiring site tuning; refill jitter and unavailable transitions need field testing.

Battery voltage/SOC, panel voltage, charge current, charging and signal-quality entities await final hardware. Do not populate a dashboard with fabricated battery percentage from LiFePO4 voltage. Required battery-low and charging-failure alerts are outstanding until valid telemetry exists. A charging-failure alert must consider daylight/irradiance, battery full state and inhibited cold charging, not simply night-time absence of charge.

Stale-measurement alert watches the sequence entity, not just API connectivity. At five-minute reporting, the example warns after 15 min stale plus 5 min persistence. Validate detection with a frozen sensor task, border-router outage and HA restart. Alert thresholds crossing during HA downtime are a remaining startup-reconciliation improvement.
