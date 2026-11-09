# Conservative solar sizing

Execute tools/power_budget.py; results are reproducible assumptions, NOT measured consumption. Baseline: processor+radio+board 80 mA at 3.3 V continuous, 85% conversion; ADC 0.3 mA; 24 V / 24 mA sensor seven seconds per 300 seconds at 80% efficiency; charger 20 mA at battery, BMS/monitor allowance 2 mA and regulator quiescent allowance 1 mA. Replace allowances with selected datasheet maxima and measured values before design release.

Provisional battery 12.8 V 20 Ah: 80% discharge utilisation, another 80% cold/aging allowance, and required energy includes 25% margin beyond seven days. This size is conditional on load budget; battery pack part and low-temperature charge cutoff remain unselected. Hardware BMS and independent load disconnect required; firmware is not the primary battery safety mechanism.

Compare 5/10/20 W at 1.5 winter equivalent sun hours and 60% overall solar yield. This is a conservative sensitivity point, not verified Maiden Gully irradiance. 20 W recovers too slowly under these assumptions (~43 days to restore the margin-inclusive reserve). A 40 W panel is the provisional candidate, subject to voltage compatibility. Check 0.5, 1, 1.5 and 2 PSH; sustained generation below load cannot be solved by battery size. A seven-day outage must also have an acceptable recovery time, not just enough stored energy.

SmartSolar 75/10 is a researched controller candidate, not committed BOM: 20 mA standby materially affects load. Small nominal-12V panel hot Vmp/startup margin needs checking: charger requires PV above battery by 5 V to start. Verify cold Voc, hot Vmp, charge profile, disabled equalisation, external battery temperature sensing and low-temperature charge inhibit. A panel wattage label alone does not establish compatibility.

Panel faces north; tilt and shadow survey to be measured. Include isolatable PV, protected battery terminals, battery-proximal DC fuse sized to cable and load faults, reverse polarity protection and weather-rated cable routes. Do not connect an unconfigured lead-acid charger to LiFePO4.
