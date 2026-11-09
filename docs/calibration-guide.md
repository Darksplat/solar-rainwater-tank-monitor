# Calibration procedure

Disable calibration on each unit until geometry and pressure calibration are verified independently. Record date, instrument ID, water temperature, density assumption and probe diaphragm elevation. Keep tank-specific records. Never infer length/width from a capacity label.

Measure internal length/width safely without entering a tank. Measure floor-referenced maximum operating level, usable bottom level/outlet, and diaphragm position. Set usable depth = maximum operating level minus unusable bottom level. Use the manufacturer method only with verified volume at a measured reference depth; a verified constant horizontal section is still required. Rated capacity is metadata.

Pressure conversion: head = (current - zero_current)/span_current * pressure_span/(density*g). Floor depth = head + diaphragm elevation. For a rounded rectangle, area = length * width − (4−π) * corner_radius²; volume = floor depth * area * 1000. Radius zero selects rectangular geometry; a capsule needs verified end radius. Usable litres exclude water below the usable bottom datum. Percentage denominator is usable capacity. At/below diaphragm the result is unresolved; a zero pressure does not distinguish an empty tank from water just below the diaphragm.

With traceable reference depths at suitable points from the diaphragm through the measured maximum operating level (for example 0, 0.25, 0.5, 1, 1.5, 2 m and maximum), collect at least ten samples ascending and descending. Empty is a diagnostic/blind-region check, not a pressure datum below the probe. Allow thermal settling and remove bubbles. Fit current = intercept + slope * head using tools/calibrate.py. Set zero current to intercept; set span current to slope * pressure_span/(density*g). Inspect residuals; never fit a line to a disconnected loop.

For each point record depth error in mm, error / maximum depth as %FS, litre error using measured cross-section, repeatability range, and ascending/descending hysteresis. Repeat after 24 h and annually to quantify drift. ±20 mm is a target, not achieved evidence. Temperature, sensor drift, diaphragm location and water density can dominate ADC resolution.

## Revision0.2 error budget

`tests/test-results/accuracy-budget-v02.json` evaluates a provisional 2.12 m head and 40 kPa span. A configured ±0.25%FS reference sensor contributes 10.22 mm; this accuracy class and thermal error still require the exact quote. Uncalibrated 0.1% shunt tolerance contributes 3.14 mm, INA228 0.05% gain 1.57 mm and 1 µV offset 0.128 mm. A 60°C excursion with 25 ppm/°C shunt and 20 ppm/°C monitor gain drift adds 4.71 and 3.77 mm. A 0.6% density allowance contributes 12.72 mm, with a separate assumed 5 mm diaphragm-survey uncertainty. These bounds are not independent noise; do not combine them by RSS or claim achieved ±20 mm.

Two-point calibration removes static gain/offset only to the quality of the reference. It does not remove unknown transmitter thermal drift, density change or movement. Measure the actual installation across depths and temperatures. For litre error multiply depth error by measured litres per metre; leave litres unavailable while geometry is unverified. No real calibration or drift measurements exist yet.
