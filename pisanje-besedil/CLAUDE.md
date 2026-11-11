# Moja besedila (pisanje-besedil/)

Spletni program za pisanje in popravljanje besedil (prej »Pisanje besedil«, nato
»Pisalnica«). Živi na https://brihta.github.io/sola/pisanje-besedil/ in je kartica
»✍️ Moja besedila« na glavni strani `sola/index.html`. Nino je avtor; piši mu v
slovenščini. Program uporabljajo v razredu, med živo uro, zato so popravki nujni
in morajo biti varni: majhni, preverjeni, takoj objavljeni.

## Datoteke
- `pisanje-besedil/index.html` je cela aplikacija v eni datoteki (HTML, CSS, JS). Urejevalnik je Quill.
- `supabase_pisanje.sql` (v korenu repozitorija) je baza: tabele, RPC funkcije, granti.
  Celo datoteko je mogoče pognati znova (`create or replace`, `add column if not exists`).
- Supabase projekt je isti kot pri Brihta-MAT in kvizih. Učenci se prijavijo z računom
  z Brihte (tabela `students`), učitelji pa s sejo iz `supabase_kvizi_ucitelj.sql` (`_sola_ucitelj`).

## Objava
- Stran: commit in push na `main` → GitHub Pages, približno 1 minuta. Učenci naj pritisnejo Ctrl+F5.
- Baza: SQL mora Nino pognati v Supabase → SQL Editor. Ko je za Macom, mu ga daj s
  `LANG=en_US.UTF-8 pbcopy`. Ko je v razredu (šolski računalnik), mu SQL pokaži tudi v
  ```sql bloku, ker odložišče z Maca tja ne pride.
- Pred objavo JS preveri sintakso: izlušči inline `<script>` in poženi `node --check`.
  Za ogled je v `matematika/.claude/launch.json` nastavitev za predogled »sola« (port 8768).

## Podatkovni model (glavno)
- `sola_pis_projekti`: ime, opis (navodilo), razred ('4', '4A' ali NULL), presoja, arhiviran,
  zaklenjen, `popravi_sam` (privzeto **true**), `ucitelj_id` (lastnik; vsak učitelj vidi samo svoje).
- `sola_pis_besedila`: en zapis na učenca in projekt: naslov, `vsebina` (Quill delta, jsonb),
  besedilo (golo), besed, `verzija` (optimistično zaklepanje → KONFLIKT), urejal ('ucenec'/'ucitelj'),
  komentar, `popravki`, `rezerva`.
- `vsebina.naslov = {a, c}`: poravnava ('left'/'center'/'right') in barva naslova. Naslov je
  ločeno polje `<input>` nad Quillom. Privzeto je na sredini.
- `popravki = {pred, po, cas}` (+ `vsebina`, `verzija` v načinu »Popravi sam«): pred/po sta
  {naslov, besedilo} kot golo besedilo, iz njiju se izriše rdeča primerjava.
- `rezerva = {naslov, vsebina, besedilo, besed, cas}` je varovalka. `_sola_pis_zapisi` jo zapiše,
  ko se besedilo z vsaj 15 besedami naenkrat več kot prepolovi. Učitelj jo vrne z gumbom
  »↶ Vrni prejšnjo različico« (`sola_pis_u_vrni_rezervo`, ki zamenja trenutno besedilo in rezervo).
- `sola_pis_presoje`: vrstniška presoja »dve zvezdi in želja« (anonimno).
- `sola_pis_ucitelji`: ime učitelja, ki ga vidijo učenci (npr. »ga. Teja«).

## Načina popravljanja
- **Popravi sam** (privzeto; Nino želi tako, ker se le tako učenec kaj nauči): učitelj popravlja
  KOPIJO (`popravki.vsebina`), učenčevo besedilo ostane. Učenec levo vidi rdeče popravke,
  desno sam popravi svoje besedilo. Učitelj nato zeleno vidi, kaj je učenec popravil.
- **Popravljam jaz**: učitelj piše naravnost v učenčevo besedilo. Nino tega načina ne želi kot privzetega.

## Odločitve in zgodovina
- Črkovalnik brskalnika je bil izklopljen, 10. 11. 2026 pa spet **vklopljen** (Nino je želel, da podčrta napake).
- Orodna vrstica: Razveljavi/Ponovi, Naslov 1, Podnaslov, Navadno, K/L/P, poravnave, barva,
  velikost. Ko je kazalec v naslovu, poravnava in barva veljata za naslov.
- Brez strežniške zgodovine različic, razen `rezerve`. Če učenec zbriše in shrani, je prejšnje
  besedilo ohranjeno samo v rezervi ali v `popravki.pred`/`po`.
- Prenos projekta k drugi učiteljici: skrbnik (`sola_pis_a_prenesi`) ali SQL `update sola_pis_projekti set ucitelj_id = …`.
- 10. 11. 2026, ura s 4.B (ga. Teja Perme): projekt »Jesenske počitnice« je prešel k Teji in je
  preklopljen na »Popravi sam«. Štirje že popravljeni teksti so bili vrnjeni učencem (oblikovanje izgubljeno).
- Podrobna zgodovina: `git log -- pisanje-besedil supabase_pisanje.sql`.

## Ideje za naprej
- Skupno lastništvo projekta (dva učitelja); zdaj ima projekt samo enega lastnika.
- Morda: učenec sam vidi gumb za vrnitev rezerve.
