Cvičenie 11
==========

**Riešenie odovzdávajte podľa
[pokynov na konci tohoto zadania](#technické-detaily-riešenia)
do Štvrtka 21.5. 23:59:59.**

Toto cvičenie je bonusové v zmysle, že si ním môžete nahradiť niektoré iné
cvičenie, t.j. zaráta sa Vám namiesto cvičenia za ktoré ste dostali najmenej
bodov (alebo ste ho neodovzdali).

Súbory potrebné pre toto cvičenie si môžete stiahnúť ako jeden zip
[`cv11.zip`](https://github.com/FMFI-UK-1-AIN-411/udvl/archive/cv11.zip).

## Logická hádanka (4b)

Nasledujúcu logickú hádanku zakódujte do výrokovej logiky a vyriešte pomocou
SAT solvera. Odovzdávajte program ktorý vygeneruje vstup pre SAT solver,
pustí SAT solver, načíta a dekóduje výstup a vypíše riešenie.
V programe (v komentároch) uveďte formuly, ktorými ste problém popísali.

Pán a pani Smithovci a ich dve deti sú typická americká rodina. Vieme, že práve
dve tvrdenia z nasledovných sú pravdivé:

- George a Dorothy sú pokrvní príbuzní
- Howard je starší než George
- Virginia je mladšia než Howard
- Virginia je staršia než Dorothy

Aké je krstné meno otca, mamy, syna, dcéry?

*Pomôcka 1*: Hádanka má práve jedno riešenie. SAT solver môže nájsť viacero
modelov vašej teórie, všetky by však mali rovnako ohodnocovať premenné, ktoré
zakóduvajú riešenie a mali by sa líšiť len ohodnotením pomocných premenných.

*Pomocka 2*: Okrem explicitne vyslovených podmienok máme aj nejaké nevyslovené,
ktoré sa skrývajú pod pojmom "typická americká rodina". Čo všetko pod tým autor
hádanky myslel?

*Pomocka 3*: Ďalšie nevyslovené podmienky, ktoré pri formalizácii musíme
uvažovať, sú typu: Tá ista osoba nemôže byť zároveň otcom aj synom.

*Pomocka 4*: Zadefinujte obmedzenia na členov rodiny pre pojmy: pokrvní
príbuzní, starší/mladší. Toto úzko súvisí s ujasnením si skutočností v pomôcke
2. Ktorí členovia rodiny môžu byž pokrvní príbuzní, ktorí môže byť starší od
ktorého, ...?

*Pomôcka 5*: Keby sme iba jednoducho zakódovali všetky tvrdenia a dali na vstup
SAT solveru, tak by našiel možnosti, kedy sú všetky naraz pravdivé. Úloha ale
hovorí, že práve dve tvrdenia majú byť pravdivé (a dve teda nepravdivé). Toto
zabezpečíme tak, že použijeme 4 pomocné premenné (jednu pre každé tvrdenie),
ktoré budú pravdivé práve vtedy keď dotyčné tvrdenie je pravdivé. Čiže na vstup
SAT solveru chceme dať tvrdenia tvaru p1 ≡ TVRDENIE1, p1 ≡ TVRDENIE1,... (toto
budú samozrejme zakaždým 2 implikácie, ktoré sa možu skonvertovať na viacero
CNF klauz) a potom tvrdenia, ktoré zabezpečia, že práve 2 platia a 2 neplatia.

*Pomôcka 6*: Zabezpečiť že práve 2 sú pravdivé, sa dá napríklad vymenovaním
všetkých možností, čo ale bude DNF z ktorého roznásobením vznikne veľa klauz.
Lepšia možnosť je povedať, že aspoň 2 musia byť pravdivé a nesmie byť viac ako
2 pravdivých (tj nesmú byť 3 pravdivé). Jednotlivé možnosti v druhej podmienke
sú negácie konjunkcií, čo sú priamo klauzy. Prvá podmienka bude ešte stále DNF,
ale iba s konjunkciami s 2 premennými. Dá sa to však tiež vylepšiť, ak ju
preformulujeme ako "nesmú byť viac ako 2 (aspoň 3) nepravdivé"

## Technické detaily riešenia

Riešenie odovzdajte do vetvy `cv11` v adresári `cv11`.

Odovzdajte súbor `cv11.py`/`cv11.cpp`/`Cv11.java`, ktorý zakóduje problém,
pustí SAT solver, načíta a dekóduje výstup a vypíše na štandartný výstup
riešenie vo formáte:

```
otec: Oooo
matka: Mmmm
syn: Ssss
dcera: Dddd
```

Ak chcete v pythone použiť knižnicu z [examples/sat](../examples/sat), nemusíte
si ju kopírovať do aktuálne adresára, stačí ak na začiatok svojej knižnice
pridáte:
```python
import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat
```

Odovzdávanie riešení v iných jazykoch konzultujte s cvičiacimi.
