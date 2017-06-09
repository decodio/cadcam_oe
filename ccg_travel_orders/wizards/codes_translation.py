# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2017 CADCAM Design Centar d.o.o. (<http://www.cadcam-group.eu/>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from genshi.path import FalseFunction



country_translation = {
"AF":("AFG", 4), "AX":("ALA", 248), "AL":("ALB", 8), "DZ":("DZA", 12), "AS":("ASM", 16),
"AD":("AND", 20), "AO":("AGO", 24), "AI":("AIA", 660), "AQ":("ATA", 10), "AG":("ATG", 28),
"AR":("ARG", 32), "AM":("ARM", 51), "AW":("ABW", 533), "AU":("AUS", 36), "AT":("AUT", 40),
"AZ":("AZE", 31), "BS":("BHS", 44), "BH":("BHR", 48), "BD":("BGD", 50), "BB":("BRB", 52),
"BY":("BLR", 112), "BE":("BEL", 56), "BZ":("BLZ", 84), "BJ":("BEN", 204), "BM":("BMU", 60),
"BT":("BTN", 64), "BO":("BOL", 68), "BQ":("BES", 535), "BA":("BIH", 70), "BW":("BWA", 72),
"BV":("BVT", 74), "BR":("BRA", 76), "IO":("IOT", 86), "BN":("BRN", 96), "BG":("BGR", 100),
"BF":("BFA", 854), "BI":("BDI", 108), "CV":("CPV", 132), "KH":("KHM", 116), "CM":("CMR", 120),
"CA":("CAN", 124), "KY":("CYM", 136), "CF":("CAF", 140), "TD":("TCD", 148), "CL":("CHL", 152),
"CN":("CHN", 156), "CX":("CXR", 162), "CC":("CCK", 166), "CO":("COL", 170), "KM":("COM", 174),
"CG":("COG", 178), "CD":("COD", 180), "CK":("COK", 184), "CR":("CRI", 188), "CI":("CIV", 384),
"HR":("HRV", 385), #"HR":("HRV", 191),
"CU":("CUB", 192), "CW":("CUW", 531), "CY":("CYP", 196), "CZ":("CZE", 203),
"DK":("DNK", 208), "DJ":("DJI", 262), "DM":("DMA", 212), "DO":("DOM", 214), "EC":("ECU", 218),
"EG":("EGY", 818), "SV":("SLV", 222), "GQ":("GNQ", 226), "ER":("ERI", 232), "EE":("EST", 233),
"ET":("ETH", 231), "FK":("FLK", 238), "FO":("FRO", 234), "FJ":("FJI", 242), "FI":("FIN", 246),
"FR":("FRA", 250), "GF":("GUF", 254), "PF":("PYF", 258), "TF":("ATF", 260), "GA":("GAB", 266),
"GM":("GMB", 270), "GE":("GEO", 268), "DE":("DEU", 276), "GH":("GHA", 288), "GI":("GIB", 292),
"GR":("GRC", 300), "GL":("GRL", 304), "GD":("GRD", 308), "GP":("GLP", 312), "GU":("GUM", 316),
"GT":("GTM", 320), "GG":("GGY", 831), "GN":("GIN", 324), "GW":("GNB", 624), "GY":("GUY", 328),
"HT":("HTI", 332), "HM":("HMD", 334), "VA":("VAT", 336), "HN":("HND", 340), "HK":("HKG", 344),
"HU":("HUN", 348), "IS":("ISL", 352), "IN":("IND", 356), "ID":("IDN", 360), "IR":("IRN", 364),
"IQ":("IRQ", 368), "IE":("IRL", 372), "IM":("IMN", 833), "IL":("ISR", 376), "IT":("ITA", 380),
"JM":("JAM", 388), "JP":("JPN", 392), "JE":("JEY", 832), "JO":("JOR", 400), "KZ":("KAZ", 398),
"KE":("KEN", 404), "KI":("KIR", 296), "KP":("PRK", 408), "KR":("KOR", 410), "KW":("KWT", 414),
"KG":("KGZ", 417), "LA":("LAO", 418), "LV":("LVA", 428), "LB":("LBN", 422), "LS":("LSO", 426),
"LR":("LBR", 430), "LY":("LBY", 434), "LI":("LIE", 438), "LT":("LTU", 440), "LU":("LUX", 442),
"MO":("MAC", 446), "MK":("MKD", 807), "MG":("MDG", 450), "MW":("MWI", 454), "MY":("MYS", 458),
"MV":("MDV", 462), "ML":("MLI", 466), "MT":("MLT", 470), "MH":("MHL", 584), "MQ":("MTQ", 474),
"MR":("MRT", 478), "MU":("MUS", 480), "YT":("MYT", 175), "MX":("MEX", 484), "FM":("FSM", 583),
"MD":("MDA", 498), "MC":("MCO", 492), "MN":("MNG", 496), "ME":("MNE", 499), "MS":("MSR", 500),
"MA":("MAR", 504), "MZ":("MOZ", 508), "MM":("MMR", 104), "NA":("NAM", 516), "NR":("NRU", 520),
"NP":("NPL", 524), "NL":("NLD", 528), "NC":("NCL", 540), "NZ":("NZL", 554), "NI":("NIC", 558),
"NE":("NER", 562), "NG":("NGA", 566), "NU":("NIU", 570), "NF":("NFK", 574), "MP":("MNP", 580),
"NO":("NOR", 578), "OM":("OMN", 512), "PK":("PAK", 586), "PW":("PLW", 585), "PS":("PSE", 275),
"PA":("PAN", 591), "PG":("PNG", 598), "PY":("PRY", 600), "PE":("PER", 604), "PH":("PHL", 608),
"PN":("PCN", 612), "PL":("POL", 616), "PT":("PRT", 620), "PR":("PRI", 630), "QA":("QAT", 634),
"RE":("REU", 638), "RO":("ROU", 642), "RU":("RUS", 643), "RW":("RWA", 646), "BL":("BLM", 652),
"SH":("SHN", 654), "KN":("KNA", 659), "LC":("LCA", 662), "MF":("MAF", 663), "PM":("SPM", 666),
"VC":("VCT", 670), "WS":("WSM", 882), "SM":("SMR", 674), "ST":("STP", 678), "SA":("SAU", 682),
"SN":("SEN", 686), "RS":("SRB", 688), "SC":("SYC", 690), "SL":("SLE", 694), "SG":("SGP", 702),
"SX":("SXM", 534), "SK":("SVK", 703), "SI":("SVN", 705), "SB":("SLB", 90), "SO":("SOM", 706),
"ZA":("ZAF", 710), "GS":("SGS", 239), "SS":("SSD", 728), "ES":("ESP", 724), "LK":("LKA", 144),
"SD":("SDN", 729), "SR":("SUR", 740), "SJ":("SJM", 744), "SZ":("SWZ", 748), "SE":("SWE", 752),
"CH":("CHE", 756), "SY":("SYR", 760), "TW":("TWN", 158), "TJ":("TJK", 762), "TZ":("TZA", 834),
"TH":("THA", 764), "TL":("TLS", 626), "TG":("TGO", 768), "TK":("TKL", 772), "TO":("TON", 776),
"TT":("TTO", 780), "TN":("TUN", 788), "TR":("TUR", 792), "TM":("TKM", 795), "TC":("TCA", 796),
"TV":("TUV", 798), "UG":("UGA", 800), "UA":("UKR", 804), "AE":("ARE", 784), "GB":("GBR", 826),
"US":("USA", 840), "UM":("UMI", 581), "UY":("URY", 858), "UZ":("UZB", 860), "VU":("VUT", 548),
"VE":("VEN", 862), "VN":("VNM", 704), "VG":("VGB", 92), "VI":("VIR", 850), "WF":("WLF", 876),
"EH":("ESH", 732), "YE":("YEM", 887), "ZM":("ZMB", 894), "ZW":("ZWE", 716)
}

def get_country_code(country_A2_code):
    code = country_translation.get(country_A2_code, False)
    if code:
        return code[1]
    else:
        return False

currency_translation = {
"ALL":("8", "albanski lek"),
"DZD":("12 ", "alžirski dinar"),
"AZM":("31 ", "azerbajdžanski manat"),
"ARS":("32 ", "argentinski peso"),
"AUD":("36 ", "australski dolar"),
"AMD":("51 ", "armenski dram"),
"CAD":("124", "kanadski dolar"),
"CNY":("156", "kineski juan"),
"HRK":("191", "hrvatska kuna"),
"CUP":("192", "kubanski peso"),
"CYP":("196", "ciparska funta"),
"CZK":("203", "češka kruna"),
"DKK":("208", "danska kruna"),
"EEK":("233", "estonska kruna"),
"GIP":("292", "gibraltarska funta"),
"HKD":("344", "honkonški dolar"),
"HUF":("348", "mađarska forinta"),
"ISK":("352", "islandska kruna"),
"INR":("356", "indijska rupija"),
"IDR":("360", "indonezijska rupija"),
"IRR":("364", "iranski rial"),
"IQD":("368", "irački dinar"),
"ILS":("376", "novi izraelski šekel"),
"JMD":("388", "jamajčanski dolar"),
"JPY":("392", "japanski jen"),
"KZT":("398", "kazahstanski tenge"),
"JOD":("400", "jordanski dinar"),
"KPW":("408", "sjevernokorejski won"),
"KRW":("410", "južnokorejski won"),
"KWD":("414", "kuvajtski dinar"),
"LVL":("428", "latvijski lats"),
"LRD":("430", "liberijski dolar"),
"LYD":("434", "libijski dinar"),
"LTL":("440", "litvanski litas"),
"MTL":("470", "malteška lira"),
"MXN":("484", "meksički peso"),
"MDL":("498", "moldavski lej"),
"MAD":("504", "marokanski dirham"),
"NZD":("554", "novozelandski dolar"),
"NGN":("566", "naira"),
"NOK":("578", "norveška kruna"),
"RON":("642", "rumunjski leu"),
"SGD":("702", "singapurski dolar"),
"SKK":("703", "slovačka kruna"),
"VND":("704", "vijetnamski dong"),
"SIT":("705", "slovenski tolar"),
"ZAR":("710", "južnoafrički rand"),
"SEK":("752", "švedska kruna"),
"CHF":("756", "švicarski franak"),
"SYP":("760", "sirijska funta"),
"THB":("764", "tajlandski baht"),
"AED":("784", "emiratski dirham"),
"TND":("788", "tuniški dinar"),
"TRL":("792", "turska lira"),
"MKD":("807", "makedonski denar"),
"RUR":("810", "ruski rubalj"),
"EGP":("818", "egipatska funta"),
"GBP":("826", "britanska funta"),
"USD":("840", "američki dolar"),
"UZS":("860", "uzbekistanski sum"),
"VEB":("862", "venezuelski bolivar"),
"YUM":("891", "jugoslavenski dinar"),
"TWD":("901", "novi tajvanski dolar"),
"RSD":("941", "srpski dinar"),
"AFA":("971", "afgani"),
"BYR":("974", "bjeloruski rubalj"),
"BGN":("975", "bugarski lev"),
"BAM":("977", "konvertibilna marka"),
"EUR":("978", "euro"),
"UAH":("980", "ukrajinska grivna"),
"GEL":("981", "gruzijski lari"),
"PLN":("985", "poljski zlot"),
"BRL":("986", "brazilski real"),
} 

def get_currency_code(currency_name):
    code = currency_translation.get(currency_name, False)
    if code:
        return code[0]
    else:
        return False

product_to_expense = {

1:(1, "Kilometrina"),
2:(2, "Domaća dnevnica"),
3:(3, "Inozemna dnevnica"),
1022330:(4, "Cestarina"),
1022351:(5, "Taksi prijevoz"),
6:(6, "Rent a car"),
1022337:(7, "Avionska karta"),
8:(8, "Aerodromska taksa"),
1021461:(9, "Hotelski smještaj"),
10:(10, "Telefonski troškovi"),
11:(11, "Ulaznice (za sajam isl.)"),
1022323:(12, "Gorivo za osobno vozilo"),
13:(13, "Gorivo za dostavno vozilo"),
1022358:(14, "Reprezentacija"),
15:(15, "Špedicija"),
1022344:(16, "Parking i garaža"),
17:(17, "Sanitarni pregled"),
18:(18, "Terenski dodatak"),
19:(19, "Razno"),
21:(21, "Prijevoz željeznicom"),
22:(22, "Cestovni prijevoz"),
23:(23, "Pomorski prijevoz"),
31:(31, "Plaćeni privatni trošak 1"),
32:(32, "Plaćeni privatni trošak 2"),
33:(33, "Plaćeni privatni trošak 3"),
99:(99, "Ostalo"),
}

def get_expense_id(ccg_product_id):
    expense = product_to_expense.get(ccg_product_id, False)
    if expense:
        return expense[0]
    else:
        return False

transportation_type_code = {
1022207:(1, 'Osobni automobil'),
1022211:(2, 'Autobus'),
1022210:(3, 'Vlak'),
1022209:(4, 'Avion'),
99:(5, 'Brod'),
1022208:(6, 'Službeni automobil'),
98:(7, 'Teretno vozilo'),
 }

def get_transportation_type(crm_id):
    total_id = transportation_type_code.get(crm_id, False)
    if total_id:
        return total_id[0]

employee_by_company_id = {
#cad cam design centar
34151:{
34374:(1, 'Zlatko Šimunec'),
34366:(8, 'Krešimir Prlić'),
219748:(25, 'Nikola Mareković'),
34402:(38, 'Ivančica Zorić'),
34382:(42, 'Mladen Stošić'),
34394:(58, 'Vanja Trošelj'),
34370:(59, 'Stjepan Razum'),
34350:(64, 'Boris Kumpar'),
34362:(65, 'Ante Muselin'),
34358:(67, 'Domagoj Mijić'),
34386:(68, 'Mate Šušnjar'),
1439129:(71, 'Dinko Kulej'),
1021753:(72, 'Inda Balagić'),
1190982:(73, 'Miran Petrović'),
4427388:(75, 'Antonio Mikulić'),
4427397:(76, 'Goran Ležaić'),
4427425:(77, 'Sandra Vukelić'),
34418:(78, 'Lucija Babić'),
1191000:(79, 'Matko Ribičić'),
},

#cad cam grupa
34156:{
34374:(1, 'Zlatko Šimunec'),
34426:(2, 'Tamara Lacković'),
34414:(5, 'Keti Kusanović'),
},

#edmd
34166:{
34374:(1, 'Zlatko Šimunec'),
34430:(2, 'Bojan Brezina'),
},

#solid world adria
34161:{
35220:(3, 'Ivan Baburić'),
34374:(4, 'Zlatko Šimunec'),
1021764:(5, 'Ivan Radoš'),
},

}
def get_employee_id(company_id, ccg_employee_id):
    company = employee_by_company_id.get(company_id,False)
    if company :
        total_employee_id = company.get(ccg_employee_id, False)
        return total_employee_id[0]
    else:
        return False
        
    
