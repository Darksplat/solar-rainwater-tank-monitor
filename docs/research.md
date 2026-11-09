# Evidence register — checked 9 November 2026

Primary sources:

- ESPHome 2026.10.2 OpenThread: https://esphome.io/components/openthread/ — MTD polling supported; processor sleep savings remain unverified. OTA requires polling disabled. Retain Thread; test power and parent loss before selecting fallback Wi-Fi deep sleep.
- HA Thread: https://www.home-assistant.io/integrations/thread/ — working IPv6 is a commissioning dependency.
- HA ESPHome: https://www.home-assistant.io/integrations/esphome/ — native API integration.
- WIKA Australian LH-10 page: https://www.wika.com/en-au/lh_10.WIKA
- Manufacturer-linked PE81.09: https://www.wika.com/media/Data-sheets/Level/Submersible-pressure-sensors/ds_pe8109_en_co.pdf
- Operating instructions: https://www.wika.com/media/Operating-instructions/Operating-instructions/Pressure/Pressure-sensors/oi_lh_10_en_de_fr_es.pdf
- TI ADC product/datasheet: https://www.ti.com/product/ADS1115 and https://www.ti.com/lit/ds/symlink/ads1115.pdf
- Charger limits: https://www.victronenergy.com/media/pg/Manual_SmartSolar_MPPT_75-10_up_to_100-20/en/technical-specifications.html
- Solar climatology: https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/ — regional 2001–2025 monthly series preserved in docs/data; site shade and actual tilted yield remain unmeasured.

Pressure candidate: WIKA LH-10, vented gauge, 0–0.4 bar, two-wire 4–20 mA, 10 m PUR cable, 316L wetted metal. This catalog range is verified; a 50 kPa custom variant is not confirmed. Request complete configured order code and current drawing from WIKA Australia. Catalog supply 10–30 V; reference accuracy 0.25% span, drift 0.2% span/year, temperature coefficients additional. No quantified service life warranty found. Budget annual verification and dry vent servicing. AU purchase route is manufacturer quotation, not an invented stocked SKU.

The owner's linked Kingspan catalogue specifies 4000 mm length ×1150 mm width ×2320 mm height, superseding the initial 4 m height assumption. The full catalogue height corresponds to about22.7 kPa, so 40 kPa provides substantial headroom and about10.2 mm reference sensor error at ±0.25%FS. Confirm actual internal shape, maximum water level and configured sensor class. ±20 mm over outdoor temperatures and annual drift remains unestablished.

Do not use RS stock 1241477 merely because it says LH-10: the surfaced variant is 4.26 psi, unsuitable for this tank height. Price, lead time, exact configured part number and garden-water suitability remain supplier dependencies. No orders placed.
