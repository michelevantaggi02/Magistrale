# Indice

- [[#Oversampling|Oversampling]]
- [[#Fixed point|Fixed point]]
- [[#Gamma Dinamica|Gamma Dinamica]]
- [[#Floating point|Floating point]]
- [[#ADC Bipolare E Unipolare.|ADC Bipolare E Unipolare.]]
- [[#Errore Di Quantizzazione|Errore Di Quantizzazione]]
	- [[#Errore Di Quantizzazione#Metriche Di Errore|Metriche Di Errore]]
	- [[#Errore Di Quantizzazione#Errore come Variabile Casuale|Errore come Variabile Casuale]]
- [[#Gamma Dinamica|Gamma Dinamica]]
- [[#Rapporto Segnale-Rumore|Rapporto Segnale-Rumore]]
- [[#Ottimizzazione Di Max|Ottimizzazione Di Max]]
- [[#Quantizzazione Non Uniforme|Quantizzazione Non Uniforme]]
- [[#Modificare Una p.d.f.|Modificare Una p.d.f.]]
	- [[#Modificare Una p.d.f.#Implementazione|Implementazione]]
- [[#Implementazioni Digitali Del Companding|Implementazioni Digitali Del Companding]]
	- [[#Implementazioni Digitali Del Companding#$\mu$-law|$\mu$-law]]
- [[#Quantizzazione Non Lineare Nel Video - HDR|Quantizzazione Non Lineare Nel Video - HDR]]
- [[#Frequenza Digitale ($\omega$) E Intervallo Di Nyquist|Frequenza Digitale ($\omega$) E Intervallo Di Nyquist]]
	- [[#Frequenza Digitale ($\omega$) E Intervallo Di Nyquist#IDTFT|IDTFT]]
- [[#Proprietà Della DTFT|Proprietà Della DTFT]]
	- [[#Proprietà Della DTFT#Ampiezze E Fasi Del Segnale|Ampiezze E Fasi Del Segnale]]
	- [[#Proprietà Della DTFT#Risposta Impulsiva E in Frequenza|Risposta Impulsiva E in Frequenza]]
	- [[#Proprietà Della DTFT#Proprietà Del Filtraggio|Proprietà Del Filtraggio]]
	- [[#Proprietà Della DTFT#Equazioni Di Parzeval|Equazioni Di Parzeval]]
- [[#IDFT|IDFT]]
- [[#Sovracampionamento|Sovracampionamento]]
- [[#Zero Padding|Zero Padding]]
- [[#Complessità Della DFT|Complessità Della DFT]]
- [[#Convoluzione Lineare Con Sequenze Di Durata Finita|Convoluzione Lineare Con Sequenze Di Durata Finita]]
	- [[#Convoluzione Lineare Con Sequenze Di Durata Finita#Fenomeni Di Transitorio|Fenomeni Di Transitorio]]
- [[#Convoluzione Circolare|Convoluzione Circolare]]

# 0. Introduzione

Libri consigliati:
- Orfanidis "Introduction to signal processing" ([download gratuito](https://rutgers.app.box.com/s/5vsu06pp556g9dfsdvayh4k50wqpataw))
- Oge Marques "Practical image and video processing using matlab" ([immagini gratuite](https://ogemarques.com/books/), [libgen](https://libgen.gl/edition.php?id=146257563))

L'esame è diviso in 2 parti:

1. Esercizi al pc su Matlab della durata di 3h. Panico, si possono usare tutte le informazioni possibili: appunti, chatgpt, internet, pezzi di codice di altri esercizi ecc..
2. Orale

# 1. Quantizzazione

La quantizzazione è un'operazione sempre con perdita di informazioni.
Per quantizzare aggiungiamo una quantità nota di rumore al segnale, ma il suo effetto varia in base alle sue caratteristiche.

![[ADC.svg|center big]]
Il filtro passa basso serve ad eliminare tutte le frequenze troppo alte per essere utilizzate.

![[filtro passa basso.svg|small center]]
- __BP__: Banda passante
- __BT__: Banda di transizione
- __BA__: Banda di arresto

>[!example]
>Il primo segnale digitalizzato era la voce nel telefono (200hz - 3500hz).
>Nelle telecamere il filtro passa basso è composto da un vetro protettivo "drogato" per non far passare frequenze di luce che possono causare aliasing

## Oversampling

Si intende per oversampling quel procedimento odove si aumenta la frequenza di campionamento ($f_c$) a un valore talmente alto che il filtro passa basso analogico non è più necessario.

Viene poi inserito un filtro digitale che effettua la __decimazione__ del segnale.
![[oversampling.svg|center mid]]

- $f_c'$: frequenza di campionamento con oversampling (2x, 3x, 4x,…)

Usare oversampling e poi inserire un filtro digitale costa molto meno ed è anche meno propenso a rottura rispetto ad un filtro analogico.

Nei sensori di immagini per effettuare oversampling si aumenta il numero di pixel, questo però fa diminuire la loro capacità di catturare la luce. Per risolvere questo problema nel processo di decimazione si utilizza un sistema chiamato __binning__ che mette insieme il risultato di più pixel vicini per ridurre il rumore.

## Fixed point

Formato di rappresentazione dei numeri decimali in virgola fissa.
La formula per calcolare il valore in binario è:

$$
N=\sum_{i = -k}^D{b_i \cdot 2^i}
$$

$$
N = b_D b_{D-1}\dots b_1b_0,b_{-1}b_{-2}\dots b_{-k}
$$

La posizione della virgola è rilevante solo per noi, l'elaboratore può trattare i dati come se fossero numeri interi, purché la posizione della virgola sia la stessa per tutti gli operandi.

>[!example]
>$[0; 2[$ in 8 bit
>Abbiamo bisogno di un solo bit per rappresentare i numeri interi, visto che 2 è escluso:
>
>$$
>b_7,b_6b_5b_4b_3b_2b_1b_0
>$$
>
>Il numero più piccolo rappresentabile: $N_{FP}= 2^{-7} = \frac 1{128}$
>Il numero massimo: $M_{FP} = 2-N_{FP}$

Possiamo usare i numeri in virgola fissa come se fossero una scala:
![[scala virgola fissa.svg|center big]]
Se iniziamo a rappresentare in digitale le informazioni del mondo reale, si capisce facilmente che abbiamo numerose limitazioni.

## Gamma Dinamica

La gamma dinamica è il rapporto tra il valore massimo rappresentabile e il valore minimo rappresentabile.

Il dynamic range di un formato fixed point è dato da:

$$
\frac{M_{FP}}{N_{FP}}=\left. \frac{(2^{B} - 1)N_{FP}}{N_{FP}}\right|_{dB} = 20\log_{10}(2^B-1) \approx 20 \log_{10}(2^B) = B(20 \log_{10}2) = 6B
$$

L'unico modo con cui possiamo aumentare i $dB$ di un fixed point è quello di aumentare i bit, aumentando i bit miglioriamo di un fattore di 6 la scala dinamica.

## Floating point

Il fixed point è molto limitato, per questo è stato sviluppato il floating point, che permette di eseguire calcoli più complessi, a discapito di un maggiore costo computazionale.

La gamma dinamica di un floating point è di : $20\log_{10}(\frac{0.999 \cdot 10^{99}}{0.100} \cdot 10^{-99}) \approx 4000dB$

Il formato floating point è estremamente efficiente, perché in base all'esponente avvicina tra loro i numeri piccoli, mentre allontana quelli più grandi.
In termini di _errore assoluto_ il floating point è meno preciso, ma l'__errore relativo__ è molto minore.

$$
\begin{matrix*}[r]
A= .5655 \cdot 10^e \\
\varepsilon_A=.0005 \cdot 10^e
\end{matrix*} \quad\varepsilon_R  = \frac {.0005 \cdot 10^e}{.5655 \cdot 10^e} = \frac{.0005}{.5655}
$$

L'errore relativo è __costante__ nel floating point.

Esistono 2 dimensioni di formati floating point:

- Float 32 bit: 1 segno, 8 esponente, 23 mantissa
- Double 64 bit: 1 segno, 11 esponente, 52 mantissa

L'esponente è rappresentato da un formato "sempre positivo", la prima metà del range è negativa (da -127 a -1), mentre la seconda metà è positiva (da -0 a 128), a parte alcune eccezioni.

Il floating point ha infatti alcuni valori speciali da utilizzare in determinati casi:

- normalized
- denormalized
- zero
- infinity
- not a number

# 2. Quantizzazione Uniforme

![[immagini/conversione_adc.png|center]]

Il condensatore posto all'interno del campionatore serve a mantenere lo stesso valore del segnale per il tempo di campionamento $T$.

Un convertitore Analogico-Digitale è caratterizzato da una __range__ in cui opera $R$, diviso equamente (per un quantizzatore uniforme) in $2^B$ __livelli di quantizzazione__.

La spaziatura tra i livelli, chiamata __larghezza dei livelli__ (quantization width) o risoluzione del quantizzatore è data dalla formula:

$$
Q=\frac R{2^B}=\text{NFP}
$$

Questa equazione può anche essere riscritta nella forma:

$$
\frac RQ = 2^B
$$

![[immagini/quantizzazione_segnale.png|center]]

## ADC Bipolare E Unipolare.

Se i valori di $R$ variano in una p.d.f. (probability density function) che varia tra

$$
 - \frac R2 \leq x_Q(nT) < \frac R2
$$

l'ADC si dice __bipolare__.

Se invece i valori variano tra

$$
 0 \leq x_Q(nT) < R
$$

allora si dice __unipolare__.

Nella pratica il segnale $x(t)$ deve essere _precondizionato analogicamente_ per rientrare nella scala di valori del quantizzatore _bipolare_.

Il limite maggiore ($\frac R2$) non è incluso tra i livelli assumibili, infatti il livello massimo è $\frac R2 - Q$.

## Errore Di Quantizzazione

Nella maggior parte dei casi i quantizzatori lavorano arrotondando il valore al livello più vicino. Si tratta della scelta preferita rispetto al troncamento per la maggior parte dei casi, in quanto produce una rappresentazione più simile al segnale.

L'__errore di quantizzazione__ è l'errore che risulta dall'utilizzo del segnale quantizzato $x_Q(nT)$ al posto del segnale reale $x(nT)$, e la sua formula è:

$$
\text e(nT) = x_Q(nT) - x(nT)
$$

In generale l'errore di quantizzazione di un numero $x$ che si trova nel range $[- \frac R2, \frac R2]$ è:

$$
e = x_Q - x
$$

dove $x_Q$ è il valore quantizzato.

### Metriche Di Errore

Con l'arrotondamento l'errore varia tra $- \frac Q2$ e $\frac Q2$, inclusi, abbiamo quindi l'errore massimo:

$$
e_{\text{max}} = \frac Q2
$$Questa è però una sovrastima dell'errore tipico che incontriamo, per ottenere un valore più rappresentativo dell'errore medio consideriamo la media e la media quadrata dei valori di $e$ definiti da:
$$

\begin{align*}
\bar{e} = \frac 1Q \int_{-\frac Q2}^{\frac Q2}{e\,\mathrm de} = 0 &\quad \text{media}\\
\bar{e^2}=\frac 1Q \int_{-\frac Q2}^{\frac Q2}{e^2\,\mathrm de} = \frac{Q^2}{12} & \quad \text{media quadrata}
\end{align*}

$$

Il risultato $\bar e = 0$ indica che in media metà dei valori vengono arrotondati per eccesso e metà per difetto, quindi $\bar e$ __non può essere usato__ come errore rappresentativo.

Un valore più utilizzato per questo scopo è la __radice del quadrato della media degli errori (RMS)__:

$$

e_{rms} = \sqrt{\bar{e^2}} = \frac Q{\sqrt{12}}

$$

### Errore come Variabile Casuale

Possiamo dare una interpretazione probabilistica assumendo che $e$ sia una variabile casuale con __distribuzione uniforme__ nel range $[- \frac Q2; \frac Q2]$ avente la funzione di probabilità:

$$

p(e) = \begin{cases} \frac 1Q & \text{se}\; -\frac Q2 \leq e \leq \frac Q2 \\ 0 & \text{altrimenti} \end{cases}

$$

La normalizzazione $\frac 1Q$ è necessaria per garantire la distribuzione uniforme:

$$

\int_{-\frac Q2}^{\frac Q2}{p(e)\,\mathrm de} = 1

$$
Si capisce che l'errore rappresenta l'**aspettativa statistica**:
$$

E[e] = \int_{-\frac Q2}^{\frac Q2}{ep(e)\,\mathrm de}

$$
$$

E[e^2] = \int_{-\frac Q2}^{\frac Q2}{e^2p(e)\,\mathrm de}

$$
L'__interpretazione probabilistica__ del rumore di quantizzazione è molto utile per determinare gli __effetti di quantizzazione__ mentre si propagano attraverso il sistema di calcolo digitale. 
$$

x_Q(n) = x(n) + e(n)

$$
Possiamo pensare che il segnale quantizzato $x_Q(n)$ sia una __versione rumorosa__ del segnale originale $x(n)$ con aggiunta una __componente di rumore__ $e(n)$.

Per i segnali a __larga ampiezza__ e __larga banda__, ovvero i segnali che variano nell'_intera scala_ di $R$ passando tra tutti i livelli di quantizzazione, la sequenza $e(n)$ può essere considerata come una __sequenza di rumore bianco__ a p.d.f. uniforme stazionaria con media 0. 

Sembra inoltre che $e(n)$ sia __scorrelata__ rispetto al segnale originale $x(n)$.

La __varianza media__ è stata calcolata come:
$$

\sigma_e^2 = E[e^2(n)] = \frac{Q^2}{12}

$$
L'assunzione che $e(n)$ sia un rumore bianco significa che la funzione delta di autocorrelazione:
$$

R_{ee}(k) = E[e(n+k)e(n)] = \sigma_e^2\delta(k)

$$
Similmente è scorrelata con $x(n)$, il che significa che ha **0 cross-correlation**:
$$

R_{ex}(k) = E[e(n+k)x(n)] = 0

$$
Il modello non è accurato per segnali che variano lentamente a bassa ampiezza, ad esempio con sinusoidi che si trovano esattamente _nel mezzo_ di due livelli con ampiezza _minore_ di Q/2. L'errore risultante sarebbe altamente periodico e diverso rispetto al rumore bianco casuale, sarebbe anche altamente correlato con la sinusoide di input.

> [!note]
> Nell'audio digitale, le distorsioni causate da segnali a basso livello sono chiamate "**granulation noise**" e causano suoni fastidiosi. Possono essere eliminate virtualmente tramite l'uso di "dither", un rumore a basso livello aggiunto al segnale prima della quantizzazione.
## Gamma Dinamica

> [!INFO]
> ![[1. Quantizzazione#Gamma Dinamica]]
$$

\frac RQ = 2^B = \frac{M_{FP}}{N_{FP}}

$$
Pensando ad $R$ e $Q$ come i range del __rumore del segnale__ ($R$) e del **rumore di quantizzazione** ($Q$), il loro rapporto è la **gamma dinamica**, che può essere espresso in $dB$:
$$

20\log_{10}(\frac RQ) = 6B \;dB

$$
## Rapporto Segnale-Rumore

![[immagini/errore.svg|center mid]]
$$

-\frac Q2 < \text{e}(n) \leq \frac Q2

$$
Il rapporto segnale-rumore di quantizzazione (**SQNR**) è dato da:
$$

\text{SQNR} = \left. \frac{P_{\text{signal}}}{P_{\text{quant\_noise}}}\right |_{dB} = 10\log_{10}\frac{P_x}{P_{\varepsilon n}}

$$
$$

P_{\varepsilon n} = \frac {Q^2}{12} = \frac{{N_{FP}}^2}{12}

$$
Dobbiamo mantenere _scollegato_ il rumore di quantizzazione dal segnale:

![[immagini/diagramma rumore.svg|center]]

Parliamo di errore di quantizzazione quando:
$$

e(n) = x(n) - \hat x_Q(n)

$$
se lo riteniamo _scollegato_ rispetto al segnale, allora lo definiamo come **rumore di quantizzazione**:
$$

\left. \text{SQNR} = \frac {P_{sig}}{P_{noise}} \right |_{dB} = 10\log_{10}\frac{P_x}{P_{\varepsilon n}}

$$
# 3. Quantizzazione Ottima

Il rapporto SQNR varia in base alla p.d.f., ma nella realtà i segnali _non hanno_ una p.d.f. uniforme.

Ad esempio la voce umana ha una p.d.f. esponenziale ($e^{- \lambda|x|}$), è quindi molto problematico utilizzare un quantizzatore uniforme.


![[caratteristica ingresso-uscita.svg |center]]

## Ottimizzazione Di Max

Il nostro obiettivo è quello di massimizzare la SQNR dato un numero di bit fissato, minimizzando la probabilità di errore.

Per arrivare a questo devo agire su $x_i$ e $y_i$, ovvero i __limiti delle zone di decisione__.

Per prima cosa si calcola la potenza dell'errore $Q$:
$$

Q =
\begin{gather}
\int_{x_{-1}}^{x_1}{x^2 P_x(x)\;\mathrm dx} & + &
2\sum_{n=1}^{N-1}\int_{x_n}^{x_{n+1}}{(x-y_n)^2 P_x(x)\; \mathrm dx} & + &
2\int_{x_n}^{\infty}{(x-y_n)^2 P_x(x) \; \mathrm dx}
\\
\text{ZONA MORTA} && \text{ZONA QUASI LINEARITÀ} && \text{ZONA SATURAZIONE}
\end{gather}

$$
Data una p.d.f., i valori di decisione ottima $x_i$ e i livelli ottimi di output $y_i$ si ottengono impostando a 0 la derivata di $Q$:
$$

y_i = \frac 1{P_i}\int_{x_i}^{x_{i+1}}{xP_x(x)\;\mathrm dx} = E\{x \mid x_i < x < x_{i+1}\}

$$

I livelli di uscita sono il __valore medio statistico__ delle zone di decisione

$$

x_i = \frac 12(y_i + y_{i+1})

$$

Si può dedurre che spostando $y_i$ si spostano anche gli $x_i$.

![[pdf_non_uniforme.png|center]]

## Quantizzazione Non Uniforme

Per segnali a p.d.f. uniforme, il quantizzatore uniforme è ottimo.

Il quantizzatore di Max si specializza per ogni segnale in ingresso, questo va però in conflitto con la natura propria dei quantizzatori, in quanto porta a dover aumentare il numero di bit.

Si può quindi seguire un altro approccio: andremo a __modificare la p.d.f.__ del segnale in ingresso per __renderla uniforme__. Ovviamente questa operazione deve essere __reversibile__ per riottenere il segnale originale.

## Modificare Una p.d.f.

$$

\eta = g(x)

$$

Dobbiamo avere una funzione che dato $x$ (variabile aleatoria) lo trasforma in una a p.d.f. uniforme.

La funzione deve seguire determinati fattori:

1. Essere invertibile
2. $g(-x) = -g(x)$ antisimmetrica
3. $g(0)  = 0$
4. $g(\infty) = \frac R2$

la p.d.f. della funzione $\eta$ si ottiene tramite:

$$

P_\eta(\eta) = \left[\frac{P_x(x)}{| \frac{\partial {g(x)}}{\partial x}|}\right]_{x = g^{-1}(\eta)}

$$

e per i nostri obiettivi deve essere _costante_.

$$

\frac{\partial g(x)}{\partial x} = P_x(x) \implies g(x) = \int \frac{P_x(x)}{P_\eta(\eta)}\; \mathrm dx

$$

Devo quindi calcolare la LUT con la formula:

$$

\eta = g(x) = \int \frac{P_x(x)}{P_\eta(\eta)}\;\mathrm dx

$$

Dove $P_\eta(\eta)$ è la funzione densità di probabilità __uniforme__ ($\frac 1R$), mentre $P_x(x)$ è quella del segnale che può essere conosciuta a priori oppure stimabile.

### Implementazione

L'implementazione vera e propria di questa funzione si chiama __amplificatore a guadagno variabile__

![[amplificatore a guadagno variabile.svg|center big]]

Ovviamente questo sistema va a cambiare lo spettro del segnale, non è quindi utilizzabile in circuiti che devono eseguirne l'analisi.

>[!EXAMPLE] Segnale vocale

$$

P_x(x)=\frac{\lambda}{2}e^{-\lambda|x|} \quad\quad \lambda^2 = \frac 2{\sigma^2}

$$
>
$$\frac{\partial g(x)}{\partial x} = P_x(x);\quad  x > 0
>
$$

$$
g(x) = \frac R2 (1- e^{-\lambda x}); \quad x > 0
>$$
>
>Bisogna provare che rispetta le proprietà:
>- $\eta = g(x) = \frac R2(1 - e^{-\lambda x}); \quad x > 0$
>- $x = g^{-1}(\eta) = -\frac 1\lambda\ln[1-2\eta]; \quad 0 \leq \eta < \frac R2$
>
>Questo per i valori positivi di $x$ e $\eta$. La simmetria viene utilizzata per ottenere i valori equivalenti negativi.

La tecnica di **companding** indica la compressione e l'espansione, ovvero la modifica e il ritorno alla funzione originale.

>[!NOTE]
>Quando parlo di **quantizzazione ottima** mi riferisco alla *quantizzazione di Max*, dove il mio obiettivo è quello di massimizzare la SQNR.
>Non sempre un approccio non lineare serve a massimizzare la SQNR, quindi la chiamiamo genericamente **quantizzazione non lineare**

## Implementazioni Digitali Del Companding

![[companding_digitale.svg|center big]]

Vogliamo codificare $x(t)$ analogico in un segnale digitale con quantizzazione non lineare.
![[companding_digitale_esempio.svg|center big]]
Il nostro target della quantizzazione è di $B$ bit, sovracampioniamo scegliendo $B' > B$ bit tali che soddisfino i requisiti di rapporto segnale-rumore (SQNR).

Il nostro obiettivo è calcolare $\eta = g(x)$ per comprimere i valori sovradimensionati $x(n)$ in una quantizzazione non lineare al target giusto ($B$).

Devo calcolarli in anticipo perché nella pratica non posso avere un sistema che riesca a calcolarli in real time, quindi li inserisco in una LUT (Look-Up Table).
![[lookup table.svg|center mid]]
Questa tecnica si può effettuare con segnali anche bidimensionali, ovviamente ridimensionando la LUT di conseguenza.


### $\mu$-law
$$\eta = g(x) = \frac{\ln(1+\mu |x|)}{\ln(1+\mu)}
$$

Questa è la formula calcolata e inserita nella LUT.

## Quantizzazione Non Lineare Nel Video - HDR

Non si occupa di migliorare il rapporto segnale-rumore, ma di estendere la dinamica il più possibile.
- La telecamera acquisisce a 14-16 bit lineari unsigned.
- I codec utilizzano 8-10 bit.
- Devo quindi applicare una legge di compressione della dinamica.
- In fase di riproduzione devo invertire la legge.
- I display quelli buoni utilizzano 10-12 bit di dinamica.

# 4. Spettro in Frequenza - DTFT

La Trasformata di Fourier non può essere applicata su segnali discretizzati nel tempo e nei valori.
Per questo sono state sviluppate 2 varianti:

- __DTFT (Discrete-Time Fourier Transform)__: si applica alle sequenze fornendo una funzione continua, non può essere applicata in ambiente digitale in quanto bisogna discretizzare anche le frequenze.
- __DFT (Discrete Fourier Transform)__: quantizza anche $\omega$ e può essere implementata digitalmente. Non rappresenta un'approssimazione della DTFT, ma una sua _rappresentazione esatta_, a patto che lo __spettro__ sia __finito__.

$$
\text{Fourier}:\quad x(t) \to X(f) = \int_{-\infty}^{+\infty}x(t)e^{-j2\pi ft}\;\mathrm dt = \int_{-\infty}^{+\infty}x(t)e^{-j\Omega t}\; \mathrm dt, \quad \Omega = 2\pi f
$$

$$
\text{DTFT :}\quad X(\omega) = \sum_{n = -\infty}^{\infty}x(n)e^{-j\omega n}, \quad \omega=\frac{2\pi f}{f_c}
$$

>[!QUESTION]
>Come si arriva ad avere $f_c$ al denominatore di $\omega$?
> Bisogna tornare un po' indietro a quando si effettua il [[1. Segnali#Campionamento |Campionamento]].

$$
 \begin{align*}
> x(t)\bigg|_{t=nT} = x(nT) & = \sum_{n = -\infty}^{\infty}x(n)e^{-j2\pi f (nT)} \\
> & = \sum_{n = -\infty}^{\infty}x(n)e^{-j\frac{2\pi f}{f_c} n}
> \end{align*} 
> 
$$

$$T = \frac 1{f_c}
> $$
>  

La risposta in frequenza $H(\omega)$ di un sistema lineare $h(n)$ è sempre la sua DTFT.
## Frequenza Digitale ($\omega$) E Intervallo Di Nyquist

La frequenza digitale (non è veramente una frequenza) è un'unità espressa in radianti/campione, ed è relazionata alla **frequenza fisica** $f$ (in Hz) da: 
$$\omega = \frac{2 \pi f}{f_c}
$$

Il campionamento del segnale produce una __periodizzazione__ dello spettro, si ha quindi che la DTFT $X(\omega)$ è periodica di periodo $2\pi$.
L'__intervallo di Nyquist__ della frequenza $[- \frac {f_c}2, \frac {f_c}2]$ nelle unità di $\omega$ è l'intervallo:

$$
[ - \pi \leq \omega \leq \pi]
$$

Possiamo quindi dire che la DTFT è una rappresentazione esatta della Trasformata di Fourier solo per segnali a banda limitata, in quanto con il campionamento viene resa periodica in $\omega$, portando a non riuscire a rappresentare frequenze al di fuori dell'intervallo di Nyquist. Tuttavia se il segnale campionato rispetta correttamente il [[1. Segnali#^e56489|Teorema del Campionamento]], avremo a disposizione tutte le frequenze necessarie.

Nell'atto pratico l'intervallo di Nyquist viene rappresentato come l'intervallo

$$
[0 \leq \omega \le 2\pi]
$$

## IDTFT

L'inversa della DTFT serve a recuperare la sequenza nel dominio del tempo discreto $x(n)$, dato lo spettro $X(\omega)$ nell'intervallo di Nyquist.

$$
x(n) = \frac1{2\pi}\int_{-\pi}^{\pi} X(\omega) e^{j\omega n}\; \mathrm d\omega
$$

Esprime $x(n)$ come una __combinazione lineare__ di sinusoidi in tempo-discreto $e^{j\omega n}$ con diverse frequenze.

Le relative ampiezze e fasi di queste sinusoidi sono fornite dalla DTFT $X(\omega)$.

# Proprietà Della DTFT

La DTFT ha le medesime proprietà della Trasformata di Fourier in tempo continuo, ovviamente adattate per funzionare in tempo discreto.

## Ampiezze E Fasi Del Segnale

La DTFT di un segnale $x(n)$ è una funzione a valori complessi, pertanto può essere caratterizzata da una parte reale $Re X(\omega)$ e una immaginaria $Im X(\omega)$, o in forma polare dal suo modulo $|X(\omega)|$ e la sua fase $arg X(\omega)$.

$$
X(\omega) = Re X(\omega) + j Im X (\omega) = |X(\omega)|e^{j arg X(\omega)}
$$

Per segnali a valore reale di $x(n)$, $X(\omega)$ soddisfa la __proprietà hermitiana__.

## Risposta Impulsiva E in Frequenza

La risposta impulsiva in tempo discreto $h(n)$ è data da una __variante tempo-discreta dell'impulso di Dirach__, dove ogni campione ha valore 0, tranne con $n=0$, dove ha valore 1.

La risposta in frequenza, è la DTFT della risposta impulsiva:

$$
H(\omega) =  \sum_{n = -\infty}^{\infty}h(n)e^{-j\omega n}
$$

## Proprietà Del Filtraggio

$$
Y(\omega) = H(\omega) \cdot X(\omega)
$$

$$
y[n] = h[n] \ast x[n]
$$

## Equazioni Di Parzeval

Possiamo calcolare __energia__ e __potenza__ di un segnale tramite le Equazioni di Parzeval:

$$
\sum_{n = -\infty}^{\infty}|x(n)|^2 = \frac 1{2\pi}\int_{-\infty}^{+\infty}|X(\omega)|^2\;\mathrm d\omega
$$

# 5. Trasformata Discreta Di Fourier (DFT)

La DFT è una trasformata __esatta__ che può essere calcolata completamente in digitale.

$$
\omega_k = \frac {2\pi}N k, \quad k = 0,...,N-1
$$

$$
f_k = \frac {kf_s}N
$$

Il problema consiste nel calcolare correttamente la frequenza $f_k$, ovvero individuare il numero corretto (N) degli spazi.

Devo essenzialmente "campionare" il segnale in base alla frequenza.

Campionare in frequenza mi dice che il segnale deve essere __finito nel tempo__, non posso quindi applicare la DFT a segnali di durata infinita.

$$
\text{DTFT :}\quad X(\omega) = \sum_{n = -\infty}^{\infty}x(n)e^{-j\omega n}, \quad \omega=\frac{2\pi f}{f_c}
$$

$$
\text{DFT :}\quad X(\omega_k) = \sum_{n = 0}^{N-1}x(n)e^{-j \frac {2\pi}N k n}, \quad x(n) \neq 0, \quad 0 \le n \le N-1
$$

 ^6ad93d

Se rispetto il vincolo $0 \le n \le N-1$ la DFT è una trasformata __esatta__.

Nulla mi vieta di scegliere un altro valore $L \le N$, dove $0 \le n  \le L-1$.

## IDFT

$$

\tilde x(n) = \frac 1N \sum_{k=0}^{N-1} x(\omega_k) e^{j\omega_kn}, \quad n=0,…,N-1

$$

## Sovracampionamento

Se scelgo un $L < N$ otterrò un sovracampionamento:

![[immagini/dft_oversampling.svg|center big]]

Si tratta di sovracampionamento perché parto da $L < N$ punti e ne ottengo $N > L$, ho quindi più punti di quanti ne utilizzo. In genere non si fa.

Questi vettori (anche senza sovracampionamento) rispettano la proprietà Hermitiana, quindi mi basta calcolare $\frac N2$ valori.

## Zero Padding

Se prendo $L < N$ valori, posso aggiungere ($D = N - L$) zeri in fondo al segnale, non avrò cambiamenti nella __DTFT__, ma li avrò nella __DFT__, perché viene calcolata in base al numero di valori di $x$.

$$\begin{align}
X_D(\omega) & = \sum_{n = 0}^{L+D-1}x_D(n)e^{-j\omega n} \\
&= \sum_{n = 0}^{L-1}x_D(n) e^{-j \omega n} &+& \sum_{n = L}^{L+D-1} 0 e^{-j\omega n}\\
&= \sum_{n = 0}^{L-1}x(n) e^{-j\omega n} &+& 0\\
&=X(\omega)
\end{align}
$$

## Complessità Della DFT

![[#^6ad93d]]

$$x(n)e^{-j\omega_k n} = x(n)(\cos(\omega_kn) -j\sin(\omega_kn))
$$

Bisogna fare quindi $2L$ __MACS__ per ogni valore $\omega_k$.

Per tutta la DFT occorrono quindi $2LN$ operazioni, o $2N^2$ per $L=N$.

Per $x(n)$ con valori complessi occorrono $4n^2$ operazioni.

>[!important] FFT
>Si può ottimizzare il costo utilizzando l'algoritmo __FFT__, che viene eseguito in $N\log_2 N$ operazioni, a patto che $N = 2^m$.
>Nella maggior parte dei casi è molto più veloce portare $N$ alla potenza del due successiva tramite lo [[#Zero padding]] ed eseguire la FFT, piuttosto che eseguire direttamente la DFT.

## Convoluzione Lineare Con Sequenze Di Durata Finita

$$
y(n) = x(n) \ast h(n) = \sum_{k=0}^{N-1}h(k)x(h-k)
$$

Se la sequenza in ingresso ha _durata finita_:

$$
x(n) \neq 0 \, \text{per}\, 0 < n<L-1,\quad L >> N
$$

Si osserveranno __fenomeni di transitorio__ e si otterrà quindi la sequenza $y(n)$ __più lunga__ rispetto alla sequenza in ingresso $x(n)$.

### Fenomeni Di Transitorio

Si tratta di 3 fenomeni:
- Il __transitorio di attacco__ si ha quando la memoria del registro è vuota e inizia a riempirsi, in questo caso si avranno i valori inizialmente con valore 0 che pian piano verranno rimpiazzati dal primo valore e dai seguenti.
- Una volta riempita la memoria si ha la __risposta a regime__, dove nel registro circolare scorrono i nuovi valori eliminando quelli più vecchi.
- Quando il segnale termina il registro circolare inizia a svuotarsi, questa fase si chiama __transitorio di rilascio__, l'esecuzione termina quando tutti i campioni tornano a 0.

## Convoluzione Circolare

# 6. Finestratura

Per poter lavorare con la DFT
