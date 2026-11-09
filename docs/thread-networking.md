# Thread implementation and validation

Use ESPHome 2026.10.2 pinned in requirements, ESP32-C6 with ESP-IDF, IPv6 enabled, device_type MTD and poll_period 5s. Do not assume SED polling puts the CPU to sleep. Conservative power model assumes active processor continuously; actual whole-node current must be measured.

Provision the existing HA Thread operational dataset locally in ignored firmware/tank_1/secrets.yaml and firmware/tank_2/secrets.yaml. Never publish it. USB initial flash; HA ESPHome integration uses native API encryption. Ensure IPv6 path from HA through border router. Neither tank is a router, so place a mains-powered Thread router if site coverage requires one. One tank failing must not break the other's radio path.

Maintenance button sets poll period to 0 for ten minutes, allowing OTA; firmware restores 5s afterward. First validate this on USB power. Dataset recovery after cold boot, parent router replacement, border-router restart, IPv6 outage and OTA interruption are hardware acceptance tests, not simulated passes.

Fallback gate: if measured energy or 72 h connectivity soak fails, first evaluate ESP-IDF light sleep SED. Wi-Fi deep sleep at five-minute intervals is second preference and requires reliable AP coverage. Do not switch protocols merely because older ESPHome documentation lacked SED.
