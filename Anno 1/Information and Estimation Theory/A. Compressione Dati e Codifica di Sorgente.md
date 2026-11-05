# A. Compressione Dati e Codifica di Sorgente

La compressione dei dati rappresenta l'applicazione ingegneristica più diretta e pervasiva della teoria dell'informazione di Shannon. L'obiettivo fondamentale della codifica di sorgente senza perdita (__lossless data compression__) consiste nel convertire una sequenza di simboli generata da una sorgente aleatoria in una sequenza binaria di lunghezza minima attesa, garantendo al contempo che il ricevitore possa ricostruire la sequenza originaria in modo deterministico e privo di errori.

La presente trattazione formalizza il modello matematico della codifica di sorgente, definisce le classi fondamentali di codici, dimostra i limiti invalicabili posti dalla disuguaglianza di Kraft-McMillan e dal Teorema di Shannon, ed espone in dettaglio gli algoritmi ottimi di Huffman, le formulazioni canoniche per gli standard industriali, la codifica di Shannon-Fano-Elias e i principi di ottimalità competitiva.

## Modello Matematico della Codifica di Sorgente

Si consideri una sorgente discreta senza memoria (__Discrete Memoryless Source__, DMS) modellata come una variabile aleatoria discreta $X$ definita su un alfabeto finito $\mathcal{X} = \{x_1, x_2, \dots, x_m\}$ e governata da una funzione di massa di probabilità (PMF) $p(x) = \text{Pr}\{X = x\}$, con $p(x_i) > 0$ per ogni $i$ e $\sum_{i=1}^m p(x_i) = 1$.

L'alfabeto di codice $\mathcal{D} = \{0, 1, \dots, D-1\}$ è un insieme discreto di cardinalità $D \ge 2$. Nel contesto delle telecomunicazioni e dell'informatica, si considera tipicamente l'alfabeto binario con $D = 2$ e $\mathcal{D} = \{0, 1\}$.

Si indica con $\mathcal{D}^*$ l'insieme di tutte le sequenze finite (stringhe o parole) costruite accostando simboli appartenenti all'alfabeto $\mathcal{D}$:

$$
\mathcal{D}^* = \bigcup_{k=1}^\infty \mathcal{D}^k = \mathcal{D} \cup \mathcal{D}^2 \cup \mathcal{D}^3 \cup \dots
$$

### Definizione di Codice di Sorgente

Un __codice di sorgente__ $C$ per una variabile aleatoria $X$ è una mappa deterministica dall'alfabeto di sorgente all'insieme delle stringhe finite di codice:

$$
C: \mathcal{X} \to \mathcal{D}^*
$$

L'immagine $C(x)$ di un simbolo di sorgente $x \in \mathcal{X}$ prende il nome di __parola di codice__ (__codeword__) associata a $x$.

La __lunghezza__ della parola di codice $C(x)$, espressa in numero di simboli di codice (bit se $D = 2$), è denotata con $l(x)$ o con $l_i = l(x_i)$.

### Lunghezza Media Attesa del Codice

La prestazione di un codice di sorgente si quantifica attraverso il valore atteso della lunghezza delle parole di codice, calcolato rispetto alla distribuzione statistica della sorgente:

$$
L(C) = \mathbb{E}[l(X)] = \sum_{x \in \mathcal{X}} p(x) l(x) = \sum_{i=1}^m p(x_i) l_i
$$

L'obiettivo teorico e applicativo della compressione priva di perdite risiede nella progettazione di codici che minimizzino la lunghezza media attesa $L(C)$ preservando la decodificabilità esatta del messaggio.

## Tassonomia e Classi Fondamentali di Codici

Non ogni funzione $C: \mathcal{X} \to \mathcal{D}^*$ risulta utilizzabile per la trasmissione o memorizzazione dei dati. A seconda dei vincoli di invertibilità imposti sulla decodifica di singoli simboli o di sequenze concatenate, i codici si articolano in quattro classi gerarchiche nidificate.

### Codici Non Singolari

Un codice $C$ si definisce __non singolare__ se assegna parole di codice distinte a simboli di sorgente distinti:

$$
x_i \neq x_j \implies C(x_i) \neq C(x_j)
$$

Se un codice fosse singolare, esisterebbero almeno due simboli differenti con la medesima parola di codice (ad esempio $C(x_1) = C(x_2) = 0$), rendendo impossibile l'inversione della mappa anche in presenza di un singolo simbolo isolato.

### Estensione di un Codice

Nella trasmissione di flussi continui, la sorgente emette una sequenza arbitraria di simboli $x_{i_1} x_{i_2} \dots x_{i_n} \in \mathcal{X}^*$. L'__estensione di codice__ $C^*$ è la funzione definita dalla concatenazione ordinata delle corrispondenti parole di codice:

$$
C^*(x_{i_1} x_{i_2} \dots x_{i_n}) = C(x_{i_1}) C(x_{i_2}) \dots C(x_{i_n}) \in \mathcal{D}^*
$$

### Codici Univocamente Decodificabili

Un codice $C$ si definisce __univocamente decodificabile__ (__uniquely decodable__) se la sua estensione $C^*$ è non singolare su sequenze di lunghezza arbitraria:

$$
\mathbf{x} \neq \mathbf{x}' \implies C^*(\mathbf{x}) \neq C^*(\mathbf{x}')
$$

In un codice univocamente decodificabile, qualsiasi stringa binaria concatenata può derivare da una e una sola sequenza originaria di simboli di sorgente. 

Un codice può essere non singolare senza essere univocamente decodificabile. Ad esempio, assegnando a una sorgente ternaria le parole $C(1) = 0$, $C(2) = 010$, $C(3) = 01$, $C(4) = 10$, il codice è chiaramente non singolare. Tuttavia, ricevendo la sequenza binaria $010$, il decodificatore non può determinare se la sorgente abbia emesso il singolo simbolo $2$, oppure la sequenza $14$ ($0$ seguito da $10$), oppure la sequenza $31$ ($01$ seguito da $0$). Il codice genera ambiguità irreversibile.

### Codici Istantanei (o Codici Prefisso)

Un codice $C$ si definisce __istantaneo__ o __codice a prefisso__ (__prefix code__) se nessuna parola di codice valida costituisce il prefisso di qualsiasi altra parola di codice dello stesso insieme:

$$
\forall i \neq j, \quad C(x_i) \text{ non è prefisso di } C(x_j)
$$

Nei codici istantanei, la fine di una parola di codice è auto-delimitata: non appena il ricevitore legge una sequenza di bit che forma una parola valida, tale parola può essere decodificata immediatamente, senza dover attendere i bit successivi e senza necessità di separatori espliciti.

L'inclusione gerarchica tra le classi segue la relazione:

$$
\text{Tutti i Codici} \supset \text{Codici Non Singolari} \supset \text{Codici Univocamente Decodificabili} \supset \text{Codici Istantanei}
$$

![[slide_12_code_classes_venn.png|center mid]]

### L'Esempio Storico del Codice Morse

Nel codice telegrafico di Samuel Morse, le lettere sono rappresentate da sequenze di punti e linee: ad esempio la lettera $E$ è codificata con un punto $(\cdot)$ e la lettera $A$ con un punto seguito da una linea $(\cdot -)$. Poiché la sequenza per $E$ è un prefisso esatto della sequenza per $A$, il codice Morse binario non sarebbe né istantaneo né univocamente decodificabile.

Nella pratica telegrafica, il sistema opera correttamente unicamente perché introduce una __pausa di silenzio__ tra lettere consecutive e una pausa più lunga tra parole. Di conseguenza, l'alfabeto di codice effettivo non è binario ma ternario: $\mathcal{D} = \{\text{punto}, \text{linea}, \text{pausa}\}$, dove la pausa funge da delimitatore esplicito di fine simbolo.

### Quadro Esemplificativo delle Classi di Codici

Si consideri una sorgente a quattro simboli $\mathcal{X} = \{1, 2, 3, 4\}$. La seguente tabella illustra il comportamento delle quattro classi:

| Simbolo | Codice Singolare | Non Singolare, Non Univocamente Decodificabile | Univocamente Decodificabile, Non Istantaneo | Codice Istantaneo (Prefisso) |
| :---: | :---: | :---: | :---: | :---: |
| $1$ | $0$ | $0$ | $10$ | $0$ |
| $2$ | $0$ | $010$ | $00$ | $10$ |
| $3$ | $0$ | $01$ | $11$ | $110$ |
| $4$ | $0$ | $10$ | $110$ | $111$ |

Nel terzo codice, la parola $C(3) = 11$ è prefisso esatto di $C(4) = 110$, impedendo la decodifica istantanea. Tuttavia, il codice è univocamente decodificabile: se i primi due bit sono $00$ o $10$, vengono decodificati immediatamente come $2$ o $1$; se iniziano per $11$, si analizzano i bit successivi: se segue un bit $1$, il primo simbolo è $3$ ($11$ seguito da $1\dots$); se segue una sequenza di zeri prima del successivo uno, un numero dispari di zeri identifica $4$ ($110$), mentre un numero pari identifica $3$ ($11$ seguito da $00$). La decodifica richiede quindi lookahead ma è priva di ambiguità. Nel quarto codice, nessuna parola è prefisso di un'altra: la lettura di uno $0$ identifica univocamente $1$, $10$ identifica $2$, $110$ identifica $3$ e $111$ identifica $4$.

## La Disuguaglianza di Kraft per Codici Istantanei

La proprietà prefissa impone un vincolo geometrico e algebrico stringente sulle lunghezze delle parole di codice ammissibili: non è possibile assegnare parole arbitrariamente corte a tutti i simboli della sorgente. Tale limite è sancito formalmente dalla __disuguaglianza di Kraft__ (1949).

### Enunciato del Teorema di Kraft

Sia dato un codice istantaneo definito su un alfabeto codice di dimensione $D$ avente parole di codice con lunghezze intere $l_1, l_2, \dots, l_m$. Allora le lunghezze soddisfano necessariamente la disuguaglianza:

$$
\sum_{i=1}^m D^{-l_i} \le 1
$$

Viceversa, assegnato un qualsiasi insieme di interi positivi $l_1, l_2, \dots, l_m$ che soddisfi tale disuguaglianza, esiste sempre un codice istantaneo su alfabeto $D$-ario avente esattamente tali lunghezze di parola.

### Dimostrazione Geometrica tramite Albero $D$-ario

Si consideri un albero $D$-ario completo di profondità $l_{\max} = \max_{1 \le i \le m} l_i$. La radice corrisponde alla stringa vuota, i rami che si diramano da ciascun nodo interno rappresentano i $D$ simboli dell'alfabeto di codice, e i nodi a profondità $l$ corrispondono biunivocamente alle sequenze di lunghezza $l$.

Il numero totale di foglie (nodi terminali) al livello massimo $l_{\max}$ è pari a:

$$
N_{\text{foglie}} = D^{l_{\max}}
$$

![[slide_17_kraft_tree.png|center mid]]

Si consideri una parola di codice $C(x_i)$ avente lunghezza $l_i \le l_{\max}$. Essa è rappresentata da un nodo posizionato a profondità $l_i$. 

Affinché il codice sia istantaneo, nessun'altra parola di codice può trovarsi nel sottoalbero generato da tale nodo (altrimenti $C(x_i)$ sarebbe prefisso di tale parola) e tale nodo non può trovarsi nel sottoalbero di una parola di codice precedente (altrimenti una parola precedente sarebbe prefisso di $C(x_i)$).

Di conseguenza, la selezione del nodo a profondità $l_i$ __riserva ed elimina__ l'intero sottoalbero sottostante. Il numero di foglie al livello massimo $l_{\max}$ che discendono dal nodo a profondità $l_i$ è pari a:

$$
D^{l_{\max} - l_i}
$$

Poiché per la condizione di prefisso nessun nodo di codice può essere discendente di un altro, gli insiemi di foglie riservate al livello $l_{\max}$ dai vari simboli di sorgente $i = 1, \dots, m$ sono mutuamente disgiunti.

La somma del numero di foglie riservate da tutte le $m$ parole di codice non può superare il numero totale di foglie disponibili all'ultimo livello dell'albero:

$$
\sum_{i=1}^m D^{l_{\max} - l_i} \le D^{l_{\max}}
$$

Raccogliendo a fattor comune $D^{l_{\max}}$ a primo membro:

$$
D^{l_{\max}} \sum_{i=1}^m D^{-l_i} \le D^{l_{\max}}
$$

Dividendo entrambi i membri per la costante positiva $D^{l_{\max}}$, si ottiene direttamente la disuguaglianza di Kraft:

$$
\sum_{i=1}^m D^{-l_i} \le 1
$$

### Dimostrazione della Condizione Sufficiente (Costruzione Inversa)

Sia $\{l_1, l_2, \dots, l_m\}$ un insieme di interi positivi ordinati in modo non decrescente ($l_1 \le l_2 \le \dots \le l_m$) che soddisfa la disuguaglianza $\sum_{i=1}^m D^{-l_i} \le 1$.

È possibile costruire l'albero di codice in modo iterativo greedy:
1. Al passo $k$, si sceglie un nodo disponibile a profondità $l_k$ che non sia discendente di alcun nodo già assegnato.
2. L'assegnazione elimina $D^{l_{\max} - l_k}$ foglie al livello $l_{\max}$.
3. Il numero totale di foglie riservate dopo $k-1$ assegnazioni è $\sum_{j=1}^{k-1} D^{l_{\max} - l_j}$.
4. Poiché $\sum_{i=1}^m D^{-l_i} \le 1$, per ogni $k \le m$ vale strettamente:

   $$
   \sum_{j=1}^{k-1} D^{l_{\max} - l_j} < D^{l_{\max}}
   $$

5. Rimane sempre almeno una foglia libera a profondità $l_{\max}$, il che garantisce l'esistenza di almeno un nodo genitore libero a profondità $l_k$.

L'algoritmo costruttivo termina con successo producendo un codice rigorosamente istantaneo.

### Disuguaglianza di Kraft Estesa per Alfabeti Numerabili

Se l'alfabeto di sorgente è numerabile ma infinito ($\{x_1, x_2, \dots\}$ con $m \to \infty$), la disuguaglianza di Kraft mantiene la propria validità sotto forma di serie convergente:

$$
\sum_{i=1}^\infty D^{-l_i} \le 1
$$

Qualsiasi sequenza di lunghezze per cui la serie diverga o superi l'unità non può corrispondere ad alcun codice istantaneo valido.

## Il Teorema di McMillan per Codici Univocamente Decodificabili

Un interrogativo fondamentale sorge spontaneo: accettando codici che non siano istantanei, ma unicamente univocamente decodificabili (ammettendo cioè ritardi di decodifica o complessità di parsing retrogrado), è possibile eludere la disuguaglianza di Kraft e ottenere parole di codice più corte?

Il __Teorema di McMillan__ (1956) risponde negativamente a tale quesito, dimostrando che la medesima disuguaglianza governa l'intera classe dei codici univocamente decodificabili.

### Enunciato del Teorema di McMillan

Sia $C$ un codice univocamente decodificabile con lunghezze delle parole di codice $l_1, l_2, \dots, l_m$ su un alfabeto di cardinalità $D$. Allora:

$$
\sum_{i=1}^m D^{-l_i} \le 1
$$

La dimostrazione formale, basata sull'elevamento a potenza polinomiale $k$-esima della sommatoria e sulla delimitazione combinatoria del numero di sequenze distinte $N_{k, j} \le D^j$, è riportata integralmente nella sezione dedicata di [[zz. Argomenti extra#Dimostrazione Integrale del Teorema di McMillan per Codici Univocamente Decodificabili|approfondimento analitico di McMillan]].

### Conseguenza Strutturale

Poiché la classe dei codici istantanei è un sottoinsieme proprio dei codici univocamente decodificabili, e poiché entrambe le classi condividono esattamente il medesimo vincolo algebrico sulle lunghezze ammissibili:

$$
\min_{C \in \text{Univocamente Decodificabili}} L(C) = \min_{C \in \text{Istantanei}} L(C)
$$

Non esiste alcun codice univocamente decodificabile che possa raggiungere una lunghezza media di parola strettamente inferiore a quella ottenibile dal miglior codice istantaneo. I progettisti di sistemi di compressione possono quindi limitare la ricerca esclusivamente ai codici istantanei senza alcuna perdita di efficienza teorica.

## Lunghezza Media Ottima e Limite di Shannon

Avendo stabilito che qualsiasi codice ammissibile deve soddisfare $\sum_{i=1}^m D^{-l_i} \le 1$, il problema della codifica di sorgente ottima si riduce a un problema di ottimizzazione matematica vincolata:

$$
\min_{l_1, \dots, l_m \in \mathbb{N}^+} \sum_{i=1}^m p_i l_i \quad \text{soggetto a} \quad \sum_{i=1}^m D^{-l_i} \le 1
$$

### Rilassamento Continuo e Derivazione Variazionale

Rilassando il vincolo di interezza e ammettendo che le lunghezze possano assumere valori reali continui $l_i \in \mathbb{R}^+$, si applica il metodo dei moltiplicatori di Lagrange. La funzione Lagrangiana è definita da:

$$
\mathcal{L}(l_1, \dots, l_m, \lambda) = \sum_{i=1}^m p_i l_i + \lambda \left( \sum_{i=1}^m D^{-l_i} - 1 \right)
$$

Scrivendo la base $D$ come esponenziale naturale $D^{-l_i} = e^{-l_i \ln D}$ e derivando rispetto alla lunghezza $l_i$:

$$
\frac{\partial \mathcal{L}}{\partial l_i} = p_i - \lambda D^{-l_i} \ln D = 0
$$

Risolvendo per $D^{-l_i}$:

$$
D^{-l_i} = \frac{p_i}{\lambda \ln D}
$$

Sommando su tutti gli indici $i$ per imporre il vincolo $\sum_{i=1}^m D^{-l_i} = 1$:

$$
\sum_{i=1}^m D^{-l_i} = \frac{\sum_{i=1}^m p_i}{\lambda \ln D} = \frac{1}{\lambda \ln D} = 1 \implies \lambda \ln D = 1
$$

Sostituendo il valore del moltiplicatore ottimo $\lambda \ln D = 1$:

$$
D^{-l_i^*} = p_i \iff l_i^* = -\log_D p_i = \log_D \frac{1}{p_i}
$$

Sostituendo le lunghezze ottime reali $l_i^*$ nell'espressione della lunghezza media attesa:

$$
L^* = \sum_{i=1}^m p_i l_i^* = -\sum_{i=1}^m p_i \log_D p_i = H_D(X)
$$

L'entropia di sorgente $H_D(X)$ rappresenta il minimo teorico assoluto della lunghezza media attesa per qualsiasi codice a parole prefisse o univocamente decodificabili.

### Distribuzioni Diadiche ($D$-adiche)

Una distribuzione di probabilità si definisce __diadica__ (o $D$-adica) se ogni probabilità è una potenza intera negativa della base di codice:

$$
p_i = D^{-k_i}, \quad k_i \in \mathbb{N}^+
$$

Per distribuzioni $D$-adiche, le lunghezze ottime continue $l_i^* = -\log_D(D^{-k_i}) = k_i$ sono numeri interi esatti. In questo caso ideale:
1. La disuguaglianza di Kraft è soddisfatta con eguaglianza stretta: $\sum D^{-k_i} = \sum p_i = 1$.
2. La lunghezza media attesa coincide esattamente con l'entropia della sorgente:

   $$
   L = H_D(X)
   $$

### Il Teorema di Shannon per Sorgenti Non Diadiche

Quando la sorgente non presenta una distribuzione $D$-adica, i valori $-\log_D p_i$ non sono interi. Per garantire la decodificabilità prefissa, Shannon propose di arrotondare ciascuna lunghezza reale all'intero superiore immediato tramite la funzione soffitto (__ceiling__):

$$
l_i = \left\lceil \log_D \frac{1}{p_i} \right\rceil
$$

Tale assegnazione definisce il cosiddetto __codice di Shannon__.

Verifichiamo che tale codice soddisfi la disuguaglianza di Kraft:

$$
l_i \ge \log_D \frac{1}{p_i} \implies D^{-l_i} \le D^{-\log_D(1/p_i)} = p_i
$$

Sommando su tutti gli stati:

$$
\sum_{i=1}^m D^{-l_i} \le \sum_{i=1}^m p_i = 1
$$

La disuguaglianza di Kraft è rigorosamente soddisfatta, assicurando l'esistenza di un codice prefisso avente tali lunghezze.

Dalla definizione della funzione soffitto, le lunghezze intere soddisfano la doppia disuguaglianza:

$$
\log_D \frac{1}{p_i} \le l_i < \log_D \frac{1}{p_i} + 1
$$

Moltiplicando ciascun termine per $p_i$ e sommando su tutti i simboli $i = 1, \dots, m$:

$$
\sum_{i=1}^m p_i \log_D \frac{1}{p_i} \le \sum_{i=1}^m p_i l_i < \sum_{i=1}^m p_i \log_D \frac{1}{p_i} + \sum_{i=1}^m p_i
$$

Poiché il primo termine è $H_D(X)$ e $\sum p_i = 1$, si ottiene il __Teorema del Limite di Shannon sulla Lunghezza Attesa__:

$$
H_D(X) \le L < H_D(X) + 1
$$

Sia $L^*$ la lunghezza media del codice prefisso globalmente ottimo (il codice di Huffman). Poiché il codice di Huffman minimizza la lunghezza media tra tutti i codici prefissi e il codice di Shannon è un codice prefisso ammissibile, vale $L^* \le L_{\text{Shannon}}$, da cui:

$$
H_D(X) \le L^* < H_D(X) + 1
$$

Il costo dell'arrotondamento all'intero non supera mai $1$ bit per simbolo.

### Abbattimento del Sovraccarico tramite Codifica a Blocchi

Il termine additivo unitario $+1$ bit/simbolo può rappresentare un'inefficienza significativa se l'entropia della sorgente è ridotta (ad esempio se $H(X) = 0.2$ bit, spendere fino a $1.2$ bit implica una ridondanza percentuale considerevole).

Per abbattere tale sovraccarico, si applica la tecnica della __codifica a blocchi__ (sorgente estesa di ordine $n$), trattando gruppi di $n$ simboli consecutivi $X^n = (X_1, X_2, \dots, X_n)$ come super-simboli definiti sull'alfabeto prodotto $\mathcal{X}^n$.

Applicando il Teorema di Shannon al blocco esteso:

$$
H_D(X_1, X_2, \dots, X_n) \le L_n^* < H_D(X_1, X_2, \dots, X_n) + 1
$$

Dividendo l'intera disuguaglianza per la lunghezza del blocco $n$, la lunghezza media per singolo simbolo di sorgente $L_n^* / n$ soddisfa:

$$
\frac{H_D(X^n)}{n} \le \frac{L_n^*}{n} < \frac{H_D(X^n)}{n} + \frac{1}{n}
$$

Se la sorgente è stazionaria e priva di memoria (i.i.d.), $H_D(X^n) = n H_D(X)$, per cui:

$$
H_D(X) \le \frac{L_n^*}{n} < H_D(X) + \frac{1}{n}
$$

Facendo tendere la dimensione del blocco all'infinito:

$$
\lim_{n \to \infty} \frac{L_n^*}{n} = H_D(X)
$$

Se la sorgente presenta memoria statistica ma è stazionaria, per il teorema dell'entropy rate vale $\lim_{n \to \infty} \frac{H(X^n)}{n} = H(\mathcal{X})$, per cui:

$$
\lim_{n \to \infty} \frac{L_n^*}{n} = H(\mathcal{X})
$$

La codifica a blocchi consente di avvicinarsi asintoticamente al limite teorico di Shannon con scarto arbitrariamente piccolo a spese di una complessità combinatoria crescente esponenzialmente con la dimensione del blocco ($m^n$).

### Il Costo della Statistica Errata (Mismatched Code)

Supponiamo che un progettista ottimizzi un codice di compressione prefisso assumendo un modello teorico descritto da una PMF $q(x)$, mentre la reale distribuzione statistica del sistema fisico è governata da $p(x)$. 

Le lunghezze del codice assegnate ai simboli saranno $l(x) = \lceil \log_2(1/q(x)) \rceil$. Calcolando la lunghezza media attesa rispetto alla reale misura di probabilità $p(x)$:

$$
\mathbb{E}_p[l_q(X)] = \sum_{x \in \mathcal{X}} p(x) \left\lceil \log_2 \frac{1}{q(x)} \right\rceil
$$

Sfruttando la delimitazione $\log_2 \frac{1}{q(x)} \le l_q(x) < \log_2 \frac{1}{q(x)} + 1$:

$$
\sum_{x \in \mathcal{X}} p(x) \log_2 \frac{1}{q(x)} \le \mathbb{E}_p[l_q(X)] < \sum_{x \in \mathcal{X}} p(x) \log_2 \frac{1}{q(x)} + 1
$$

Scomponendo il logaritmo mediante l'artificio algebrico $\log_2 \frac{1}{q(x)} = \log_2 \frac{p(x)}{q(x)} + \log_2 \frac{1}{p(x)}$:

$$
\sum_{x \in \mathcal{X}} p(x) \log_2 \frac{1}{p(x)} + \sum_{x \in \mathcal{X}} p(x) \log_2 \frac{p(x)}{q(x)} = H(p) + D(p \parallel q)
$$

Ne discende il Teorema del Codice Mismatched:

$$
H(p) + D(p \parallel q) \le \mathbb{E}_p[l_q(X)] < H(p) + D(p \parallel q) + 1
$$

Il prezzo esatto, misurato in bit addizionali per simbolo, pagato per aver formulato un modello probabilistico errato coincide esattamente con la __divergenza di Kullback-Leibler__ $D(p \parallel q)$ tra la realtà fisica e il modello teorico.

## L'Algoritmo di Huffman Ottimo (1952)

Mentre il codice di Shannon assegna lunghezze teoriche $l_i = \lceil \log(1/p_i) \rceil$ senza garantire la stretta ottimalità per alfabeti a lunghezza finita, David Huffman (1952) sviluppò un algoritmo costruttivo greedy deterministico che calcola la codifica prefissa a minima lunghezza media attesa assoluta.

### Procedura Costruttiva Bottom-Up

L'algoritmo di Huffman opera iterativamente fondendo i simboli a probabilità minore a partire dal basso (foglie) verso l'alto (radice):

1. __Ordinamento__: Si elencano i simboli della sorgente ordinandoli in modo decrescente di probabilità.
2. __Riduzione (Merge)__: Si selezionano i due simboli con le probabilità più basse e si fondono in un unico super-simbolo aggregato avente probabilità pari alla somma delle due probabilità.
3. __Ricorsione__: Si riordina il nuovo insieme di $m-1$ elementi e si ripete la fusione finché non rimane un unico elemento radice di probabilità $1$.
4. __Espansione Retrograda (Backtracking)__: Partendo dalla radice, a ciascun ramo della biforcazione si assegna un bit binario ('0' al ramo superiore, '1' al ramo inferiore). Ripercorrendo l'albero fino ai simboli originari, si ricavano le parole di codice univoche.

### Esempio Didattico Dettagliato

Si consideri una sorgente a 5 simboli $\mathcal{X} = \{1, 2, 3, 4, 5\}$ avente le seguenti probabilità:

$$
p(1) = 0.25, \quad p(2) = 0.25, \quad p(3) = 0.20, \quad p(4) = 0.15, \quad p(5) = 0.15
$$

![[slide_04_huffman_reduction_example.png|center mid]]

L'albero di riduzione procede attraverso le seguenti iterazioni:
1. I due simboli a minima probabilità sono $4$ e $5$ ($p(4)=p(5)=0.15$). Vengono fusi nel super-simbolo $\{4, 5\}$ di probabilità $0.15 + 0.15 = 0.30$.
2. L'insieme ridotto contiene ora $\{1, 2, 3, \{4, 5\}\}$ con probabilità $\{0.25, 0.25, 0.20, 0.30\}$. Ordinando: $\{4, 5\}: 0.30$, $1: 0.25$, $2: 0.25$, $3: 0.20$.
3. I due simboli a minima probabilità sono $2$ e $3$. Vengono fusi nel nodo $\{2, 3\}$ con probabilità $0.25 + 0.20 = 0.45$.
4. L'insieme ridotto contiene $\{\{4, 5\}: 0.30, 1: 0.25, \{2, 3\}: 0.45\}$. Si fondono i due nodi minori $\{4, 5\}$ e $1$, generando il nodo $\{\{4, 5\}, 1\}$ con probabilità $0.30 + 0.25 = 0.55$.
5. Rimangono due super-nodi: $\{\{4, 5\}, 1\}$ ($0.55$) e $\{2, 3\}$ ($0.45$). La loro unione genera la radice con probabilità $1.00$.

Ripercorrendo l'albero per l'assegnazione dei bit:

| Simbolo $x$ | $p(x)$ | Parola di Codice $C(x)$ | Lunghezza $l(x)$ | Lunghezza Ottima Continua $l^*(x)$ |
| :---: | :---: | :---: | :---: | :---: |
| $1$ | $0.25$ | $01$ | $2$ bit | $2.00$ bit |
| $2$ | $0.25$ | $10$ | $2$ bit | $2.00$ bit |
| $3$ | $0.20$ | $11$ | $2$ bit | $2.32$ bit |
| $4$ | $0.15$ | $000$ | $3$ bit | $2.74$ bit |
| $5$ | $0.15$ | $001$ | $3$ bit | $2.74$ bit |

Calcolo della lunghezza media del codice di Huffman:

$$
L(C_{\text{Huff}}) = 0.25(2) + 0.25(2) + 0.20(2) + 0.15(3) + 0.15(3) = 0.50 + 0.50 + 0.40 + 0.45 + 0.45 = 2.30 \quad \text{bit}
$$

Calcolo dell'entropia di Shannon della sorgente:

$$
H(X) = 2(0.25 \log_2 4) + 0.20 \log_2 5 + 2(0.15 \log_2(1/0.15)) \approx 2(0.50) + 0.20(2.3219) + 0.30(2.737) \approx 2.2855 \quad \text{bit}
$$

La ridondanza del codice è minima:

$$
L(C_{\text{Huff}}) - H(X) = 2.30 - 2.2855 = 0.0145 \quad \text{bit/simbolo}
$$

L'efficienza del codice $\eta = H(X)/L = 2.2855 / 2.30 \approx 99.37\%$.

### Codifica di Huffman $D$-aria e Simboli Fittizi di Padding

Quando l'alfabeto di codice ha cardinalità $D > 2$ (ad esempio ternario con $D = 3$), a ciascun passo di fusione si devono aggregare $D$ simboli anziché $2$.

A ciascuna riduzione, il numero totale di elementi si riduce esattamente di $D - 1$:

$$
m_{\text{nuovo}} = m_{\text{vecchio}} - (D - 1)
$$

Affinché l'albero si chiuda perfettamente su un unico nodo radice dopo un numero intero $k$ di aggregazioni, la dimensione dell'alfabeto iniziale deve soddisfare la congruenza modulare:

$$
m = 1 + k(D - 1) \iff m \equiv 1 \pmod{D - 1}
$$

Se la dimensione originaria $m$ non soddisfa tale condizione, l'ultimo passo di riduzione si troverebbe con un numero parziale di rami compreso tra $2$ e $D-1$, generando una biforcazione incompleta alla radice che viola la compattezza dell'albero ottimo.

La soluzione consiste nell'introdurre $m_{\text{dummy}}$ __simboli fittizi__ (__dummy symbols__) aventi probabilità rigorosamente nulla ($p_{\text{dummy}} = 0$), calcolati in modo tale che $(m + m_{\text{dummy}}) \equiv 1 \pmod{D - 1}$:

$$
m_{\text{dummy}} = [-(m - 1)] \bmod (D - 1) = \begin{cases} 0 & \text{se } (m - 1) \bmod (D - 1) = 0 \\ (D - 1) - [(m - 1) \bmod (D - 1)] & \text{altrimenti} \end{cases}
$$

I simboli fittizi si collocano in fondo alla lista delle probabilità e vengono assorbiti nella primissima fusione, garantendo la perfetta simmetria dell'albero $D$-ario.

### Dimostrazione dell'Ottimalità di Huffman

L'ottimalità dell'algoritmo di Huffman poggia sulle tre proprietà canoniche dei codici prefissi ottimi (inversione di monotonia, parità di lunghezza dei due simboli meno probabili, gemellaggio come nodi fratelli). 

La dimostrazione formale rigorosa per induzione sul numero di simboli $m$ è presentata integralmente nella sezione [[zz. Argomenti extra#Dimostrazione Formale del Teorema di Ottimalità dei Codici di Huffman tramite Riduzione Canonica|dimostrazione formale di ottimalità di Huffman]].

## Codici di Huffman Canonici e Applicazioni Industriali

In un'applicazione software o hardware reale (come la decompressione di un archivio ZIP o la visualizzazione di un'immagine JPEG), la trasmissione dell'albero di Huffman rappresenta un overhead rilevante: descrivere esplicitamente la topologia dell'albero e le parole di codice assegnate a un alfabeto di $256$ simboli byte richiederebbe centinaia di byte aggiuntivi.

I __Codici Canonici di Huffman__ risolvono tale problema standardizzando in modo deterministico l'assegnazione dei bit a partire dalla sola conoscenza della lista ordinata delle lunghezze delle parole di codice $\{l_1, l_2, \dots, l_m\}$.

### Regole di Generazione dei Codici Canonici

1. I simboli vengono ordinati primariamente per lunghezza di parola crescente ($l_i \le l_{i+1}$) e secondariamente per ordine lessicografico o alfabetico per simboli aventi pari lunghezza.
2. Alla prima parola di codice (la più corta) viene assegnata la sequenza formata da $l_1$ zeri:

   $$
   C(x_1) = 00\dots0
   $$

3. Per passare alla parola successiva $C(x_{i+1})$ avente lunghezza $l_{i+1}$:
   - Si incrementa di $1$ in aritmetica binaria intera il valore numerico della parola precedente $C(x_i)$:

     $$
     V_{i+1}' = V_i + 1
     $$

   - Se la lunghezza della nuova parola è maggiore ($l_{i+1} > l_i$), si esegue uno shift a sinistra di $l_{i+1} - l_i$ posizioni, accodando $l_{i+1} - l_i$ zeri:

     $$
     V_{i+1} = (V_i + 1) \ll (l_{i+1} - l_i)
     $$

Grazie a questa convenzione:
- Il trasmettitore deve comunicare al ricevitore unicamente il numero di bit assegnato a ciascun simbolo (pochi byte di metadati).
- La decodifica può essere implementata in modo estremamente rapido tramite lookup table dirette indicizzate per lunghezza, eliminando i puntatori ad albero in memoria RAM.
- Tale architettura costituisce il motore di compressione interno di formati onnipresenti quali __Deflate (PKZIP, Gzip)__, __PNG__, __JPEG__ e __Brotli__.

## Equivalenza tra Codifica di Sorgente e il Gioco delle "20 Domande"

Un'interpretazione epistemologica profonda della codifica di sorgente risiede nella sua stretta equivalenza con il celebre gioco d'azzardo logico delle "20 Domande", in cui un giocatore deve identificare un oggetto incognito $X \sim p(x)$ formulando domande binarie a risposta esclusiva (Sì / No).

### Domande Libere e Strategia Ottima

Sia $Q$ il numero di domande binarie necessarie a identificare univocamente l'oggetto incognito $X$. Ciascuna domanda corrisponde a partizionare lo spazio campionario $\mathcal{X}$ in due sottoinsiemi $A$ e $A^c$, chiedendo «$X \in A$ ?».

Se il giocatore è libero di costruire arbitrariamente i sottoinsiemi $A$ ad ogni iterazione:
- Ciascuna strategia di gioco definisce un albero binario le cui foglie sono i singoli elementi di $\mathcal{X}$.
- Il numero di domande formulate per raggiungere la foglia $x$ coincide esattamente con la profondità del nodo, ossia la lunghezza della parola di codice $l(x)$ in un codice prefisso binario.
- Il numero medio atteso di domande necessarie coincide con la lunghezza media attesa del codice:

  $$
  \mathbb{E}[Q] = \sum_{x \in \mathcal{X}} p(x) l(x) = L
  $$

- La strategia di interrogazione che minimizza il numero medio di domande corrisponde all'__algoritmo di Huffman__.
- Il numero medio di domande è delimitato dall'entropia di Shannon:

  $$
  H(X) \le \mathbb{E}[Q_{\text{ottimo}}] < H(X) + 1
  $$

### Domande Vincolate all'Ordine e Codici a Fetta (Slice Codes / Codici Alfabetici)

Nel gioco standard delle 20 domande, l'algoritmo di Huffman formula quesiti su sottoinsiemi arbitrari $\mathcal{A} \subseteq \mathcal{X}$ («$X \in \mathcal{A}$ ?»). Consideriamo ora lo stesso gioco con un insieme ristretto di domande: assumiamo che i simboli di $\mathcal{X} = \{1, 2, \dots, m\}$ siano ordinati e che le uniche domande ammissibili siano della forma «$X > a$ ?» per una certa soglia $a$ (domande a fetta o __slice questions__).

Si distinguono due scenari fondamentali (Cover & Thomas Sez. 5.9; Lucidi 12–13):

1. __Ordinamento Naturale per Probabilità Decrescente ($p_1 \ge p_2 \ge \dots \ge p_m$)__:
   - L'albero standard generato dalla procedura di fusione di Huffman potrebbe non corrispondere a fette ordinate (nell'esempio a 5 simboli, il codice originario per $4$ è $000$ e per $1$ è $01$, non ordinati lessicograficamente).
   - Tuttavia, prelevando il vettore delle lunghezze ottime ordinate di Huffman $l_1 \le l_2 \le \dots \le l_m$ (ad esempio $\{2, 2, 2, 3, 3\}$) e assegnando i simboli ordinati al primo nodo disponibile da sinistra a destra sull'albero, si ottiene la nuova assegnazione:

     $$
     1 \to 00, \quad 2 \to 01, \quad 3 \to 10, \quad 4 \to 110, \quad 5 \to 111
     $$

   - Ciascun bit divide l'insieme dei nodi in fette contigue $\{x : x \le a\}$ e $\{x : x > a\}$.
   - Poiché le lunghezze $\{l_i\}$ sono identiche a quelle di Huffman, tale codice a fette è __simultaneamente alfabetico e globalmente ottimo__:

     $$
     L_{\text{slice}} = L_{\text{Huff}} = 2.30 \quad \text{bit}
     $$

2. __Ordinamento Lessicografico Arbitrario Indipendente dalle Probabilità__:
   - Se l'alfabeto possiede un ordine prefissato arbitrario (ad esempio alfabetico $A, B, C, \dots$) in cui la sequenza di probabilità non è monotona, l'assegnazione di Huffman può violare il vincolo d'ordine e non può essere riordinata senza alterare le lunghezze.
   - Il codice ottimo con vincolo d'ordine (detto __codice alfabetico__ o albero di ricerca binaria ottimo) si ricava tramite algoritmi specializzati (quali l'algoritmo di Hu-Tucker o di Gilbert-Moore).
   - In questo scenario generale, la lunghezza media del codice alfabetico ottimo soddisfa il limite:

     $$
     H(X) \le L_{\text{alfabetico}} < H(X) + 2
     $$

## Confronto tra Algoritmi di Codifica: Shannon, Fano e Huffman

Prima dell'invenzione del metodo di Huffman, Claude Shannon (1948) e Robert Fano (1949) avevano proposto due approcci alternativi di codifica a prefisso.

### Codifica di Shannon
Assegna direttamente a ciascun simbolo la lunghezza arrotondata per eccesso $l_i = \lceil \log_2(1/p_i) \rceil$. Garantisce la proprietà prefissa e la convergenza a blocchi, ma per alfabeti piccoli può risultare sensibilmente inefficiente rispetto a Huffman.

### Codifica di Fano (Top-Down Greedy)
L'algoritmo di Fano adotta un approccio opposto a quello di Huffman, procedendo in modo top-down:
1. Si elencano i simboli in ordine decrescente di probabilità.
2. Si partiziona la sequenza in due gruppi contigui in modo tale che la somma delle probabilità dei due blocchi sia il più vicina possibile ($p(A) \approx p(B) \approx 0.5$).
3. Si assegna il bit '0' al primo blocco e '1' al secondo blocco.
4. Si itera ricorsivamente la bipartizione su ciascun sottogruppo finché ogni sottoinsieme contiene un unico simbolo.

### Controesempio di Sub-Ottimalità di Fano

Sebbene intuitiva, la procedura greedy top-down di Fano non garantisce l'ottimalità globale, poiché una scelta localmente ottima alla radice può vincolare le partizioni successive a sottoalberi inefficienti.

Si consideri la classica distribuzione a 5 simboli (Cover & Thomas, Esempio 5.5.1):

| Simbolo $x$ | $p(x)$ | Codice Fano | Lunghezza Fano $l_F(x)$ | Codice Huffman | Lunghezza Huffman $l_H(x)$ |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $1$ | $0.35$ | $00$ | $2$ bit | $0$ | $1$ bit |
| $2$ | $0.17$ | $01$ | $2$ bit | $100$ | $3$ bit |
| $3$ | $0.17$ | $10$ | $2$ bit | $101$ | $3$ bit |
| $4$ | $0.16$ | $110$ | $3$ bit | $110$ | $3$ bit |
| $5$ | $0.15$ | $111$ | $3$ bit | $111$ | $3$ bit |

Analisi delle due costruzioni:
1. __Costruzione di Fano__:
   - Prima bipartizione: l'algoritmo minimizza la differenza partizionando tra $\{1, 2\}$ ($\sum = 0.52$) e $\{3, 4, 5\}$ ($\sum = 0.48$), con scarto $|0.52 - 0.48| = 0.04$ (rispetto a $|0.35 - 0.65| = 0.30$).
   - Questo assegna prefisso '0' a $\{1, 2\}$ e prefisso '1' a $\{3, 4, 5\}$.
   - Le successive suddivisioni generano le lunghezze $\{2, 2, 2, 3, 3\}$.
   - Lunghezza media attesa di Fano:

     $$
     L_{\text{Fano}} = 0.35(2) + 0.17(2) + 0.17(2) + 0.16(3) + 0.15(3) = 0.70 + 0.34 + 0.34 + 0.48 + 0.45 = 2.31 \quad \text{bit}
     $$

2. __Costruzione di Huffman__:
   - Fusione bottom-up dei simboli minimi $4$ e $5$: $0.16 + 0.15 = 0.31$.
   - Fusione dei due simboli successivi $2$ e $3$: $0.17 + 0.17 = 0.34$.
   - Fusione dei due super-nodi: $0.34 + 0.31 = 0.65$.
   - Fusione finale alla radice: il simbolo $1$ ($0.35$) si unisce con il super-nodo ($0.65$).
   - Al simbolo più probabile $1$ viene assegnata una parola di un solo bit ('0'), mentre agli altri quattro simboli è assegnata una parola di $3$ bit.
   - Lunghezza media attesa di Huffman:

     $$
     L_{\text{Huff}} = 0.35(1) + 0.17(3) + 0.17(3) + 0.16(3) + 0.15(3) = 0.35 + 3(0.65) = 2.30 \quad \text{bit}
     $$

Il confronto numerico dimostra in modo inconfutabile la stretta sub-ottimalità dell'approccio top-down di Fano:

$$
L_{\text{Huff}} = 2.30 \quad \text{bit} < L_{\text{Fano}} = 2.31 \quad \text{bit}
$$

## Codifica di Shannon-Fano-Elias

La codifica di __Shannon-Fano-Elias__ costituisce uno schema analitico fondamentale, non solo per il suo valore teorico, ma perché stabilisce il ponte concettuale diretto tra la codifica a simboli discreti e la moderna __codifica aritmetica__.

### La Funzione di Ripartizione Cumulativa Modificata

Sia $\mathcal{X} = \{1, 2, \dots, m\}$ un alfabeto discreto ordinato con probabilità $p(x) > 0$. Si definisce la funzione di distribuzione cumulativa (CDF):

$$
F(x) = \sum_{a=1}^x p(a)
$$

con la convenzione $F(0) = 0$.

Poiché la funzione $F(x)$ definisce gradini discreti di ampiezza $p(x)$, Peter Elias propose di utilizzare il __punto medio__ di ciascun gradino, introducendo la funzione cumulativa modificata:

$$
\bar{F}(x) = \sum_{a=1}^{x-1} p(a) + \frac{1}{2} p(x) = F(x-1) + \frac{1}{2} p(x)
$$

Poiché per ipotesi $p(x) > 0$, i punti medi di simboli distinti sono rigorosamente separati:

$$
x \neq y \implies \bar{F}(x) \neq \bar{F}(y)
$$

Di conseguenza, il valore reale $\bar{F}(x) \in [0, 1)$ identifica univocamente il simbolo $x$.

![[slide_28_shannon_fano_elias_interval.png|center mid]]

### Troncamento Binario ed Estrazione del Codice

Essendo un numero reale continuo nell'intervallo $[0, 1)$, $\bar{F}(x)$ richiederebbe una precisione infinita (un numero infinito di bit). 

Per ottenere un codice a lunghezza finita, si tronca lo sviluppo binario di $\bar{F}(x)$ a un numero finito $l(x)$ di cifre binarie. Lo sviluppo in base 2 è dato da:

$$
\bar{F}(x) = 0.b_1 b_2 b_3 \dots = \sum_{i=1}^\infty b_i 2^{-i}
$$

Si definisce il troncamento a $l(x)$ bit:

$$
\lfloor \bar{F}(x) \rfloor_{l(x)} = 0.b_1 b_2 \dots b_{l(x)} = \sum_{i=1}^{l(x)} b_i 2^{-i}
$$

La sequenza binaria finita $b_1 b_2 \dots b_{l(x)}$ costituisce la parola di codice $C(x)$.

### Teorema sulla Lunghezza e Proprietà Prefissa

Scegliendo la lunghezza di troncamento:

$$
l(x) = \left\lceil \log_2 \frac{1}{p(x)} \right\rceil + 1
$$

il codice di Shannon-Fano-Elias risulta rigorosamente __istantaneo (prefisso)__.

#### Dimostrazione

Dalla scelta di $l(x) = \lceil \log_2(1/p(x)) \rceil + 1 \ge \log_2(1/p(x)) + 1$, si ottiene:

$$
2^{-l(x)} \le 2^{-(\log_2(1/p(x)) + 1)} = \frac{p(x)}{2}
$$

D'altra parte, per la natura del troncamento binario, l'errore commesso trascurando i bit oltre l'indice $l(x)$ soddisfa strettamente:

$$
\bar{F}(x) - \lfloor \bar{F}(x) \rfloor_{l(x)} = \sum_{i=l(x)+1}^\infty b_i 2^{-i} < 2^{-l(x)} \le \frac{p(x)}{2}
$$

Ne deriva che l'intervallo diadico associato al troncamento:

$$
I(x) = \left[ \lfloor \bar{F}(x) \rfloor_{l(x)}, \, \lfloor \bar{F}(x) \rfloor_{l(x)} + 2^{-l(x)} \right)
$$

ha ampiezza al più $p(x)/2$. Poiché $\lfloor \bar{F}(x) \rfloor_{l(x)} \le \bar{F}(x)$ e $\lfloor \bar{F}(x) \rfloor_{l(x)} + 2^{-l(x)} > \bar{F}(x)$, e dato che $\bar{F}(x) = F(x-1) + \frac{1}{2}p(x)$ dista esattamente $p(x)/2$ da entrambi gli estremi del gradino $[F(x-1), F(x))$, l'intervallo diadico $I(x)$ cade interamente all'interno del gradino:

$$
I(x) \subset [F(x-1), F(x))
$$

Poiché i gradini $[F(x-1), F(x))$ corrispondenti a simboli differenti sono disgiunti per costruzione, anche gli intervalli diadici $I(x)$ e $I(y)$ per $x \neq y$ sono reciprocamente disgiunti. 

Nessuna parola di codice può pertanto essere prefisso di un'altra (il che corrisponderebbe al contenimento di un intervallo diadico dentro un altro). Il codice è quindi rigorosamente prefisso.

### Calcolo della Lunghezza Media Attesa

Calcolando il valore atteso della lunghezza del codice:

$$
L = \sum_{x \in \mathcal{X}} p(x) l(x) = \sum_{x \in \mathcal{X}} p(x) \left( \left\lceil \log_2 \frac{1}{p(x)} \right\rceil + 1 \right)
$$

Poiché $\lceil z \rceil < z + 1$:

$$
l(x) < \log_2 \frac{1}{p(x)} + 2
$$

Moltiplicando per $p(x)$ e sommando:

$$
L < \sum_{x \in \mathcal{X}} p(x) \left( \log_2 \frac{1}{p(x)} + 2 \right) = H(X) + 2 \quad \text{bit}
$$

Il codice di Shannon-Fano-Elias richiede al più $2$ bit aggiuntivi rispetto all'entropia teorica della sorgente:

$$
H(X) + 1 \le L_{\text{SFE}} < H(X) + 2
$$

Sebbene richieda circa 1 bit in più rispetto a Huffman, questo schema consente la decomposizione aritmetica ricorsiva per flussi sequenziali continui, rappresentando il fondamento matematico diretto della __Codifica Aritmetica__.

## Teorema sull'Ottimalità Competitiva della Codifica di Sorgente

La formulazione classica di ottimalità di un codice mira a minimizzare la lunghezza media attesa:

$$
C^* = \arg\min_C \mathbb{E}[l_C(X)]
$$

Tuttavia, in un'ottica decisionale o di teoria dei giochi competitiva, ci si potrebbe domandare: *è possibile che un codice alternativo $C'$ risulti migliore del codice ottimo nella maggioranza delle trasmissioni individuali, pur avendo una media leggermente peggiore a causa di parole molto lunghe assegnate a eventi rari?*

Il __Teorema dell'Ottimalità Competitiva__ (Cover & Thomas, Sez. 5.10; Lucido 32–33) inquadra il confronto tra codici prefissi come un gioco a somma zero tra due giocatori. Dati una PMF $p(x)$ e un simbolo estratto $X \sim p(x)$, il payoff per il primo codificatore vale $+1$ se la sua parola è strettamente più corta ($l(X) < l'(X)$), $0$ se hanno pari lunghezza ($l(X) = l'(X)$), e $-1$ se è più lunga ($l(X) > l'(X)$).

### Enunciato del Teorema di Cover & Thomas

Sia $l(x) = \lceil \log_2(1/p(x)) \rceil$ la lunghezza della parola di codice assegnata dal codice di Shannon per una distribuzione $p(x)$. Sia $l'(x)$ la lunghezza assegnata da un qualsiasi altro codice univocamente decodificabile. 

Allora, per ogni intero $c \ge 1$, la probabilità che il codice concorrente superi il codice di Shannon di almeno $c$ bit è delimitata esponenzialmente:

$$
\text{Pr}\{l(X) \ge l'(X) + c\} \le \frac{1}{2^{c-1}}
$$

In particolare:
- Per $c = 2$: la probabilità che un codice alternativo batta il codice di Shannon di $2$ o più bit non può superare la metà:

  $$
  \text{Pr}\{l(X) - l'(X) \ge 2\} \le \frac{1}{2}
  $$

- Per margini elevati la probabilità decade esponenzialmente: ad esempio, un concorrente può vincere di $c = 5$ bit in meno di $2^{-(5-1)} = 1/16$ dei casi.
- Nel gioco competitivo, il codice di Shannon (e a fortiori il codice ottimo di Huffman) garantisce che la probabilità di vincere sia maggiore o uguale alla probabilità di perdere:

  $$
  \text{Pr}\{l(X) < l'(X)\} \ge \text{Pr}\{l(X) > l'(X)\}
  $$

  assicurando un payoff medio atteso intrinsecamente non negativo: $\mathbb{E}[\text{Payoff}] \ge 0$.

La dimostrazione analitica rigorosa, basata sulla disuguaglianza di McMillan e sul bound esponenziale pesato $\text{Pr}\{l(X) - l'(X) \ge c\} \le 2^{-(c-1)}$, è dettagliata nella sezione [[zz. Argomenti extra#Teorema sull'Ottimalità Competitiva della Codifica di Shannon e Huffman|approfondimento sull'ottimalità competitiva]].

## Quadro Sinottico Comparativo dei Metodi di Codifica di Sorgente

La tabella seguente riassume le caratteristiche strutturali, algoritmiche e prestazionali degli schemi di codifica senza perdita analizzati:

| Algoritmo di Codifica | Approccio Costruttivo | Vincolo di Lunghezza $l(x)$ | Delimitazione della Lunghezza Media $L$ | Ottimalità Dimostrata | Standard e Ambiti Applicativi Tipici |
| :--- | :--- | :--- | :--- | :--- | :--- |
| __Codice di Shannon (1948)__ | Assegnazione analitica diretta | $l(x) = \lceil \log_D(1/p(x)) \rceil$ | $H_D(X) \le L < H_D(X) + 1$ | Sub-ottimo a blocchi finiti; asintotico per $n \to \infty$ | Basi teoriche, dimostrazioni analitiche di Shannon |
| __Codice di Fano (1949)__ | Top-down greedy per bisezione di massa | Partizione ricorsiva con $p(A) \approx p(B)$ | $H(X) \le L < H(X) + 2$ | Sub-ottimo (decisioni top-down irreversibili) | Primi sistemi telematici e architetture storiche |
| __Codice di Huffman (1952)__ | Bottom-up iterativo con fusione nodi minimi | Risultato della topologia dell'albero | $H_D(X) \le L^* < H_D(X) + 1$ | __Ottimo Assoluto__ su blocchi di simboli a cardinalità fissa | Archivi ZIP, gzip, compressori generici |
| __Huffman Canonico__ | Standardizzazione lessicografica deterministica | Vettore di lunghezze di Huffman $\{l_i\}$ | Identica al codice di Huffman | Ottimo con minimo consumo di metadati d'intestazione | __JPEG__, __PNG__, __Deflate__, __MP3__, __Brotli__ |
| __Shannon-Fano-Elias__ | Troncamento binario del punto medio CDF | $l(x) = \lceil \log_2(1/p(x)) \rceil + 1$ | $H(X) + 1 \le L < H(X) + 2$ | Sub-ottimo per simboli singoli (+2 bit) | Fondamento concettuale della __Codifica Aritmetica__ |
| __Codifica a Blocchi ($n$-estesa)__ | Huffman applicato a super-simboli $\mathcal{X}^n$ | Lunghezze su alfabeto $\mathcal{X}^n$ | $H(\mathcal{X}) \le \frac{L_n}{n} < H(\mathcal{X}) + \frac{1}{n}$ | Asintoticamente convergente all'entropy rate | Trasmissione di testi naturali, compressione fax |
