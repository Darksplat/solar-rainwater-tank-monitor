"""Consolidate exact PCB candidates and external equipment; unknown prices stay blank."""
from pathlib import Path
from collections import defaultdict
import json,csv
p=Path(__file__).resolve().parents[1]
parts=json.loads((p/'hardware/pcb/circuit-resolved.json').read_text())['parts'];groups=defaultdict(list)
for part in parts:
 if not part['ref'].startswith('TP'):groups[part['mpn']].append(part)
fields=['stage','manufacturer','part_number','references','quantity_two_units','supplier','product_url','unit_price_AUD','price_basis','availability_observed','datasheet_url','alternative','status']
lookups=json.loads((p/'bom/supplier-lookups-v02.json').read_text())['records']
rows=[]
for mpn,group in sorted(groups.items()):
 first=group[0];ref=first['ref'];manufacturer=''
 if mpn.startswith(('RC','RT')):manufacturer='Yageo'
 elif mpn.startswith('C') and 'tdk' in first['datasheet']:manufacturer='TDK'
 elif mpn.startswith(('WSL','CRCW','SS36')):manufacturer='Vishay'
 elif mpn.startswith(('INA','TPS')):manufacturer='Texas Instruments'
 elif mpn.startswith(('AP','DMP','B360','BC847','1N4148')):manufacturer='Diodes Incorporated'
 elif mpn.startswith('LTC4365'):manufacturer='Analog Devices'
 elif mpn.startswith('IPD50'):manufacturer='Infineon'
 elif mpn.startswith('1N5408'):manufacturer='Vishay'
 elif mpn.startswith('ESP32'):manufacturer='Espressif'
 elif mpn.startswith('SRP'):manufacturer='Bourns'
 elif mpn.startswith('SMBJ'):manufacturer='Littelfuse'
 elif mpn.startswith('Phoenix'):manufacturer='Phoenix Contact'
 elif mpn.startswith('TSW'):manufacturer='Samtec'
 elif mpn.startswith('LTST'):manufacturer='Lite-On'
 elif mpn.startswith('TL3342'):manufacturer='E-Switch'
 rows.append(dict(stage='rev0.2 PCB candidate',manufacturer=manufacturer,part_number=mpn,references=' '.join(x['ref'] for x in group),quantity_two_units=2*len(group),supplier='DigiKey AU / Mouser AU / element14 quote',product_url='',unit_price_AUD='',price_basis='quote required; not estimated',availability_observed='not independently confirmed at checkout',datasheet_url=first['datasheet'],alternative='same footprint/rating only after engineering review',status='nominal selection; exact stock, DC bias and assembly qualification gates apply'))
for row in rows:
 key=row['part_number'].replace('Phoenix ','');rec=lookups.get(key,{})
 if rec:
  row.update(supplier='DigiKey AU' if '.com.au/' in rec['url'] else 'DigiKey international; AU quote required',product_url=rec['url'],unit_price_AUD=rec.get('unit_price_AUD',''),price_basis=rec.get('basis','price not verified'),availability_observed=rec.get('availability','unconfirmed'))
def external(mfr,mpn,qty,url='',supplier='',price='',basis='quote required',status='candidate',datasheet='',alternative='engineering review required'):
 rows.append(dict(stage='rev0.2 external',manufacturer=mfr,part_number=mpn,references='',quantity_two_units=qty,supplier=supplier,product_url=url,unit_price_AUD=price,price_basis=basis,availability_observed='reconfirm before purchase',datasheet_url=datasheet,alternative=alternative,status=status))
external('WIKA','LH-10 0–0.4bar 4–20mA vented PUR 10m',2,'https://www.wika.com/en-au/lh_10.WIKA','WIKA Australia',status='configured order code, current drawing and water-contact suitability require quote',datasheet='https://www.wika.com/media/Data-sheets/Level/Submersible-pressure-sensors/ds_pe8109_en_co.pdf')
external('Victron','SPM040201200',4,'https://www.everybattery.com.au/product/spm040201200-victron-solar-panel-20w-12v-mono-440x350x25mm-series-4a/','Every Battery',51.95,'listed inc GST 2026-11-09','discontinued; listed remaining stock must be secured before final release','https://www.victronenergy.com/upload/documents/Datasheet-BlueSolar-Monocrystalline-Panels-EN.pdf','30W current model NOT drop-in: PV protection redesign')
external('Victron','BAT512020705',2,'https://batteriesdirect.com.au/shop/product/35244/lfp-lsp12.8/20.html','Batteries Direct',status='exact BMS version and low-temperature charge cutoff require written confirmation')
external('Victron','SmartSolar MPPT 75/10',2,'','Australian Victron distributor',status='selected for model; quote/stock required',datasheet='https://www.victronenergy.com/media/pg/Manual_SmartSolar_MPPT_75-10_up_to_100-20/en/index.html')
external('Victron','BPR065022000',2,'https://baintech.com.au/product/victron-smart-battery-protect-12-24v-65a/','Baintech stockist',102.30,'listed RRP; GST basis confirm','7 listed; configure voltage mode A, not BMS-only mode C','https://www.victronenergy.com/upload/documents/Smart_BatteryProtect_12V_24V/114439-Smart_BatteryProtect-pdf-en.pdf')
external('Fibox','8120087 ARCA403021S',2,'https://au.rs-online.com/web/p/general-purpose-enclosures/2880946','RS Australia',status='manufacturer currently specifies IP65; assembled system unrated',datasheet='https://www.fibox.com/products/ARCA-IEC/ARCA-403021/8120087')
external('Fibox','8120841 PMK ARCA30',2, supplier='Fibox Australian distributor',status='selected proprietary pole kit, supports 100–300mm diameter; site pole/footing review',datasheet='https://www.fibox.com/products/ARCA-IEC/ARCA-403021/8120087')
external('Hummel','1.209.1600.50 HSK-K M16 4–8mm',4,supplier='Australian industrial distributor quote',status='candidate two PV single-cable glands per cabinet; actual cable OD and UV formulation confirmation',datasheet='https://www.hummel.com/en/cable-glands/products/plastic-cable-glands/hsk-k/')
external('Hummel','1.209.2000.50 HSK-K M20 6–12mm',2,supplier='Australian industrial distributor quote',status='probe gland candidate; actual cable OD and formulation must match',datasheet='https://www.hummel.com/en/cable-glands/products/plastic-cable-glands/hsk-k/')
external('Bopla','52041000 DAE M12',2,supplier='Australian Bopla distributor quote',status='pressure vent candidate; current dimensions and mounting torque required',datasheet='https://www.bopla.de/en/enclosure-technology/cable-glands-general-accessories/pressure-compensation-elements')
external('Littelfuse','0FHA0001ZXJ',4,supplier='DigiKey AU / element14 quote',status='5A battery and 2A protected board branch holders; 32V DC, 105C family specification',datasheet='https://www.littelfuse.com/assetdocs/ato-fha-datasheet?assetguid=988addec-bfe3-4ea2-9204-e2982cbb488e')
for mpn in ['0287005.H','0287002.H']:
 rec=lookups.get(mpn,{})
 external('Littelfuse',mpn,4,rec.get('url',''),'DigiKey AU',rec.get('unit_price_AUD',''),rec.get('basis','quote required'),'2 installed +2 spares; 32V DC 1000A family interrupt rating must exceed actual battery prospective fault current')
external('procurement specification','PV-rated DC isolator >=100V DC, >=3A, suitable switching polarity',2,status='exact part selection requires site enclosure/cable arrangement and supplier confirmation')
for description,qty in [('M3 10mm standoff and M3 screws/washers kit',8),('M5 shelf bolts and locking nuts',8),('rated 20mm battery restraint straps with buckles',4),('316 stainless probe guard and independent suspension',2),('dry atmospheric vent filter/desiccant terminal',2),('UV solar cable and matched connectors','site measured length'),('105C cabinet wire, ferrules and M5/M6 lugs','cut list after dry fit'),('rated positive distribution connector and mount',2),('PCB 4-layer 130x110 1.6mm and assembly',2),('250x350x4 service plate and bent 2mm battery shelf',2),('solar rail/clamp kit and site-rated post/footing',2),('3.3V UART programmer and calibrated bench test equipment',1)]:
 external('procurement specification',description,qty,status='not an exact purchased part yet; close from drawings, cable survey or supplier quote')
with (p/'bom/master-bom.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(p/'bom/cost-status.json').write_text(json.dumps({'date':'2026-11-09','consolidated_rows':len(rows),'known_listed_subtotal_AUD':round(sum(float(r['unit_price_AUD'])*float(r['quantity_two_units']) for r in rows if r['unit_price_AUD']),2),'subtotal_is_not_project_total':True,'unpriced_rows':sum(not r['unit_price_AUD'] for r in rows),'shipping':'unknown; no address or checkout quote used','prototype_costs':'existing 0.1 DevKit exploration separate; not required in custom-PCB production BOM','assembly_and_tooling':'quote required; no fabricated estimate'},indent=2))
print('Consolidated',len(rows),'purchasing lines; unknown costs left explicit')
