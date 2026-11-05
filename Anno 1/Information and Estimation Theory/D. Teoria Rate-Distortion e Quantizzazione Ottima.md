# D. Teoria Rate-Distortion e Quantizzazione Ottima

La codifica di sorgente senza perdita (lossless), formalizzata nei capitoli precedenti dai teoremi di Shannon e dagli algoritmi di Huffman e Lempel-Ziv, impone che la sequenza originale di dati possa essere ricostruita con probabilità d'errore esattamente nulla. In tale paradigma, il limite invalicabile al tasso medio di compressione è rappresentato dall'entropia di Shannon della sorgente:

$$
R \ge H(X)
$$

Quando si trattano segnali fisici continui nel tempo o nell'ampiezza (quali tracce audio, immagini digitali, flussi video, segnali radar e telemetrie robotiche ad alta frequenza), una rappresentazione digitale esatta richiederebbe un'accuratezza infinita ($\Delta \to 0$), determinando la divergenza dell'entropia discreta a infinito ($H(X^\Delta) \to \infty$). Di conseguenza, la fedeltà perfetta implicherebbe una capacità di trasmissione o uno spazio di memoria illimitati.

La __compressione con perdita__ (lossy compression) risolve tale limite strutturale rilassando il vincolo di ricostruzione deterministica: si accetta una discrepanza controllata o distorsione tra la sorgente originale $X$ e la sua approssimazione digitale $\hat{X}$, al fine di conseguire un drastico abbattimento del numero di bit necessari. 

La __Teoria Rate-Distortion__, introdotta da Claude Shannon nel suo saggio fondamentale del 1959 (*Coding Theorems for a Discrete Source in the Presence of a Fidelity Criterion*), stabilisce il limite teorico ultimo e insuperabile tra:
- il __tasso di codifica__ $R$ (misurato in bit per simbolo o bit al secondo);
- la __distorsione media__ tollerata $D$ (misurata mediante un opportuno criterio di fedeltà, quale l'errore quadratico medio).

La teoria fornisce sia le basi analitiche per la progettazione di quantizzatori scalari e vettoriali ottimi (algoritmi di Lloyd-Max e Linde-Buzo-Gray), sia i criteri variazionali per l'allocazione ottimale dei bit nei sistemi di codifica per trasformata (Reverse Water-Filling).

## Quantizzazione Scalare Ottima di Lloyd-Max

Il dispositivo fondamentale alla base di qualsiasi sistema di conversione da grandezze continue ad un formato numerico discreto a tasso finito è il __quantizzatore scalare__.

Si consideri una variabile aleatoria continua $X \in \mathbb{R}$ caratterizzata da una funzione di densità di probabilità $f(x)$. Un quantizzatore scalare a $K$ livelli è un'applicazione deterministica:

$$
Q: \mathbb{R} \to \{y_1, y_2, \dots, y_K\}
$$

che opera partizionando l'asse reale in $K$ intervalli disgiunti (celle di quantizzazione) mediante $K+1$ soglie di decisione ordinate:

$$
-\infty = b_0 < b_1 < b_2 < \dots < b_{K-1} < b_K = +\infty
$$

Tale partizione assegna a ciascun intervallo $\mathcal{R}_i = (b_{i-1}, b_i]$ un unico livello di ricostruzione discreto (codevalue o centroide) $y_i \in \mathbb{R}$:

$$
Q(x) = y_i \quad \text{se } x \in \mathcal{R}_i = (b_{i-1}, b_i]
$$

Adottando come misura del degrado l'errore quadratico medio (Mean Squared Error, MSE), la distorsione totale prodotta dal quantizzatore è espressa dal funzionale:

$$
D = \mathbb{E}[(X - Q(X))^2] = \sum_{i=1}^K \int_{b_{i-1}}^{b_i} (x - y_i)^2 f(x) \mathrm{d}x
$$

Il problema della quantizzazione scalare ottima consiste nell'individuare simultaneamente le $K-1$ soglie interne $\{b_i\}_{i=1}^{K-1}$ e i $K$ livelli di ricostruzione $\{y_i\}_{i=1}^K$ che minimizzano la distorsione quadratica $D$.

### Le Condizioni di Ottimalità di Lloyd-Max

Derivando il funzionale di distorsione $D$ rispetto alle variabili decisionali e imponendo l'annullamento dei gradienti, Stuart Lloyd (1957, pubblicato nel 1982) e Joel Max (1960) hanno dimostrato che qualsiasi quantizzatore ottimo deve soddisfare simultaneamente due proprietà necessarie:

1. __Condizione del Vicino Più Prossimo (Nearest-Neighbor / Partizione di Voronoi)__:
   Derivando $D$ rispetto alla generica soglia interna $b_i$:

$$
   \frac{\partial D}{\partial b_i} = (b_i - y_i)^2 f(b_i) - (b_i - y_{i+1})^2 f(b_i) = 0
$$

   Assumendo che la densità di probabilità sia non nulla sulla soglia ($f(b_i) > 0$):

$$
   (b_i - y_i)^2 = (b_i - y_{i+1})^2 \implies b_i - y_i = -(b_i - y_{i+1})
$$

   da cui si ricava la regola fondamentale:

$$
   b_i = \frac{y_i + y_{i+1}}{2}, \quad i = 1, 2, \dots, K-1
$$

   Fissato l'insieme dei livelli di ricostruzione $\{y_i\}$, ciascuna soglia di decisione ottima coincide esattamente con il punto medio tra due livelli adiacenti. Ciascuna regione $\mathcal{R}_i$ costituisce una cella di Voronoi unidimensionale in cui ogni campione $x$ è associato al livello $y_i$ geometricamente più vicino.

2. __Condizione del Centroide (Centroid Condition / Stima MMSE)__:
   Derivando $D$ rispetto al generico livello di ricostruzione $y_i$:

$$
   \frac{\partial D}{\partial y_i} = -2 \int_{b_{i-1}}^{b_i} (x - y_i) f(x) \mathrm{d}x = 0 \implies \int_{b_{i-1}}^{b_i} x f(x) \mathrm{d}x = y_i \int_{b_{i-1}}^{b_i} f(x) \mathrm{d}x
$$

   da cui discende:

$$
   y_i = \frac{\int_{b_{i-1}}^{b_i} x f(x) \mathrm{d}x}{\int_{b_{i-1}}^{b_i} f(x) \mathrm{d}x} = \mathbb{E}[X \mid X \in \mathcal{R}_i], \quad i = 1, 2, \dots, K
$$

   Fissata la partizione dello spazio in regioni $\{\mathcal{R}_i\}$, ciascun livello di ricostruzione ottimo coincide con il __baricentro probabilistico__ o valore atteso condizionato di $X$ all'interno della rispettiva cella, in perfetta risonanza con il principio dello stimatore bayesiano MMSE.

### Algoritmo Iterativo di Lloyd-Max

Poiché le due equazioni di ottimalità sono mutuamente accoppiate (le soglie ottime dipendono dai livelli, i quali dipendono a loro volta dalle soglie), la soluzione analitica esplicita non è calcolabile in forma chiusa per distribuzioni generiche. L'__algoritmo di Lloyd-Max__ risolve il sistema tramite una procedura iterativa ad alternanza:

1. __Inizializzazione__: Si sceglie un insieme arbitrario di $K$ livelli di ricostruzione distinti $\{y_i^{(0)}\}$.
2. __Passo di Partizione__: Si calcolano le nuove soglie di decisione come punti medi tra i livelli correnti:

$$
   b_i^{(k)} = \frac{y_i^{(k)} + y_{i+1}^{(k)}}{2}
$$

3. __Passo del Centroide__: Si ricalcolano i livelli come baricentri condizionati sulle nuove regioni:

$$
   y_i^{(k+1)} = \mathbb{E}\left[ X \mid X \in (b_{i-1}^{(k)}, b_i^{(k)}] \right]
$$

4. __Verifica di Arresto__: Si calcola la distorsione media $D^{(k)}$. Poiché ogni singolo semipasso non può che ridurre (o lasciare invariata) la distorsione, la successione $\{D^{(k)}\}$ è monotona non crescente e converge al minimo (globale per densità log-concave come la gaussiana).

### Esempio Analitico: Quantizzatore a 1 Bit per Sorgente Gaussiana

Si consideri una sorgente gaussiana a media nulla $X \sim \mathcal{N}(0, \sigma^2)$ quantizzata con $R = 1$ bit per campione, disponendo quindi di $K = 2^1 = 2$ livelli di ricostruzione ($y_1 < y_2$).

Per ragioni di simmetria rispetto all'origine:
- La soglia di decisione ottima è $b_1 = 0$, con regioni $\mathcal{R}_1 = (-\infty, 0]$ e $\mathcal{R}_2 = (0, +\infty)$.
- I livelli di ricostruzione sono opposti: $y_1 = -y_2$.

Calcoliamo il livello positivo $y_2$ tramite la condizione del centroide:

$$
y_2 = \mathbb{E}[X \mid X > 0] = \frac{\int_0^{+\infty} x \frac{1}{\sqrt{2\pi\sigma^2}} e^{-\frac{x^2}{2\sigma^2}} \mathrm{d}x}{\text{Pr}\{X > 0\}} = \frac{\frac{1}{\sqrt{2\pi\sigma^2}} \left[ -\sigma^2 e^{-\frac{x^2}{2\sigma^2}} \right]_0^{+\infty}}{\frac{1}{2}}
$$

Sviluppando i termini:

$$
y_2 = 2 \cdot \frac{\sigma^2}{\sqrt{2\pi\sigma^2}} (0 - (-1)) = 2 \cdot \frac{\sigma}{\sqrt{2\pi}} = \sqrt{\frac{2}{\pi}} \sigma \approx 0.7979 \sigma
$$

I due livelli ottimi di ricostruzione sono:

$$
y_1 = -\sqrt{\frac{2}{\pi}}\sigma, \quad y_2 = +\sqrt{\frac{2}{\pi}}\sigma
$$

Calcoliamo la distorsione quadratica media risultante:

$$
D = \mathbb{E}[(X - Q(X))^2] = \mathbb{E}[X^2] - 2\mathbb{E}[X Q(X)] + \mathbb{E}[Q(X)^2]
$$

Poiché $Q(X)^2 = y_2^2 = \frac{2}{\pi}\sigma^2$ con probabilità 1, e:

$$
\mathbb{E}[X Q(X)] = \int_{-\infty}^0 x y_1 f(x)\mathrm{d}x + \int_0^{+\infty} x y_2 f(x)\mathrm{d}x = y_2 \int_0^{+\infty} x f(x)\mathrm{d}x - y_1 \int_{-\infty}^0 (-x) f(x)\mathrm{d}x = 2 y_2 \left( \frac{1}{2} y_2 \right) = y_2^2
$$

La distorsione minima vale:

$$
D = \sigma^2 - 2 y_2^2 + y_2^2 = \sigma^2 - y_2^2 = \sigma^2 - \frac{2}{\pi}\sigma^2 = \sigma^2 \left( 1 - \frac{2}{\pi} \right) \approx 0.3634 \sigma^2
$$

Il rapporto segnale-rumore di quantizzazione (Signal-to-Quantization-Noise Ratio, SQNR) espresso in decibel è:

$$
\text{SQNR} = 10 \log_{10}\left( \frac{\sigma^2}{D} \right) = 10 \log_{10}\left( \frac{1}{1 - 2/\pi} \right) \approx 10 \log_{10}(2.752) \approx 4.40 \quad \text{dB}
$$

### Esempio Numerico: Quantizzatore a 2 Bit per Sorgente Gaussiana

Implementando l'algoritmo di Lloyd-Max per $K = 4$ livelli ($R = 2$ bit) su una gaussiana standard $X \sim \mathcal{N}(0, 1)$, l'iterazione numerica converge ai seguenti valori ottimi simmetrici:
- Soglie di decisione: $b_1 = -0.9816$, $b_2 = 0.0000$, $b_3 = +0.9816$.
- Livelli di ricostruzione: $y_1 = -1.5104$, $y_2 = -0.4528$, $y_3 = +0.4528$, $y_4 = +1.5104$.
- Distorsione quadratica media: $D \approx 0.1175 \sigma^2$.
- Rapporto segnale-rumore: $\text{SQNR} \approx 9.30$ dB.

Rispetto a un quantizzatore a passo uniforme con 4 livelli (il quale produce un SQNR di circa $7.84$ dB), il quantizzatore ottimo di Lloyd-Max garantisce un guadagno di fedeltà pari a $1.46$ dB senza alcun incremento nel tasso di trasmissione.

## Fondamenti della Teoria Rate-Distortion di Shannon

Nonostante la sua eleganza, il quantizzatore scalare di Lloyd-Max presenta un limite intrinseco: opera campione per campione in modo separato. La Teoria dell'Informazione dimostra che è possibile conseguire prestazioni di gran lunga superiori codificando blocchi o vettori di campioni congiunti.

Per stabilire il confine teorico ultimo della compressione lossy, Shannon definì formalmente il modello analitico di una sorgente con criterio di fedeltà.

### Misure di Distorsione

Sia $\mathcal{X}$ l'alfabeto dei simboli generati dalla sorgente e $\hat{\mathcal{X}}$ l'alfabeto dei simboli di ricostruzione. Una __funzione di distorsione__ (o metrica di costo) per singolo simbolo è un'applicazione non negativa:

$$
d: \mathcal{X} \times \hat{\mathcal{X}} \to \mathbb{R}^+, \quad (x, \hat{x}) \mapsto d(x, \hat{x}) \ge 0
$$

che quantifica il costo soggettivo o oggettivo subito dal destinatario quando il simbolo reale $x$ viene riprodotto mediante $\hat{x}$. Le due metriche canoniche della teoria sono:

1. __Distorsione di Hamming (alfabeti discreti)__:

$$
   d_H(x, \hat{x}) = \begin{cases} 0 & \text{se } x = \hat{x} \\ 1 & \text{se } x \neq \hat{x} \end{cases}
$$

   La distorsione media attesa $\mathbb{E}[d_H(X, \hat{X})]$ coincide esattamente con la probabilità di errore di simbolo $P_e = \text{Pr}\{X \neq \hat{X}\}$.

2. __Distorsione Quadratica (alfabeti continui)__:

$$
   d(x, \hat{x}) = (x - \hat{x})^2
$$

   La distorsione media coincide con l'errore quadratico medio $\mathbb{E}[(X - \hat{X})^2]$, misura standard nell'elaborazione dei segnali audio, video e nei problemi di stima.

Estendendo il criterio a blocchi vettoriali di $n$ campioni $\mathbf{x} = (x_1, \dots, x_n) \in \mathcal{X}^n$ e $\hat{\mathbf{x}} = (\hat{x}_1, \dots, \hat{x}_n) \in \hat{\mathcal{X}}^n$, la distorsione su sequenze è definita dalla media aritmetica delle distorsioni sulle singole componenti (distorsione additiva senza memoria):

$$
\bar{d}(\mathbf{x}, \hat{\mathbf{x}}) = \frac{1}{n} \sum_{i=1}^n d(x_i, \hat{x}_i)
$$

### Codici a Blocchi Rate-Distortion e Regione Ammissibile

Un codice Rate-Distortion $(2^{nR}, n)$ è costituito da:
1. Una funzione di codifica (encoder) che mappa ciascuna sequenza di sorgente $\mathbf{x} \in \mathcal{X}^n$ in un indice binario compreso in un vocabolario di $M = \lceil 2^{nR} \rceil$ messaggi:

$$
   f_n: \mathcal{X}^n \to \{1, 2, \dots, M\}
$$

2. Una funzione di decodifica (decoder) che mappa ciascun indice in una parola di codice di ricostruzione $\hat{\mathbf{x}} \in \hat{\mathcal{X}}^n$:

$$
   g_n: \{1, 2, \dots, M\} \to \hat{\mathcal{X}}^n
$$

Il tasso di trasmissione del codice è $R = \frac{\log_2 M}{n}$ bit per simbolo di sorgente.

Una coppia tasso-distorsione $(R, D)$ è detta __ammissibile__ (achievable) se esiste una successione di codici $(2^{nR}, n)$ tale che la distorsione media asintotica soddisfa:

$$
\lim_{n \to \infty} \mathbb{E}\left[ \bar{d}(X^n, g_n(f_n(X^n))) \right] \le D
$$

L'insieme di tutte le coppie ammissibili $(R, D)$ definisce la __Regione Rate-Distortion__ dello spazio cartesiano. La frontiera inferiore di tale regione è descritta dalla __funzione Rate-Distortion operativa__ $R(D)$, che specifica il minimo tasso in bit necessario per comprimere la sorgente garantendo una distorsione media non superiore a $D$.

![[slide_20_rate_distortion_curve.png|center mid]]

### Funzione di Informazione Rate-Distortion e Teorema di Shannon

Shannon introdusse la definizione puramente probabilistica e computabile della __funzione di informazione Rate-Distortion__ per una sorgente stazionaria senza memoria distribuita secondo $p(x)$:

$$
R(D) = \min_{p(\hat{x} \mid x): \, \mathbb{E}[d(X, \hat{X})] \le D} I(X; \hat{X})
$$

dove la minimizzazione è condotta su tutte le matrici di transizione stocastiche condizionate $p(\hat{x} \mid x)$ (canali test) che rispettano il vincolo di distorsione:

$$
\mathbb{E}[d(X, \hat{X})] = \sum_{x \in \mathcal{X}} \sum_{\hat{x} \in \hat{\mathcal{X}}} p(x) p(\hat{x} \mid x) d(x, \hat{x}) \le D
$$

Il cardine teorico della compressione con perdita è il __Teorema Fondamentale di Rate-Distortion di Shannon__ (1959):
1. __Parte Diretta (Raggiungibilità)__: Per qualsiasi tasso $R > R(D)$, esiste una sequenza di codici a blocchi di dimensione $n$ sufficientemente grande in grado di ricostruire la sorgente con distorsione media inferiore o uguale a $D$.
2. __Parte Inversa (Converse)__: Nessun codice, indipendentemente dalla lunghezza del blocco $n$ o dalla complessità dell'algoritmo di compressione, potrà mai conseguire una distorsione media $\le D$ operando a un tasso $R < R(D)$.

Pertanto, la funzione informativa coincide esattamente con il limite operativo fisico del sistema.

## Funzione Rate-Distortion per la Sorgente Binaria

Si consideri una sorgente discreta binaria memoryless che genera simboli $X \in \{0, 1\}$ secondo una legge di Bernoulli con parametro di sbilanciamento $p$:

$$
\text{Pr}\{X = 1\} = p, \quad \text{Pr}\{X = 0\} = 1 - p
$$

Assumendo senza perdita di generalità $p \le \frac{1}{2}$, e adottando la metrica di errore di Hamming $d_H(x, \hat{x})$.

### Teorema della Funzione $R(D)$ Binaria

La funzione Rate-Distortion per una sorgente binaria $\text{Bern}(p)$ sotto distorsione di Hamming vale:

$$
R(D) = \begin{cases} H_B(p) - H_B(D) & \text{se } 0 \le D \le p \\ 0 & \text{se } D > p \end{cases} \quad \text{bit/simbolo}
$$

dove $H_B(q) = -q \log_2 q - (1-q)\log_2(1-q)$ è la funzione di entropia binaria.

__Dimostrazione analitica__:
Sviluppiamo l'informazione mutua per qualsiasi canale test $p(\hat{x} \mid x)$:

$$
I(X; \hat{X}) = H(X) - H(X \mid \hat{X}) = H_B(p) - H(X \oplus \hat{X} \mid \hat{X})
$$

dove $\oplus$ indica la somma modulo 2 (operatore XOR). Poiché il condizionamento non può che ridurre l'entropia:

$$
H(X \oplus \hat{X} \mid \hat{X}) \le H(X \oplus \hat{X})
$$

La variabile casuale binaria $E = X \oplus \hat{X}$ assume valore 1 quando si verifica un errore ($X \neq \hat{X}$) e valore 0 quando la ricostruzione è esatta. La probabilità media di errore è vincolata da:

$$
\text{Pr}\{E = 1\} = \mathbb{E}[d_H(X, \hat{X})] \le D
$$

Essendo la funzione di entropia binaria $H_B(\cdot)$ monotona crescente nell'intervallo $[0, 1/2]$ per $D \le p \le 1/2$:

$$
H(X \oplus \hat{X}) = H_B(\text{Pr}\{E = 1\}) \le H_B(D)
$$

Combinando le disuguaglianze:

$$
I(X; \hat{X}) \ge H_B(p) - H_B(D)
$$

L'uguaglianza è raggiunta costruendo il canale test inverso in cui $X = \hat{X} \oplus Z$, con $Z \sim \text{Bern}(D)$ indipendente da $\hat{X}$, e scegliendo $\hat{X} \sim \text{Bern}\left(\frac{p-D}{1-2D}\right)$. Se infine $D \ge p$, ponendo deterministicamente $\hat{X} = 0$, la distorsione media è $\text{Pr}\{X = 1\} = p \le D$, richiedendo $R(D) = 0$ bit.

### Esempio Applicativo: Mappe di Occupazione per Robotica Mobile

Nella navigazione autonoma di robot mobili (ad esempio, un robot aspirapolvere o un veicolo a guida autonoma AGV), l'ambiente di lavoro è discretizzato in una griglia di occupazione bidimensionale (Occupancy Grid). Ciascuna cella della griglia è modellata come una variabile binaria: $X = 1$ indica la presenza di un ostacolo, $X = 0$ indica spazio libero.

In un tipico ambiente interno, la densità di ostacoli è pari al $30\%$ ($p = 0.30$). La trasmissione della mappa completa senza errori richiederebbe:

$$
H_B(0.30) = -0.30 \log_2(0.30) - 0.70 \log_2(0.70) \approx 0.8813 \quad \text{bit/cella}
$$

Se l'algoritmo di pianificazione delle traiettorie tollera un tasso d'errore di classificazione delle celle pari al $10\%$ ($D = 0.10$):

$$
H_B(0.10) = -0.10 \log_2(0.10) - 0.90 \log_2(0.90) \approx 0.4690 \quad \text{bit/cella}
$$

Il tasso teorico minimo di trasmissione crolla a:

$$
R(0.10) = H_B(0.30) - H_B(0.10) = 0.8813 - 0.4690 = 0.4123 \quad \text{bit/cella}
$$

Accettando una distorsione del $10\%$, il robot può dimezzare il consumo di banda radio sul canale wireless, conseguendo un risparmio trasmissivo netto del $53.2\%$.

## Funzione Rate-Distortion per la Sorgente Gaussiana

Il risultato cardine per l'elaborazione dei segnali continui è la caratterizzazione della funzione Rate-Distortion di una sorgente normale sotto distorsione quadratica.

### Teorema di Shannon per la Sorgente Gaussiana

Sia $X \sim \mathcal{N}(0, \sigma^2)$ una variabile continua gaussiana con varianza $\sigma^2$ e misura di distorsione $d(x, \hat{x}) = (x - \hat{x})^2$. La funzione Rate-Distortion è:

$$
R(D) = \begin{cases} \frac{1}{2} \log_2 \left( \frac{\sigma^2}{D} \right) & \text{se } 0 \le D \le \sigma^2 \\ 0 & \text{se } D > \sigma^2 \end{cases} \quad \text{bit/campione}
$$

e la corrispondente funzione di distorsione in funzione del rate $D(R)$ è:

$$
D(R) = \sigma^2 2^{-2R}
$$

La dimostrazione analitica rigorosa, articolata nella delimitazione inferiore dell'entropia differenziale $h(X - \hat{X})$ e nella costruzione del canale test inverso gaussiano $X = \hat{X} + Z$ con $Z \sim \mathcal{N}(0, D)$, è esposta integralmente in [[zz. Argomenti extra#Teorema di Rate-Distortion per la Sorgente Gaussiana con Distorsione Quadratica]].

### La Regola dei 6 dB per Bit

La formulazione $D(R) = \sigma^2 2^{-2R}$ rivela una legge ingegneristica universale:
Esprimendo il rapporto segnale-rumore di distorsione (SDR) in decibel in funzione del tasso di compressione $R$:

$$
\text{SDR}_{\text{dB}} = 10 \log_{10}\left( \frac{\sigma^2}{D(R)} \right) = 10 \log_{10}(2^{2R}) = 2R \cdot 10\log_{10}(2) \approx 6.02 \cdot R \quad \text{dB}
$$

__Regola fondamentale dei 6 dB/bit__: Ciascun bit supplementare allocato per campione nella codifica con perdita di una sorgente continua dimezza la deviazione standard dell'errore di quantizzazione, riducendo la distorsione quadratica di un fattore 4 e incrementando la qualità della ricostruzione esattamente di circa $6.02$ dB.

### Esempio Applicativo: Telemetria Sensoristica su Reti LoRaWAN

Si consideri un nodo sensore a basso consumo in ambito Internet of Things (IoT) o monitoraggio strutturale, connesso tramite tecnologia radio a lungo raggio LoRaWAN. Il sensore campiona una vibrazione meccanica modellata come una gaussiana $\mathcal{N}(0, \sigma^2)$.

A causa delle severe limitazioni di duty-cycle e throughput della rete LoRa, il sistema deve operare a bitrate strettamente ridotti:
- A $R = 1$ bit/campione: il limite di Shannon impone una distorsione minima $D = \sigma^2 / 4$, fornendo uno $\text{SDR} = 6.02$ dB (a fronte dei $4.40$ dB ottenuti dal quantizzatore scalare di Lloyd-Max: il codice vettoriale ideale guadagna $1.62$ dB a parità di rate).
- A $R = 2$ bit/campione: la distorsione scende a $D = \sigma^2 / 16$, raggiungendo uno $\text{SDR} = 12.04$ dB (rispetto ai $9.30$ dB di Lloyd-Max, con un vantaggio informativo di $2.74$ dB).

## Quantizzazione Vettoriale (VQ) vs Quantizzazione Scalare (SQ)

Il divario prestazionale tra il limite teorico di Shannon $R(D)$ e le curve conseguite dal quantizzatore scalare di Lloyd-Max dimostra che operare campione per campione è intrinsecamente sub-ottimo. Per colmare tale scarto si ricorre alla __Quantizzazione Vettoriale__ (Vector Quantization, VQ).

In un quantizzatore vettoriale di dimensione $n$, i campioni della sorgente vengono raggruppati in blocchi vettoriali $\mathbf{X} = (X_1, \dots, X_n)^T \in \mathbb{R}^n$, e lo spazio euclideo multidimensionale viene partizionato direttamente in celle di Voronoi $n$-dimensionali, associando a ciascuna cella una parola di codice vettoriale (codeword) $\mathbf{y}_j \in \mathbb{R}^n$.

Come formalizzato da Lookabaugh e Gray (1989), la superiorità della quantizzazione vettoriale rispetto alla quantizzazione scalare deriva da tre fattori distinti:

1. __Guadagno di Memoria (Memory/Correlation Gain)__:
   Se i campioni consecutivi del segnale sono correlati o statisticamente dipendenti, la loro densità di probabilità congiunta si concentra lungo iper-ellissoidi orientati. La quantizzazione scalare, partizionando lo spazio mediante una griglia cartesiana rigida di ipercubi, alloca un numero enorme di celle in regioni a probabilità pressoché nulla. La quantizzazione vettoriale adatta la geometria del codebook distribuendo i centroidi esclusivamente dove la densità congiunta è densa.

2. __Guadagno di Spazio/Forma (Shape Gain)__:
   Anche per sorgenti perfettamente i.i.d. (prive di memoria e incorrelate), la quantizzazione vettoriale risulta strettamente superiore alla quantizzazione scalare. Le celle cartesiane scalari hanno forma di ipercubi. Nello spazio euclideo, un ipercubo è una forma inefficiente per contenere un volume a parità di momento d'inerzia: gli spigoli dell'ipercubo si estendono lontano dal centroide, aumentando l'errore quadratico medio per i punti periferici. Le celle della quantizzazione vettoriale assumono invece conformazioni sferoidali o politopiche regolari.

3. __Guadagno di Riempimento dello Spazio (Space-Filling Gain)__:
   Nello spazio bidimensionale $\mathbb{R}^2$, il reticolo che garantisce la tassellazione a minimo momento quadratico d'inerzia normalizzato è il __reticolo esagonale__ $A_2$:

$$
   G(A_2) = \frac{5}{36\sqrt{3}} \approx 0.080188
$$

   mentre il reticolo cubico cartesiano $\mathbb{Z}^2$ (prodotto di quantizzatori scalari) ha un coefficiente pari a:

$$
   G(\mathbb{Z}^2) = \frac{1}{12} \approx 0.083333
$$

   Il reticolo esagonale produce un guadagno immediato di:

$$
   \Delta \text{SNR} = 10 \log_{10}\left( \frac{0.083333}{0.080188} \right) \approx 0.169 \quad \text{dB}
$$

   Al crescere della dimensione $n \to \infty$, il teorema di Zador dimostra che il guadagno di forma e riempimento satura asintoticamente a:

$$
   \Delta \text{SNR}_{\text{max}} = 10 \log_{10}\left( \frac{\pi e}{6} \right) \approx 1.53 \quad \text{dB}
$$

![[slide_41_lbg_vector_quantization.png|center mid]]

## L'Algoritmo di Linde-Buzo-Gray (LBG 1980)

La progettazione analitica di un quantizzatore vettoriale ottimo imporrebbe il calcolo di integrali multipli di volume su domini di integrazione complessi e non lineari in $\mathbb{R}^n$, operazione analiticamente e computazionalmente impossibile per dimensioni elevate.

Nel 1980, Yoseph Linde, Andrés Buzo e Robert M. Gray pubblicarono una pietra miliare della codifica numerica (*An Algorithm for Vector Quantizer Design*), introducendo l'__algoritmo LBG__, che consente di sintetizzare un codebook vettoriale ottimo operando direttamente su un insieme empirico di vettori di addestramento (Training Set), senza alcuna necessità di conoscere la PDF analitica della sorgente.

### Formulazione del Problema di Ottimizzazione Empirica

Sia dato un insieme di addestramento composto da $N$ vettori continui $n$-dimensionali rappresentativi della sorgente:

$$
\mathcal{T} = \{ \mathbf{x}_1, \mathbf{x}_2, \dots, \mathbf{x}_N \}, \quad \mathbf{x}_k \in \mathbb{R}^n
$$

Si desidera progettare un codebook costituito da $K$ vettori di ricostruzione $\mathcal{C} = \{ \mathbf{y}_1, \mathbf{y}_2, \dots, \mathbf{y}_K \}$ in modo da minimizzare la distorsione empirica media calcolata sul dataset:

$$
J = \frac{1}{N} \sum_{k=1}^N \min_{1 \le j \le K} \|\mathbf{x}_k - \mathbf{y}_j\|^2
$$

### I Due Passi Alternati dell'Algoritmo LBG

L'algoritmo LBG generalizza la dinamica a due passi di Lloyd-Max agli spazi vettoriali empirici (rappresentando l'analogo computazionale dell'algoritmo di clustering $k$-means per l'ingegneria dell'informazione):

1. __Passo di Partizione dei Cluster (Voronoi Partition)__:
   Dato il codebook corrente $\{\mathbf{y}_j\}$, si assegna ciascun vettore $\mathbf{x}_k \in \mathcal{T}$ al centroide più vicino secondo la distanza euclidea minima, partizionando l'insieme di addestramento in $K$ insiemi disgiunti $\mathcal{S}_1, \dots, \mathcal{S}_K$:

$$
   \mathcal{S}_j = \left\{ \mathbf{x} \in \mathcal{T} : \|\mathbf{x} - \mathbf{y}_j\|^2 \le \|\mathbf{x} - \mathbf{y}_i\|^2 \quad \forall i \neq j \right\}
$$

2. __Passo di Aggiornamento dei Centroidi (Centroid Update)__:
   Fissata la partizione $\{\mathcal{S}_j\}$, ciascuna parola di codice viene aggiornata calcolando il centroide empirico (la media aritmetica vettoriale) dei soli campioni appartenenti al cluster:

$$
   \mathbf{y}_j = \frac{1}{|\mathcal{S}_j|} \sum_{\mathbf{x} \in \mathcal{S}_j} \mathbf{x}
$$

Ciascuna iterazione riduce monotonicamente la distorsione media $J$. Il ciclo viene arrestato quando il decremento relativo di distorsione scende al di sotto di una tolleranza prefissata $\frac{J^{(k-1)} - J^{(k)}}{J^{(k)}} < \epsilon$.

### Inizializzazione mediante Splitting del Codebook

Per evitare di incorrere in minimi locali sfavorevoli, l'algoritmo LBG adotta una tecnica ricorsiva di __sdoppiamento dei centroidi__ (Codebook Splitting) per progettare codebook la cui cardinalità è una potenza di due ($K = 2^m$):
1. Si inizia calcolando il centroide globale unico dell'intero dataset:

$$
   \mathbf{y}_1^{(0)} = \frac{1}{N} \sum_{k=1}^N \mathbf{x}_k
$$

2. Si sdoppia ciascun centroide esistente $\mathbf{y}_j$ lungo un vettore di perturbazione casuale $\boldsymbol{\epsilon}$:

$$
   \mathbf{y}_j^+ = \mathbf{y}_j + \boldsymbol{\epsilon}, \quad \mathbf{y}_j^- = \mathbf{y}_j - \boldsymbol{\epsilon}
$$

   raddoppiando istantaneamente il numero di vettori del codebook ($1 \to 2 \to 4 \to 8 \dots \to K$).
3. Si esegue l'alternanza LBG a ciascun livello di sdoppiamento fino a convergenza prima di procedere al livello successivo.

### Evidenza Sperimentale su Dati Gaussiani Correlati

L'efficacia dell'algoritmo LBG emerge nitidamente comprimendo una sorgente bivariata gaussiana fortemente correlata ($\rho = 0.8$) a un tasso complessivo di 6 bit/vettore ($K = 64$ centroidi):
- __Quantizzazione Scalare Indipendente__: Quantizzando separatamente le due coordinate con 3 bit ciascuna (griglia cartesiana uniforme $8 \times 8$), l'errore quadratico medio risultante è pari a $D_{\text{scalar}} = 0.0345$.
- __Quantizzazione Vettoriale LBG__: L'algoritmo LBG adatta l'orientamento delle 64 parole di codice disponendole densamente lungo l'asse principale dell'ellisse di covarianza, abbattendo l'errore quadratico medio a $D_{\text{vector}} = 0.0174$.

A parità identica di bitrate di trasmissione (6 bit per coppia di campioni), la quantizzazione vettoriale LBG dimezza esattamente la distorsione, conseguendo un guadagno netto di $3.0$ dB.

## Sorgenti Gaussiane Parallele e Principio di Reverse Water-Filling

Nelle applicazioni avanzate di elaborazione di immagini e suoni, i segnali sono composti da un insieme di componenti spettrali o canali paralleli indipendenti con varianze differenti (come i coefficienti delle trasformate DCT, Wavelet o KLT).

Si consideri un vettore di $m$ sorgenti gaussiane continue mutuamente indipendenti:

$$
X_i \sim \mathcal{N}(0, \sigma_i^2), \quad i = 1, 2, \dots, m
$$

ordinate in ordine non crescente di varianza $\sigma_1^2 \ge \sigma_2^2 \ge \dots \ge \sigma_m^2$. Si assegni al codificatore un budget di distorsione quadratica totale pari a $D$, ripartito tra le singole componenti in modo tale che $\sum_{i=1}^m D_i = D$.

![[slide_46_reverse_water_filling.png|center mid]]

La soluzione ottima del problema variazionale vincolato conduce al celebre principio di __Reverse Water-Filling__ (riempimento d'acqua inverso), la cui dimostrazione basata sui moltiplicatori di Lagrange e sulle condizioni di Karush-Kuhn-Tucker è illustrata in [[zz. Argomenti extra#Derivazione Rigorosa della Soluzione di Reverse Water-Filling per Sorgenti Gaussiane Parallele]].

### La Legge di Allocazione della Distorsione e del Rate

Fissato il budget di distorsione totale $D$, la distorsione ottima $D_i$ allocata alla generica componente $i$-esima è data da:

$$
D_i = \min(\lambda, \sigma_i^2) = \begin{cases} \lambda & \text{se } \sigma_i^2 > \lambda \\ \sigma_i^2 & \text{se } \sigma_i^2 \le \lambda \end{cases}
$$

dove il parametro costante $\lambda$ (livello dell'acqua o soglia di taglio) è determinato univocamente dalla condizione di bilancio:

$$
\sum_{i=1}^m \min(\lambda, \sigma_i^2) = D
$$

Il tasso di codifica (rate in bit) assegnato alla componente $i$ vale conseguentemente:

$$
R_i = \max\left( 0, \, \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) \right) = \begin{cases} \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) & \text{se } \sigma_i^2 > \lambda \\ 0 & \text{se } \sigma_i^2 \le \lambda \end{cases}
$$

e il tasso complessivo per l'intero blocco di sorgenti è:

$$
R(D) = \sum_{i=1}^m R_i = \sum_{i=1}^m \max\left( 0, \, \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) \right)
$$

### Interpretazione Fisica e Connessione con la Codifica per Trasformata

La denominazione *Reverse Water-Filling* esprime la dinamica geometrica del processo di quantizzazione:
1. Si visualizza un recipiente a canne d'organo in cui ogni colonna ha un'altezza pari alla varianza $\sigma_i^2$ della rispettiva componente.
2. Si versa "acqua" (che rappresenta la distorsione totale tollerata $D$) fino a raggiungere una quota uniforme pari a $\lambda$.
3. __Sorgenti dominanti ad elevata varianza ($\sigma_i^2 > \lambda$)__: La distorsione allocata è plafonata al valore massimo $\lambda$. A queste componenti viene assegnato un rate $R_i > 0$ proporzionale alla loro energia eccedente, investendo più bit per proteggere le componenti di segnale più significative.
4. __Sorgenti deboli a bassa varianza ($\sigma_i^2 \le \lambda$)__: Il livello dell'acqua supera l'altezza della colonna. La distorsione coincide con la varianza stessa ($D_i = \sigma_i^2$) e il rate assegnato è nullo ($R_i = 0$). Il codificatore scarta completamente queste componenti, approssimandole con zero ($\hat{X}_i = 0$).

Questo principio variazionale costituisce il fondamento teorico della __codifica per trasformata__ (Transform Coding, Goyal 2001). In algoritmi industriali quali JPEG o compressioni audio, il segnale viene prima decorrelato mediante trasformate ortogonali (KLT, DCT), concentrando l'energia su pochi coefficienti a grande varianza e scartando le frequenze a varianza inferiore alla soglia $\lambda$.

## Proprietà Matematiche della Funzione Rate-Distortion

La funzione Rate-Distortion $R(D)$ gode di proprietà analitiche fondamentali che ne governano il comportamento in ogni applicazione trasmissiva.

### Convessità di $R(D)$

Per qualsiasi sorgente stazionaria e qualsiasi criterio di distorsione, la funzione $R(D)$ è una funzione __strettamente convessa__ di $D$:

$$
R(\alpha D_1 + (1 - \alpha) D_2) \le \alpha R(D_1) + (1 - \alpha) R(D_2), \quad \forall \alpha \in [0, 1]
$$

La dimostrazione formale, basata sulla miscela di canali di transizione e sulla convessità dell'informazione mutua rispetto alla distribuzione condizionata, è disponibile in [[zz. Argomenti extra#Dimostrazione della Convessità della Funzione di Rate-Distortion $R(D)$]].

Dalla convessità discendono conseguenze cardinali:
1. $R(D)$ è una funzione monotona non crescente con derivata prima (pendenza della curva) negativa e monotona crescente:

$$
   s = \frac{\mathrm{d}R}{\mathrm{d}D} \le 0, \quad \frac{\mathrm{d}^2 R}{\mathrm{d}D^2} \ge 0
$$

2. Il beneficio marginale decresce rapidamente: abbattere la distorsione a livelli prossimi allo zero ($D \to 0$) richiede una spesa esponenziale di bit, con pendenza $s \to -\infty$.

### Teorema di Separazione Sorgente-Canale con Distorsione

Unendo i risultati del capitolo [[B. Capacità di Canale e Teorema di Shannon]] con la teoria della quantizzazione, Shannon dimostrò il __Teorema di Separazione Congiunta con Criterio di Fedeltà__:
Una sorgente stazionaria caratterizzata da una funzione Rate-Distortion $R(D)$ può essere trasmessa su un canale discreto o continuo avente capacità di canale $C$ e ricostruita a destinazione con distorsione media non superiore a $D$ se e solo se:

$$
R(D) < C
$$

Se $R(D) > C$, è matematicamente impossibile conseguire una distorsione media inferiore o uguale a $D$, indipendentemente dalla lunghezza dei blocchi di codifica adottati.

### Limite Inferiore di Shannon (Shannon Lower Bound)

Per variabili continue con misura di distorsione basata sulla differenza $d(x - \hat{x})$, Shannon formulò un limite analitico universale denominato __Shannon Lower Bound (SLB)__:

$$
R(D) \ge h(X) - \frac{1}{2}\log_2(2\pi e D)
$$

dove $h(X)$ è l'[[C. Entropia Differenziale e Canale Gaussiano|entropia differenziale]] della sorgente.
- Per sorgenti gaussiane, il bound coincide esattamente con la funzione $R(D)$.
- Per qualsiasi sorgente continua con densità non gaussiana, l'SLB è asintoticamente esatto nel limite di alta fedeltà (bassa distorsione, $D \to 0$):

$$
  \lim_{D \to 0} \left[ R(D) - \left( h(X) - \frac{1}{2}\log_2(2\pi e D) \right) \right] = 0
$$

### Algoritmo di Blahut-Arimoto per il Calcolo Numerico di $R(D)$

Nei casi in cui la distribuzione della sorgente o la metrica di distorsione non ammettono forme chiuse, la funzione $R(D)$ viene calcolata numericamente tramite l'__algoritmo di Blahut-Arimoto__ (1972).

Riformulando il problema tramite un funzionale di doppia minimizzazione su coordinate alternate (Alternating Minimization) parametrizzato dalla pendenza lagrangiana $s = \frac{\mathrm{d}R}{\mathrm{d}D} < 0$:

$$
\min_{p(\hat{x} \mid x)} \min_{q(\hat{x})} \sum_{x} \sum_{\hat{x}} p(x) p(\hat{x} \mid x) \ln \frac{p(\hat{x} \mid x)}{q(\hat{x})} - s \sum_{x} \sum_{\hat{x}} p(x) p(\hat{x} \mid x) d(x, \hat{x})
$$

l'algoritmo alterna l'aggiornamento della distribuzione condizionata $p(\hat{x} \mid x)$ secondo una forma di Gibbs ed il ricalcolo della marginale $q(\hat{x})$, convergendo monotonicamente e globalmente al valore esatto della coppia $(D(s), R(s))$. La derivazione completa è dettagliata in [[zz. Argomenti extra#Algoritmo di Blahut-Arimoto per il Calcolo Numerico della Funzione Rate-Distortion]].

