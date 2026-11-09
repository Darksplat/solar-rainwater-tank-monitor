# Calibration procedure

Disable calibration on each unit until geometry and pressure calibration are verified independently. Record date, instrument ID, water temperature, density assumption and probe diaphragm elevation. Keep tank-specific records. Never infer length/width from a capacity label.

Measure internal length/width safely without entering a tank. Measure floor-referenced maximum operating level, usable bottom level/outlet, and diaphragm position. Set usable depth = maximum operating level minus unusable bottom level. Use the manufacturer method only with verified volume at a measured reference depth; rectangular constant section is still required. Rated capacity is metadata.

Pressure conversion: head = (current - zero_current)/span_current * pressure_span/(density*g). Floor depth = head + diaphragm elevation. Volume = floor depth * length * width * 1000. Usable litres exclude water below the usable bottom datum. Percentage denominator is usable capacity. At/below diaphragm the result is unresolved; a zero pressure does not distinguish an empty tank from water just below the diaphragm.

With traceable reference depths at 0, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 3.5 and maximum operating level, collect at least ten samples ascending and descending. Empty is a diagnostic/blind-region check, not a pressure datum below the probe. Allow thermal settling and remove bubbles. Fit current = intercept + slope * head using tools/calibrate.py. Set zero current to intercept; set span current to slope * pressure_span/(density*g). Inspect residuals; never fit a line to a disconnected loop.

For each point record depth error in mm, error / maximum depth as %FS, litre error using measured cross-section, repeatability range, and ascending/descending hysteresis. Repeat after 24 h and annually to quantify drift. ±20 mm is a target, not achieved evidence. Temperature, sensor drift, diaphragm location and water density can dominate ADC resolution.
