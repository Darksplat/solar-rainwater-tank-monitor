# Alternatives and rejected assumptions

- WIKA 40 kPa: smaller headroom than 60 kPa catalog variant; do not use a 4.26 psi RS variant for 3.85 m tank depth.
- A nominal 12 V 40 W panel with 17.2 V Vmp may be a poor match to MPPT startup/hot-panel conditions. Resolve higher-voltage panel or different qualified charger before purchase.
- 5 W and 10 W fail conservative energy balance; 20 W has slow reserve recovery. Smaller panels may become viable only after measured low-power firmware and low-standby controller selection.
- 15 Ah fails conservative seven-day+margin requirement; 20 Ah is provisional.
- LiFePO4 SOC inferred from voltage is not acceptable telemetry. Select a coulomb-counting gauge and synchronize to verified full charge.
- PLA printed outdoor enclosure rejected as an IP/UV assumption. Use purchased certified enclosure and test penetrations/assembled system.
