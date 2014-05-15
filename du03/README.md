Domáca úloha 3
==============

Domácu úlohu odovzdávajte elektronicky do Nedele 24.5. 23:59:59, fyzicky
najneskôr na prednáške alebo cvičeniach vo štvrtok 21.5.

Úlohu odovzdávajte buď fyzicky na papier formátu A4 (čitateľne označenom a
podpísanom) na prednáške alebo na cvičeniach, alebo elektronicky vo formáte PDF
(ako súbor `du03.pdf`), ako obyčjaný textový alebo súbor (`du03.txt`), alebo
ako súbor v GitHub Markdown formáte (`du03.md`) do vetvy `du03` (v adresári
`du03`). Nezabudnite vyrobiť pull request.

## 3.1 (2b)

Zapíšte v prvorádovej logike nasledovné tvrdenia (ak sú v zátvorke uvedené konkrétne
predikáty, použitie tie):


1.  Kto sa smeje naposledy, ten sa smeje najlepšie (ako hocikto iný).
    (`smejesa(kto,kedy)`, `skor(casSkor,casNeskor)`,
     `smejeSaLepsieAko(x,y)` - `x` sa smeje lepšie ako `y`)
1.  Každej pesničke býva koniec.
1. "[You Know Nothing, Jon Snow](http://knowyourmeme.com/memes/you-know-nothing-jon-snow)".
1.  Nepriatelia mojich nepriateľov sú mojimi priateľmi.
    (`priatel(kto, koho)`)
1.  Pomôž iným, pomôžeš aj sebe. (Potrebujete predikát `iny(x,y)` resp `≠`.)
1.  Vodič nesmie počas vedenia vozidla používať telefónny prístroj okrem
    telefonovania s použitím systému "voľné ruky" alebo vykonávať inú obdobnú
    činnosť, ktorá nesúvisí s vedením vozidla; to neplatí pre vodiča vozidla
    ozbrojených síl Slovenskej republiky (ďalej len "ozbrojené sily"),
    ozbrojených bezpečnostných zborov, ozbrojených zborov, Vojenskej polície,
    obecnej polície, Hasičského a záchranného zboru, ostatných hasičských
    jednotiek, Horskej záchrannej služby, záchrannej zdravotnej služby, banskej
    záchrannej služby, Vojenského spravodajstva a Slovenskej informačnej služby
    pri plnení svojich úloh.  
    (Zákon o cestnej premávke, § 4, ods. 2l)
1.  A sláva zašlých vekov junáka oviala;  
    a duša jeho svätým ohňom splápolala,

## 3.2 (2b)
Sformalizujte v prvorádovej logike a dokážte (tablovou metódou):

Dobre sformátovaný súbor nemôže obsahovať naraz (ako indentáciu) medzery
aj tabulátory.
Ak programátor, ktorý nemá rad tabulátory, needituje žiadny súbor s
tabulátormi, tak je spokojný (ak všetky súbory, ktoré edituje, neobsahujú
tabulátory, tak je spokojný).
Existuje aspoň jeden nespokojný programátor, ktorý nemá rád
tabulátory.
Všetky súbory obsahujú medzery.
Dokážte, že aspoň jeden súbor nie je dobre sformátovaný.

\medskip
Jednotlivé tvrdenia sformalizujte pomocou predikátov:
- `p(x)` - `x` je programátor;
- `s(x)` - `x` je súbor;
- `e(x,y)` - (programátor) `x` edituje (súbor) `y`;
- `sp(x)` - `x` je spokojný;
- `mt(x)` - `x` má rád tabulátory.
- `df(x)` - `x` je dobre sformátovaný;
- `om(x)` - `x` obsahuje medzery;
- `ot(x)` - `x` obsahuje tabulátory.


## 3.3 (2b)

Pre každú z nasledujúcich troch formúl vždy **doplňte** štruktúru M tak, aby formula
bola v M a) pravdivá, b) nepravdivá, alebo dokážte že to nejde.

M = (D,i):
- D = { 0, 1, 2 }
- i(c) = **???**
- i(f):
    - f(0) = 0
    - **???**
- i(P) = { (0), **???** }
- i(Q) = { (0,0), (1,1), (2,0), (2,1), (2,2), **???** }

1. ( ∀x(¬P(x) ∨ ¬Q(x,f(c))) → (∀x¬P(x) ∨ ∀x¬Q(x,f(c))) )
1. ( ∀xP(x) ∧ ∃x¬P(f(x)) )
1. ( (¬∃xP(x) ∧ ∀x∃y¬Q(x,f(y))) → ∀x(¬P(x) ∧ ¬∀yQ(f(x),y)) )

- - -
Prikad pre formulu ∀xP(x):

a) Doplníme  i(P) = { (0), (1), (2) }. Formula ∀xP(x) je teraz pravdivá (na
interpretácii ostatných symbolov nezáleží, mohli by sme ale ešte aspoň
dodefinovat f, nech je to korektná funkcia)

b) Doplníme (resp. nedoplníme :-)  i(P) = { (0) }. Formula ∀xP(x) je teraz nepravdivá.
