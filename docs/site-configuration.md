# Owner-specific configuration — 9 November 2026

Both tanks are used for garden water; one can also serve as a fire tank. The owner explicitly does not want a minimum-reserve display. No reserve allocation, pump control or valve control is added.

The supplied [Kingspan10000L Slimline page](https://kingspanwatertanks.com.au/products/10000-litre-slimline-water-tank) lists **4000mm length ×1150mm width ×2320mm height**. The original4m **height** assumption is superseded;4m is the catalogue length. Kingspan also makes this range to measure, so the delivered dimensions still need confirmation. The [manufacturer data sheet](https://kingspanwebdatastorage.z8.web.core.windows.net/webfiles/Urban/kingspan-water-tanks-urban-slimline-tank-data-sheet-en-au.pdf) defines capacity as nominal before fitting location and size. The10000L label is not verified usable volume.

Slimline tanks have rounded geometry. Do not multiply the external bounding length×width×height and treat the result as water volume. Firmware now supports an internal corner radius `r`:

`area = internal_length × internal_width − (4 − π) × r²`

Zero radius gives the original rectangle. Radius equal to half the width gives a straight-sided capsule with semicircular ends. Other rounded rectangles use the measured/design corner radius. This geometric formula assumes constant vertical cross-section and the stated corner shape; do not assume the actual Kingspan curve matches a perfect capsule without a drawing or measured confirmation. A verified volume at measured reference depth remains the preferred alternative when the internal profile is uncertain.

Initial firmware planning values are maximum operating level2.17m and usable depth2.12m, derived from the catalogue height minus a provisional150mm freeboard and50mm unusable bottom layer. These are **not measured overflow or outlet settings**. Internal dimensions, corner radius/reference volume and calibration remain unverified; calibration defaults disabled and no litres/percentage are valid until explicitly commissioned.

A0–0.4bar (40kPa) LH-10 configuration is now preferred for the catalogue-sized tank: even2.32m water head is about22.7kPa, leaving ample measurement headroom. The original0–0.6bar remains electrically compatible if that is the actual ordered range. Set the new “Pressure full scale” number to the exact transmitter range; do not correct a range mismatch by inventing geometry. The new default is40kPa; existing retained settings require review during any upgrade.

The owner has a Raspberry Pi Zero2W with PoE HAT and a Sonoff USB radio already in Thread mode. The supplied ASIN B0G2LTBM1M identifies the Dongle-LMG21 / EFR32MG21 family; SONOFF documents that model as [Dongle LiteMG21](https://dongle.sonoff.tech/guide/dongle-lmg21/dongle-lmg21-introduction/). The Amazon page was inaccessible to the research tool, so the mapping is corroborated catalogue identification rather than a read from the physical radio. Preserve the existing working RCP firmware, serial configuration and Thread network. See thread-networking.md; no reflash, network reset or live configuration change has been performed.
