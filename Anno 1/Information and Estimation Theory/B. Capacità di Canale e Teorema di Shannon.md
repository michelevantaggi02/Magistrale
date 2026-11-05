# B. Capacità di Canale e Teorema di Shannon

La trasmissione affidabile di segnali e dati numerici attraverso mezzi fisici reali costituisce il nucleo fondante della teoria delle telecomunicazioni e dell'ingegneria informatica. Qualsiasi canale fisico — sia esso una fibra ottica, un collegamento radio wireless, un bus su circuito stampato, una cella di memoria flash o un canale satellitare — è intrinsecamente soggetto ad attenuazione, dispersione e rumore termico stocastico.

Nel suo capolavoro del 1948, Claude Shannon rivoluzionò l'intera comunità scientifica dimostrando un risultato profondamente controintuitivo: il rumore fisico non impone un limite insuperabile all'affidabilità della trasmissione, ma determina unicamente un limite superiore al __tasso di trasmissione__ (espresso in bit per uso di canale). Fintanto che la velocità di trasmissione si mantiene al di sotto di tale soglia critica, denominata __capacità di canale__ ($C$), è teoricamente possibile comunicare con una probabilità d'errore arbitrariamente piccola mediante l'impiego di codici a correzione d'errore sufficientemente lunghi.

La presente trattazione formalizza il modello matematico del canale discreto senza memoria, definisce la nozione di insiemi non confondibili, calcola in forma chiusa la capacità dei canali notevoli (BSC, BEC, canali simmetrici), dimostra il celebre Secondo Teorema di Shannon (Channel Coding Theorem) nelle sue componenti diretta e inversa, ed espone il Teorema di Separazione Sorgente-Canale.

## Il Modello del Canale di Comunicazione

Da un punto di vista epistemologico e fisico, un processo di comunicazione tra un trasmettitore $A$ e un ricevitore $B$ consiste nel fare in modo che le azioni fisiche compiute da $A$ inducano uno stato fisico desiderato e correlato in $B$. La comunicazione ha successo se e solo se $A$ e $B$ concordano univocamente sul messaggio scambiato.

Un sistema di trasmissione digitale viene formalizzato attraverso lo schema a blocchi universale di Shannon:

![[slide_02_communication_system_block.png|center mid]]

### Componenti dell'Architettura di Canale

1. __Sorgente di Informazione e Messaggio__: La sorgente seleziona un messaggio $W$ appartenente a un insieme discreto e finito di messaggi equiprobabili:

   $$
   W \in \mathcal{W} = \{1, 2, \dots, M\}
   $$

   La quantità di informazione generata dalla scelta del messaggio è data da $\log_2 M$ bit.

2. __Codificatore di Canale (Encoder)__: Mappa l'indice di messaggio $W$ in una sequenza di $n$ simboli di canale, producendo la parola di codice (__codeword__):

   $$
   X^n(W) = (X_1(W), X_2(W), \dots, X_n(W)) \in \mathcal{X}^n
   $$

   Il parametro intero $n$ rappresenta la __lunghezza di blocco__ (il numero di utilizzi del canale necessari per trasmettere il messaggio).

3. __Canale Rumoroso__: È il mezzo fisico di propagazione, modellato statisticamente da una famiglia di probabilità di transizione condizionate $p(y^n \mid x^n)$. Il canale distorce la sequenza trasmessa introducendo incertezza probabilistica, producendo in uscita la sequenza aleatoria:

   $$
   Y^n = (Y_1, Y_2, \dots, Y_n) \in \mathcal{Y}^n
   $$

4. __Decodificatore di Canale (Decoder)__: Riceve la sequenza perturbata $Y^n$ e applica una regola di decisione deterministica:

   $$
   g: \mathcal{Y}^n \to \{1, 2, \dots, M\}
   $$

   producendo la stima del messaggio trasmesso $\hat{W} = g(Y^n)$.

Il __tasso di trasmissione__ (__rate__) del codice di canale, misurato in bit per uso di canale (bit/simbolo), è definito dal rapporto tra l'informazione trasmessa e il numero di utilizzi del canale:

$$
R = \frac{\log_2 M}{n} \quad \text{bit/uso} \iff M = \lceil 2^{nR} \rceil
$$

Un codice caratterizzato da $M$ messaggi e lunghezza di blocco $n$ viene denotato sinteticamente come un codice $(2^{nR}, n)$ o $(M, n)$.

## Confusione tra Sequenze e Sottoinsiemi Non Confondibili

L'origine degli errori di ricezione risiede nel fenomeno della __confusione di canale__: poiché il rumore è un processo stocastico, due sequenze di ingresso distinte $X^n(1)$ e $X^n(2)$ possono entrambe produrre in uscita la medesima sequenza osservata $Y^n$ con probabilità non nulla.

### L'Esempio del Linguaggio Naturale

Si consideri la trasmissione di due messaggi distinti attraverso un canale con rumore testuale:
- Messaggio 1: «The cat sat on the mat»
- Messaggio 2: «The cat sat on the map»

Se il canale altera l'ultimo carattere scambiandolo con una 'd', la sequenza ricevuta diviene:
- Ricevuto: «The cat sat on the mad»

In fase di decodifica, entrambe le ipotesi originarie risultano ugualmente plausibili: il ricevitore ottiene una stima ambigua «The cat sat on the ma?». Gli ingressi sono tra loro __confondibili__ (__confusable__) poiché la distanza metrica tra le sequenze trasmesse è insufficiente a compensare la dispersione introdotta dal rumore.

### Il Principio delle Sequenze Non Confondibili

Per eliminare l'ambiguità, è necessario inserire __ridondanza controllata__: anziché utilizzare tutte le possibili sequenze dell'alfabeto di canale, il trasmettitore seleziona un sottoinsieme opportunamente distanziato di sequenze di ingresso (un codice a correzione d'errore).

Consideriamo i medesimi messaggi protetti da ridondanza:
- Messaggio 1 codificato: «The cat sat on the mattt»
- Messaggio 2 codificato: «The cat sat on the mappp»

Se il canale introduce un errore sulla consonante centrale e altera l'estensione, producendo in ricezione:
- Ricevuto: «The cat sat on the madpp»

Il decodificatore esamina le sequenze lecite e rileva che la configurazione osservata presenta una correlazione statistica schiacciante con il Messaggio 2 rispetto al Messaggio 1. La stima risulta corretta e univoca: $\hat{W} =$ «The cat sat on the map».

Questo principio geometrico costituisce il cardine della trasmissione affidabile:
- A ciascuna parola di codice trasmessa $X^n(w)$ corrisponde nello spazio delle uscite $\mathcal{Y}^n$ un cono o sfera di diffusione di sequenze ricevute probabili (avente volume orientativo $\approx 2^{n H(Y \mid X)}$).
- Lo spazio totale delle sequenze di uscita ha volume orientativo $\approx 2^{n H(Y)}$.
- Il numero massimo di messaggi distinti che possono essere allocati nello spazio di ricezione senza che le rispettive sfere di rumore si sovrappongano è limitato dal rapporto dei volumi:

  $$
  M \approx \frac{2^{n H(Y)}}{2^{n H(Y \mid X)}} = 2^{n [H(Y) - H(Y \mid X)]} = 2^{n I(X; Y)}
  $$

- Il massimo tasso a cui è possibile trasmettere con sfere di decodifica non sovrapposte coincide esattamente con la mutua informazione $I(X; Y)$.

## Definizione Formale di Canale Discreto e Capacità di Informazione

Un canale di comunicazione discreto è caratterizzato formalmente da:
- Un alfabeto d'ingresso discreto e finito $\mathcal{X}$;
- Un alfabeto d'uscita discreto e finito $\mathcal{Y}$;
- Una famiglia coerente di probabilità di transizione condizionate che specificano la probabilità di osservare $y$ all'uscita dato che $x$ è stato applicato all'ingresso:

  $$
  p(y \mid x) = \text{Pr}\{Y = y \mid X = x\}, \quad \forall x \in \mathcal{X}, \; y \in \mathcal{Y}
  $$

  soggetta ai vincoli di stocasticità $\sum_{y \in \mathcal{Y}} p(y \mid x) = 1$ per ogni $x \in \mathcal{X}$.

### Il Canale Discreto Senza Memoria (DMC)

Un canale si definisce __discreto senza memoria__ (__Discrete Memoryless Channel__, DMC) se la distribuzione di probabilità dell'uscita all'istante presente dipende unicamente dal simbolo d'ingresso al medesimo istante, risultando condizionatamente indipendente da tutti gli ingressi e le uscite passate:

$$
p(y_k \mid x_1, x_2, \dots, x_k, y_1, y_2, \dots, y_{k-1}) = p(y_k \mid x_k)
$$

Come conseguenza diretta della memoria nulla, la distribuzione condizionata di un intero blocco di lunghezza $n$ si fattorizza nel prodotto marginale:

$$
p(y^n \mid x^n) = p(y_1, y_2, \dots, y_n \mid x_1, x_2, \dots, x_n) = \prod_{k=1}^n p(y_k \mid x_k)
$$

### Definizione di Capacità di Informazione di Canale

Si definisce __capacità di informazione di canale__ di un canale discreto senza memoria la massima informazione mutua tra l'ingresso $X$ e l'uscita $Y$ su un singolo uso di canale, calcolata massimizzando rispetto a tutte le possibili distribuzioni di probabilità d'ingresso $p(x)$:

$$
C = \max_{p(x)} I(X; Y)
$$

La massimizzazione avviene vincolando il vettore di probabilità $p(x)$ al simplesso probabilistico:

$$
p(x) \ge 0, \quad \sum_{x \in \mathcal{X}} p(x) = 1
$$

Poiché per un canale con matrice $p(y \mid x)$ fissata la funzione di informazione mutua $I(X; Y)$ è una funzione __concava__ rispetto alla distribuzione d'ingresso $p(x)$ definita su un insieme convesso e compatto, la capacità $C$ esiste sempre finita ed è unica. Ogni massimo locale corrisponde al massimo globale assoluto.

### Capacità Operativa di Canale

La __capacità operativa di canale__ rappresenta il supremo di tutti i tassi di trasmissione $R$ per i quali esiste una sequenza di codici di blocco $(2^{nR}, n)$ avente probabilità d'errore di decodifica asintoticamente nulla:

$$
C_{\text{operativa}} = \sup \left\{ R : \lim_{n \to \infty} P_e^{(n)} = 0 \right\}
$$

Il cardine teorico della teoria dell'informazione risiede nell'eguaglianza fondamentale stabilita da Shannon:

$$
C_{\text{operativa}} = C = \max_{p(x)} I(X; Y)
$$

La quantità matematica astratta $C = \max I(X; Y)$ governa in modo esatto la massima velocità fisica a cui è possibile trasmettere dati numerici attraverso il canale con affidabilità ideale.

## Calcolo della Capacità per Canali Notabili

L'applicazione della definizione variazionale $C = \max_{p(x)} I(X; Y)$ consente di calcolare in forma analitica chiusa la capacità delle topologie fondamentali di canale di comunicazione.

### Canale Perfetto Privo di Rumore (Noiseless Channel)

Nel canale ideale privo di rumore, l'uscita riproduce fedelmente l'ingresso ($Y = X$). La matrice di transizione è la matrice identità: $p(y \mid x) = \delta_{xy}$.

Calcolando l'informazione mutua:

$$
I(X; Y) = H(X) - H(X \mid Y) = H(X) - 0 = H(X)
$$

Massimizzando rispetto alla distribuzione d'ingresso:

$$
C = \max_{p(x)} H(X) = \log_2 |\mathcal{X}| \quad \text{bit/uso}
$$

Il massimo è raggiunto per la distribuzione d'ingresso uniforme: $p^*(x) = 1/|\mathcal{X}|$. A ciascun uso di canale è possibile trasmettere $\log_2 |\mathcal{X}|$ bit privi di incertezza.

### Canale con Uscite Disgiunte Non Sovrapposte

Si consideri un canale in cui a ciascun simbolo d'ingresso $x$ corrisponde un insieme di uscite possibili disgiunto da quello degli altri ingressi. Ad esempio, per $\mathcal{X} = \{0, 1\}$ e $\mathcal{Y} = \{1, 2, 3, 4\}$:
- Se $X = 0$, $Y$ assume equiprobabilmente i valori $\{1, 2\}$;
- Se $X = 1$, $Y$ assume equiprobabilmente i valori $\{3, 4\}$.

Sebbene il canale sia rumoroso (l'uscita $Y$ è stocastica), osservando $Y$ il ricevitore determina senza alcuna ambiguità quale simbolo $X$ sia stato inviato: $H(X \mid Y) = 0$.

Di conseguenza:

$$
I(X; Y) = H(X) - H(X \mid Y) = H(X) \implies C = \max_{p(x)} H(X) = \log_2 |\mathcal{X}| = 1 \quad \text{bit/uso}
$$

Pur in presenza di aleatorietà, la capacità è identica a quella di un canale perfetto poiché il rumore non genera alcuna confusione tra gli ingressi.

### La Macchina da Scrivere Rumorosa (Noisy Typewriter)

Si consideri una tastiera con un alfabeto circolare di $26$ lettere. Quando viene premuto un tasto $x$, il meccanismo batte fedelmente la lettera $x$ con probabilità $1/2$, oppure batte la lettera immediatamente successiva $(x+1) \bmod 26$ con probabilità $1/2$.

Calcolando l'entropia condizionata:

$$
H(Y \mid X = x) = H_B(1/2) = 1 \quad \text{bit} \implies H(Y \mid X) = 1 \quad \text{bit}
$$

L'informazione mutua vale:

$$
I(X; Y) = H(Y) - H(Y \mid X) = H(Y) - 1
$$

Poiché $Y$ appartiene a un alfabeto di $26$ lettere, l'entropia di uscita è limitata superiormente da $H(Y) \le \log_2 26$. Ponendo all'ingresso la distribuzione uniforme $p(x) = 1/26$, per simmetria l'uscita risulta uniforme ($H(Y) = \log_2 26$). La capacità vale:

$$
C = \log_2 26 - 1 = \log_2 26 - \log_2 2 = \log_2\left( \frac{26}{2} \right) = \log_2 13 \quad \text{bit/uso}
$$

Interpretazione operativa: per trasmettere a probabilità d'errore esattamente nulla su questo canale rumoroso, è sufficiente utilizzare unicamente $13$ lettere alternate dell'alfabeto (ad esempio $A, C, E, G, \dots$). In questo modo, le uscite associate a simboli distinti non si sovrappongono mai, consentendo la decodifica perfetta a un tasso di $\log_2 13$ bit per battuta.

### Il Canale Binario Simmetrico (Binary Symmetric Channel, BSC)

Il Canale Binario Simmetrico rappresenta il modello fondamentale della teoria delle comunicazioni digitali per sistemi affetti da rumore binario invertente (bit-flip).

Gli alfabeti sono binari: $\mathcal{X} = \{0, 1\}$ e $\mathcal{Y} = \{0, 1\}$. La probabilità di errore o inversione del singolo bit è $q \in [0, 1]$:

$$
p(0 \mid 0) = 1 - q, \quad p(1 \mid 0) = q, \quad p(0 \mid 1) = q, \quad p(1 \mid 1) = 1 - q
$$

![[slide_06_bsc_channel_model.png|center mid]]

Nel BSC, il rumore commuta i bit in modo totalmente cieco rispetto al messaggio: i bit ricevuti non forniscono alcun indizio su dove l'errore si sia manifestato; tutti i bit ricevuti sono ugualmente inaffidabili.

Calcoliamo analiticamente la capacità. L'entropia condizionata dell'uscita dato l'ingresso è indipendente dallo stato trasmesso:

$$
H(Y \mid X = 0) = H_B(q) = -q \log_2 q - (1 - q) \log_2(1 - q)
$$

$$
H(Y \mid X = 1) = H_B(q)
$$

Mediare rispetto a qualsiasi distribuzione d'ingresso $p(x)$:

$$
H(Y \mid X) = \sum_{x \in \{0, 1\}} p(x) H(Y \mid X = x) = p(0) H_B(q) + p(1) H_B(q) = H_B(q)
$$

L'informazione mutua si sviluppa come:

$$
I(X; Y) = H(Y) - H(Y \mid X) = H(Y) - H_B(q)
$$

Per massimizzare $I(X; Y)$, dobbiamo massimizzare l'entropia marginale di uscita $H(Y)$. Essendo $Y$ una variabile binaria, la sua entropia è limitata superiormente da $1$ bit:

$$
H(Y) \le 1 \quad \text{bit}
$$

con eguaglianza se e solo se $Y$ è uniformemente distribuita: $\text{Pr}\{Y = 0\} = \text{Pr}\{Y = 1\} = 1/2$. Esprimendo la probabilità di uscita in funzione della probabilità d'ingresso $p = \text{Pr}\{X = 1\}$:

$$
\text{Pr}\{Y = 1\} = p(1 - q) + (1 - p)q = p + q - 2pq
$$

Ponendo $\text{Pr}\{Y = 1\} = 1/2$, si ottiene l'unica soluzione $p = 1/2$, valida per ogni $q \neq 1/2$. Scegliendo la distribuzione d'ingresso uniforme $p^*(0) = p^*(1) = 1/2$, si raggiunge $H(Y) = 1$.

Si ottiene la formula classica della __capacità del Canale Binario Simmetrico__:

$$
C_{\text{BSC}} = 1 - H_B(q) \quad \text{bit/uso}
$$

#### Analisi dei Casi Limite del BSC

1. __Canale Perfetto ($q = 0$)__:

   $$
   H_B(0) = 0 \implies C = 1 - 0 = 1 \quad \text{bit/uso}
   $$

   Nessun bit viene invertito: il canale trasmette alla massima velocità teorica binaria.

2. __Canale a Rumore Puro ($q = 1/2$)__:

   $$
   H_B(1/2) = 1 \implies C = 1 - 1 = 0 \quad \text{bit/uso}
   $$

   L'uscita è statisticamente indipendente dall'ingresso: l'osservazione di $Y$ non fornisce alcuna informazione su $X$. La capacità si annulla completamente; nessuna trasmissione affidabile è possibile a tasso positivo.

3. __Canale Invertitore Deterministico ($q = 1$)__:

   $$
   H_B(1) = 0 \implies C = 1 - 0 = 1 \quad \text{bit/uso}
   $$

   Ogni bit trasmesso viene sistematicamente negato ($0 \to 1$, $1 \to 0$). Poiché l'inversione è deterministica e nota, il ricevitore inverte semplicemente tutti i bit osservati ($\hat{X} = 1 - Y$), recuperando la sequenza corretta al tasso massimo di $1$ bit per uso.

4. __Simmetria Funzionale__:
   Poiché la funzione di entropia binaria è simmetrica rispetto a $q = 1/2$ ($H_B(q) = H_B(1 - q)$), la capacità $C_{\text{BSC}}$ è simmetrica: trasmettere su un canale con probabilità d'errore $q = 0.9$ è matematicamente identico a trasmettere su un canale con $q = 0.1$ (avendo entrambi capacità $C = 1 - H_B(0.1) \approx 0.531$ bit).

### Il Canale Binario con Cancellazione (Binary Erasure Channel, BEC)

In molti canali fisici (ad esempio la trasmissione di pacchetti su reti IP dove il checksum corrotto causa lo scarto del pacchetto, oppure celle flash con tensione intermedia), il ricevitore non commette errori di inversione inosservati, ma è in grado di rilevare l'avvenuta perdita del simbolo.

Il __Canale Binario con Cancellazione__ (BEC) è caratterizzato da un alfabeto d'ingresso binario $\mathcal{X} = \{0, 1\}$ e da un alfabeto d'uscita ternario $\mathcal{Y} = \{0, 1, e\}$, dove $e$ indica il __simbolo di cancellazione__ (__erasure__). La probabilità di cancellazione è $\alpha \in [0, 1]$:

$$
p(0 \mid 0) = 1 - \alpha, \quad p(e \mid 0) = \alpha, \quad p(1 \mid 0) = 0
$$

$$
p(1 \mid 1) = 1 - \alpha, \quad p(e \mid 1) = \alpha, \quad p(0 \mid 1) = 0
$$

Sia $p = \text{Pr}\{X = 1\}$ la probabilità d'ingresso. La distribuzione di probabilità dell'uscita è:

$$
\text{Pr}\{Y = 0\} = (1 - p)(1 - \alpha), \quad \text{Pr}\{Y = 1\} = p(1 - \alpha), \quad \text{Pr}\{Y = e\} = \alpha
$$

Per calcolare l'entropia dell'uscita $H(Y)$, si scompone la variabile introducendo l'evento indicatore di cancellazione $E = 1_{\{Y = e\}}$:

$$
H(Y) = H(Y, E) = H(E) + H(Y \mid E) = H_B(\alpha) + (1 - \alpha) H(Y \mid E = 0) + \alpha H(Y \mid E = 1)
$$

Condizionatamente a $E = 0$ (simbolo non cancellato), $Y$ assume i valori $\{0, 1\}$ con probabilità $1 - p$ e $p$, per cui $H(Y \mid E = 0) = H_B(p)$. Condizionatamente a $E = 1$, $Y$ è deterministicamente pari a $e$, per cui $H(Y \mid E = 1) = 0$.

Ne deriva:

$$
H(Y) = H_B(\alpha) + (1 - \alpha) H_B(p)
$$

Calcolando l'entropia condizionata: per qualsiasi ingresso $x$, l'uscita può essere pari a $x$ con probabilità $1 - \alpha$ o cancellata $e$ con probabilità $\alpha$, da cui:

$$
H(Y \mid X) = H_B(\alpha)
$$

Sottraendo i due termini, l'informazione mutua risulta:

$$
I(X; Y) = H(Y) - H(Y \mid X) = H_B(\alpha) + (1 - \alpha) H_B(p) - H_B(\alpha) = (1 - \alpha) H_B(p)
$$

Poiché $H_B(p) \le 1$, il massimo è raggiunto per la distribuzione d'ingresso uniforme $p^* = 1/2$:

$$
C_{\text{BEC}} = 1 - \alpha \quad \text{bit/uso}
$$

#### Confronto Critico tra BSC e BEC

La differenza tra il canale BSC e il canale BEC è profonda:
- Nel BSC con probabilità d'errore $q$, la capacità è $C_{\text{BSC}} = 1 - H_B(q)$. Per $q \to 0$, $H_B(q) \approx -q \log_2 q$, la cui derivata prima diverge logaritmicamente a $-\infty$.
- Nel BEC con probabilità di cancellazione $\alpha$, la capacità è lineare: $C_{\text{BEC}} = 1 - \alpha$.
- A parità di tasso di corruzione del mezzo ($\alpha = q$), il canale BEC offre una capacità nettamente superiore: per $\alpha = 0.1$, $C_{\text{BEC}} = 0.90$ bit/uso, mentre $C_{\text{BSC}} \approx 0.53$ bit/uso. Sapere *dove* si è verificata la perdita di informazione riduce drasticamente l'incertezza residua rispetto a subire errori non tracciabili.

### Canali Simmetrici e Debolmente Simmetrici

Una classe geometricamente rilevante è costituita dai canali simmetrici.

1. Un canale si definisce __simmetrico__ se:
   - Ogni riga della matrice di transizione $[p(y \mid x)]$ è una permutazione di qualsiasi altra riga;
   - Ogni colonna della matrice è una permutazione di qualsiasi altra colonna.
2. Un canale si definisce __debolmente simmetrico__ (__weakly symmetric__) se:
   - Ogni riga della matrice di transizione è una permutazione delle altre righe (ossia l'entropia di riga $H(\mathbf{r}) = -\sum_y p(y \mid x) \log_2 p(y \mid x)$ è identica per ogni $x$);
   - Tutte le somme per colonna sono identiche: $\sum_{x \in \mathcal{X}} p(y \mid x) = \frac{|\mathcal{X}|}{|\mathcal{Y}|}$ per ogni $y \in \mathcal{Y}$.

#### Teorema di Capacità per Canali Debolmente Simmetrici

Per qualsiasi canale debolmente simmetrico, la capacità di informazione vale:

$$
C = \log_2 |\mathcal{Y}| - H(\mathbf{r})
$$

dove $\mathbf{r}$ indica una riga arbitraria della matrice di transizione. La capacità è raggiunta dalla distribuzione di probabilità d'ingresso uniforme:

$$
p^*(x) = \frac{1}{|\mathcal{X}|}, \quad \forall x \in \mathcal{X}
$$

#### Dimostrazione

Per l'ipotesi di permutazione delle righe, l'entropia condizionata vale per qualsiasi ingresso $x$:

$$
H(Y \mid X = x) = -\sum_{y \in \mathcal{Y}} p(y \mid x) \log_2 p(y \mid x) = H(\mathbf{r}) \implies H(Y \mid X) = H(\mathbf{r})
$$

L'informazione mutua è data da:

$$
I(X; Y) = H(Y) - H(Y \mid X) = H(Y) - H(\mathbf{r}) \le \log_2 |\mathcal{Y}| - H(\mathbf{r})
$$

Scegliendo la distribuzione uniforme all'ingresso $p(x) = 1/|\mathcal{X}|$, la distribuzione marginale di uscita è:

$$
p(y) = \sum_{x \in \mathcal{X}} p(x) p(y \mid x) = \frac{1}{|\mathcal{X}|} \sum_{x \in \mathcal{X}} p(y \mid x) = \frac{1}{|\mathcal{X}|} \left( \frac{|\mathcal{X}|}{|\mathcal{Y}|} \right) = \frac{1}{|\mathcal{Y}|}
$$

L'uscita risulta rigorosamente uniforme sull'alfabeto $\mathcal{Y}$, saturando il limite superiore $H(Y) = \log_2 |\mathcal{Y}|$ e provando la tesi.

## Il Secondo Teorema Fondamentale di Shannon (Channel Coding Theorem)

Il Teorema di Codifica di Canale di Claude Shannon (1948) costituisce la pietra miliare dell'intera teoria dell'informazione. Esso stabilisce che la capacità $C$ delimita in modo netto e non negoziabile la frontiera tra trasmissione affidabile priva di errori e collasso informativo inevitabile.

### Enunciato Globale del Teorema

Sia assegnato un canale discreto senza memoria con capacità di informazione $C = \max_{p(x)} I(X; Y)$.

1. __Parte Diretta (Achievability)__:
   Per ogni tasso di trasmissione $R < C$ e per qualsiasi margine di tolleranza $\epsilon > 0$, per $n$ sufficientemente grande esiste un codice di canale $(2^{nR}, n)$ avente probabilità massima d'errore di decodifica limitata da:

   $$
   \lambda^{(n)} = \max_{w \in \{1, \dots, 2^{nR}\}} \text{Pr}\{g(Y^n) \neq w \mid W = w\} < \epsilon
   $$

2. __Parte Inversa (Converse)__:
   Qualsiasi sequenza di codici di blocco $(2^{nR}, n)$ che tenti di operare a un tasso $R > C$ presenta una probabilità d'errore $P_e^{(n)}$ delimitata inferiormente lontano da zero per $n \to \infty$:

   $$
   P_e^{(n)} \ge 1 - \frac{C}{R} - \frac{1}{nR} \xrightarrow{n \to \infty} 1 - \frac{C}{R} > 0
   $$

   È impossibile comunicare con affidabilità arbitraria se il rate supera la capacità di canale.

### L'Intuizione Rivoluzionaria di Shannon

Prima del 1948, il paradigma classico delle telecomunicazioni assumeva che per abbattere la probabilità d'errore indotta dal rumore fosse inevitabile ripetere ciascun simbolo un numero sempre crescente di volte, facendo tendere la velocità effettiva di trasmissione a zero ($R \to 0$).

Shannon dimostrò che tale approccio è profondamente sub-ottimo. La ripetizione semplice concentra le parole su direzioni collineari; al contrario, progettando parole di codice multidimensionali di lunghezza $n$ sufficientemente grande, le sequenze possono essere disposte all'interno dello spazio $n$-dimensionale in modo tale che le rispettive "sfere di rumore" si disgiungano quasi totalmente, consentendo una trasmissione priva di errori a qualsiasi tasso positivo $R$ inferiore a $C$.

### Struttura della Dimostrazione Diretta (Random Coding e Joint AEP)

La dimostrazione ideata da Shannon non costruisce esplicitamente il codebook ottimo deterministico (compito che ha richiesto decenni di ricerca algebrica portando ai codici Turbo, LDPC e Polari), ma dimostra l'esistenza di tale codice mediante tre artifici analitici:
1. __Generazione Casuale dell'Ensemble (Random Coding)__: Le $2^{nR}$ parole di codice $X^n(w)$ vengono estratte in modo indipendente e identicamente distribuito secondo la distribuzione d'ingresso ottima $p(x) = \prod_{j=1}^n p(x_j)$.
2. __Decodifica per Tipicità Congiunta (Joint Typicality Decoding)__: Il ricevitore cerca l'unico indice $w$ tale che la coppia $(X^n(w), Y^n)$ appartenga all'insieme congiuntamente tipico $A_\epsilon^{(n)}$.
3. __Analisi di Errore tramite Joint AEP__:
   - La parola corretta $X^n(1)$ è congiuntamente tipica con $Y^n$ con probabilità che tende a 1 ($1 - \epsilon$);
   - Ciascuna delle altre $2^{nR} - 1$ parole errate è statisticamente indipendente dall'uscita $Y^n$. La probabilità che una parola indipendente cada casualmente nell'insieme congiuntamente tipico decade esponenzialmente come $2^{-n(I(X; Y) - 3\epsilon)}$.
   - Mediante lo union bound, la probabilità media d'errore sull'ensemble soddisfa:

     $$
     \mathbb{E}[P_e^{(n)}] \le \epsilon + 2^{nR} 2^{-n(I(X; Y) - 3\epsilon)} = \epsilon + 2^{-n(I(X; Y) - R - 3\epsilon)}
     $$

     Se $R < I(X; Y) - 3\epsilon$, l'esponente è negativo e il secondo termine decade a zero per $n \to \infty$.

4. __Diserbo (Expurgation)__: Poiché la media dell'ensemble è $< 2\epsilon$, esiste un codice con errore medio $< 2\epsilon$. Eliminando la metà peggiore delle parole, si ottiene un codice a errore massimo $\lambda^{(n)} < 4\epsilon$.

I passaggi algebrici completi della dimostrazione diretta sono consultabili nella sezione [[zz. Argomenti extra#Dimostrazione del Teorema di Codifica di Canale (Diretta: Random Coding e Joint AEP)|dimostrazione diretta di Shannon]].

### Struttura della Dimostrazione Inversa (Converse via Fano)

La dimostrazione dell'impossibilità di superare $C$ poggia sull'applicazione della Disuguaglianza di Fano alla stima del messaggio $W$ a partire dall'uscita $Y^n$:

$$
H(W \mid Y^n) \le 1 + P_e^{(n)} n R
$$

Sfruttando la catena di relazioni:

$$
nR = H(W) = H(W \mid Y^n) + I(W; Y^n) \le 1 + P_e^{(n)} n R + I(X^n; Y^n) \le 1 + P_e^{(n)} n R + n C
$$

Dividendo per $n$ e riordinando, si ottiene il limite inferiore invalicabile:

$$
P_e^{(n)} \ge 1 - \frac{C}{R} - \frac{1}{nR}
$$

I dettagli analitici della parte inversa sono riportati nella sezione [[zz. Argomenti extra#Dimostrazione della Parte Inversa del Teorema di Codifica di Canale (Converse via Fano)|dimostrazione della parte inversa del teorema di canale]].

## La Dualità tra Compressione Dati e Trasmissione su Canale

Esiste una profonda simmetria matematica e concettuale (dualità di Shannon) tra i due problemi cardine della teoria dell'informazione:

1. __Compressione Dati__: Il segnale emesso da una sorgente fisica contiene correlazione, memoria e disomogeneità statistica (ridondanza). Il codificatore di sorgente rimuove sistematicamente tutta la ridondanza naturale, comprimendo il messaggio fino a raggiungere l'entropia $H(X)$. La sequenza compressa risultante appare priva di struttura e indistinguibile da rumore bianco puramente casuale.
2. __Trasmissione su Canale__: Per trasmettere tale sequenza compressa attraverso un mezzo rumoroso, il codificatore di canale reintroduce una forma di ridondanza rigidamente strutturata (bit di parità, vincoli di traliccio o matrici di controllo di parità a bassa densità). Questa ridondanza geometrica allontana le parole nello spazio delle configurazioni, consentendo al decodificatore di correggere le perturbazioni introdotte dal canale.

## Il Teorema di Separazione Sorgente-Canale di Shannon

In linea di principio, si potrebbe ipotizzare che progettando congiuntamente la compressione del messaggio e la modulazione di canale (un unico super-blocco non lineare che mappa direttamente la voce o il testo nei simboli di canale) sia possibile ottenere prestazioni superiori rispetto a un'architettura modulare a stadi separati.

Il __Teorema di Separazione Sorgente-Canale__ (Shannon 1948) prova che tale ipotesi è errata: la separazione in due stadi indipendenti è __globalmente ottima__.

### Enunciato del Teorema

Sia dato un processo di sorgente stazionario ed ergodico con tasso di entropia $H(\mathcal{V})$, e sia assegnato un canale discreto senza memoria con capacità $C$.

1. Se $H(\mathcal{V}) < C$, la sorgente può essere trasmessa attraverso il canale e ricostruita con probabilità d'errore asintoticamente nulla.
2. Se $H(\mathcal{V}) > C$, è impossibile trasmettere la sorgente con probabilità d'errore arbitrariamente piccola; per qualsiasi codice congiunto, la probabilità d'errore è limitata inferiormente lontano da zero.

La dimostrazione analitica formale è presentata nella sezione [[zz. Argomenti extra#Dimostrazione del Teorema di Separazione Sorgente-Canale di Shannon|approfondimento sul teorema di separazione]].

### Importanza Ingegneristica del Principio di Separazione

Il Teorema di Separazione ha plasmato l'intera architettura dell'era digitale e delle reti di calcolatori:
- Ha consentito di separare la progettazione dei formati multimediali e dei compressori (JPEG, MP3, H.264, Deflate) dalla progettazione dei modem, delle schede Ethernet, delle reti 5G e dei sistemi Wi-Fi.
- Un ingegnere che progetta un algoritmo di compressione video deve preoccuparsi unicamente di minimizzare l'entropy rate del file, senza conoscere se il video viaggerà su fibra ottica, ponte radio satellitare o cavo coassiale.
- L'ingegnere delle telecomunicazioni deve unicamente garantire che il canale fornisca una capacità $C$ superiore al bitrate della sorgente, trasmettendo pacchetti di bit senza dover conoscere il significato semantico dei dati trasmessi.

## Capacità di Canale in Presenza di Feedback

Un ulteriore quesito teorico riguarda l'impiego del __feedback__: se il ricevitore dispone di un canale di ritorno privo di rumore attraverso il quale comunica al trasmettitore i simboli $Y$ effettivamente ricevuti negli istanti precedenti, la capacità del canale di trasmissione aumenta?

### Teorema di Shannon sulla Capacità con Feedback

Per qualsiasi canale discreto senza memoria (DMC), l'introduzione di un canale di feedback non incrementa in alcun modo la capacità di canale:

$$
C_{\text{feedback}} = C
$$

#### Dimostrazione

In presenza di feedback causale, il simbolo trasmesso all'istante $i$ può dipendere dal messaggio $W$ e da tutte le uscite di canale precedenti $Y^{i-1}$:

$$
X_i = X_i(W, Y_1, Y_2, \dots, Y_{i-1})
$$

Applicando la disuguaglianza di Fano alla stima del messaggio $W \sim \text{Uniform}\{1, \dots, 2^{nR}\}$:

$$
nR = H(W) = H(W \mid Y^n) + I(W; Y^n) \le 1 + P_e^{(n)} n R + I(W; Y^n)
$$

Sviluppiamo la mutua informazione $I(W; Y^n)$:

$$
I(W; Y^n) = H(Y^n) - H(Y^n \mid W) = \sum_{i=1}^n H(Y_i \mid Y^{i-1}) - \sum_{i=1}^n H(Y_i \mid Y^{i-1}, W)
$$

Poiché il condizionamento riduce l'entropia, $H(Y_i \mid Y^{i-1}) \le H(Y_i)$. Inoltre, per la proprietà di memoria nulla del canale, condizionatamente all'ingresso $X_i$ l'uscita $Y_i$ è statisticamente indipendente da $Y^{i-1}$ e da $W$:

$$
H(Y_i \mid Y^{i-1}, W, X_i) = H(Y_i \mid X_i)
$$

Poiché $X_i$ è una funzione deterministica di $(W, Y^{i-1})$, il condizionamento rispetto a $(Y^{i-1}, W)$ coincide con il condizionamento congiunto a $(Y^{i-1}, W, X_i)$:

$$
H(Y_i \mid Y^{i-1}, W) = H(Y_i \mid X_i)
$$

Ne deriva la disuguaglianza:

$$
I(W; Y^n) \le \sum_{i=1}^n H(Y_i) - \sum_{i=1}^n H(Y_i \mid X_i) = \sum_{i=1}^n I(X_i; Y_i) \le \sum_{i=1}^n C = n C
$$

Sostituendo nel bound di Fano:

$$
nR \le 1 + P_e^{(n)} n R + n C \implies R \le \frac{1}{n} + P_e^{(n)} R + C
$$

Facendo tendere $n \to \infty$ con $P_e^{(n)} \to 0$, si conclude che $R \le C$. Pertanto, $C_{\text{feedback}} \le C$. Poiché la trasmissione senza feedback è un caso particolare di trasmissione con feedback (in cui il trasmettitore ignora il segnale di ritorno), vale banalmente $C_{\text{feedback}} \ge C$, concludendo che $C_{\text{feedback}} = C$.

#### Ruolo Operativo del Feedback

Sebbene il feedback non alteri il valore asintotico della capacità per canali privi di memoria, esso riveste un ruolo tecnologico enorme:
1. Permette di progettare codici di canale a complessità computazionale quasi nulla (come gli schemi ARQ e le strategie di Horstein-Schalkwijk-Kailath);
2. Accelera esponenzialmente il tasso di convergenza della probabilità d'errore verso zero (aumentando la pendenza dell'esponente d'errore di affidabilità);
3. Nei canali con memoria o tempo-varianti, il feedback incrementa la capacità consentendo al trasmettitore di adattare la modulazione allo stato istantaneo del canale.

## Quadro Sinottico dei Modelli di Canale e Capacità

La tabella seguente riassume le caratteristiche analitiche, geometriche e probabilistiche dei principali canali discreti esaminati:

| Tipologia di Canale | Alfabeti $\mathcal{X}, \mathcal{Y}$ | Parametri di Rumore | Distribuzione d'Ingresso Ottima $p^*(x)$ | Formula Chiusa della Capacità $C$ | Significato Operativo e Limiti |
| :--- | :--- | :--- | :--- | :--- | :--- |
| __Canale Perfetto (Noiseless)__ | $|\mathcal{X}| = |\mathcal{Y}| = m$ | Nessun rumore ($Y = X$) | Uniforme: $p^*(x) = 1/m$ | $\log_2 m \quad \text{bit/uso}$ | Canale ideale privo di interferenza |
| __Canale a Uscite Disgiunte__ | $|\mathcal{X}| = m, \; |\mathcal{Y}| = m \cdot k$ | Rumore interno non sovrapposto | Uniforme: $p^*(x) = 1/m$ | $\log_2 m \quad \text{bit/uso}$ | Zero errori senza correzione d'errore |
| __Macchina da Scrivere Rumorosa__ | $|\mathcal{X}| = |\mathcal{Y}| = 26$ | Errore circolare: $\text{Pr} = 1/2$ | Uniforme su 13 lettere alternate | $\log_2 13 \approx 3.70 \quad \text{bit/uso}$ | Trasmissione affidabile con alfabeto dimezzato |
| __Canale Binario Simmetrico (BSC)__ | $\mathcal{X} = \mathcal{Y} = \{0, 1\}$ | Inversione bit con probabilità $q$ | Uniforme: $p^*(0) = p^*(1) = 1/2$ | $1 - H_B(q) \quad \text{bit/uso}$ | Modello universale per bit-flip non tracciati |
| __Canale Binario con Cancellazione (BEC)__ | $\mathcal{X} = \{0, 1\}, \; \mathcal{Y} = \{0, 1, e\}$ | Cancellazione con probabilità $\alpha$ | Uniforme: $p^*(0) = p^*(1) = 1/2$ | $1 - \alpha \quad \text{bit/uso}$ | Modello per reti a pacchetti con packet drop |
| __Canale Debolmente Simmetrico__ | Alfabeti generici discreti | Righe e colonne permutate | Uniforme: $p^*(x) = 1/|\mathcal{X}|$ | $\log_2 |\mathcal{Y}| - H(\mathbf{r}) \quad \text{bit/uso}$ | Generalizzazione per canali simmetrici $M$-ari |
| __Canale DMC con Feedback__ | Alfabeti del canale originario | Feedback causale privo di rumore | Identica al canale senza feedback | Identica alla capacità $C$ del DMC | Semplifica la complessità senza aumentare $C$ |
