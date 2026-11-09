"""Conditional worst-case contributions; this is not a measured accuracy result."""
from pathlib import Path
import json
rho=998.2;g=9.80665;span=40000;head=2.12
amps=.004+.016*head*rho*g/span
metres_per_amp=span/(rho*g*.016)
entries={
 'transmitter_reference_0p25pct_FS_mm':span*.0025/(rho*g)*1000,
 'uncalibrated_shunt_0p1pct_at_operating_current_mm':amps*.001*metres_per_amp*1000,
 'INA228_gain_0p05pct_mm':amps*.0005*metres_per_amp*1000,
 'INA228_offset_1uV_at_2ohm_mm':.000001/2*metres_per_amp*1000,
 'shunt_drift_25ppm_60C_span_mm':amps*25e-6*60*metres_per_amp*1000,
 'INA228_gain_drift_20ppm_60C_span_mm':amps*20e-6*60*metres_per_amp*1000,
 'density_allowance_0p6pct_mm':head*.006*1000,
 'diaphragm_survey_allowance_mm':5,
}
report={'date':'2026-11-09','head_m':head,'pressure_span_Pa':span,'density_kg_m3':rho,'operating_current_A':amps,'contributions':entries,'interpretation':'bounded illustrative contributors, not independent random uncertainties; do not RSS or claim achieved accuracy','transmitter_accuracy_class':'conditional on configured quote; thermal error not yet bounded','calibration':'two-point chain calibration removes static gain/offset only to the reference uncertainty; does not remove unmeasured thermal drift, density change or mounting error','target_plus_minus_20mm':'not verified or guaranteed'}
(Path(__file__).resolve().parents[1]/'tests/test-results/accuracy-budget-v02.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
