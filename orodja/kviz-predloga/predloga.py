import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

OUT = sys.argv[1]
F = "Arial"
VRSTE = ["Izbira", "Drži / Ne drži", "Poveži", "Razvrsti", "Število"]
RUMENA = PatternFill("solid", fgColor="FFF8D6")
GLAVA = PatternFill("solid", fgColor="C0392B")   # rdeča Brihta
SIVA = PatternFill("solid", fgColor="F2F2F2")
ZELENA = PatternFill("solid", fgColor="D5F0DC")
ROZA = PatternFill("solid", fgColor="FBE0DD")
tanka = Side(style="thin", color="D0D0D0")
rob = Border(left=tanka, right=tanka, top=tanka, bottom=tanka)
PRVA, ZADNJA = 6, 65   # vrstice vprašanj (60 vprašanj)

def pomoc(r):
    b = f"$B{r}"
    return (f'=IF({b}="Izbira","Odgovor 1 = pravilni, Odgovor 2 do 5 = napačni (vsaj 1)",'
            f'IF({b}="Drži / Ne drži","Odgovor 1 = Drži ali Ne drži",'
            f'IF({b}="Poveži","Vsak odgovor je par: pojem = razlaga (vsaj 2 para)",'
            f'IF({b}="Razvrsti","Odgovori v PRAVILNEM vrstnem redu (vsaj 2)",'
            f'IF({b}="Število","Odgovor 1 = pravilno število","")))))')

def preveri(r):
    b, c, d = f"$B{r}", f"$C{r}", f"$D{r}"
    vsi = f"$D{r}:$I{r}"
    pari = f'SUMPRODUCT(--ISNUMBER(SEARCH(" = ",{vsi})))'
    return (f'=IF(AND({b}="",{c}="",COUNTA({vsi})=0),"",'
            f'IF({b}="","Izberi vrsto vprašanja",'
            f'IF({c}="","Manjka vprašanje",'
            f'IF({b}="Izbira",IF({d}="","Manjka pravilni odgovor (Odgovor 1)",'
                f'IF(COUNTA($E{r}:$H{r})=0,"Dodaj vsaj en napačen odgovor",'
                f'IF($I{r}<>"","Pri izbiri je največ 4 napačnih (Odgovor 6 pusti prazen)","✓ V redu"))),'
            f'IF({b}="Drži / Ne drži",IF(OR({d}="Drži",{d}="Ne drži"),"✓ V redu","V Odgovor 1 napiši Drži ali Ne drži"),'
            f'IF({b}="Poveži",IF({pari}<2,"Vsaj 2 para v obliki pojem = razlaga",'
                f'IF({pari}<COUNTA({vsi}),"Vsak par potrebuje presledek, enačaj, presledek ( = )","✓ V redu")),'
            f'IF({b}="Razvrsti",IF(COUNTA({vsi})<2,"Vsaj 2 odgovora v pravilnem vrstnem redu","✓ V redu"),'
            f'IF({b}="Število",IF(ISNUMBER({d}),"✓ V redu","Odgovor 1 mora biti število"),'
            f'"Neznana vrsta: izberi s seznama"))))))))')

def list_kviza(ws, naslov, opis, vprasanja):
    ws.sheet_view.showGridLines = False
    widths = {"A": 5, "B": 16, "C": 46, "D": 24, "E": 22, "F": 22, "G": 22, "H": 22, "I": 22, "J": 44, "K": 34}
    for k, v in widths.items():
        ws.column_dimensions[k].width = v
    ws["A1"] = "Naslov kviza"; ws["A2"] = "Opis (ni obvezno)"
    for r in (1, 2):
        ws.cell(r, 1).font = Font(name=F, bold=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=6)
        ws.cell(r, 3).fill = RUMENA; ws.cell(r, 3).border = rob
    ws["C1"] = naslov; ws["C2"] = opis
    ws["C1"].font = Font(name=F, bold=True, size=13); ws["C2"].font = Font(name=F)
    ws.row_dimensions[1].height = 22
    ws["A4"] = ("Piši samo v rumena polja: naslov, vrsta, vprašanje in odgovori. "
                "Vrsto izberi s spustnega seznama: klikni celico v stolpcu Vrsta in nato puščico ▾ desno od nje. "
                "Stolpca Kaj vpišem in Preverjanje se izpolnita sama: ko so vsa vprašanja »✓ V redu«, kviz naloži na Brihto. "
                "Slike dodaš na Brihti, ko je kviz že narejen.")
    ws["A4"].font = Font(name=F, italic=True, size=9, color="555555")
    ws["A4"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A4:K4"); ws.row_dimensions[4].height = 30
    glave = ["Št.", "Vrsta ▾", "Vprašanje", "Odgovor 1", "Odgovor 2", "Odgovor 3",
             "Odgovor 4", "Odgovor 5", "Odgovor 6", "Kaj vpišem (samo)", "Preverjanje (samo)"]
    for i, g in enumerate(glave, 1):
        c = ws.cell(PRVA - 1, i, g)
        c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = GLAVA
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True); c.border = rob
    ws.row_dimensions[PRVA - 1].height = 22
    for r in range(PRVA, ZADNJA + 1):
        ws.cell(r, 1, r - PRVA + 1).font = Font(name=F, color="888888")
        ws.cell(r, 1).alignment = Alignment(horizontal="center", vertical="top")
        for col in range(2, 10):
            c = ws.cell(r, col); c.fill = RUMENA; c.border = rob
            c.font = Font(name=F); c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(r, 10, pomoc(r)); ws.cell(r, 11, preveri(r))
        for col in (10, 11):
            c = ws.cell(r, col); c.fill = SIVA; c.border = rob
            c.font = Font(name=F, size=9, color="555555"); c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, v in enumerate(vprasanja):
        r = PRVA + i
        for j, x in enumerate(v):
            ws.cell(r, 2 + j, x)
    rng = f"B{PRVA}:B{ZADNJA}"
    dv = DataValidation(type="list", formula1="Seznami!$A$1:$A$5", allow_blank=True,
                        showErrorMessage=True, errorTitle="Vrsta vprašanja",
                        error="Izberi vrsto s seznama: " + ", ".join(VRSTE) + ".",
                        promptTitle="Vrsta vprašanja", prompt="Klikni puščico ▾ desno od celice in izberi vrsto.")
    dv.showInputMessage = True
    ws.add_data_validation(dv); dv.add(rng)
    # barvni namig: pravilni zeleno, napačni roza
    ws.conditional_formatting.add(f"D{PRVA}:D{ZADNJA}", FormulaRule(
        formula=[f'OR($B{PRVA}="Izbira",$B{PRVA}="Drži / Ne drži",$B{PRVA}="Število")'], fill=ZELENA))
    ws.conditional_formatting.add(f"E{PRVA}:H{ZADNJA}", FormulaRule(
        formula=[f'$B{PRVA}="Izbira"'], fill=ROZA))
    ws.conditional_formatting.add(f"K{PRVA}:K{ZADNJA}", FormulaRule(
        formula=[f'LEFT(K{PRVA},1)="✓"'], font=Font(name=F, size=9, color="1E7B34", bold=True)))
    ws.conditional_formatting.add(f"K{PRVA}:K{ZADNJA}", FormulaRule(
        formula=[f'AND(K{PRVA}<>"",LEFT(K{PRVA},1)<>"✓")'], font=Font(name=F, size=9, color="C0392B", bold=True)))
    ws.freeze_panes = f"D{PRVA}"

wb = Workbook()
sez = wb.create_sheet("Seznami")
for i, v in enumerate(VRSTE, 1):
    sez.cell(i, 1, v)
sez.sheet_state = "hidden"
kviz = wb.active; kviz.title = "Kviz"
list_kviza(kviz, "", "", [])

primer = wb.create_sheet("Primer")
list_kviza(primer, "Živali na kmetiji", "Primer: tako je videti izpolnjen kviz.", [
    ["Izbira", "Katera žival daje mleko?", "krava", "kokoš", "konj", "pes", "mačka"],
    ["Drži / Ne drži", "Kokoš ima štiri noge.", "Ne drži"],
    ["Poveži", "Poveži žival z njenim mladičem.", "krava = tele", "ovca = jagnje", "kokoš = pišče", "konj = žrebe"],
    ["Razvrsti", "Razvrsti od najmanjše do največje živali.", "piščanec", "mačka", "ovca", "konj"],
    ["Število", "Koliko nog ima krava?", 4],
])
primer.sheet_properties.tabColor = "7F8C8D"

nav = wb.create_sheet("Navodila", 0)
nav.sheet_view.showGridLines = False
nav.column_dimensions["A"].width = 18; nav.column_dimensions["B"].width = 52; nav.column_dimensions["C"].width = 52
vr = [
    ("Brihta: predloga za kviz", "naslov"),
    ("1. Shrani svojo kopijo te datoteke (Datoteka › Shrani kopijo). Predloge ne spreminjaj.", "t"),
    ("2. Na listu »Kviz« vpiši naslov in vprašanja: eno vprašanje v eno vrstico.", "t"),
    ("3. V stolpcu Vrsta klikni celico in nato puščico ▾: izberi Izbira, Drži / Ne drži, Poveži, Razvrsti ali Število. Stolpec »Kaj vpišem« ti pove, kaj gre v odgovore.", "t"),
    ("4. Ko je v stolpcu Preverjanje povsod »✓ V redu«, se prijavi na Brihti, odpri modul in naloži datoteko.", "t"),
    ("5. Slike dodaš na Brihti, ko je kviz že narejen. Učencem se odgovori premešajo, zato ne piši »vse zgoraj navedeno«.", "t"),
    ("", "t"),
]
r = 1
for txt, k in vr:
    c = nav.cell(r, 1, txt); nav.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
    c.font = Font(name=F, bold=True, size=16, color="C0392B") if k == "naslov" else Font(name=F, size=11)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    nav.row_dimensions[r].height = 28 if k == "naslov" else 18
    r += 1
for i, g in enumerate(["Vrsta", "Kaj vpišeš v odgovore", "Primer"], 1):
    c = nav.cell(r, i, g); c.font = Font(name=F, bold=True, color="FFFFFF"); c.fill = GLAVA; c.border = rob
r += 1
tabela = [
    ("Izbira", "Odgovor 1 = pravilni odgovor.\nOdgovor 2 do 5 = napačni odgovori (vsaj 1, največ 4). Najboljši so pogoste napačne predstave učencev.",
     "Katera žival daje mleko?\n1: krava  2: kokoš  3: konj  4: pes"),
    ("Drži / Ne drži", "Odgovor 1 = Drži ali Ne drži.", "Kokoš ima štiri noge.\n1: Ne drži"),
    ("Poveži", "Vsak odgovor je par: pojem = razlaga (presledek, enačaj, presledek). Vsaj 2 para, največ 6.",
     "Poveži žival z mladičem.\n1: krava = tele  2: ovca = jagnje"),
    ("Razvrsti", "Odgovori v PRAVILNEM vrstnem redu. Vsaj 2, največ 6. Učencem se premešajo.",
     "Od najmanjše do največje.\n1: piščanec  2: mačka  3: konj"),
    ("Število", "Odgovor 1 = pravilno število. Učenec ga vpiše sam. Decimalna vejica je v redu.",
     "Koliko nog ima krava?\n1: 4"),
]
for row in tabela:
    for i, x in enumerate(row, 1):
        c = nav.cell(r, i, x); c.border = rob
        c.font = Font(name=F, bold=(i == 1)); c.alignment = Alignment(wrap_text=True, vertical="top")
    nav.row_dimensions[r].height = 48
    r += 1
r += 1
c = nav.cell(r, 1, "Vsako vprašanje je 1 točka. Na listu »Primer« je izpolnjen kviz, ki ga lahko poskusno naložiš.")
nav.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
c.font = Font(name=F, italic=True, size=10, color="555555")
nav.sheet_properties.tabColor = "C0392B"
kviz.sheet_properties.tabColor = "F1C40F"
for w in wb.worksheets:
    w.page_setup.orientation = "landscape"; w.page_setup.paperSize = 9
    w.page_setup.fitToWidth = 1; w.page_setup.fitToHeight = 0
    w.sheet_properties.pageSetUpPr.fitToPage = True
wb.active = 1
wb.save(OUT)
print("ok")
