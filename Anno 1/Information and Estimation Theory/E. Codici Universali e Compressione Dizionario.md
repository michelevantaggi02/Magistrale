# E. Codici Universali e Compressione Dizionario

La teoria della codifica di sorgente sviluppata nei capitoli precedenti ha stabilito le basi matematiche per la compressione dati senza perdita (lossless), culminando nell'algoritmo di Huffman e nei codici ottimi di Shannon. Tuttavia, l'applicabilità pratica di tali tecniche presuppone una conoscenza esatta e preliminare della funzione di massa di probabilità (PMF) $p(x)$ che governa la sorgente.

Nei moderni sistemi informatici, nelle reti di telecomunicazione e nei file system, tale assunzione teorica è quasi sempre violata:
1. La statistica della sorgente è raramente nota a priori (si pensi a un archivio compresso contenente codice sorgente, testo formattato, eseguibili binari e database).
2. Molti processi reali sono non stazionari: la frequenza locale dei caratteri varia dinamicamente lungo il flusso dei dati.
3. Spesso i dati consistono in una singola sequenza finita e deterministica (un file di testo o un firmware) priva di un ensemble probabilistico sottostante, la cui comprimibilità ultima è legata alla __complessità di Kolmogorov__.

Un approccio empirico a due passate (offline), consistente nel calcolare l'istogramma dei caratteri nella prima passata e codificare i dati nella seconda mediante Huffman, introduce latenze inaccettabili nei sistemi streaming e richiede la trasmissione preliminare dell'albero o della tabella del codice, con un sensibile sovraccarico (overhead).

La __codifica universale di sorgente__ risolve questo limite mediante algoritmi a singola passata (online / streaming): il codificatore non assume alcuna conoscenza probabilistica a priori, ma "impara" la struttura statistica del flusso man mano che elabora i simboli, sfruttando progressivamente le regolarità riscontrate per comprimere il testo.

Un algoritmo di compressione è definito __asintoticamente universale__ se, applicato a qualsiasi processo stocastico stazionario ed ergodico $\{\mathcal{X}\}$, la lunghezza media per simbolo $l(X^n)/n$ converge con probabilità 1 al limite teorico assoluto di Shannon:

$$
\lim_{n \to \infty} \frac{1}{n} l(X^n) = H(\mathcal{X}) \quad \text{quasi certamente}
$$

Questo capitolo illustra l'intera gerarchia della compressione universale: dai codici di Golomb-Rice per distribuzioni geometriche, alla codifica aritmetica a intervalli continui, fino alla famiglia degli algoritmi a dizionario adattivo di Lempel-Ziv (LZ77, LZ78, LZW) che costituisce l'ossatura tecnologica del web e dell'archiviazione dati moderna.

## Codici di Golomb-Rice per Distribuzioni Geometriche (Run-Length Coding)

Quando i dati da comprimere sono costituiti da numeri interi non negativi $x \in \mathbb{N}_0 = \{0, 1, 2, \dots\}$ con probabilità fortemente decrescenti (come le lunghezze delle sequenze di zeri nella codifica Run-Length, o gli errori di predizione nei codec lossless), la costruzione di un albero di Huffman classico su un alfabeto potenzialmente illimitato risulterebbe impraticabile.

La famiglia dei __codici di Golomb__ (1966) e la sua specializzazione binaria, i __codici di Rice__ (1979), forniscono una soluzione universale parametrizzata e a complessità computazionale minima.

### Il Codice Unario

La forma più elementare di codifica per interi è il __codice unario__: ciascun intero $x \ge 0$ viene codificato mediante una sequenza di $x$ bit posti a '1' seguiti da un singolo bit di stop '0':

$$
C_{\text{unario}}(x) = \underbrace{11\dots1}_{x \text{ volte}} 0
$$

La lunghezza della parola di codice è $l(x) = x + 1$ bit:
- $x = 0 \implies 0$ (1 bit)
- $x = 1 \implies 10$ (2 bit)
- $x = 2 \implies 110$ (3 bit)
- $x = 4 \implies 11110$ (5 bit)

Il codice unario coincide esattamente con il codice di Huffman ottimo per una sorgente discreta supportata sull'alfabeto infinito $\mathbb{N}_0$ avente distribuzione geometrica diadica di parametro $\theta = \frac{1}{2}$:

$$
p(x) = 2^{-(x+1)}, \quad x = 0, 1, 2, \dots
$$

Poiché le probabilità sono potenze intere di due ($l(x) = -\log_2 p(x) = x + 1$), il codice unario è istantaneo e raggiunge l'entropia della sorgente con efficienza unitaria pari al $100\%$.

### Struttura del Codice di Golomb con Parametro $M$

Per distribuzioni geometriche generiche $p(x) = (1 - \theta)\theta^x$ con parametro di decadimento $\theta \in (0, 1)$ arbitrario, Solomon Golomb (1966) ha introdotto una famiglia di codici prefissi indicizzati da un intero positivo $M \ge 1$.

Il numero intero $x \ge 0$ viene scomposto tramite divisione euclidea per $M$:

$$
x = q M + r
$$

dove:
- $q = \left\lfloor \frac{x}{M} \right\rfloor \in \{0, 1, 2, \dots\}$ è il quoziente intero;
- $r = x \bmod M \in \{0, 1, \dots, M-1\}$ è il resto.

La parola di codice $C_M(x)$ è formata dalla concatenazione di due codici prefissi indipendenti:
1. __Codifica del quoziente $q$__: Viene codificato in unario ($q$ uni seguiti da uno zero), richiedendo $q + 1$ bit.
2. __Codifica del resto $r$__: Poiché $r$ può assumere $M$ valori distinti, viene codificato tramite un codice a troncamento binario (Truncated Binary Code) a lunghezza variabile:
   - Siano $k = \lfloor \log_2 M \rfloor$ e $u = 2^{k+1} - M$.
   - I primi $u$ valori di resto ($0 \le r < u$) sono codificati con $k$ bit standard.
   - I rimanenti $M - u$ valori ($u \le r < M$) sono codificati con $k + 1$ bit rappresentando il valore $r + u$.

### Esempio Analitico: Codice di Golomb per $M = 5$

Per $M = 5$, abbiamo $k = \lfloor \log_2 5 \rfloor = 2$, $\lceil \log_2 5 \rceil = 3$, e $u = 2^3 - 5 = 3$:
- I resti $r \in \{0, 1, 2\}$ usano $k = 2$ bit: $0 \to 00$, $1 \to 01$, $2 \to 10$.
- I resti $r \in \{3, 4\}$ usano $k+1 = 3$ bit rappresentando $r + 3$: $3 \to 110$, $4 \to 111$.

Valutiamo la codifica per i primi interi:
- $x = 0 \implies q = 0, r = 0 \implies C(0) = 0 \, 00$ (3 bit)
- $x = 1 \implies q = 0, r = 1 \implies C(1) = 0 \, 01$ (3 bit)
- $x = 2 \implies q = 0, r = 2 \implies C(2) = 0 \, 10$ (3 bit)
- $x = 3 \implies q = 0, r = 3 \implies C(3) = 0 \, 110$ (4 bit)
- $x = 4 \implies q = 0, r = 4 \implies C(4) = 0 \, 111$ (4 bit)
- $x = 5 \implies q = 1, r = 0 \implies C(5) = 10 \, 00$ (4 bit)
- $x = 8 \implies q = 1, r = 3 \implies C(8) = 10 \, 110$ (5 bit)
- $x = 13 \implies q = 2, r = 3 \implies C(13) = 110 \, 110$ (6 bit)

Per estendere la codifica all'insieme dei numeri interi relativi $\mathbb{Z}$, si applica la trasformazione biunivoca di alternanza di segno:

$$
x_{\text{mappato}} = \begin{cases} 2x & \text{se } x \ge 0 \\ 2|x| - 1 & \text{se } x < 0 \end{cases}
$$

### Codici di Rice ($M = 2^k$) ed Efficienza Hardware

Quando il parametro $M$ è vincolato ad essere una potenza intera di due:

$$
M = 2^k, \quad k \in \mathbb{N}
$$

il codice di Golomb prende il nome di __codice di Rice__ (Robert Rice, 1979). In questo caso $u = 2^{k+1} - 2^k = 2^k = M$, per cui tutti gli $M$ valori di resto sono codificati rigorosamente con una parola binaria di lunghezza fissa pari a $k$ bit.

Il vantaggio computazionale del codice di Rice è immenso nelle implementazioni elettroniche e nei microcontrollori:
- Il quoziente $q$ si ottiene con un semplice shift a destra logico di $k$ posizioni: $q = x \gg k$.
- Il resto $r$ si estrae con un'operazione bitwise AND con una maschera binaria: $r = x \ \& \ (2^k - 1)$.
- Non è richiesta alcuna operazione di divisione aritmetica o calcolo di modulo, operando a velocità di clock elevatissime.

Il Teorema di Gallager-Van Voorhis (1975) dimostra che scegliendo il parametro $M = \lceil -1/\log_2 \theta \rceil$, il codice di Golomb-Rice coincide esattamente con il codice di Huffman ottimo sull'alfabeto infinito. La dimostrazione è esposta in [[zz. Argomenti extra#Dimostrazione dell'Ottimalità dei Codici di Golomb per Distribuzioni Geometriche]]. I codici di Rice costituiscono lo standard nei formati multimediali lossless audio (FLAC), nella compressione di immagini spaziali (CCSDS 121.0-B-3) e nei codec video H.264 / H.265.

## Codifica Aritmetica (Arithmetic Coding)

L'algoritmo di Huffman assegna a ciascun simbolo di sorgente un numero intero di bit di codice. Quando una sorgente binaria o alfabetica presenta probabilità fortemente sbilanciate (ad esempio, un simbolo con $p = 0.95$ e l'altro con $p = 0.05$), l'auto-informazione del simbolo più frequente è:

$$
I(x) = -\log_2(0.95) \approx 0.074 \quad \text{bit}
$$

Poiché Huffman è vincolato ad assegnare almeno 1 bit intero a ciascuna parola di codice, la perdita di efficienza è considerevole: si spende 1 bit per rappresentare un contenuto informativo di appena $0.074$ bit. Per ridurre tale scarto con Huffman, occorrerebbe raggruppare i simboli in blocchi lunghi $n$, ma la complessità dell'albero esploderebbe esponenzialmente ($|\mathcal{X}|^n$).

La __codifica aritmetica__ (Arithmetic Coding, Rissanen 1976; Pasco 1976; Witten, Neal & Cleary 1987) supera definitivamente il vincolo della lunghezza intera dei simboli: invece di associare una stringa binaria a ciascun simbolo isolato, mappa l'intera sequenza di simboli $x_1 x_2 \dots x_n$ in un unico sotto-intervallo del segmento reale unitario $[0, 1)$.

### Fondamento Matematico: Il Teorema di Trasformata Integrale di Probabilità

La motivazione teorica della codifica aritmetica trae origine dal codice di Shannon-Fano-Elias e dal __Lemma della Trasformata Integrale di Probabilità__:
Sia $Y$ una variabile aleatoria continua con funzione di distribuzione cumulativa $F(y)$. Allora la variabile aleatoria $U = F(Y)$ è distribuita uniformemente nell'intervallo $[0, 1]$:

$$
U \sim \mathcal{U}[0, 1]
$$

Se si considera una sequenza infinita di simboli $X_1, X_2, \dots$ come la parte frazionaria di un numero reale $0.X_1 X_2 \dots$, la CDF su sequenze continue mappa tale numero in una variabile uniforme $U \in [0, 1]$. La rappresentazione binaria standard di un numero estratto da una distribuzione uniforme $\mathcal{U}[0, 1]$ genera una successione di cifre binarie $0.F_1 F_2 \dots$ indipendenti ed equiprobabili ($\text{Bern}(1/2)$). Tali bit presentano un'entropia massima di 1 bit e sono quindi assolutamente incomprimibili: essi costituiscono già la rappresentazione compressa ottima della sequenza.

### Meccanismo di Partizione Progressiva dell'Intervallo

La codifica aritmetica opera per suddivisione progressiva dell'intervallo reale unitario:
1. Inizializzazione: Si pone l'intervallo corrente pari a $[L^{(0)}, H^{(0)}) = [0, 1)$.
2. All'arrivo del generico simbolo $x_k \in \{1, 2, \dots, m\}$ avente probabilità $p(x_k)$ e probabilità cumulativa $F(x) = \sum_{y \le x} p(y)$ (con $F(0) = 0$), l'intervallo corrente $[L^{(k-1)}, H^{(k-1)})$ viene suddiviso internamente in sotto-intervalli proporzionali alle probabilità dei simboli.
3. Si aggiornano i limiti inferiore e superiore dell'intervallo secondo le relazioni analitiche:

$$
L^{(k)} = L^{(k-1)} + \left( H^{(k-1)} - L^{(k-1)} \right) F(x_k - 1)
$$

$$
H^{(k)} = L^{(k-1)} + \left( H^{(k-1)} - L^{(k-1)} \right) F(x_k)
$$

L'ampiezza dell'intervallo al termine dell'elaborazione di $n$ simboli indipendenti coincide esattamente con la probabilità congiunta dell'intera sequenza:

$$
\text{Width}^{(n)} = H^{(n)} - L^{(n)} = \prod_{k=1}^n p(x_k) = p(x_1, \dots, x_n) = p(x^n)
$$

Qualsiasi numero reale appartenente all'intervallo finale $[L^{(n)}, H^{(n)})$ identifica univocamente la sequenza originale $x^n$.

![[slide_16_arithmetic_coding_3ary_example.png|center mid]]

### Generazione della Parola di Codice e Lunghezza Ottima

Per convertire l'intervallo finale in un flusso di bit binario univocamente decodificabile:
1. Si seleziona il punto medio dell'intervallo:

$$
   T = \frac{L^{(n)} + H^{(n)}}{2}
$$

2. Si tronca l'espansione binaria del numero reale $T$ alla lunghezza di:

$$
   l(x^n) = \left\lceil -\log_2 p(x^n) \right\rceil + 1 \quad \text{bit}
$$

Sfruttando la proprietà dei troncamenti diadici, il sotto-intervallo diadico di ampiezza $2^{-l}$ centrato su $T$ cade rigorosamente all'interno di $[L^{(n)}, H^{(n)})$, garantendo l'istantaneità e l'assenza totale di ambiguità nella decodifica.

Calcolando la lunghezza media per simbolo su una sorgente stazionaria di entropia $H(X)$:

$$
\frac{1}{n} \mathbb{E}[l(X^n)] \le \frac{1}{n} \mathbb{E}\left[ -\log_2 p(X^n) + 2 \right] = \frac{n H(X) + 2}{n} = H(X) + \frac{2}{n} \quad \text{bit/simbolo}
$$

Al crescere della lunghezza della sequenza ($n \to \infty$), il termine di overhead additivo $\frac{2}{n}$ tende asintoticamente a zero:

$$
\lim_{n \to \infty} \frac{1}{n} \mathbb{E}[l(X^n)] = H(X)
$$

La codifica aritmetica raggiunge l'entropia della sorgente senza richiedere alcuna aggregazione a blocchi preliminare.

### Esempio Operativo: Codifica Aritmetica su Alfabeto Ternario

Si consideri un alfabeto ternario $\mathcal{X} = \{A, B, C\}$ con vettore delle probabilità:

$$
p(A) = 0.40, \quad p(B) = 0.40, \quad p(C) = 0.20
$$

La funzione di distribuzione cumulativa è:

$$
F(A) = 0.40, \quad F(B) = 0.80, \quad F(C) = 1.00 \quad (F(0) = 0)
$$

Si desidera codificare in streaming la sequenza di 4 simboli:

$$
x^4 = A \, C \, A \, A
$$

Seguiamo l'evoluzione degli intervalli passo dopo passo:
1. __Inizio__: $[L^{(0)}, H^{(0)}) = [0.0000, 1.0000)$, ampiezza $\text{Width} = 1.0000$.
2. __Primo simbolo $A$__:
   - $L^{(1)} = 0 + 1.0 \cdot F(0) = 0.0000$
   - $H^{(1)} = 0 + 1.0 \cdot F(A) = 0.4000$
   - Nuovo intervallo: $[0.0000, 0.4000)$, ampiezza $0.4000$.
3. __Secondo simbolo $C$__:
   - Ampiezza precedente: $0.4000 - 0.0000 = 0.4000$.
   - $L^{(2)} = 0.0000 + 0.4000 \cdot F(B) = 0.0000 + 0.4000 \cdot 0.80 = 0.3200$
   - $H^{(2)} = 0.0000 + 0.4000 \cdot F(C) = 0.0000 + 0.4000 \cdot 1.00 = 0.4000$
   - Nuovo intervallo: $[0.3200, 0.4000)$, ampiezza $0.0800$.
4. __Terzo simbolo $A$__:
   - Ampiezza precedente: $0.4000 - 0.3200 = 0.0800$.
   - $L^{(3)} = 0.3200 + 0.0800 \cdot F(0) = 0.3200$
   - $H^{(3)} = 0.3200 + 0.0800 \cdot F(A) = 0.3200 + 0.0800 \cdot 0.40 = 0.3520$
   - Nuovo intervallo: $[0.3200, 0.3520)$, ampiezza $0.0320$.
5. __Quarto simbolo $A$__:
   - Ampiezza precedente: $0.3520 - 0.3200 = 0.0320$.
   - $L^{(4)} = 0.3200 + 0.0320 \cdot F(0) = 0.3200$
   - $H^{(4)} = 0.3200 + 0.0320 \cdot F(A) = 0.3200 + 0.0320 \cdot 0.40 = 0.3328$
   - Intervallo finale: $[0.3200, 0.3328)$.

Verifichiamo la probabilità congiunta della sequenza:

$$
p(ACAA) = 0.40 \cdot 0.20 \cdot 0.40 \cdot 0.40 = 0.0128
$$

L'ampiezza dell'intervallo finale è esattamente:

$$
H^{(4)} - L^{(4)} = 0.3328 - 0.3200 = 0.0128 = p(ACAA)
$$

Calcoliamo il punto medio e il numero di bit richiesti:

$$
T = \frac{0.3200 + 0.3328}{2} = 0.3264
$$

$$
l = \lceil -\log_2(0.0128) \rceil + 1 = \lceil 6.2877 \rceil + 1 = 7 + 1 = 8 \quad \text{bit}
$$

Convertiamo il valore decimale $T = 0.3264$ nella sua espansione binaria tramite moltiplicazioni successive per 2:
- $0.3264 \times 2 = 0.6528 \to 0$
- $0.6528 \times 2 = 1.3056 \to 1$ (sottraendo 1: $0.3056$)
- $0.3056 \times 2 = 0.6112 \to 0$
- $0.6112 \times 2 = 1.2224 \to 1$ (sottraendo 1: $0.2224$)
- $0.2224 \times 2 = 0.4448 \to 0$
- $0.4448 \times 2 = 0.8896 \to 0$
- $0.8896 \times 2 = 1.7792 \to 1$ (sottraendo 1: $0.7792$)
- $0.7792 \times 2 = 1.5584 \to 1$

La sequenza binaria a 8 bit emessa dal codificatore è:

$$
01010011
$$

Il decodificatore, ricevendo tale sequenza, esegue il confronto tra il valore binario $0.01010011_2 \approx 0.3242$ e le soglie cumulative dell'alfabeto, ricostruendo determinatamente e sequenzialmente i singoli simboli $A$, $C$, $A$, $A$.

## Compressione a Dizionario: L'Algoritmo LZ77 a Finestra Scorrevole

La famiglia degli algoritmi di compressione a dizionario, introdotta da Jacob Ziv e Abraham Lempel nei due storici articoli del 1977 e 1978, abbandona completamente il modello della sorgente a simboli isolati. L'idea guida consiste nel sostituire gruppi ripetuti di caratteri con riferimenti (puntatori) a occorrenze identiche già apparse in precedenza nel flusso dei dati.

L'algoritmo __LZ77__ (Ziv & Lempel 1977), nella sua formulazione classica ottimizzata da Storer e Szymanski (1982), mantiene in memoria una __finestra scorrevole__ (Sliding Window) di dimensione finita $W$, composta da due buffer adiacenti:
1. __Search Buffer__ (buffer di ricerca): Contiene gli ultimi $W$ caratteri già codificati e memorizzati nella cronologia recente.
2. __Lookahead Buffer__ (buffer di anticipazione): Contiene la sequenza di simboli entranti ancora da comprimere.

![[slide_24_lz77_sliding_window_example.png|center mid]]

### Meccanismo Operativo di Ricerca e Struttura dei Token

Il codificatore analizza i simboli nel lookahead buffer e cerca all'interno del search buffer la più lunga sottostringa identica (Longest Match):
- Sia $P$ la posizione di inizio del match all'interno del buffer di ricerca, misurata come __offset all'indietro__ rispetto alla testina di lettura corrente ($1 \le P \le W$).
- Sia $L$ la __lunghezza__ della sottostringa corrispondente ($L \ge 1$).

Per distinguere tra testo compresso e testo letterale non trovato, l'algoritmo emette due tipologie di token distinti prefissati da un flag binario $F$:
1. __Token Letterale $(F = 0, C)$__: Emesso quando non si riscontra alcuna corrispondenza nel buffer di ricerca (o quando il match è lungo un solo carattere ed è inefficiente inviare un puntatore). Il flag $F = 0$ è seguito direttamente dalla codifica del carattere non compresso $C \in \mathcal{X}$.
2. __Token Puntatore $(F = 1, P, L)$__: Emesso quando si identifica una corrispondenza di lunghezza $L \ge 2$. Il flag $F = 1$ è seguito dall'offset all'indietro $P$ e dalla lunghezza $L$.

### La Proprietà di Sovrapposizione (Overlap) del Match

Una caratteristica distintiva e potente di LZ77 risiede nel fatto che la corrispondenza ricercata può estendersi oltre la fine del search buffer ed entrare nel lookahead buffer stesso ($L > P$).

Se la sequenza da codificare è un pattern ripetitivo periodico (ad esempio `ABABABAB...` con offset $P = 2$), il puntatore può descrivere una lunghezza $L \gg P$, poiché il decodificatore, copiando i caratteri a ritroso, genera deterministicamente la ripetizione in avanti. In questo modo, LZ77 implementa nativamente e senza alcuna istruzione speciale la compressione Run-Length.

### Esempio Dettagliato di LZ77

Si consideri una sorgente sull'alfabeto binario $\{A, B\}$, una finestra di ricerca di dimensione $W = 4$, e la stringa da codificare composta da 16 caratteri:

$$
\text{"ABBABBABBBAABABA"}
$$

Inizialmente il search buffer è vuoto. La stringa viene segmentata in 8 frasi progressive:
1. `A`: Search buffer vuoto. Nessun match $\implies$ Token letterale: $(0, A)$.
2. `B`: Nel search buffer è presente solo `A`. Nessun match $\implies$ Token letterale: $(0, B)$.
3. `B`: Nel search buffer c'è `AB`. Il carattere `B` compare a offset $P = 1$ con lunghezza $L = 1 \implies$ Token puntatore: $(1, 1, 1)$.
4. `ABBABB`: Nel search buffer c'è `ABB`. La sottostringa `ABBABB` (6 caratteri) inizia a offset $P = 3$ e si ripete con periodo 3 sfruttando l'overlap $\implies$ Token puntatore: $(1, 3, 6)$.
5. `BA`: Search buffer aggiornato a `BABB`. La sottostringa `BA` compare a offset $P = 4$ con lunghezza $L = 2 \implies$ Token puntatore: $(1, 4, 2)$.
6. `A`: Search buffer contiene `BBBA`. Il carattere `A` compare a offset $P = 1$ con lunghezza $L = 1 \implies$ Token puntatore: $(1, 1, 1)$.
7. `BA`: Search buffer contiene `BBAA`. La stringa `BA` compare a offset $P = 3$ con lunghezza $L = 2 \implies$ Token puntatore: $(1, 3, 2)$.
8. `BA`: Search buffer contiene `AABA`. La stringa `BA` compare a offset $P = 2$ con lunghezza $L = 2 \implies$ Token puntatore: $(1, 2, 2)$.

La sequenza compressa emessa è composta dalla successione di 8 token:

$$
(0, A), \, (0, B), \, (1, 1, 1), \, (1, 3, 6), \, (1, 4, 2), \, (1, 1, 1), \, (1, 3, 2), \, (1, 2, 2)
$$

Poiché $P = 0$ ed $L = 0$ non sono ammessi, l'implementazione pratica ottimizza l'allocazione binaria codificando le coppie $(F, P-1, L-1)$:
- Token letterale $(F = 0, C)$: 1 bit per il flag $F = 0$ e 1 bit per il carattere binario $C \in \{A=0, B=1\}$ (totale 2 bit);
- Token puntatore $(F = 1, P-1, L-1)$: 1 bit per il flag $F = 1$, 2 bit per l'offset $P-1 \in \{0, 1, 2, 3\}$ e 3 bit per la lunghezza $L-1 \in \{0, \dots, 7\}$ (totale 6 bit).

Il flusso binario risultante è pari a 40 bit complessivi:

$$
\underbrace{00}_{(0,A)} \quad \underbrace{01}_{(0,B)} \quad \underbrace{100000}_{(1,1,1)} \quad \underbrace{110101}_{(1,3,6)} \quad \underbrace{111001}_{(1,4,2)} \quad \underbrace{100000}_{(1,1,1)} \quad \underbrace{110001}_{(1,3,2)} \quad \underbrace{101001}_{(1,2,2)}
$$

### Standard Industriali e Teorema del Tempo di Ricorrenza di Kac

L'algoritmo LZ77 costituisce il motore computazionale dello standard __Deflate__, impiegato quotidianamente nei formati di compressione `gzip`, `zip`, `pkzip`, `7z` e nel formato di immagini raster `PNG` (in cui i token LZ77 sono successivamente ricompressi mediante codici di Huffman canonici).

La dimostrazione formale dell'ottimalità asintotica di LZ77, basata sulla teoria dei tempi di ricorrenza di Kac e sul teorema di Wyner-Ziv:

$$
\frac{1}{n} \mathbb{E}[\log_2 R_n] \to H(\mathcal{X})
$$

è esposta rigorosamente in [[zz. Argomenti extra#Teorema del Tempo di Ricorrenza di Kac e Ottimalità Asintotica di LZ77]].

## Compressione ad Albero di Prefissi: L'Algoritmo LZ78

Mentre LZ77 effettua ricerche lineari all'interno di un buffer di scorrimento a memoria limitata, l'algoritmo __LZ78__ (Ziv & Lempel 1978) memorizza le stringhe incontrate in un __dizionario dinamico indicizzato ad albero__.

### Parsing Incrementale

La sequenza di dati entrante viene segmentata (parsed) sequenzialmente in un insieme di $c(n)$ frasi distinte:

$$
x^n = w_1 \, w_2 \, \dots \, w_{c(n)}
$$

secondo la regola fondamentale:
Ciascuna frase $w_k$ è la più breve sottostringa della sequenza che non è mai comparsa tra le frasi precedentemente archiviate nel dizionario.

Di conseguenza, ogni nuova frase $w_k$ può essere univocamente descritta concatenando una frase prefissa $w_{j(k)}$ già censita nel dizionario ad un indice precedente $j(k) < k$ con un unico carattere finale innovativo $c_k \in \mathcal{X}$:

$$
w_k = w_{j(k)} \cdot c_k
$$

dove per convenzione $w_0 = \emptyset$ rappresenta la parola vuota.

Il token trasmesso ad ogni passo è la coppia:

$$
(j, c)
$$

dove:
- $j \in \{0, 1, \dots, k-1\}$ è l'indice numerico del prefisso nel dizionario;
- $c \in \mathcal{X}$ è il nuovo carattere.

![[slide_27_lz78_tree_structure.png|center mid]]

### Esempio Operativo di Parsing e Albero di LZ78

Si consideri la sequenza binaria di 17 caratteri:

$$
\text{"ABBABBABBBAABABAA"}
$$

Il dizionario viene popolato incrementalmente registrando ciascuna frase non ancora vista:
1. `A`: Non presente $\implies$ Token $(0, A)$, Nuova frase 1: `A`.
2. `B`: Non presente $\implies$ Token $(0, B)$, Nuova frase 2: `B`.
3. `BA`: `B` è nel dizionario (frase 2), `BA` no $\implies$ Token $(2, A)$, Nuova frase 3: `BA`.
4. `BB`: `B` è nel dizionario (frase 2), `BB` no $\implies$ Token $(2, B)$, Nuova frase 4: `BB`.
5. `AB`: `A` è nel dizionario (frase 1), `AB` no $\implies$ Token $(1, B)$, Nuova frase 5: `AB`.
6. `BBA`: `BB` è nel dizionario (frase 4), `BBA` no $\implies$ Token $(4, A)$, Nuova frase 6: `BBA`.
7. `ABA`: `AB` è nel dizionario (frase 5), `ABA` no $\implies$ Token $(5, A)$, Nuova frase 7: `ABA`.
8. `BAA`: `BA` è nel dizionario (frase 3), `BAA` no $\implies$ Token $(3, A)$, Nuova frase 8: `BAA`.

La sequenza delle 8 frasi distinte generate e dei relativi token è:

$$
(0, A), \, (0, B), \, (2, A), \, (2, B), \, (1, B), \, (4, A), \, (5, A), \, (3, A)
$$

Poiché l'indice massimo del dizionario raggiunto prima dell'emissione dei puntatori è compreso nell'intervallo $[0, 5]$, sono necessari $\lceil \log_2 6 \rceil = 3$ bit per l'indice del prefisso e 1 bit per il carattere innovativo ($A=0, B=1$). Il bitstream complessivo a 32 bit è dato da:

$$
\underbrace{0000}_{(0,A)} \quad \underbrace{0001}_{(0,B)} \quad \underbrace{0100}_{(2,A)} \quad \underbrace{0101}_{(2,B)} \quad \underbrace{0011}_{(1,B)} \quad \underbrace{1000}_{(4,A)} \quad \underbrace{1010}_{(5,A)} \quad \underbrace{0110}_{(3,A)} \implies 32 \text{ bit}
$$

La dimostrazione che il numero di frasi soddisfa il bound combinatorio $c(n) \le \frac{n}{(1-\epsilon_n)\log_{|\mathcal{X}|} n}$ e che la lunghezza media di codice converge quasi certamente all'entropia per qualsiasi sorgente stazionaria ed ergodica è esposta in [[zz. Argomenti extra#Dimostrazione del Teorema di Ziv-Lempel sull'Efficienza Asintotica di LZ78]].

## L'Algoritmo LZW (Lempel-Ziv-Welch 1984)

Nell'algoritmo LZ78 classico, l'emissione di un carattere letterale esplicito $c$ ad ogni token introduce una ridondanza non trascurabile. Nel 1984, Terry A. Welch pubblicò una raffinata variante ingegneristica denominata __LZW__ (*A Technique for High-Performance Data Compression*), che ha dominato le applicazioni commerciali degli anni '80 e '90.

### Il Principio di Pre-Popolazione del Dizionario

La modifica architetturale introdotta da LZW consiste nel __pre-popolare il dizionario__ con tutti i simboli dell'alfabeto di base prima di iniziare la compressione.

Nel caso standard di un flusso di byte a 8 bit ($|\mathcal{X}| = 256$):
- Le prime 256 posizioni del dizionario (indici $0\text{–}255$) sono pre-assegnate ai singoli caratteri ASCII/byte isolati.
- Il token emesso dal codificatore non contiene più alcun carattere letterale esplicito: esso è costituito __esclusivamente da un indice intero di dizionario__.

### Meccanismo di Sincronizzazione Encoder-Decoder in Lockstep

Il decodificatore possiede lo stesso dizionario pre-popolato (indici $0\text{–}255$).
- Quando l'encoder individua la più lunga sequenza $S$ presente nel dizionario e riceve il simbolo successivo $c$, emette l'indice di $S$ e inserisce nel dizionario la stringa estesa $S \cdot c$.
- Quando il decoder riceve l'indice di $S$, recupera la stringa dal proprio dizionario e la emette in uscita; quindi, non appena riceve l'indice successivo, ricostruisce il carattere $c$ e memorizza autonomamente la stessa stringa $S \cdot c$ alla medesima posizione del proprio dizionario.

Non vi è alcuna necessità di trasmettere le stringhe del dizionario: i dizionari di trasmissione e ricezione si mantengono perfettamente sincronizzati in parallelo (in lockstep).

### Esempio Passo-Passo di LZW

Si consideri la medesima sequenza binaria di 17 caratteri `ABBABBABBBAABABAA` su alfabeto $\{A, B\}$.
- Pre-popolazione del dizionario: Indice 1 = `A`, Indice 2 = `B`.

Evoluzione sequenziale della codifica:
1. Legge `A`. Successivo `B`. La stringa `AB` non è nel dizionario. Emette l'indice di `A` (__1__). Inserisce nel dizionario Indice 3 = `AB`.
2. Legge `B`. Successivo `B`. `BB` non è presente. Emette l'indice di `B` (__2__). Inserisce Indice 4 = `BB`.
3. Legge `B`. Successivo `A`. `BA` non è presente. Emette l'indice di `B` (__2__). Inserisce Indice 5 = `BA`.
4. Legge `AB` (presente come 3). Successivo `B`. `ABB` non è presente. Emette indice __3__ (`AB`). Inserisce Indice 6 = `ABB`.
5. Legge `BA` (presente come 5). Successivo `B`. `BAB` non è presente. Emette indice __5__ (`BA`). Inserisce Indice 7 = `BAB`.
6. Legge `BB` (presente come 4). Successivo `B`. `BBB` non è presente. Emette indice __4__ (`BB`). Inserisce Indice 8 = `BBB`.
7. Legge `BA` (presente come 5). Successivo `A`. `BAA` non è presente. Emette indice __5__ (`BA`). Inserisce Indice 9 = `BAA`.
8. Legge `AB` (presente come 3). Successivo `A`. `ABA` non è presente. Emette indice __3__ (`AB`). Inserisce Indice 10 = `ABA`.
9. Legge `ABA` (presente come 10). Successivo `A`. `ABAA` non è presente. Emette indice __10__ (`ABA`). Inserisce Indice 11 = `ABAA`.
10. Legge `A` (presente come 1). Fine sequenza. Emette indice finale __1__ (`A`).

La sequenza emessa da LZW consiste nella successione di 10 indici interi:

$$
1, \, 2, \, 2, \, 3, \, 5, \, 4, \, 5, \, 3, \, 10, \, 1
$$

Allocando un numero crescente di bit all'aumentare delle voci censite nel dizionario, la codifica binaria si articola come:

$$
\underbrace{0}_{(1)} \quad \underbrace{01}_{(2)} \quad \underbrace{01}_{(2)} \quad \underbrace{010}_{(3)} \quad \underbrace{100}_{(5)} \quad \underbrace{011}_{(4)} \quad \underbrace{100}_{(5)} \quad \underbrace{0010}_{(3)} \quad \underbrace{1001}_{(10)} \quad \underbrace{0000}_{(1)}
$$

per un totale di soli __29 bit__, a fronte dei 40 bit di LZ77 e dei 32 bit di LZ78 sulla medesima sorgente.

### Il Caso Limite Eccezionale di Decodifica ($c \cdot s \cdot c \cdot s \cdot c$)

Nell'algoritmo LZW esiste una nota eccezione algoritmica che si verifica quando la sorgente presenta un pattern del tipo $c \cdot s \cdot c \cdot s \cdot c$ (dove $c$ è un carattere e $s$ una sottostringa, es. `ABABABA`):
- Il codificatore inserisce una nuova stringa $S$ nel dizionario e al passo immediatamente successivo rileva ed emette la stessa stringa $S$.
- Quando il decodificatore riceve l'indice, quell'indice non è ancora stato registrato nel dizionario locale (è un indice avanti di 1 rispetto all'ultimo nodo creato).

Welch dimostrò che tale apparente paradosso si risolve deterministicamente: la stringa misteriosa ha necessariamente come primo e ultimo carattere lo stesso simbolo iniziale della stringa precedente:

$$
S_{\text{ignota}} = S_{\text{precedente}} \cdot \text{FirstChar}(S_{\text{precedente}})
$$

Consentendo al decodificatore di completare la voce e proseguire senza interruzioni.

L'algoritmo LZW è stato adottato in celebri standard applicativi:
- Lo storico comando `compress` dei sistemi operativi Unix/Linux;
- Il formato grafico d'immagine `GIF` (Graphics Interchange Format, 1987);
- Il formato di archiviazione grafica `TIFF` (Tagged Image File Format);
- La compressione dei flussi di testo e vettoriali nei documenti `PDF`;
- Lo standard di compressione per modem telefonici ad alta velocità `ITU-T V.42bis`.

## Quadro Sinottico Comparativo dei Metodi di Compressione

La tabella sottostante riassume e mette a confronto l'intero spettro delle tecnologie di codifica di sorgente studiate nel corso:

| Algoritmo | Conoscenza Statistica Richiesta | Modello di Codifica | Lunghezza Media per Simbolo | Complessità di Memoria | Ambiti e Standard di Riferimento |
| :--- | :--- | :--- | :--- | :--- | :--- |
| __Huffman__ | Conoscenza esatta a priori della PMF $p(x)$ | Simbolo isolato o blocchi prefissati | $H(X) \le L < H(X) + 1$ | Ridotta (tabella dell'albero) | JPEG (codifica DCT finale), MP3, deflate |
| __Golomb-Rice__ | Conoscenza del parametro $\theta$ (distribuzione geometrica) | Divisione euclidea: quoziente unario + resto binario | $H(X) \le L < H(X) + 1$ | Minima (operazioni bitwise shift/mask in Rice) | FLAC, JPEG-LS, telemetria spaziale CCSDS, H.264 |
| __Aritmetica__ | Conoscenza della PMF (statica o adattiva) | Mappatura dell'intera sequenza in un sotto-intervallo di $[0, 1)$ | $H(X) \le L_n/n \le H(X) + \frac{2}{n}$ | Moderata (registri aritmetici a precisione finita) | CABAC (H.264/HEVC), JPEG 2000, VP9 |
| __LZ77__ | Nessuna (Universale, 1-pass) | Puntatori a ritroso $(P, L)$ in finestra scorrevole $W$ | $\to H(\mathcal{X})$ per $W \to \infty$ | Costante (limitata alla dimensione finestra $W$) | `gzip`, `zip`, `PNG`, formato Deflate |
| __LZ78__ | Nessuna (Universale, 1-pass) | Parsing incrementale ad albero dinamico di prefissi $(j, c)$ | $\to H(\mathcal{X})$ per $n \to \infty$ | Crescente con la lunghezza del file (albero dinamico) | Standard modem V.42bis, compressione testuale |
| __LZW__ | Nessuna (Universale, 1-pass) | Dizionario pre-popolato; emissione di soli indici | $\to H(\mathcal{X})$ per $n \to \infty$ | Media (dizionario a $2^{12}$ o $2^{16}$ ingressi con reset) | Unix `compress`, immagini `GIF`, `TIFF`, `PDF` |

