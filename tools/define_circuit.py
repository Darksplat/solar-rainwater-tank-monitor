"""Rev 0.2 circuit source. External charger and fused battery remain off-board."""
from pathlib import Path
import json
p=Path(__file__).resolve().parents[1]
parts=[]
def add(ref,lib,value,fp,nets,section,mpn='',datasheet=''):
 parts.append(dict(ref=ref,lib=lib,value=value,footprint=fp,nets={str(k):v for k,v in nets.items()},section=section,mpn=mpn,datasheet=datasheet))
R='Resistor_SMD:R_0603_1608Metric';C='Capacitor_SMD:C_0603_1608Metric'
def res(ref,value,a,b,section,fp=R,mpn=''):add(ref,'Device:R',value,fp,{1:a,2:b},section,mpn)
def cap(ref,value,a,b,section,fp=C,mpn=''):add(ref,'Device:C',value,fp,{1:a,2:b},section,mpn)
T='TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal'
for ref,val,n1,n2 in [('J1','BATTERY FUSED 5A','BAT_RAW','GND'),('J2','CHARGER BAT','CHARGER_BAT','GND'),('J3','PROTECTED LOAD','LOAD_IN','GND'),('J4','PV INPUT','PV_RAW','PV_NEG'),('J5','CHARGER PV','PV_OUT','PV_NEG'),('J6','PRESSURE LOOP','LOOP_P','GND')]:
 add(ref,'Connector_Generic:Conn_01x02',val,T,{1:n1,2:n2},'connections','Phoenix 1715721','https://www.phoenixcontact.com/en-pc/products/pcb-terminal-block-mkds-15-2-508-1715721')
# Bidirectional battery path with reverse-input detection, not a charging-blocking diode.
add('U7','Power_Management:LTC4365TS8','LTC4365ITS8#TRMPBF','Package_TO_SOT_SMD:TSOT-23-8',{1:'BAT_RAW',2:'REV_UV',3:'REV_OV',4:'GND',5:'REV_SHDN',6:'REV_FAULT',7:'BAT_FUSED',8:'REV_GATE'},'reverse','LTC4365ITS8#TRMPBF','https://www.analog.com/media/en/technical-documentation/data-sheets/4365fa.pdf')
for ref,drain in [('Q2','BAT_RAW'),('Q3','BAT_FUSED')]:
 add(ref,'Transistor_FET:Q_NMOS_GDS','IPD50N06S4L-12','Package_TO_SOT_SMD:TO-252-2',{1:'REV_GATE',2:drain,3:'REV_SOURCE'},'reverse','IPD50N06S4L12ATMA2','https://www.infineon.com/part/IPD50N06S4L-12')
res('R60','2.74M','BAT_RAW','REV_UV','reverse');res('R61','215k','REV_UV','REV_OV','reverse');res('R62','84.5k','REV_OV','GND','reverse');res('R63','510k','BAT_RAW','REV_SHDN','reverse')
res('R64','10k','V3V3','REV_FAULT','controller')
add('D9','Device:D','1N5408','TankMonitor:1N5408_DO201AD_P20.32',{1:'PV_IN',2:'PV_RAW'},'pv','1N5408-E3/54','https://www.vishay.com/docs/88516/1n5400.pdf')
# Independent raw-positive presence detector, so an unpowered controller cannot
# masquerade as an attached battery when PV still powers the system bus.
add('Q4','Transistor_BJT:Q_NPN_BEC','BC847B-7-F','Package_TO_SOT_SMD:SOT-23',{1:'RAW_BASE',2:'GND',3:'RAW_PRESENT'},'reverse','BC847B-7-F','https://www.diodes.com/datasheet/download/BC847B.pdf')
res('R65','100k','BAT_RAW','RAW_BASE','reverse');res('R66','100k','V3V3','RAW_PRESENT','controller');res('R67','10k','RAW_BASE','GND','reverse')
add('D10','Device:D','1N4148W-7-F','Diode_SMD:D_SOD-123',{1:'RAW_BASE',2:'GND'},'reverse','1N4148W-7-F','https://www.diodes.com/datasheet/download/1N4148W.pdf')
res('R1','0.01R 1% 1W','BAT_FUSED','CHARGER_BAT','battery','Resistor_SMD:R_2512_6332Metric','WSL2512R0100FEA')
res('R2','0.02R 1% 1W','PV_IN','PV_OUT','pv','Resistor_SMD:R_2512_6332Metric','WSL2512R0200FEA')
add('D1','Device:D_Schottky','B360A-13-F','Diode_SMD:D_SMA',{1:'VIN',2:'LOAD_IN'},'buck','B360A-13-F','https://www.diodes.com/datasheet/download/B360A.pdf')
add('D2','Device:D_Zener','SMBJ15A','Diode_SMD:D_SMB',{1:'VIN',2:'GND'},'buck','SMBJ15A','https://www.littelfuse.com/assetdocs/littelfuse-tvs-diode-smbj-datasheet?assetguid=18cc865c-d88b-4e4c-a33f-6c1c0f621906')
add('U1','Regulator_Switching:AP63203WU','AP63203WU-7','Package_TO_SOT_SMD:TSOT-23-6',{1:'V3V3',2:'EN_BUCK',3:'VIN',4:'GND',5:'SW_BUCK',6:'BST'},'buck','AP63203WU-7','https://www.diodes.com/datasheet/download/AP63200-AP63201-AP63203-AP63205.pdf')
res('R3','100k','VIN','EN_BUCK','buck');res('R4','100k','EN_BUCK','GND','buck')
cap('C1','10u 50V X7R','VIN','GND','buck','Capacitor_SMD:C_1210_3225Metric')
cap('C2','100n 50V','VIN','GND','buck');cap('C3','100n 16V','BST','SW_BUCK','buck')
add('L1','Device:L','4.7uH Isat>=4A','Inductor_SMD:L_Bourns_SRP5030T',{1:'SW_BUCK',2:'V3V3'},'buck','SRP5030TA-4R7M')
for i in [4,5]:cap('C'+str(i),'22u 16V X7R','V3V3','GND','buck','Capacitor_SMD:C_1210_3225Metric')
# Fully switched boost input: P-MOS gate high = off, hardware pullup.
add('Q1','TankMonitor:DMP2035U','DMP2035U-7','Package_TO_SOT_SMD:SOT-23',{1:'BOOST_GATE',2:'V3V3',3:'BOOST_IN'},'boost','DMP2035U-7','https://www.diodes.com/datasheet/download/DMP2035U.pdf')
res('R5','100k','BOOST_GATE','V3V3','boost');res('R6','1k','LOOP_EN_N','BOOST_GATE','boost')
add('U2','TankMonitor:TPS61170','TPS61170DRVR','Package_SON:WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm',{1:'FB_BOOST',2:'COMP',3:'GND',4:'SW_BOOST',5:'BOOST_IN',6:'BOOST_IN',7:'GND'},'boost','TPS61170DRVR','https://www.ti.com/lit/ds/symlink/tps61170.pdf')
cap('C6','4.7u 16V X7R','BOOST_IN','GND','boost','Capacitor_SMD:C_0805_2012Metric')
add('L2','Device:L','10uH Isat>=1.6A','Inductor_SMD:L_Bourns_SRP5030T',{1:'BOOST_IN',2:'SW_BOOST'},'boost','SRP5030TA-100M')
add('D3','Device:D_Schottky','B360A-13-F','Diode_SMD:D_SMA',{1:'LOOP_SUPPLY',2:'SW_BOOST'},'boost','B360A-13-F')
cap('C7','4.7u 50V X7R','LOOP_SUPPLY','GND','boost','Capacitor_SMD:C_1210_3225Metric')
res('R7','130k 0.1%','LOOP_SUPPLY','FB_BOOST','boost');res('R8','10k 0.1%','FB_BOOST','GND','boost')
res('R9','4.99k','COMP','COMP_RC','boost');cap('C8','10n','COMP_RC','GND','boost')
res('R10','100k','LOOP_SUPPLY','GND','boost')
add('D4','Device:D_Zener','SMBJ18A','Diode_SMD:D_SMB',{1:'LOOP_SUPPLY',2:'GND'},'boost','SMBJ18A')
# Shunt before two independently rated limiting resistors, no ADC rail clamps.
res('R11','2R 0.1% 25ppm','LOOP_SUPPLY','LOOP_SHUNT_OUT','loop','Resistor_SMD:R_1206_3216Metric','RT1206BRD072RL')
res('R12','110R 1.5W','LOOP_SHUNT_OUT','LOOP_LIMIT_MID','loop','Resistor_SMD:R_2512_6332Metric','CRCW2512110RFKEGHP')
res('R13','110R 1.5W','LOOP_LIMIT_MID','LOOP_P','loop','Resistor_SMD:R_2512_6332Metric','CRCW2512110RFKEGHP')
# Three high-voltage monitors. Battery current positive is discharge.
for ref,prefix,a0,plus,minus,vbus in [('U3','BAT','GND','BAT_FUSED','CHARGER_BAT','BAT_FUSED'),('U4','PV','V3V3','PV_IN','PV_OUT','PV_OUT'),('U5','LOOP','SDA','LOOP_SUPPLY','LOOP_SHUNT_OUT','LOOP_P')]:
 add(ref,'Sensor_Energy:INA228','INA228AIDGSR','Package_SO:TSSOP-10_3x3mm_P0.5mm',{1:'GND',2:a0,3:None,4:'SDA',5:'SCL',6:'V3V3',7:'GND',8:prefix+'_VBUS',9:prefix+'_N',10:prefix+'_P'},prefix.lower(),'INA228AIDGSR','https://www.ti.com/lit/ds/symlink/ina228.pdf')
 idx={'BAT':20,'PV':30,'LOOP':40}[prefix]
 for offset,src,target in [(0,plus,prefix+'_P'),(1,minus,prefix+'_N'),(2,vbus,prefix+'_VBUS')]:
  res('R'+str(idx+offset),'10R' if prefix!='PV' else '47R',src,target,prefix.lower())
 cap('C'+str(idx),'100n 100V',prefix+'_P',prefix+'_N',prefix.lower(),'Capacitor_SMD:C_0805_2012Metric')
 cap('C'+str(idx+1),'100n', 'V3V3','GND',prefix.lower())
 if prefix=='PV':
  for num,net in [(5,prefix+'_P'),(6,prefix+'_N'),(7,prefix+'_VBUS')]:
   add('D'+str(num),'Device:D_Zener','SMBJ51A','Diode_SMD:D_SMB',{1:net,2:'GND'},'pv','SMBJ51A')
# Module nets assigned by pin NAME by generator, not assumed DevKit pin order.
add('U6','RF_Module:ESP32-C6-MINI-1','ESP32-C6-MINI-1-N4','TankMonitor:ESP32-C6-MINI-1-edge-silk',{},'controller','ESP32-C6-MINI-1-N4','https://www.espressif.com/sites/default/files/documentation/esp32-c6-mini-1_mini-1u_datasheet_en.pdf')
parts[-1]['named_nets']={'GND':'GND','3V3':'V3V3','EN':'EN','GPIO6':'SDA','GPIO7':'SCL','GPIO4':'LOOP_EN_N','GPIO9':'BOOT','GPIO8':'STRAP8','TXD0':'TXD','RXD0':'RXD','GPIO12':None,'GPIO13':None}
res('R50','4.7k','V3V3','SDA','controller');res('R51','4.7k','V3V3','SCL','controller')
res('R52','10k','V3V3','EN','controller');cap('C50','1u','EN','GND','controller')
res('R53','10k','V3V3','BOOT','controller');res('R54','10k','V3V3','STRAP8','controller')
cap('C51','10u 35V X5R','V3V3','GND','controller','Capacitor_SMD:C_0805_2012Metric');cap('C52','100n','V3V3','GND','controller')
for ref,net in [('SW1','EN'),('SW2','BOOT')]:add(ref,'Switch:SW_Push','RESET' if ref=='SW1' else 'BOOT','Button_Switch_SMD:SW_SPST_TL3342',{1:net,2:'GND'},'controller','TL3342F160QG-TR')
add('J7','Connector_Generic:Conn_01x06','UART 3.3V ONLY','Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical',{1:'GND',2:'V3V3',3:'TXD',4:'RXD',5:'BOOT',6:'EN'},'controller','2.54mm 1x6 header')
add('D8','Device:LED','STATUS','LED_SMD:LED_0603_1608Metric',{1:'LED_K',2:'LED_A'},'controller','LTST-C190KGKT')
res('R55','2.2k','V3V3','LED_A','controller')
# Sink LED from spare GPIO18; no permanently lit power LED.
parts[[i for i,c in enumerate(parts) if c['ref']=='U6'][0]]['named_nets']['GPIO18']='LED_K'
parts[[i for i,c in enumerate(parts) if c['ref']=='U6'][0]]['named_nets']['GPIO19']='REV_FAULT'
parts[[i for i,c in enumerate(parts) if c['ref']=='U6'][0]]['named_nets']['GPIO20']='RAW_PRESENT'
for i,net in enumerate(['GND','V3V3','VIN','LOOP_SUPPLY','LOOP_P','SDA','SCL','BAT_FUSED','CHARGER_BAT','PV_IN','PV_OUT','LOOP_EN_N'],1):
 add('TP'+str(i),'Connector:TestPoint',net,'TestPoint:TestPoint_Pad_D2.0mm',{1:net},'test')
# Exact passive candidates; procurement status and DC-bias gates are recorded separately.
resistor_mpns={'2.74M':'RC0603FR-072M74L','215k':'RC0603FR-07215KL','84.5k':'RC0603FR-0784K5L','510k':'RC0603FR-07510KL','100k':'RC0603FR-07100KL','1k':'RC0603FR-071KL','130k 0.1%':'RT0603BRD07130KL','10k 0.1%':'RT0603BRD0710KL','4.99k':'RC0603FR-074K99L','10R':'RC0603FR-0710RL','47R':'RC0603FR-0747RL','4.7k':'RC0603FR-074K7L','10k':'RC0603FR-0710KL','2.2k':'RC0603FR-072K2L'}
capacitor_mpns={'C1':'C3225X7R1H106K250AC','C2':'C1608X7R1H104K080AA','C3':'C1608X7R1H104K080AA','C4':'C3225X7R1C226M250AC','C5':'C3225X7R1C226M250AC','C6':'C2012X7R1C475K125AB','C7':'C3225X7R1H475K250AB','C8':'C1608X7R1H103K080AA','C20':'C2012X7R2A104K125AA','C21':'C1608X7R1H104K080AA','C30':'C2012X7R2A104K125AA','C31':'C1608X7R1H104K080AA','C40':'C2012X7R2A104K125AA','C41':'C1608X7R1H104K080AA','C50':'C1608X7R1C105K080AC','C51':'C2012X5R1V106K085AC','C52':'C1608X7R1H104K080AA'}
for part in parts:
 if not part['mpn'] and part['ref'].startswith('R'):
  part['mpn']=resistor_mpns[part['value']]
  part['datasheet']='https://www.yageogroup.com/component-documentation/download/specsheet/'+part['mpn']
 if part['ref'] in capacitor_mpns:
  part['mpn']=capacitor_mpns[part['ref']]
  part['datasheet']='https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no='+part['mpn']
 if part['ref']=='J7':
  part['mpn']='TSW-106-07-G-S';part['datasheet']='https://www.samtec.com/products/tsw-106-07-g-s'
 if part['ref'] in ['D1','D3']:part['datasheet']='https://www.diodes.com/datasheet/download/B360A.pdf'
 if part['ref'] in ['R12','R13']:part['datasheet']='https://www.vishay.com/docs/20115/crcwhp.pdf'
 if part['ref']=='R11':part['datasheet']='https://www.yageogroup.com/component-documentation/download/specsheet/RT1206BRD072RL'
 if part['ref'] in ['L1','L2']:part['datasheet']='https://www.bourns.com/docs/product-datasheets/srp5030ta.pdf?sfvrsn=f08a91f1_28'
(p/'hardware/pcb/circuit.json').write_text(json.dumps({'revision':'0.2-dev','parts':parts},indent=2))
print(len(parts),'parts')
