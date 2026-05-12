# Indice

- [[#0. Introduzione|0. Introduzione]]
- [[#1. Quantizzazione|1. Quantizzazione]]
	- [[#1. Quantizzazione#Oversampling|Oversampling]]
	- [[#1. Quantizzazione#Fixed point|Fixed point]]
	- [[#1. Quantizzazione#Gamma Dinamica|Gamma Dinamica]]
	- [[#1. Quantizzazione#Floating point|Floating point]]
- [[#2. Quantizzazione Uniforme|2. Quantizzazione Uniforme]]
	- [[#2. Quantizzazione Uniforme#ADC Bipolare E Unipolare.|ADC Bipolare E Unipolare.]]
	- [[#2. Quantizzazione Uniforme#Errore Di Quantizzazione|Errore Di Quantizzazione]]
	- [[#2. Quantizzazione Uniforme#Gamma Dinamica|Gamma Dinamica]]
	- [[#2. Quantizzazione Uniforme#Rapporto Segnale-Rumore|Rapporto Segnale-Rumore]]
- [[#3. Quantizzazione Ottima|3. Quantizzazione Ottima]]
	- [[#3. Quantizzazione Ottima#Ottimizzazione Di Max|Ottimizzazione Di Max]]
	- [[#3. Quantizzazione Ottima#Quantizzazione Non Uniforme|Quantizzazione Non Uniforme]]
	- [[#3. Quantizzazione Ottima#Modificare Una p.d.f.|Modificare Una p.d.f.]]
	- [[#3. Quantizzazione Ottima#Implementazioni Digitali Del Companding|Implementazioni Digitali Del Companding]]
	- [[#3. Quantizzazione Ottima#Quantizzazione Non Lineare Nel Video - HDR|Quantizzazione Non Lineare Nel Video - HDR]]
- [[#4. Spettro in Frequenza - DTFT|4. Spettro in Frequenza - DTFT]]
	- [[#4. Spettro in Frequenza - DTFT#Frequenza Digitale ($\omega$) E Intervallo Di Nyquist|Frequenza Digitale ($\omega$) E Intervallo Di Nyquist]]
	- [[#4. Spettro in Frequenza - DTFT#Proprietà Della DTFT|Proprietà Della DTFT]]
- [[#5. Trasformata Discreta Di Fourier (DFT)|5. Trasformata Discreta Di Fourier (DFT)]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#IDFT|IDFT]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#Sovracampionamento|Sovracampionamento]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#Zero Padding|Zero Padding]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#Complessità Della DFT|Complessità Della DFT]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#Convoluzione Lineare Con Sequenze Di Durata Finita|Convoluzione Lineare Con Sequenze Di Durata Finita]]
	- [[#5. Trasformata Discreta Di Fourier (DFT)#Convoluzione Circolare|Convoluzione Circolare]]
- [[#6. Finestratura|6. Finestratura]]
	- [[#6. Finestratura#Finestra Nel Dominio Delle Frequenze|Finestra Nel Dominio Delle Frequenze]]
	- [[#6. Finestratura#Finestra Di Hanning|Finestra Di Hanning]]
- [[#Finestre Parametriche Di Kaiser|Finestre Parametriche Di Kaiser]]
- [[#7. Stima Spettrale Di Segnali Non Stazionari|7. Stima Spettrale Di Segnali Non Stazionari]]
	- [[#7. Stima Spettrale Di Segnali Non Stazionari#Short-Time Fourier Transform|Short-Time Fourier Transform]]
- [[#8. Filtri FIR - Finite Impulse Response|8. Filtri FIR - Finite Impulse Response]]
	- [[#8. Filtri FIR - Finite Impulse Response#Comportamenti Di Non Idealità|Comportamenti Di Non Idealità]]
	- [[#8. Filtri FIR - Finite Impulse Response#Progettare Un Filtro FIR - Metodo Delle Finestre|Progettare Un Filtro FIR - Metodo Delle Finestre]]
	- [[#8. Filtri FIR - Finite Impulse Response#Filtro Sotto-Banda|Filtro Sotto-Banda]]
- [[#9. Filtri IIR - Infinite Impulse Response|9. Filtri IIR - Infinite Impulse Response]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Introduzione - Trasformata Z|Introduzione - Trasformata Z]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Pattern Poli - Zeri|Pattern Poli - Zeri]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Sviluppo in Fratti Parziali E Inversa Della Trasformata Z|Sviluppo in Fratti Parziali E Inversa Della Trasformata Z]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Modalità Equivalenti per Descrivere I Filtri Digitali|Modalità Equivalenti per Descrivere I Filtri Digitali]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Risposta Sinusoidale|Risposta Sinusoidale]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Filtri Di Primo Ordine - Smoother|Filtri Di Primo Ordine - Smoother]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Filtri Di Secondo Ordine - Resonator|Filtri Di Secondo Ordine - Resonator]]
	- [[#9. Filtri IIR - Infinite Impulse Response#Equalizzatore Parametrico|Equalizzatore Parametrico]]
- [[#A. Sistemi Multi-Rate|A. Sistemi Multi-Rate]]
	- [[#A. Sistemi Multi-Rate#Interpolazione|Interpolazione]]
	- [[#A. Sistemi Multi-Rate#Decimazione|Decimazione]]
	- [[#A. Sistemi Multi-Rate#Sample Rate Converter|Sample Rate Converter]]
	- [[#A. Sistemi Multi-Rate#Filtri Multi Stadio|Filtri Multi Stadio]]
	- [[#A. Sistemi Multi-Rate#Equalizzazione DAC|Equalizzazione DAC]]

# 0. Introduzione

Libri consigliati:
- Orfanidis "Introduction to signal processing" ([download gratuito](https://rutgers.app.box.com/s/5vsu06pp556g9dfsdvayh4k50wqpataw))
- Oge Marques "Practical image and video processing using matlab" ([immagini gratuite](https://ogemarques.com/books/), [libgen](https://libgen.gl/edition.php?id=146257563))

L'esame è diviso in 2 parti:

1. Esercizi al pc su Matlab della durata di 3h. Complesso perché gli esercizi non sono esattamente come fatti a lezione, ti da un problema e devi capire tu come risolverlo (ex: devi capire se progettare un filtro FIR, o un equalizzatore parametrico, o devi effettuare una quantizzazione di un segnale). Puoi però usare qualsiasi strumento, appunti, internet ecc…
2. Orale a domanda secca da cui poi devi dire tutto il possibile, non ancora dato ma impossibile sbagliare (nel senso che se non la sai non puoi cambiare argomento e sei bocciato)

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
$$

Questa è però una sovrastima dell'errore tipico che incontriamo, per ottenere un valore più rappresentativo dell'errore medio consideriamo la media e la media quadrata dei valori di $e$ definiti da:

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

Si capisce che l'errore rappresenta l'__aspettativa statistica__:

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

Similmente è scorrelata con $x(n)$, il che significa che ha __0 cross-correlation__:

$$

R_{ex}(k) = E[e(n+k)x(n)] = 0

$$

Il modello non è accurato per segnali che variano lentamente a bassa ampiezza, ad esempio con sinusoidi che si trovano esattamente _nel mezzo_ di due livelli con ampiezza _minore_ di Q/2. L'errore risultante sarebbe altamente periodico e diverso rispetto al rumore bianco casuale, sarebbe anche altamente correlato con la sinusoide di input.

> [!note]
> Nell'audio digitale, le distorsioni causate da segnali a basso livello sono chiamate "__granulation noise__" e causano suoni fastidiosi. Possono essere eliminate virtualmente tramite l'uso di "dither", un rumore a basso livello aggiunto al segnale prima della quantizzazione.

## Gamma Dinamica

> [!INFO]
> ![[1. Quantizzazione#Gamma Dinamica]]

$$

\frac RQ = 2^B = \frac{M_{FP}}{N_{FP}}

$$

Pensando ad $R$ e $Q$ come i range del __rumore del segnale__ ($R$) e del __rumore di quantizzazione__ ($Q$), il loro rapporto è la __gamma dinamica__, che può essere espresso in $dB$:

$$

20\log_{10}(\frac RQ) = 6B \;dB

$$

## Rapporto Segnale-Rumore

![[immagini/errore.svg|center mid]]

$$

-\frac Q2 < \text{e}(n) \leq \frac Q2

$$

Il rapporto segnale-rumore di quantizzazione (__SQNR__) è dato da:

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

se lo riteniamo _scollegato_ rispetto al segnale, allora lo definiamo come __rumore di quantizzazione__:

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
>
>$$
>P_x(x)=\frac{\lambda}{2}e^{-\lambda|x|} \quad\quad \lambda^2 = \frac 2{\sigma^2}
>$$
>
>$$
>\frac{\partial g(x)}{\partial x} = P_x(x);\quad  x > 0
>$$
>
>$$
>g(x) = \frac R2 (1- e^{-\lambda x}); \quad x > 0
>$$
>
>Bisogna provare che rispetta le proprietà:
>- $\eta = g(x) = \frac R2(1 - e^{-\lambda x}); \quad x > 0$
>- $x = g^{-1}(\eta) = -\frac 1\lambda\ln[1-2\eta]; \quad 0 \leq \eta < \frac R2$
>
>Questo per i valori positivi di $x$ e $\eta$. La simmetria viene utilizzata per ottenere i valori equivalenti negativi.

La tecnica di __companding__ indica la compressione e l'espansione, ovvero la modifica e il ritorno alla funzione originale.

>[!NOTE]
>Quando parlo di __quantizzazione ottima__ mi riferisco alla _quantizzazione di Max_, dove il mio obiettivo è quello di massimizzare la SQNR.
>Non sempre un approccio non lineare serve a massimizzare la SQNR, quindi la chiamiamo genericamente __quantizzazione non lineare__

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

$$
\eta = g(x) = \frac{\ln(1+\mu |x|)}{\ln(1+\mu)}
$$

Questa è la formula calcolata e inserita nella LUT, con $\mu = 0$ si ha la quantizzazione lineare.

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
>
> $$
>  \begin{align*}
> x(t)\bigg|_{t=nT} = x(nT) & = \sum_{n = -\infty}^{\infty}x(n)e^{-j2\pi f (nT)} \\
> & = \sum_{n = -\infty}^{\infty}x(n)e^{-j\frac{2\pi f}{f_c} n}
> \end{align*} 
> $$
>
> $$
> T = \frac 1{f_c}
> $$

La risposta in frequenza $H(\omega)$ di un sistema lineare $h(n)$ è sempre la sua DTFT.

## Frequenza Digitale ($\omega$) E Intervallo Di Nyquist

La frequenza digitale (non è veramente una frequenza) è un'unità espressa in radianti/campione, ed è relazionata alla __frequenza fisica__ $f$ (in Hz) da:

$$
\omega = \frac{2 \pi f}{f_c}
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

### IDTFT

L'inversa della DTFT serve a recuperare la sequenza nel dominio del tempo discreto $x(n)$, dato lo spettro $X(\omega)$ nell'intervallo di Nyquist.

$$
x(n) = \frac1{2\pi}\int_{-\pi}^{\pi} X(\omega) e^{j\omega n}\; \mathrm d\omega
$$

Esprime $x(n)$ come una __combinazione lineare__ di sinusoidi in tempo-discreto $e^{j\omega n}$ con diverse frequenze.

Le relative ampiezze e fasi di queste sinusoidi sono fornite dalla DTFT $X(\omega)$.

## Proprietà Della DTFT

La DTFT ha le medesime proprietà della Trasformata di Fourier in tempo continuo, ovviamente adattate per funzionare in tempo discreto.

### Ampiezze E Fasi Del Segnale

La DTFT di un segnale $x(n)$ è una funzione a valori complessi, pertanto può essere caratterizzata da una parte reale $Re X(\omega)$ e una immaginaria $Im X(\omega)$, o in forma polare dal suo modulo $|X(\omega)|$ e la sua fase $arg X(\omega)$.

$$
X(\omega) = Re X(\omega) + j Im X (\omega) = |X(\omega)|e^{j arg X(\omega)}
$$

Per segnali a valore reale di $x(n)$, $X(\omega)$ soddisfa la __proprietà hermitiana__.

### Risposta Impulsiva E in Frequenza

La risposta impulsiva in tempo discreto $h(n)$ è data da una __variante tempo-discreta dell'impulso di Dirach__, dove ogni campione ha valore 0, tranne con $n=0$, dove ha valore 1.

La risposta in frequenza, è la DTFT della risposta impulsiva:

$$
H(\omega) =  \sum_{n = -\infty}^{\infty}h(n)e^{-j\omega n}
$$

### Proprietà Del Filtraggio

$$
Y(\omega) = H(\omega) \cdot X(\omega)
$$

$$
y[n] = h[n] \ast x[n]
$$

### Equazioni Di Parzeval

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

$$

\begin{align}
X_D(\omega) & = \sum_{n = 0}^{L+D-1}x_D(n)e^{-j\omega n} \\
&= \sum_{n = 0}^{L-1}x_D(n) e^{-j \omega n} &+& \sum_{n = L}^{L+D-1} 0 e^{-j\omega n}\\
&= \sum_{n = 0}^{L-1}x(n) e^{-j\omega n} &+& 0\\
&=X(\omega)
\end{align}

$$

## Complessità Della DFT

![[#^6ad93d]]

$$
x(n)e^{-j\omega_k n} = x(n)(\cos(\omega_kn) -j\sin(\omega_kn))
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
x(n) \neq 0 \, \text{per}\, 0 < n<L-1,\quad L >> N$$
Si osserveranno **fenomeni di transitorio** e si otterrà quindi la sequenza $y(n)$ **più lunga** rispetto alla sequenza in ingresso $x(n)$.

### Fenomeni Di Transitorio

Si tratta di 3 fenomeni:
- Il **transitorio di attacco** si ha quando la memoria del registro è vuota e inizia a riempirsi, in questo caso si avranno i valori inizialmente con valore 0 che pian piano verranno rimpiazzati dal primo valore e dai seguenti.
- Una volta riempita la memoria si ha la **risposta a regime**, dove nel registro circolare scorrono i nuovi valori eliminando quelli più vecchi.
- Quando il segnale termina il registro circolare inizia a svuotarsi, questa fase si chiama **transitorio di rilascio**, l'esecuzione termina quando tutti i campioni tornano a 0.

## Convoluzione Circolare

Nella [[4. Spettro in frequenza - DTFT|DTFT]] utilizziamo la [[Lezioni integrative DSP-merged#Convoluzione Lineare (Integrale Di Convoluzione)|Convoluzione Lineare]]  come nel tempo continuo, questo però non possiamo farlo con la DFT.

>[!IMPORTANT]
>Dobbiamo imporre il vincolo secondo cui le sequenze hanno __durata finita__.

- $x_1(n) \quad 0 \leq n \leq L-1$
- $x_2(n) \quad 0 \leq n  \leq M-1$

Possiamo calcolare le DFT considerando $N \geq \max(L,M)$:
$$

\begin{align}
X_1(\omega_k) = \text{DFT}_N\{x_1(n)\} &\\
& \quad0 \leq k \leq N-1\\
X_2(\omega_k) = \text{DFT}_N\{x_2(n)\}
\end{align}

$$
$$

\begin{align}
x_3(n) & = x_1(n) \circledast x_2(n) \\ \\
\updownarrow F & \quad \updownarrow F \quad \updownarrow F\\
\\
X_3(\omega_k) & = X_1(\omega_k) \cdot X_2(\omega_k)
\end{align}

$$

La DFT mantiene la lunghezza delle sequenze in quanto diventano __periodiche__ di lunghezza $N$.

Si chiama convoluzione circolare proprio perché lavora su sequenze periodiche (circolari).

![[circ_conv_1.jpg|center]]
![[circ_conv_2.jpg|center]]



# 6. Finestratura

![[schema_blocchi_finestra.svg|center big]]
1. Progettazione del filtro passa basso in base alle frequenze di lavoro
2. Progettazione ADC in base al rumore e al SQNR
3. Progettazione della finestra, porta ad un ulteriore perdita di frequenze
4. Calcolo della DFT/FFT con precisione da determinare

Dobbiamo studiare la finestratura nella DTFT, perché la DFT lavora soltanto con segnali finiti.

$$

w(n) = \begin{cases}
1, & 0 \leq n \leq L-1\\
0, & \text{altrove}
\end{cases}

$$

$$

x_L(n) = x(n) \cdot w(n) = w(n) = \begin{cases}
x(n), & 0 \leq n \leq L-1\\
0, & \text{altrove}
\end{cases}

$$

$$

\begin{align*}
X(\omega) &= \sum_{n=-\infty}^{\infty}x(n)e^{-j\omega n}\\\\
X_L(\omega) &= \sum_{n=0}^{L-1}x(n)e^{-j\omega n}\\\\

&X(\omega) \neq X_L(\omega)
\end{align*}

$$

$$

\begin{align}
x_L(n) & = x(n) \cdot w(n) \\ \\
\updownarrow F & \quad \updownarrow F \quad \updownarrow F\\
\\
X_L(\omega) & = X(\omega) * W(\omega)
\end{align}

$$

## Finestra Nel Dominio Delle Frequenze

Si ha quindi che la formula per il segnale finestrato nel dominio delle frequenze è:

$$

X_L(\omega) = \int_{-\pi}^{\pi}X(\omega)\cdot W(\omega) \; \mathrm d \frac \omega{2\pi}

$$

Ma qual è la formula della funzione finestra? Calcoliamo la DTFT:

>[!NOTE] Serie geometrica
>
>$$
>\sum_{k=0}^n x^k = \frac {1-x^{n+1}}{1-x}
>$$

$$

\begin{align}
W(\omega) &= \sum_{n =-\infty}^{+\infty}w[n]e^{-j\omega n} = \sum_{n = 0}^{L-1}w[n]e^{-j\omega n} = \sum_{n=0}^{L-1}e^{-j\omega n}\\
&= \frac{1- e^{-j\omega L}}{1-e^{-j\omega}}=\frac{\sin(\omega L /2)}{\sin(\omega/2)} \cdot e^{-j\omega(L-1) /2}
\end{align}

$$

Dove la prima parte rappresenta il __modulo__ e la seconda la __fase__.

In particolare il modulo di $W(\omega)$ può essere ricondotto alla rappresentazione di un qualcosa di simile ad un _sinc_ con periodicità $2\pi$.

![[sidelobes.png|center]]

### Frequency Leakage

Creare una finestra porta al __frequency leakage__, ovvero l'inserimento di frequenze spurie (sidelobes) non presenti nel segnale originale, causato da taglio netto del segnale ai lati della finestra.

Porta anche ad una perdita di __risoluzione delle frequenze__, rendendo più difficile riconoscere sinusoidi diverse.

>[!IMPORTANT] Risoluzione in frequenza
>La distanza minima in frequenza che due toni sinusoidali possono avere per essere comunque distinguibili nel segnale.
>Nella finestratura è limitato dalla lunghezza dei dati

$$

\Delta f = \frac 1{T_L}

$$

![[ris_frequenza.png|center]]

Se $\Delta f$ è troppo piccolo i 2 segnali si possono confondere, questo ci porta a __diminuire__ la gamma delle ampiezze che possiamo utilizzare.

Non possiamo migliorare la situazione aumentando la risoluzione, bisogna utilizzare delle finestre in grado di generare uno spettro con lobi meno marcati, per farlo queste finestre dovranno effettuare un troncamento meno netto delle frequenze.

## Finestra Di Hanning

Finestra a forma di coseno rialzato:

$$

w(n) = \begin{cases}
0.54 - 0.46\cos(\frac{2\pi}{L-1}), &0\leq n\leq L-1\\
0&\text{altrimenti}
\end{cases}

$$

![[hamming.png|center]]

Ho dimezzato la risoluzione rispetto alla finestra rettangolare, ma per raggiungere il nostro target ci basta aumentare $L$.

# Finestre Parametriche Di Kaiser

$$

w(n) = \frac{I_0(\alpha \sqrt{1- \frac{(n-M)^2}{M^2} })}{I_0(\alpha)}
$$

>[!NOTE]
>$I_0$ è la [Funzione di Bessel](https://www.mhtlab.uwaterloo.ca/courses/me755/web_chap4.pdf) modificata del primo tipo e di ordine 0

Possiamo generare una finestra parametrica tramite le equazioni sviluppate da Kaiser, dati l'attenuazione dei lobi laterali $R$ e la risoluzione in frequenza $\Delta f$, ricaviamo la lunghezza $L$ e il __parametro di forma__ $\alpha$ della finestra:

$$
L -1 = \frac{c f_c}{\Delta f_w} \iff \Delta f_w = \frac{cf_c}{L-1}
$$

$$
c = \frac{6 (R+12)}{155}
$$

$$
\alpha = \begin{cases}
0, & R < 13.26\\
0.76609(R - 13.26)^{0.4} + 0.09834(R-13.26), &13.26<R<60\\
0.12438(R+6.3), &60<R<120
\end{cases}$$

>[!important]
>__Non possiamo__ utilizzare la finestra di Kaiser per valori di attenuazione __superiori__ a 120 dB.


In generale, per abbassare i lobi laterali bisogna aumentare $c$ o diminuire la risoluzione in frequenza $\Delta f$.

In questo modo sono in grado calcolare L in base alla frequenza di campionamento, $c$ e la risoluzione in frequenza:

| __Finestra__ |   __R__   |         __c__         |
| :----------: | :-------: | :-------------------: |
| Rettangolare |  -13 dB   |           1           |
|   Hanning    |  -40 dB   |           2           |
|    Kaiser    | Variabile | $\frac{6(R+12)}{155}$ |

Possiamo avere la dimensione dei lobi che vogliamo variando $R$, modificando di conseguenza anche $c$.

 



# 7. Stima Spettrale Di Segnali Non Stazionari

Un segnale stazionario _non varia_ le sue caratteristiche nel tempo (ampiezza e frequenze), a differenza di un segnale __non stazionario__ che modifica il suo spettro nel tempo.

Per trattare questi segnali incontro 2 problemi:

1. Come varia lo spettro nel tempo (spettro istantaneo)
2. Spettro medio

Bisogna determinare un __intervallo di tempo__ abbastanza piccolo da poter considerare il segnale in quell'intervallo come stazionario.

Quasi tutti i segnali possono essere rappresentati come stazionari __a tratti__.

>[!IMPORTANT] Tempo di stazionarietà
>L'intervallo di tempo dove il segnale è stazionario.

## Short-Time Fourier Transform

$$
x(k,m) = \sum_{n=mL}^{(m+1)L -1}x(n)e^{j\frac{2\pi mk}{N}}
$$

Calcola la DFT per il tempo di stazionarietà

![[schema_blocchi_stazionario.svg|center]]



# 8. Filtri FIR - Finite Impulse Response

![[Filtri_FIR.svg|center mid]]

Creare un filtro con dei tagli netti nella banda è fisicamente impossibile, perché portano una risposta impulsiva di durata infinita.

## Comportamenti Di Non Idealità

Nel caso ideale il valore della _banda passante_ è 1, ma nella realtà questo oscilla intorno a 1 con un valore $\delta_{\text{pass}}$ (ripple in banda passante), quindi tra $[1 - \delta_{\text{pass}}, 1+ \delta_{\text{pass}}]$.

Nella _banda di arresto_ il valore dovrebbe essere 0, ma nella realtà è impossibile e si cerca di tenere la _risposta in frequenza_ al di sotto di un valore $\delta_{\text{stop}}$.

>[!IMPORTANT] Attenuazione in banda d'arresto
>L'__attenuazione in banda di arresto__ è la differenza in _dB_ tra la risposta in frequenza nella banda passante e quella della banda d'arresto.

$f_{\text{pass}}$ indica il punto in cui la risposta in frequenza della banda passante diminuisce fino a superare $1 - \delta_{\text{pass}}$ raggiungendo la banda d'arresto accettata al punto $f_{\text{stop}}$.

>[!NOTE] Selettività dei filtri
> Un filtro è detto selettivo se ha la banda di transizione più stretta possibile.
> Più la banda di transizione è stretta, più il filtro è selettivo.

### Ritardi

Il filtro FIR produce un ritardo per ogni frequenza (proprietà della linearità della fase). Questo serve a garantire la stabilità del sistema. Il ritardo prodotto è pari alla metà del suo ordine.

## Progettare Un Filtro FIR - Metodo Delle Finestre

Per prima cosa bisogna scrivere la formula che vogliamo per $D(\omega)$ e calcoliamo la [[4. Spettro in frequenza - DTFT#IDTFT|IDTFT]] per ricavare $d(k)$:

$$
D(\omega) = \sum_{k=-\infty}^{\infty}d(k) e^{j\omega k} \iff d(k) = \int_{-\pi}^{\pi}D(\omega)e^{j\omega k}\;\frac{\mathrm d\omega}{2\pi}
$$

In genere, la __risposta impulsiva__ è infinita e simmetrica al centro.

>[!EXAMPLE] Filtro passa basso (LP)
>
>$$D(\omega) = \begin{cases}1, & -\omega_c \leq \omega \leq \omega_c \\ 0, & -\pi \leq \omega < -\omega_c \wedge \omega_c < \omega \leq \pi \end{cases}$$
>
>$$\begin{align}d(k) &= \int_{-\pi}^{\pi}D(\omega)e^{j\omega k} \frac{\mathrm d \omega}{2\pi} = \int_{-\omega_c}^{\omega_c} 1 \cdot e^{j\omega k} \frac{\mathrm d \omega}{2\pi} \\&= [\frac{e^{j \omega k}}{2 \pi}]^{\omega_c}_{-\omega_c} = \frac{e^{j\omega_c k} - e^{-j \omega_c k}}{2 \pi j k}\end{align}$$
>
>Che può essere riscritto come:
>
>$$d(k) = \frac{\sin(\omega_c k)}{\pi k} \quad -\infty < k < \infty$$
>
>$$d(0) = \frac {\omega_c}\pi$$
>
>Un filtro è fatto bene se __ha i nulli ai multipli di L__

>[!EXAMPLE] Altri filtri
>### Passa alto (HP)
>Si può sfruttare la __proprietà di complementarietà__ della risposta in frequenza:
>
>$$\underset{HP}{D(\omega)} = 1 - \underset{LP}{D(\omega)} \to \underset{HP}{d(k)} = \delta(k) - \underset{LP}{d(k)}$$
>
>### Passa banda (BP)
>Si calcola con la differenza tra due filtri passa basso
>
>$$\underset{BP}{D(\omega)} = \underset{LP_b}{D(\omega)} - \underset{LP_a}{D(\omega)}$$
>
>### Arresta banda (BS)
>
>$$\underset{BS}{D(\omega)} = 1 - \underset{BP}{D(\omega)}$$

### Causalità

Una sequenza che parte per $h = 0$ è detta __causale__.

Un segnale __anticausale__ è un segnale presente in precedennza e che termina nel momento in cui inizio a osservarlo.

Un segnale __misto__ è sempre esistito e continua ad esistere anche dopo.

Il concetto di casualità cambia se si osserva nello __spazio__ invece che nel _tempo_:

$$y(n) = \sum_{k=-M}^Mh(k)x(n-k) = \sum_{k=0}^Mh(k)x(n-k) + \overbracket{\sum_{k=-M}^{-1}h(k)\underbracket{x(n-k)}_{\text{campioni futuri}}}^{\text{non lo posso calcolare}}
$$

Per poterlo calcolare possiamo effettuare la finestratura della risposta impulsiva così da renderla di durata finita.

Ovviamente, se sto valutando segnali in real time non posso avere la parte anticausale, e non possiamo nemmeno spostare la risposta impulsiva in modo che sia causale, perché in entrambi i casi si genera un __ritardo__.

>[!IMPORTANT]
>I filtri FIR hanno __sempre__ un ritardo di $M = \frac N2$ campioni.

### Finestratura Rettangolare

$$
d(k) = \int_{-\pi}^{\pi}D(\omega)e^{j\omega k}\frac {\mathrm d \omega}{2\pi}, \quad -M \leq k \leq M 
$$

Effettuo un taglio netto (sappiamo già che non è fisicamente possibile) nella risposta impulsiva M campioni prima e dopo lo 0, avrò quindi un _numero di coefficienti_ __dispari__ $N = 2M + 1$.

$$
d=[d_{-M}, d_{-M+1}, ..., d_{-1}, d_0, d_1, ..., d_{M -1}, d_M]
$$

L'origine $k=0$ sta al centro del risposta impulsiva ($d_0$), abbiamo quindi un filtro misto. Per rendere il filtro __causale__ dobbiamo __spostare__ l'origine temporale verso sinistra, generando di fatto un __ritardo di $M$ campioni__.

$$
h(k) = d(k) = [h_0, h_1, ..., h_N]
$$

Il filtro $h(k)$ è lo stesso di $d(k)$, ma con l'indicizzazione che inizia dal primo campione.

>[!EXAMPLE] Filtro passa basso
>L'approssimazione del filtro passa basso ideale sarebbe:

$$
h(n) = d(n - M) = \frac {\sin(\omega_c (n - M))}{\pi (n - M)}, \quad n=0,...,M,...,N-1
>
$$

Infine per calcolare il segnale filtrato si segue la formula:

$$
y(n) = \sum_{k=0}^{2M}h(k)x(n-k)
$$

Nel dominio delle frequenze, l'approssimazione di $D(\omega)$ è equivalente al __troncamento__ della DTFT, nella somma finita:

$$
\hat D(\omega) = \sum_{k = -M}^Md(k) e^{-j\omega k}
$$

$$
H(\omega) = e^{-j\omega M} \hat D(\omega) = e^{-j\omega M}\sum_{k = -M}^Md(k) e^{-j\omega k}
$$

La __proprietà di linearità della fase__ è una conseguenza diretta di questa equazione.

$\hat D(\omega)$ troncato ha le stesse proprietà di simmetria/antisimmetria di $D(\omega)$. Quindi nel caso simmetrico, $\hat D(\omega)$ è reale e pari in $\omega$. Segue che il filtro FIR progettato avrà __fase lineare__, derivante dal __fattore di ritardo__ $e^{-j \omega M}$.

#### Approssimazione Del Filtro Ideale

Prendiamo come esempio un filtro passa basso ideale, con cutoff $\omega_c = 0.3 \pi$, con una finestra di dimensione $N=41$ e un'altra di dimensione $N=121$.

per la prima avremo:

$$h(n) = d(n - 20) = \frac{\sin(0.3 \pi ( n- 20))}{\pi (n - 20)}, \quad N = 0,...,40
$$

e per la seconda:

$$h(n) = d(n - 60) = \frac{\sin(0.3 \pi ( n- 60))}{\pi (n - 60)}, \quad N = 0,...,120
$$

La loro risposta impulsiva sarà:
![[FIR_rec_window_response.png|center big]]
Mentre la risposta in frequenza:
![[FIR_rec_window_freq_res.png|center big]]

I ripple che si vedono nella risposta in frequenza sono dati dalla [[6. Finestratura#Finestra Nel Dominio Delle Frequenze|finestra rettangolare]].

La formula del filtro $h(n)$ per segnali _infiniti_ è infatti:

$$h(n) = w(n) d(n-M), \quad -\infty < n<\infty
$$

E nel dominio delle frequenze:

$$\begin{align}H(\omega) &= \int_{-\pi}^\pi W(\omega - \omega') e^{-j\omega' M} D(\omega') \frac{\mathrm d \omega'}{2 \pi}\\ &= \int_{-\omega_c}^{\omega_c} W(\omega - \omega') e^{-j\omega' M} \frac{\mathrm d \omega'}{2\pi}\end{align}
$$

Possiamo notare 3 differenze principali tra le due risposte in frequenza:

1. Il ripple diminuisce all'aumentare di $N$, si ha quindi che $\hat D(\omega) \to D(\omega)$ per $N \to\infty$.
2. La banda di transizione diminuisce all'aumentare di $N$.
3. I ripple più grandi tendono a fondersi nel punto di transizione, ma non diminuiscono di dimensione (indipendente da $N$, 8.9%). Eventualmente con $N \to \infty$ questi ripple vengono schiacciati nella discontinuità a $\omega = \omega_c$, occupando un set di dimensione 0. (Fenomeno di Gibbs).

### Finestra Di Hamming

Per eliminare il ripple del 8.9%, dobbiamo rimpiazzare la finestra rettangolare con una che abbia un taglio meno netto ai bordi.

$$w(n) = 0.54 - 0.46\cos(\frac{2\pi n}{N-1}), \quad n=0,1,...,N-1
$$

$$
h(n)=w(n)d(n-M) = [0.54 - 0.46\cos(\frac{2\pi n}{N-1})] \cdot\frac{\sin(\omega_c(n-M))}{\pi(n-M)}$$

![[FIR_hamming_ris_freq.png|center big]]

A parità di dimensione la finestra di Hamming diminuisce significativamente i ripple (sono ancora presenti ma hanno una dimensione dello 0.2%), a scapito di una __banda di transizione più larga__.

### Finestra Di Kaiser

$$w(n) = \frac{I_0(\alpha \sqrt{1 - \frac{ (n - M)^2}{M^2}})}{I_0(\alpha)}$$

Le finestre Rettangolare e di Hamming sono molto semplici ma non ci danno un buon controllo sulle specifiche del filtro da progettare.

Infatti hanno un ripple fisso del 0.2% o 8.9%, e non possiamo cambiarlo in base alle esigenze.

Per questo possiamo progettare i filtri utilizzando le finestre di Kaiser, per farlo dobbiamo individuare una maschera che rappresenti approssimativamente la risposta in frequenza del filtro desiderato.

I valori con cui si specifica questa maschera sono:

- $\delta_{pass}$
- $\delta_{stop}$
- $f_{pass}$
- $f_{stop}$

Le frequenze dove finisce la banda passante e dove inizia la banda di arresto sono relazionate alla __frequenza di taglio__ $f_c$ e alla __banda di transizione__ $\Delta f$:

$$f_c = \frac 12 (f_{pass} + f_{stop}), \quad \Delta f = f_{stop} - f_{pass}$$

Che nella versione normalizzata hanno la formula:
$$\omega_{pass} = \frac {2 \pi f_{pass}}{f_s}, \quad \omega_{stop} = \frac {2 \pi f_{stop}}{f_s}, \quad \omega_{c} = \frac {2 \pi f_{c}}{f_s}, \quad \Delta\omega = \frac {2 \pi \Delta f}{f_s}$$

Mentre il valore di __attenuazione__ del segnale (in dB) si calcola con la formula:

$$A_{pass} = 20 \log_{10}(\frac{1 + \delta_{pass}}{1 - \delta_{pass}}), \quad A_{stop} = - 20 \log_{10} \delta_{stop}$$
Il metodo di Kaiser __non permette__ di decidere arbitrariamente $A_{pass}$ e $A_{stop}$, ma sono dipendenti l'una dall'altra.

Si sceglie quindi $\delta = \min (\delta_{pass}, \delta_{stop})$, che equivale quasi sempre ad $\delta_{stop}$.

>[!NOTE] Formula inversa
>$$A = -20 \log_{10}(\delta), \quad \delta = 10^{- \frac A{20}}$$

#### Parametro Di Forma

Come per la stima spettrale devo anche calcolare il __parametro di forma__ $\alpha$:

>[!WARNING]
>il parametro di forma ha valori __completamente diversi__ rispetto a quando viene usato nella finestratura, perché nella convoluzione tra 2 forme integro anche i lobi laterali portando a risultati diversi di quelli della stima spettrale.
>$$\alpha = \begin{cases}0.1102(A - 8.7) & A \geq50\\0.5842(A - 21)^{0.4} +0.07886(A - 21) & 21 < A <50\\0& A \leq 21\end{cases}$$
#### Banda Di Transizione E Lunghezza Del Filtro
La banda di transizione dipende dalla lunghezza del filtro ($N$), e viceversa:
$$

\Delta f = \frac{Df_s}{N - 1} \iff N - 1 = \frac{Df_s}{\Delta f}

$$
Il fattore $D$ si ottiene calcolando in termini di $A$:
$$

D = \begin{cases}
\frac{A - 7.95}{14.36} & A > 21\\
0.922 & A \leq 21
\end{cases}

$$
### Passaggi per Progettare Kaiser

1. Calcola $f_c$ e $\Delta f$ partendo dalle frequenze delle bande
2. Calcola $\omega_c = \frac {2\pi f_c}{f_s}$
3. Calcola $\delta_{pass}$ e $\delta_{stop}$
4. Calcola $\delta = \min (\delta_{pass}, \delta_{stop})$ e l'attenuazione $A = -20 \log_{10} \delta$ in dB
5. Calcola $\alpha$ e $D$
6. Calcola la lunghezza $N$ del filtro e arrotondala all'intero _dispari_ più vicino
7. Calcola $M = (N - 1)/2$
8. Calcola la funzione finestra di Kaiser $w(n)$
9. Calcola la risposta impulsiva del segnale finestrato:
$$

h(n) = w(n)d(n-M) = w(n) \frac{\sin(\omega_c(n-M))}{\pi(n-M)}

$$
>[!NOTE]
>in particolare avremo
$$h(M) = w(M)\omega_c / \pi = \omega_c / \pi$$
>Dato che $w(M) = 1$

## Metodo Del Campionamento in Frequenza

Nel caso in cui la finestra abbia una risposta in frequenza di forma diversa rispetto a quelle creabili con Kaiser posso applicare il campionamento e poi calcolare $h(w)$ con una [[5. Trasformata discreta di Fourier (DFT)#IDFT|IDFT]].
$$

^14b2ae

\omega_k = \frac{2\pi}{N}k, \quad -M \leq k \leq M

$$
$$

d(k) = IDFT(D(\omega_k))

$$
$$h(n) = w(n) \cdot d(n - M)
$$

## Filtro Sotto-Banda

Scompone il segnale $x(n)$ con spettro $X(f)$ in un numero $M$ di segnali: $x_1(n),x_2(n),…,x_M(n)$

Ogni segnale è __una sottobanda__ del segnale originale, e

$$

\sum_{i=1}^Mx_i(n) = x(n)

$$

Per soddisfare questi vincoli consideriamo $M$ filtri:

$$

h_1(n), h_2(n),…,h_M(n)

$$

Che nel mondo reale significa:
- Le bande di transizione sono __sovrapposte__ e __complementari__ ($f_{pass}$ di un filtro corrisponde a $f_{stop}$ di un altro)
- Nel caso della finestra di Kaiser avermo filtri dello __stesso ordine__, che è quello che vogliamo in quanto avremo lo stesso ritardo.
- Stessa attenuazione in banda di arresto



# 9. Filtri IIR - Infinite Impulse Response

Come dice il nome, sono filtri con risposta impulsiva infinita.

## Introduzione - Trasformata Z

La Trasformata Z è l'equivalente numerico della Trasformata di Laplace (ambiente analogico).

Permette di progettare i filtri IIR tramite il __calcolo polinomiale__.

$$
\begin{aligned}
\text{FIR} \\
h(n)\neq 0, \quad 0 \leq n \leq N-1\\
y(n) = \sum_{k=0}^{N-1}{h(k)x(n-k)}
\end{aligned}
$$

$$
\begin{aligned}
\text{IIR}\\
h(n)\neq 0, \quad 0\leq n \leq \infty\\

y(n) = \sum_{k=0}^{\infty}{h(k)x(n-k)}
\end{aligned}
$$

Si potrebbe pensare che non sono implementabili.

>[!EXAMPLE] Accumulatore
>Somma tutti i campioni
>
>$$
>y(n) = \sum_{k=0}^{\infty}1x(n-k)
>$$
>
>$$
>\begin{align*}x(0) & \to  y(0) = x(0)& \\x(1) & \to  y(1) = x(1)+y(0) &= x(1) + x(0)\\x(2) & \to  y(2) = x(2) + y(1) &= x(2)+x(1)+x(0)\\\vdots\\x(n) &\to y(n)=x(n)+y(n-1)\end{align*}
>$$
>
>I filtri IIR possono essere sviluppati solo se li riconduco a una __equazione alle differenze__.

### Trasformata Z

$$
X(z) = \sum_{n = -\infty}^\infty x(n) z^{-n} = \underbracket{\sum_{n=-\infty}^{-1}x(n)z^{-n}}_{\text{anticausali}} + \underbracket{\sum_{n=0}^{\infty}x(n)z^{-n}}_{\text{causali}}
$$

dove $z$ è un numero complesso.

Se $x(n)$ è _causale_ avremo $z$ con esponente negativo, se è _anticausale_ avremo esponente positivo, se misto entrambi.

La Trasformata Z si può applicare alla _risposta impulsiva_, diventando la __funzione di trasferimento__:

$$
X(z) = \sum_{n = -\infty}^\infty h(n) z^{-n}
$$

Se $z$ si muove nell'__intervallo di Nyquist__ ($z=e^{j\omega}$) abbiamo la _risposta in frequenza_, la [[4. Spettro in frequenza - DTFT|DTFT]] è quindi associabile alla trasformata z.

>[!NOTE]
>In un filtro FIR la trasformata z è un polinomio in $z^{-1}$ di grado ($N-1$)

### Proprietà Della Trasformata Z

- __Proprietà di linearità__: la Trasformata Z di una combinazione lineare di segnali è uguale alla combinazione lineare della Trasformata Z.
- __Proprietà del ritardo__: ritardare un segnale di $D$ campioni equivale a moltiplicare la Trasformata Z di un fattore $z^{-D}$.
- __Proprietà della convoluzione__: la convoluzione nel dominio del tempo diventa la moltiplicazione nel dominio Z ([[2. Segnali nei sistemi lineari#^05349e|proprietà del filtraggio]]).

Posso scrivere i filtri (normalmente scritti come vettori) in forma chiusa:

$$
h_a = [2,3,5,2], \quad h_b = [1,0,0,0,-1]
$$

$$
h_a = 2\delta(n) + 3 \delta(n-1) + 5 \delta(n-2) + 2 \delta(n-3)
$$

$$
h_b = \delta(n) - \delta(n-4)
$$

$$
\delta(n) \xrightarrow z \sum_{n = -\infty}^\infty\delta(n)z^{-n} = \delta(0)z^{-0} = 1
$$

per la proprietà del ritardo:

$$
\begin{align}\delta(n-1) \xrightarrow z z^{-1} \cdot 1 = z^{-1}\\
\vdots\\
\delta(n-k) \xrightarrow z z^{-k}
\end{align}
$$

$$
h_a = 2 + 3z^{-1} + 5 z^{-2} + 2z^{-3}, \quad h_b = 1 - z^{-4}
$$

### Gradino Unitario

![[Gradino unitario.svg|center big]]

$$
u(n) = \begin{cases}
1 & n \geq 0\\
0 & n < 0
\end{cases}
$$

![[Gradino unitario 1.svg|center big]]

$$
u(n) - u(n-1) = \delta(n)
$$

$$
x(n) - x(n-1) = u(n) - u(n-1) = \delta(n)
$$

$$
X(z) - z^{-1}X(z) = 1
$$

$$
X(z) = \frac 1{1 - z^{-1}}
$$

Ottengo gli stessi valori anche per la versione anticausale, anche se sono totalmente diversi nel dominio del tempo.

### Regione Di Convergenza

$$
ROC = \{z \in C | X(z) = \sum_{n=-\infty}^\infty x(n) z^{-n} \neq \infty\}
$$

La regione di convergenza permette di avere __invertibilità__ nella Trasformata Z, definire la __causalità__ e la __stabilità__ del sistema.
Nella risposta in frequenza questo non poteva accadere in quanto il sistema doveva essere obbligatoriamente stabile.

>[!EXAMPLE]
>
>$$x(n) = (0.5)^n u(n) = p^n u(n)$$
>
>$$\begin{align}X(z) &= \sum_{n = -\infty}^{infty} (0.5)^n u(n) z^{-n} \\&= \sum_{n = 0}^{\infty}(0.5)^n z^{-n} \\&= \sum_{n=0}^{\infty}(\underbracket{0.5 z}_{x}) ^n \\&= \sum_{n=0}^\infty x^n = \frac 1{1 - x} = \frac 1{0.5z^{-1}} = \frac z{z - 0.5}\end{align}$$
>
>è valido solo per $|x| < 1$
>
>$$|x| = |0.5 z^{-1}| < 1 \implies |z| > 0.5$$
>
>$$ROC = \{z \in C : |z| > 0.5\}$$

Possiamo generalizzarla come:

$$
p^n u(n) \to \frac 1{1 - pz^{-1}}
$$

$$
\text{polo} \to z = p\quad |z| > p
$$

La Trasformata Z e la regione di convergenza sono determinate unicamente dal segnale $x(n)$.
È però possibile che due segnali diversi abbiano la stessa Trasformata Z, questi segnali possono essere distinti tra loro dalla loro regione di convergenza.

### Trasformata Z E DTFT

$$
X(z)  =\left.\sum_{n = -\infty}^\infty x(n) z^{-n} \right|_{z= e^{j\omega}} = \sum_{n = -\infty}^\infty x(n) e^{-j\omega n}
$$

Se la Trasformata Z __fa parte del cerchio unitario__, $z$ sarà uguale a $e^{j\omega}$ e si ha quindi la DTFT.
La Trasformata di Fourier (e quindi la risposta in frequenza) esiste solo per segnali stabili.

#### Segnali Marginali

I segnali stabili _marginali_ non hanno uno spettro perché hanno i poli sul cerchio unitario (ex: sinusoidi), per questo la valutazione della Trasformata Z sul cerchio unitario diverge per certi $z$. È comunque intuitivamente utile considerare i loro spettro.

>[!EXAMPLE]
>Sinusoide complessa causale
>
>$$
>x(n) = e^{j \omega_0 n} u(n) \xrightarrow{z} X(z) = \frac 1{1 - e^{j \omega_0 z^{-1}}}
>$$
>
>$$
>\left. X(z) \right|_{z={e^{j\omega}}} = X(\omega) = \frac 1{1 - e^{j\omega_0}\underbracket{e^{-j \omega}}_{z^{-1}}} = \frac 1{1 - e^{j(\omega_0 - \omega)}}
>$$
>
>Che diverge a $\omega = \omega_0$, a causa della complessità. Se fosse stata una sinusoide pura $x(n) = e^{j \omega n}$ il suo spettro sarebbe stato una singola linea concentrata in $\omega = \omega_0$.

## Pattern Poli - Zeri

$$
H(z) = \frac{N(z)}{D(z)} \to H(z) = \frac{\prod_i(1 - z_i \cdot z^{-1})}{\prod_j(1 - p_j \cdot z^{-1})}
$$

La forma dello spettro $X(\omega)$ o $H(\omega)$ è affetta dal __pattern poli/zeri__ della Trasformata Z $X(z)$ o $H(z)$, si tratta delle __posizioni geometriche relative__ dei poli e degli zeri sul __piano z__ (piano complesso).
Per vederlo consideriamo una semplice Trasformata Z avente un singolo polo a $z = p_1$ e un singolo zero a $z=z_1$.

$$
\left. X(z) = \frac{1 - z_1z^{-1}}{1 - p_1z^{-1}} = \frac{z - z_1}{z - p_1} \right|_{z = e^{j\omega}}
$$

Lo spettro corrispondente e la sua magnitudine sono ottenuti rimpiazzando $z$ con $e^{j\omega}$:

$$
X(\omega) = \frac{e^{j\omega} - z_1}{e^{j\omega} - p_1} \implies |X(\omega)| = \frac{|e^{j\omega} - z_1|}{|e^{j\omega} - p_1|}
$$

![[poli_zeri.png|center]]

Più uno zero si avvicina al cerchio unitario, più il $|H(\omega)|$ si avvicina a 0, questa proprietà viene usata per progettare i filtri notch.

È conveniente dividere il cerchio unitario in regioni di basse, medie e alte frequenze a seconda della applicazione. Questo aiuta nel posizionare i poli e gli zeri.

Ad esempio per creare un filtro passa basso che enfatizzi le basse frequenze attenuando le alte, uno dovrebbe piazzare i poli all'interno del cerchio da qualche parte nella zona a basse frequenze e/o gli zeri nella zona ad alte frequenze.

![[cerchio_unitario.png]]

## Sviluppo in Fratti Parziali E Inversa Della Trasformata Z

$$
H(z) = \frac{b_0 + b_1z^{-1} + ... +b_mz^{-m}}{a_0 + a_1z^{-1}+...+a_nz^{-n}} = \frac{\prod_i^m(1-z_iz^{-1})}{\prod_j^n(1-z_jz^{-1})}\to\underbracket{\sum_iA_i\frac 1{1-p_iz^{-1}}}_{\text{fraz. parziale}} \to  \sum_iA_ip_i^n\cdot u(n) = h(n)
$$

Per invertire una trasformata zeta bisogna trovare il segnale $x(n)$ tale che la sua trasformata z sia $X(z)$. Come sappiamo già la risposta __non è necessariamente unica__. Può essere resa unica specificando la ROC corrispondente.

Per invertire una trasformata z è conveniente riscriverla nella sua forma in __fratti parziali__, ovvero come una somma di poli individuali del tipo:

$$
X(z) = \frac{A_1}{1 - p_1z^{-1}} + \frac{A_2}{1 - p_2z^{-1}} + \frac{A_3}{1 - p_3z^{-1}} +...
$$

Una volta scritta in questa forma dobbiamo invertire ogni termine, causalmente o anticausalmente a seconda della ROC scelta.

In genere i cerchi sui poli a $z = p_1, z=p_2$ ecc dividono il piano z in __regioni non sovrapposte__, tutte possibili candidate per la ROC. Ognuna di queste risulterà in un $x(n)$ differente, ma __soltanto una sarà stabile__, perché il cerchio unitario si trova perfettamente in una delle possibili ROC.

Il metodo di decomposizione in fratti parziali può essere applicato alle trasformate z che sono divisioni di polinomi in $z^{-1}$ nella forma:

$$
H(z) = \frac{N(z)}{D(z)} = \frac{b_0 + b_1z^{-1} + ... +b_mz^{-m}}{a_0 + a_1z^{-1}+...+a_nz^{-n}} = \frac{\prod_i^m(1-z_iz^{-1})}{\prod_j^n(1-z_jz^{-1})}
$$

Nel polinomio al _denominatore_ abbiamo i _poli_, in quello al _numeratore_ abbiamo gli _zeri_.

Assumendo che $D(z)$ abbia $n$ poli, e assumendo che possono essere riscritti in forma fattorizzata come:

$$
D(z) = (1 - p_1z^{-1})(1 - p_2z^{-1})...(1 - p_nz^{-1})
$$

L'espansione in fratti parziali è data da

$$
H(z) = \frac{N(z)}{D(z)} = \frac{N(z)}{(1-p_1z^{-1})(1-p_2z^{-1})...(1-p_nz^{-1})} = \frac{A_1}{1-p_1z^{-1}} + ...+\frac{A_n}{1-p_nz^{-1}}
$$

### Caso 1: Grado $N(z) < D(z)$

Per rendere possibile questa espansione come identità in $z^{-1}$, il grado del __polinomio al numeratore__ deve essere __strettamente minore__ del grado $n$ del polinomio al denominatore.

I coefficienti di espansione $A_i$ possono essere calcolati con la formula:

$$
A_i = [(1 - p_iz^{-1})X(z)]_{z=p_i} = \left[\frac{N(z)}{\prod_{j \neq i (1 - p_j z^{-1})}}\right]_{z=p_i} \quad i=1,...,n
$$

In parole, il fattore $(1 - p_iz^{-1})$ viene eliminato dal denominatore e l'espressione rimanente è valutata al polo $z = p_i$.

### Caso 2: Grado $N(z) = D(z)$

Nel caso in cui il grado del polinomio al numeratore sia __uguale__ al grado del denominatore, allora l'espansione in fratti parziali deve __essere modificata__ aggiungendo un termine extra $A_0$. I coefficenti da 1 a $n$ vengono calcolati allo stesso modo, mentre il termine extra viene calcolando valutando la trasformata z con $z=0$:

$$
A_0 =\left. H(z)\right|_{z=0}
$$

### Caso 3: Grado $N(z) > D(z)$

Nel caso in cui il grado del polinomio al numeratore sia __maggiore__ al grado del denominatore, posso dividere il polinomio per $D(z)$ e trovare __quoziente e resto__:

$$
N(z) = Q(z)D(z)+R(z)
$$

$$
H(z) = \frac{N(z)}{D(z)} = \frac{Q(z)D(z) + R(z)}{D(z)} = Q(z) + \frac{R(z)}{D(z)}
$$

Avremo quindi il _secondo termine_ che permette una normale espansione in fratti parziali, perché il grado del polinomio resto $R(z)$ è strettamente minore di $n$.

### Complessi E Coniugati

L'assunzione che al numeratore e al denominatore i polinomi abbiano coefficienti a __valore reale__ implica che i __poli complessi__ di $H(z)$ sono in __coppie di complessi e coniugati__. In tal caso, l'espansione in fratti parziali prende la forma:

$$
H(z) = \frac{A_1}{1 - p_1z^{-1}} + \frac{A_1^*}{1 - p_1^*z^{-1}} + \frac{A_2}{1 - p_2z^{-1}} + \frac{A_2^*}{1 - p_2^*z^{-1}} + ...
$$

 Con la sua corrispondente trasformata z che sarà a _valori reali_.

Infatti, considerando il caso causale avremo:

$$
x(n) = \underbracket{A_1p_1^nu(n) + A_1^*p_1^{*n}u(n)} + A_2p_2^nu(n) + ...
$$

Dato che i primi due termini sono complesso e coniugato, possiamo usare la formula $C + C^* = 2Re(C)$, per ogni numero complesso $C$, per scrivere il primo termine come:

$$
A_1p_1^n + A_1^*p_1^{*n} = 2Re[A_1p_1^n]
$$

Convertendo $A_1$ e $p_1$ nelle loro __forme polari__ avremo:

$$
\begin{align}
A_1 = B_1e^{j\alpha_1},\quad &B_1>0\\
p_1 = R_1e^{j\omega_1},\quad &R_1>0\\
\end{align}
$$

$$
Re[A_1p_1^n] = Re[B_1e^{j\omega_1}R_1^ne^{j\omega_1n}]=B_1R_1^nRe[e^{j\omega_1n+j\alpha_1}]
$$

Se poi prendiamo la parte reale dell'esponenziale troviamo:

$$
A_1p_1^n + A_1^*p_1^{*n} = 2Re[A_1p_1^n] = 2B_1R_1^n\cos(\omega_1 n + \alpha_1)
$$

$$
x(n) = 2B_1R_1^n\cos(\omega_1 n +\alpha_1)u(n) + 2B_2R_2^n\cos(\omega_2 n +\alpha_2)u(n) +...
$$

I poli a valori complessi corrispondono quindi a __sinusoidi decadenti esponenzialmente__ (per $R_1  < 1$).

Il grado di decadimento $R_1^n$ e la frequenza $\omega_1$ dipendono dal _polo complesso_ $p_1 = R_1e^{j\omega_1}$.

## Modalità Equivalenti per Descrivere I Filtri Digitali

![[descrizioni_filtri.png|center]]

- Definisci un insieme di __risposte in frequenza specifiche__
- Tramite il metodo di design dei filtri ottieni la __funzione di trasferimento__ $H(z)$
- A partire da $H(z)$ si può ricavare la realizzazione del __diagramma a blocchi__
- Dal diagramma a blocchi si può ricavare l'__algoritmo di processing__
- Per i __filtri FIR__ si può ottenere la risposta impulsiva e si può effettuare la __convoluzione__
- Per i __filtri IIR__ si può ottenere il __pattern poli/zeri__ e l'__equazione alle differenze__

>[!EXAMPLE]
>
>$$
>H(z) = \frac{5 + 2z^{-1}}{1 - 0.8z^{-1}}
>$$
>
>La risposta impulsiva va fatta tramite lo [[#Sviluppo in Fratti Parziali E Inversa Della Trasformata Z|sviluppo in fratti parziali]]
>
>$$
>H(z) = A_0 + \frac{A_1}{1-0.8z^{-1}} = -2.5 + \frac{7.5}{1 - 0.8z^{-1}}
>$$
>
>Dove $A_0$ e $A_1$ sono ottenuti tramite:
>
>$$
>A_0 = H(z)|_{z=0} =\left. \frac{5 + 2z^{-1}}{1 - 0.8z^{-1}}\right|_{z= 0}=\left. \frac{5z + 2}{z - 0.8}\right|_{z= 0} = \frac{2}{-0.8} = -2.5
>$$
>
>$$
>A_1 = (1 - 0.8z^{-1})H(z)|_{z=0.8} = (5 + 2z^{-1})|_{z =0.8} =5 + \frac 2{0.8} = 7.5 
>$$
>
>Assumendo che il filtro sia causale troviamo:
>
>$$
>h(n) = -2.5\delta (n) + 7.5(0.8)^nu(n)
>$$
>
>In genere però si calcola l'equazione alle differenze togliendo il denominatore:
>
>$$
>(1-0.8z^{-1}) H(z) = 5 + 2z^{-1} \implies H(z) = -0.8z^{-1} H(z) + 5 +2z^{-1} 
>$$
>
>Sfruttando le proprietà di linearità e ritardo calcolo l'inversa di z:
>
>$$
>h(n) = 0.8 h(n-1) + 5\delta(n) +2\delta(n-1)
>$$
>
>Allo stesso modo calcoliamo __L'equazione alle differenze ingresso-uscita__:
>
>$$
> Y(z) = H(z)X(z) 
>$$
>
>$$
> Y(z) = \frac{5+2z^{-1}}{1-0.8z^{-1}}X(z) \implies
>$$
>
>$$
> \begin{align} (1-0.8z^{-1})Y(z)&= (5+2z^{-1})X(z) \\ Y(z) - 0.8 z^{-1} Y(z) &= 5X(z)+2z^{-1}X(z) \\ y(n) - 0.8 y(n-1)&= 5x(n)+2x(n-1) \end{align} 
>$$
>
>$$
>y(n) = 0.8 y(n-1) \underbrace{+5x(n) +2x(n-1)}_{\text{FIR}} 
>$$

Un'uscita di un filtro IIR è composta dall'uscita del filtro FIR più una parte che tiene conto dell'uscita precedente.

$$
y_n = \underbracket{\sum_{i=1}^M a_iy_{n-i}}_{\text{IIR}} + \underbracket{\sum_{j=0}^Lb_jx_{n-j}}_{\text{FIR}}
$$

## Risposta Sinusoidale

Data la __sinusoide complessa__ di frequenza $\omega_0$:

$$
x(n) = e^{j\omega_0 n}, \quad -\infty < n < + \infty
$$

La sua risposta in frequenza si chiama __risposta sinusoidale__. La conoscenza del comportamento delle sinusoidi quando vengono filtrate è essenziale dato che sono i blocchi che costruiscono segnali più complessi.

Se filtriamo la sinusoide con un filtro stabile l'uscita può essere caratterizzata in due modi:

- Usando la convoluzione nel dominio del tempo
- Usando la moltiplicazione nel dominio della frequenza

Se applico la convoluzione:

$$
\begin{align}y(n) &= \sum_m h(m)x(n-m) \\&= \sum_mh(m)e^{j(n-m)\omega_0}\\&=e^{j\omega_0n}\underbracket{\sum_mh(m)e^{-j\omega_0m}}_{\text{DTFT}}\\&=H(\omega_0)e^{j\omega_0n}\end{align}
$$

L'uscita avrà la stessa frequenza dell'ingresso, ma sarà scalata dal modulo della risposta in frequenza $H(\omega_0)$.

Dato che $H(\omega)$ è una funzione a valori complessi, possiamo riscriverla nella forma modulo e fase, osservando la presenza di un __ritardo di fase__ causato dal filtro:

$$
H(\omega_0)e^{j\omega_0n} \to |H(\omega_0)| e^{j\omega_0n + j\arg(H(\omega_0))} 
$$

Abbiamo infatti che il ritardo di fase $d(\omega)$ è dato da:

$$
d(\omega) = - \frac{\arg H(\omega)}{\omega} \implies \arg H(\omega) = -\omega d(\omega)
$$

Mentre il ritardo di gruppo di un filtro è dato da:

$$
d_g(\omega) = - \frac \partial {\partial \omega}\arg H(\omega)
$$

I filtri _a fase lineare_ (tutti i FIR) hanno la proprietà che il loro ritardo è __indipendente dalla frequenza__

$$
d(\omega) = D
$$

Tali filtri hanno infatti tutti i loro componenti in frequenza ritardati della stessa quantità, con un ritardo complessivo in uscita di:

$$
e^{j\omega n} \xrightarrow H |H(\omega) e^{j\omega (n - D)}
$$

Questo ritardo può essere visto dalla IDTFT:

$$
x(n) = \int_{-\pi}^\pi X(\omega)e^{j\omega n} \frac{\mathrm d \omega}{2\pi} \xrightarrow H y(n) = \int_{-\pi}^\pi |H(\omega)|e^{j\omega (n - D)} \frac{\mathrm d \omega}{2\pi}
$$

I filtri IIR che hanno _fase lineare_ in tutto l'intervallo di Nyquist _non_ possono essere progettati. Possono però essere progettati per avere _approssimativamente_ __fase lineare sulla loro banda passante__ (ex: filtri di Bessel).

### Risposta Al Transitorio

L'analisi al transitorio è fondamentale sia perché tutti i segnali hanno un inizio che perché per transitori lunghi devo poter seguire le variazioni nel segnale.

>[!WARNING]
>Non seguire il transitorio per la banda passante, aspetta che la risposta vada a regime

Se iniziamo a filtrare l'input a $n = 0$, il filtro non saprà immediatamente che il segnale in ingresso è una sinusoide.

Il filtro infatti impiega un certo periodo di tempo per __stabilizzarsi__.

L'analisi della risposta del filtro in questo caso può essere eseguita con la trasformata z:

$$
x(n) = e^{j\omega_0 n} u(n)\xrightarrow Z X(z) = \frac 1{1-e^{j\omega_0}z^{-1}}
$$

avente $ROC |z| > |e^{j\omega_0}| = 1$.

Assumiamo di avere un filtro nella forma:

$$
H(z) = \frac{N(z)}{D(z)} = \frac{N(z)}{(1-p_1z^{-1})(1-p_2z^{-1})...(1-p_Mz^{-1})}
$$

con $M$ poli che si trovano strettamente nel cerchio unitario, così che il filtro sia stabile e causale.

L'uscita della trasformata z sarebbe:

$$
Y(z) = H(z)X(z) = \frac{N(z)}{\underbracket {(1-e^{j\omega_0}z^{-1})}_{X(z)} \;\underbracket {(1-p_1z^{-1})(1-p_2z^{-1})...(1-p_Mz^{-1})}_{H(z)}}
$$

Assumendo che il grado del _numeratore_ $N(z)$ sia __strettamente minore__ del grado $M+1$ del _denominatore_, possiamo scrivere l'espansione in fratti parziali come:

$$
Y(z) = \frac C{1 - e^{j\omega_0}z^{-1}} + \frac{B_1}{1 - p_1 z^{-1}} + \frac{B_2}{1 - p_2 z^{-1}} +...+ \frac{B_M}{1 - p_M z^{-1}}
$$

Dove l'equazione del primo termine $C$ è data da:

$$
\begin{align}C &= (1 - e^{j\omega_0}z^{-1})Y(z)|_{z=e^{j\omega_0}} \\&= \left[(1 - e^{j\omega_0}z^{-1}) \frac{H(z)}{1 - e^{j\omega_0}z^{-1}}\right]_{z=e^{j\omega_0}} \\&=H(z)|_{z=e^{j\omega_0}} \\&=H(\omega_0) \end{align}
$$

$$
Y(z) = \frac {H(\omega_0)}{1 - e^{j\omega_0}z^{-1}} + \frac{B_1}{1 - p_1 z^{-1}} + \frac{B_2}{1 - p_2 z^{-1}} +...+ \frac{B_M}{1 - p_M z^{-1}}
$$

 Prendendo la trasformata z inversa nella forma causale (con ROC |z| > 1), troviamo:

 $$
y(n) = H(\omega_0)e^{j\omega_0n} + B_1p_1^n+ B_2p_2^n+ ... + B_Mp_M^n, \quad n \geq 0
$$

 Dato che assumiamo che il filtro abbia i poli tutti all'interno del cerchio unitario, il limite per $n$ grande dei termini $p_i^n$ converge esponenzialmente a 0, e quindi per filtri stabili:

 $$
y(n) \to H(\omega_0)e^{j\omega_0n}, \quad n\to\infty
$$

 Per valori di $n$ più piccoli si avrà invece la risposta al transitorio.

Questo ci fa capire come la __stabilità__ sia un requisito essenziale per i filtri. Se un qualsiasi polo fosse al di fuori del cerchio unitario, il termine $p_i^n$ sarebbe instabile e divergerebbe.

Questo porterebbe al dominio di tutti i poli fuori dal cerchio unitario, a scapito di quelli all'interno, non avendo più una risposta stabile.

Inoltre, assumendo che il filtro debba essere strettamente stabile, tutti i termini transitori $p_i^n$ convergeranno a 0 esponenzialmente, alcuni più velocemente di altri.

La __costante temporale__ per raggiungere la risposta stabile è indicata dal __polo che converge più lentamente__ ovvero il __polo più vicino al cerchio unitario__ (quindi con magnitudine più alta).

Ovviamente questi poli non arrivano mai esattamente a 0, si può quindi definire una certa soglia $\varepsilon$ sotto la cui il filtro si può definire stabile (in genere $\varepsilon = 1\% = 0.01$ ).

La costante temporale effettiva (il numero di campioni dopo i quali il filtro è considerato stabile) può essere calcolata con la formula:

$$
\rho = \max|p_i|,\quad\rho^{n_{\text{eff}}} = \varepsilon
$$

$$
n_{\text{eff}} = \frac{\ln\varepsilon}{\ln \rho} = \frac{\ln(1/\varepsilon)}{\ln(1/ \rho)}
$$

La costante temporale aumenta se abbassiamo $\varepsilon$ oppure se avviciniamo al cerchio unitario $\rho$.

## Filtri Di Primo Ordine - Smoother

Il piazzamento dei poli e degli zeri può essere usato per progettare dei filtri semplici, come i filtri di primo ordine __smoothers__.

L'ordine di un filtro indica quanti poli ha, un filtro di primo ordine ha 1 polo e 1 zero e a seconda della distanza dal cerchio unitario di questi avremo risposte diverse.

$$
H(z) = \frac{G \cdot (1 + bz^{-1})}{1 - az^{-1}}
$$

Sia lo zero che il polo sono a valori reali positivi minori di 1.
Il fattore di gain $G$ è arbitrario e dipende dalle specifiche richieste.

In genere se ho il polo a $\omega = 0$ avrò lo zero a $\omega = \pi$, e viceversa. Equivalgono ai filtri Passa-Basso e Passa-Alto dei FIR.

Si chiamano smoother perché non tagliano direttamente come i filtri FIR, ma attenuano progressivamente la banda fino a raggiungere lo 0.

I valori del filtro con $\omega = 0$ e $\omega = \pi$ si ottengono rimpiazzando $z = \pm 1$:

$$
H(0) = \frac{G \cdot [1 - b(-1)]}{1 - a(+1)} = \frac{G \cdot (1 + b)}{1 - a}
$$

$$
H(\pi) = \frac{G \cdot [1 - b(+1)]}{1 - a(-1)} = \frac{G \cdot (1 - b)}{1 + a}
$$

L'attenuazione della frequenza più alta in relazione alla più bassa sarà:

$$
\frac{H(\pi)}{H(0)} = \frac{(1 - b) ( 1- a)}{(1 + b)(1 + a)}
$$

Dobbiamo determinare ora $a$ e $b$.

Per determinare $a$ possiamo basarci sul valore desiderato della soglia, e quindi anche sulla specifica della durata del transitorio che vogliamo:

$$
\rho^{n_{\text{eff}}} = \varepsilon, \quad n_{\text{eff}} = 20
$$

$$
a = \varepsilon^{1/n_{\text{eff}}} = (0.01)^{1/20} \approx 0.8
$$

Dopo aver trovato $a$ , definiamo qual è il rapporto di attenuazione che deve avere il filtro (ad esempio $\frac{H(\pi)}{H(0)} = \frac 1{21}$) e possiamo ricavare $b$:

$$
\frac{(1 - b) ( 1 - 0.8)}{(1 + b)(1 + 0.8)} = \frac 1{21}  \implies b = 0.4
$$

Abbiamo così definito i parametri per la progettazione del filtro, ci manca solo di definire il gain $G$ desiderato:

$$
H(z) = \frac{G(1 + 0.4z^{-1})}{1 - 0.8z^{-1}}
$$

Ora possiamo calcolare l'output con l'__equazione alle differenze__:

$$
\begin{align}Y(z) &= X(z) H(z)\\ &=X(z)\frac{G(1 + 0.4z^{-1})}{1 - 0.8z^{-1}}\end{align}
$$

$$
(1- 0.8z^{-1})Y(z) = X(z)G(1 + 0.4z^{-1})
$$

$$
Y(z) - 0.8z^{-1}Y(z) = X(z)G + 0.4X(z)Gz^{-1}
$$

$$
\begin{align}y[n] &= 0.8y[n-1] + x[n]G+0.4x[n-1]G\\
&= 0.8y[n-1]+G(x[n]+0.4x[n-1])\end{align}
$$

Questo filtro richiede 3 MACS per essere calcolato.

## Filtri Di Secondo Ordine - Resonator

Un altro esempio è quello dei filtri __resonator__ di secondo ordine, la cui risposta in frequenza è dominata da un singolo picco ai poli.
![[resonator 1.png]]

Per inserire un picco a $\omega = \omega_0$ piazziamo il polo nel cerchio unitario, con angolo di fase $\omega_0$, ovvero alla posizione complessa:

$$
p = Re^{j\omega_0}
$$

insieme anche al suo coniugato:

$$
p^* =Re^{-j\omega_0}
$$

Otteniamo quindi la funzione di trasferimento:

$$
H(z) = \frac{G}{(1 - Re^{j\omega_0}z^{-1})(1 - Re^{-j\omega_0}z^{-1})} = \frac G{1 + a_1z^{-1} + a_2z^{-2}}
$$

Dove $a_1$ e $a_2$ sono i 2 elementi del polinomio ricavati dai poli tramite:

$$
a_1 = -2R\cos\omega_0, \quad a_2 = R^2
$$

### Calcolo Del Gain

Il gain $G$ deve essere fissato per normalizzare il filtro ad $\omega_0$, cosi che $|H(\omega_0)|=1$.
La risposta in frequenza del filtro si ottiene sostituendo $z = e^{j\omega}$:

$$
H(\omega) = \frac G{(1 - Re^{j\omega_0e^{-j\omega}})(1 - Re^{-j\omega_0}e^{-j\omega})} = \frac G{1 + a_1e^{-j\omega} + a_2e^{-2j\omega}}
$$

Il requisito di normalizzazione ci da la condizione:

$$
|H(\omega_0)| = \frac G{|(1 - Re^{j\omega_0e^{-j\omega}})(1 - Re^{-j\omega_0}e^{-j\omega})|}  = 1
$$

$$
G = (1- R) \sqrt{1 - 2R\cos(2\omega_0) + R^2}
$$

### Calcolo Dell'ampiezza

La magnitudine della risposta al quadrato può essere espressa nella forma:

$$
|H(\omega)|^2 = \frac{G^2}{(1 - 2R\cos(\omega - \omega_0) + R^2)(1 - 2R\cos(\omega + \omega_0) + R^2)}
$$

L'ampiezza a 3dB ($\Delta\omega$) del picco è definita come la __larghezza a metà della magnitudine massima della risposta al quadrato__

$$
|H(\omega)|^2 = \frac 12 |H(\omega_0)|^2 = \frac 12
$$

che in dB equivale a:

$$
20\log_{10}\left|\frac{H(\omega)}{H(\omega_0)}\right| = 10\log_{10}\left(\frac12\right) = -3dB
$$

Questa equazione ha 2 soluzioni ($\omega_1$ e $\omega_2$), e l'ampiezza è data da:

$$
\Delta\omega = \omega_2 - \omega_1
$$

Queste due frequenze vengono chiamate frequenze ai 3dB e si può osservare che l'ampiezza dipende dalla vicinanza del polo $p$ al cerchio unitario:

$$
\Delta\omega\simeq 2(1 -R)
$$

Ovviamente possiamo ricavare la distanza $R$ del polo a partire dalla specifica dell'ampiezza.

>[!important]
>Quindi __più sarà vicino il polo__ al cerchio unitario, __più sarà stretta l'ampiezza__ della campana,__più sarà lungo il transitorio__.

La __risposta impulsiva causale__ del filtro può essere ottenuta usando fratti parziali.

Troviamo infatti per $n\geq 0$:

$$
h(n) = \frac G{\sin\omega_0}R^n\sin(\omega_0n +\omega_0)
$$

L'equazione alle differenze per l'output filtrato sarà quindi:

$$
Y(z) = H(z)X(z) = \frac G{1 + a_1z^{-1} + a_2z^{-2}}X(z)
$$

$$
(1 + a_1z^{-1} + a_2{z^{-2}})Y(z) = G\cdot X(z)
$$

$$
y(n)  + a_1y(n-1) + a_2y(n-2) = Gx(n)
$$

$$
y(n) = - a_1y(n-1) - a_2y(n-2) + Gx(n)
$$

>[!example]
>$f_0 = 500Hz, \quad \Delta f  =32Hz, \quad f_s=10kHz$
>Convertiamo in frequenze digitali:
>
>$$
>\omega_0 = \frac{2\pi f_0}{f_s} = 0.1\pi
>$$
>
>$$
>\Delta\omega = \frac {2\pi\Delta f}{f_s} = 0.02\pi
>$$
>
>Troviamo la distanza del polo dal cerchio unitario:
>
>$$
>2(1-R) = 0.02 \implies R  = 0.99
>$$
>
>A partire da $R$ troviamo i parametri del filtro:
>
>$$
>G = 0.0062,\quad a_1 = -1.8831,\quad a_2 = 0.9801
>$$
>
>E scriviamo la formula della funzione di trasferimento del filtro:
>
>$$
>H(z) = \frac{0.0062}{1 - 1.8831z^{-1} + 0.9801z^{-2}}
>$$

## Equalizzatore Parametrico

Si può generalizzare il filtro resonator appena visto piazzando una coppia di zeri nella stessa direzione dei poli, alle posizioni:

$$
z_1 = r\cdot e^{j\omega_0}, \quad z_1^* = r\cdot e^{-j\omega_0}
$$

dove $r$ è la distanza dal centro del cerchio unitario (come $R$), ed ha quindi valori $0 \leq r \leq 1$.

La funzione di trasferimento diventa quindi:

$$
H(z) = \frac{(1 - re^{j\omega_0}z^{-1})(1 - re^{-j\omega_0}z^{-1})}{(1 - Re^{j\omega_0}z^{-1})(1 - Re^{-j\omega_0}z^{-1})} = \frac {1 + b_1z^{-1} + b_2z^{-2}}{1 + a_1z^{-1} + a_2z^{-2}}
$$

dove i coefficienti del polinomio superiore sono ricavati allo stesso modo di quelli al polinomio inferiore:

$$
\begin{align}
b_1 &= -2r\cos\omega_0 & b_2&=r^2\\
a_1 &= -2R\cos\omega_0 & a_2&=R^2
\end{align}
$$

Nel caso in cui il polo è più vicino al cerchio unitario rispetto allo zero ($r < R$) si avrà un __guadagno__ in dB, mentre al contrario ($R < r$) si avrà un'__attenuazione__ in dB.

![[eq_param_pole_zero_pattern.png]]

### Filtro Notch

![[notch.png]]
Nel caso in cui si ponga $r=1$, si avrà un __filtro notch__, e il calcolo dei suoi coefficienti può essere semplificato come:

$$
a_1 = Rb_1 = -2R\cos\omega_0, \quad a_2 = R^2b_2=R^2
$$

$$
H(z) = \frac {1 + b_1z^{-1} + b_2z^{-2}}{1 + a_1z^{-1} + a_2z^{-2}} = \frac{N(z)}{N(R^{-1} z)}
$$

Dove $N(z)$ è ovviamente il polinomio al _numeratore_, avente gli zeri alle posizioni $z = e^{\pm j\omega_0}$:

$$
\begin{align}
N(z)  &=1 + b_1z^{-1}+b_2z^{-2} \\
&=1 - 2z^{-1}\cos\omega_0 + z^{-2}\\
&= (1 - e^{j\omega_0}z^{-1})(1 - e^{-j\omega_0}z^{-1})
\end{align}
$$

### Filtro Comb

Questo metodo può essere generalizzato per costruire un filtro notch con picchi a determinate frequenze.

Se sono presenti $M$ frequenze notch desiderate, allora $N(z)$ sarà definito come un polinomio di grado $M$ con zeri alle frequenze $z_i = e^{j\omega_i}, \quad i = 1,…,M$:

$$
N(z) = \prod_{i = 1}^{M}(1 - e^{j\omega_i}z^{-1})
$$

Il denominatore sarà quindi, per qualche parametro $0 <\rho<1$:

$$
D(z) = N(\rho^{-1}z) = \prod_{i = 1}^M(1 - e^{j\omega_i}\rho z^{-1})
$$

Gli zeri del denominatore $D(z)$ si trovano alla stessa frequenza (e quindi la stessa direzione) degli zeri del notch, ma vengono spinti all'interno del cerchio unitario al raggio $\rho$.

Quindi per ogni zero desiderato $z_i = e^{j\omega_i}$ sarà presente un polo $p_i = \rho e^{j\omega_i}$.

Possiamo scrivere la formula del filtro nella forma espansa come:

$$
H(z) = \frac {N(z)}{N(p^{-1}z)} = \frac{1 + b_1z^{-1} + ... + b_Mz^{-M}}{1 + \rho^1 b_1z^{-1} + ... + \rho^Mb_Mz^{-M}}
$$

Dove i coefficienti del dominatore, sono scelti come __versioni scalate__ dei coefficienti del numeratore:

$$
a_1 = p^ib_i, \quad i=1,...,M
$$

Se $\rho\lesssim 1$ le distanze tra polo e zero diminuiscono e il picco del filtro si restringe.

![[comb.png]]

>[!NOTE]
>Se si muovono gli zeri dal cerchio unitario "dietro" i poli, il filtro cambierà funzionamento e invece di attenuare le frequenze volute, le amplificherà.
>
>![[comb_inverso.png]]



# A. Sistemi Multi-Rate

Questi sistemi si basano sui filtri FIR per effettuare __interpolazione, decimazione e rate conversion__.

Fino ad ora abbiamo soltanto sistemi single-rate, dove la frequenza di campionamento $f_s$ non cambia tra input e output.

I sistemi multi-rate lavorano __cambiando le frequenze__ di uscita. Sono utili ad esempio quando bisogna convertire da uno standard ad un altro.

![[esempi_multirate.png]]

Un sistema digitale multi-rate produce la frequenza di campionamento scalata di un valore intero o di un rapporto tra valori interi.

## Interpolazione

![[blocchi_interp.png]]

Nell'interpolazione andremo ad utilizzare una frequenza di campionamento più grande di un certo fattore rispetto a quella del teorema di Nyquist.

Non ha matematicamente senso utilizzare un sovracampionamento del genere, questo procedimento può essere fatto interamente in digitale con una serie di passaggi.

![[ex_interp.svg]]

Si possono calcolare in maniera ideale in digitale perché $f_{s1}$ rispetta il teorema del campionamento, ed ho quindi un segnale campionato matematicamente equivalente.

![[schema_upsampler.png]]

Quando effettuo il campionamento il segnale diventa periodico nelle frequenze, se devo ricostruire il segnale devo costruire un filtro passa basso che ammette solo le frequenze iniziali.

![[filtro_interpolatore.png]]

La frequenza di campionamento $f_s$ è più alta del necessario perché dobbiamo evitare che il filtro FIR prenda le repliche delle frequenze in un altro intervallo.

### Tipi Di Impulsi per L'interpolazione

Per ogni campione $y[n]$, viene emesso un impulso $p(t - nT_s)$ con ampiezza proporzionale al valore dell'impulso.

Il segnale ricavato è la __superposizione__ di tutti gli impulsi:

$$
y(t) = \sum_{n=-\infty}^\infty y[n] p(t - nT_s) \iff p(t) = \frac{\sin(\frac\pi{T_s}t)}{\frac\pi{T_s}t}, \quad -\infty < t < \infty
$$

Gli __impulsi ideali__ non sono realizzabili, dato che hanno durata infinita. Per questo si ricorre a impulsi non ottimali, ma che possono essere effettivamente utilizzati.

Come vedremo successivamente, il problema principale sarà l'__oversampling__.

![[tipi_impulso.png]]

### Zero-order Hold Interpolation (Impulso rettangolare)

![[zero-hold.png]]

Lo zero-order hold è la forma di impulso più semplice, è piatta per tutta la durata dei singoli campioni.

Può avere bassi risultati a meno che non si abbia una frequenza di campionamento abbastanza alta.

### Interpolazione Lineare (Impulso triangolare)

![[linear_interp.png]]

Un impulso triangolare effettua l'interpolazione lineare tra due campioni adiacenti, la sua durata è il doppio di quella dell'impulso rettangolare.

Questo impulso produce un'approssimazione migliore della forma d'onda originale, ma è ancora presente un sostanziale errore.

### Interpolazione Parabolica (Impulso parabolico)

![[interp_parab.png]]

L'interpolazione parabolica ha la durata del doppio di quella triangolare, quindi quattro volte quella rettangolare.

Ha gli zeri a $0$, $\pm T_s$, $\pm 2 T_s , e genera risultati migliori.

### Sovracampionamento per L'interpolazione

Se il segnale originale non varia di molto nella durata dell'impulso è facile ottenere una buona ricostruzione.

Il sovracampionamento è una pratica comune per ottenere un segnale ricostruito accurato, utilizzando un DAC semplice.

Un DAC, che ha tipicamente una risposta $\frac{\sin x}{x}$, rimuove parzialmente le repliche spettrali, mentre il filtro successivo le rimuove completamente. La combinazione di un DAC a scala e del filtro simula la ricostruzione ideale di un filtro analogico.

Il ricostruttore ideale è un filtro passa basso con frequenza di taglio a $f_s /2$. Ha una transizione netta tra la banda passante e quella di arresto.

![[filtro_ricor.png]]

Nelle applicazioni audio, per mantenere un alta qualità del segnale analogico ricostruito, si deve utilizzare un filtro analogico di alta qualità, che potrebbe essere troppo costoso.

Un modo per alleggerire i requisiti per il filtro è quello di aumentare la frequenza di campionamento. Questo causa l'aumento dello spazio tra le repliche e, di conseguenza, richiede requisiti meno stringenti per il filtro passa basso.

![[fir_oversampled.png]]


La stessa conclusione si può raggiungere nel dominio del tempo, dove a frequenze di campionamento diverse si avrà un grafico più o meno simile al segnale originale.

![[oversampling_id.png]]

Questo approccio è però impratico, perché richiede di ricampionare il segnale ad una frequenza più alta.

Per risolvere questo problema si può ricorrere all'utilizzo di un filtro interpolatore, che lavora alla frequenza di campionamento più bassa, per poi filtrarlo.

Rispetto alla nuova frequenza di campionamento data dall'interpolatore, lo spettro dei campioni a bassa rate sarà mostrato come in figura.

>[!note]
>Da notare che il nuovo intervallo di Nyquist è dato dalla nuova frequenza:
>
>$$\left[-\frac{f_s'}{2}, \frac{f_s'}{2}\right]$$
>
>E che quindi all'interno sono presenti delle repliche del vecchio intervallo

![[oversampling_interpolatore.png]]

Questo è anche lo spettro del segnale scalato alla frequenza più alta all'uscita del rate expander.

Si può mettere un filtro passa basso digitale con frequenza di taglio a $f_s' /8$ (nell'esempio dove $L=4$) che opera alla nuova frequenza $f_s'$ così da poter __eliminare le repliche in eccesso__, con risultato uno spettro identico al segnale sovracampionato direttamente alla frequenza più alta.

Il filtro digitale, essendo periodico in $f$ con periodo $f_s'$, non può rimuovere le repliche centrate ai multipli di $f_s'$. Queste verranno poi rimosse dal ricostruttore DA e dal filtro anti repliche quando si effettuerà di nuovo la conversione in analogico.

### Forma Diretta

![[blocchi_interpolatore.png]]

Dati i campioni a bassa rate $x(n)$, i campioni della sequenza interpolata $x_{\text{up}}(n)$ sono dati come:

$$x_{\text{up}}(nL) = x(n)$$

$$x_{\text{up}}(nL + i) = 0, \quad i=1,…,L-1$$

I campioni ai multipli di $L$ rappresentano i campioni iniziali, l'upsampler aggiunge $L-1$ campioni impostati inizialmente a $0$ negli spazi tra i campioni iniziali.

![[campioni_upsampler.png]]

Normalmente posso vedere la periodicità nell'intervallo di Nyquist, ma grazie all'upsampler l'intervallo si allarga e riesco a vedere anche le altre repliche (Come spiegato nella sezione precedente), permettendomi ora di filtrare l'intervallo centrale.

Per calcolare la frequenza di taglio adeguata alla nuova rate, si usano le formule:

$$f_c = \frac{f_s}2 = \frac{f_s'}{2L}, \quad \omega_c' = \frac{2\pi f_c}{f_s'} = \frac \pi L$$

Il filtro interpolatore passa basso deve avere un __guadagno__ di $L$ perché così compensa la presenza dei campioni impostati a 0.

### Tecnica Di Progettazione Polifase

Partendo dal filtro interpolatore progettato, possiamo scrivere l'espressione della sequenza interpolata come:

$$y_{\text{up}}(n') = \sum_{k'=-LM}^{LM} d(k') x_{\text{up}}(n'-k') \quad \text{somma convoluzionale non causale}$$

dove $N=ML$ è la lunghezza del filtro.

Posso risparmiare un fattore pari ad $L$ di costo computazionale costruendo $L$ filtri FIR che lavorano in parallelo invece di un unico filtro interpolatore.

Andiamo a considerare i campioni intermedi tra i campioni a bassa rate $x_{\text{up}}(nL)$ e $x_{\text{up}}(nL + L)$, ovvero i campioni con attualmente valore 0, indicizzandoli con $n'=nL+i, \quad i=0,…,L-1$:

$$y_{\text{up}}(nL+i) = \sum_{k'=-LM}^{LM} d(k') x_{\text{up}}(nL+i-k'), \quad i=0,…,L-1$$

Abbiamo scomposto la singola equazione in $L$ equazioni.

Possiamo fare lo stesso ragionamento con $d(k')$, in quanto ha dimensione $N=2LM + 1$ e posso indicizzarlo con $k' = kL+j$:

$$y_{\text{up}}(nL+i) = \sum_{k'=-M}^{M-1}\sum_{j=0}^{L-1} d(kL+j) x_{\text{up}}(nL+i-kL-j), \quad i=0,…,L-1$$

Possiamo quindi definire $L$ filtri polifase come:

$$d_i(k) = d(kL+i), \quad -M\leq k\leq M-1$$

Il filtro di ordine 0 $d_0(k)$ si comporta come un filtro passa tutto, avrà quindi tutti i valori a 0, tranne per il campione a passo $L$ che avrà il valore esatto dell'equivalente a bassa rate, in formule:

$$\begin{align} x_{\text{up}}(nL) &= x(n) \\ x_{\text{up}}(nL + i) &= 0\end{align}\quad\quad i\neq j$$

Possiamo quindi semplificare la formula mantenendo solo la parte dove $i=j$, ottenendo:

$$\begin{align} y_{\text{up}}(nL+i) &= \sum_{k'=-M}^{M-1}\sum_{j=0}^{L-1} d_j(k) \underbracket {x_{\text{up}}(nL+i-kL-j)}_{\text{0 per } i \neq j}\\ &= \sum_{k=-M}^{M-1}d_i(k)x(nL-kL) \\ y_i(n) &= \sum_{k=-M}^{M-1}d_i(k)x(n-k) \end{align} \quad ,i=0,…,L-1$$

![[filtro_polifase.png]]

## Decimazione

La decimazione è l'operazione inversa dell'interpolazione, ovvero l'operazione di convertire il segnale da una frequenza di campionamento più alta ad una più bassa.

>[!attention]
>Non dobbiamo confondere il _sottocampionamento_ con la __decimazione__, in quanto con la decimazione dobbiamo essere sicuri di __rispettare l'intervallo di Nyquist__.
>
>Nel caso in cui voglio decimare un segnale interpolato in precedenza con lo stesso ordine, allora decimazione e sottocampionamento coincidono.

### Decimatore Ideale

![[decimatore_ideale.svg]]

Devo garantire che il mio segnale abbia spettro fino a $\frac{f_s''}{2}$, creo quindi un filtro passa basso.

Ho una perdita di informazioni irreversibile, ma necessaria per poter rappresentare il segnale alla nuova frequenza di campionamento.

![[blocchi_ideal_decim.png]]

>[!note]
>Ovviamente non possiamo utilizzare i filtri ideali, tipicamente si usano filtri FIR con Kaiser:
>
>$$f_{\text{stop}} < \frac{f_s''}{2}$$
>
>$$\Delta f = 2(\frac{f_s''}{2} - f_{\text{stop}})$$

Il costo computazionale sarebbe $N=2ML$, solo che dovendo scartare i campioni intermedi posso effettuare il calcolo ogni $L$ campioni, portando il costo computazionale equivalente a quello di un filtro polifase $N=2M$.

### ADC Basati Sulla Decimazione

![[adc_decim.png]]

Con il decimatore ho 2 vantaggi principali:
- Il filtro Anti-aliasing è semplificato
- L'ADC veloce può usare meno bit, o a parità di bit ha un rapporto segnale-rumore migliore

## Sample Rate Converter

$$f_s'' = \frac LM f_s'$$

Si implementa concatenando un interpolatore con un decimatore.

>[!important]
>Si potrebbe pensare che l'ordine non conti, ma bisogna ricordare che la decimazione è un'operazione distruttiva (con perdita di dati), bisogna quindi sempre fare __prima l'interpolazione__ e poi la decimazione.

C'è inoltre un vantaggio applicabile all'architettura del rate converter:


![[blocchi_rate_conv.svg]]

Posso quindi implementare un solo filtro con:

$$\omega_c'' = \frac{2\pi f_c}{f_s''} = \min(\frac \pi L, \frac \pi M) = \frac \pi{\max(L,M)}$$

I 2 filtri sono però molto diversi tra loro, quindi in base a quale è più grande dovrò progettare un filtro interpolatore o decimatore.

## Filtri Multi Stadio

Per interpolatori e decimatori con coefficienti molto grandi il filtro rischia di diventare eccessivamente costoso.

Per risolvere il problema si possono implementare più interpolatori in serie, con coefficienti molto più piccoli (si tende a restare sotto il 10).

Nei rate converter si scompone soltanto il componente di cui si deve progettare il filtro.

L'ordine con cui mettere in serie i filtri più piccoli dipende dal convertitore:

- Dal più grande al più piccolo per gli interpolatori
- Dal più piccolo al più grande per i decimatori

![[multi_stato.jpg]]

## Equalizzazione DAC

![[dac_eq_blocchi.png]]

In genere la risposta impulsiva di un DAC è rettangolare con durata il tempo di stazionamento.

In un sistema con oversampling l'uscita dell'interpolatore viene ricostruita da un DAC a scala, che opera alla frequenza interpolata.

In questo caso la sua risposta in frequenza (normalizzata al gain) è:

$$H_{\text{dac}}(f) = \frac{\sin(\pi f / f_s')}{\pi f / f_s'}e^{j \pi f / f_s'}$$

Che causa dell'attenuazione nell'intervallo di Nyquist per un massimo di 4dB.

Per un filtro interpolatore con coefficiente $L$, che ha la frequenza di taglio $f_c = \frac{f_s}2 = \frac{f_s'}{2L}$, la massima attenuazione in banda passante sarà:

$$|H_{\text{dac}}(f)| =\left| \frac{\sin(\pi f / f_s')}{\pi f / f_s'}\right | = \frac{\sin(\pi / 2L)}{\pi / 2L}$$

Per valori molto grandi di $L$ l'attenuazione è insignificante e tendente a 0dB.

Per valori piccoli di $L$ (Ad esempio per $L \leq 8$) è desiderabile compensare questa attenuazione progettando il filtro interpolatore in modo che abbia una __forma inversa__ rispetto alla risposta del DAC nella banda passante.

![[disegno_eq_dac.png]]

Il filtro _equalizzato_ desiderato avrà quindi la formula:

$$D(f) = \begin{cases} 
LD_{\text{eq}}(f), & \text{se } |f| \leq \frac{f_s}2\\
0,& \text{se } \frac{f_s}2 < |f| \leq \frac{f_s'}2
\end{cases}$$
dove $D_{\text{eq}}(f)$ è l'inversa della risposta $H_{\text{dac}}(f)$ con la sua fase rimossa per lavorare solo con la parte reale.

In digitale avremo:

$$D(\omega') = \begin{cases}
L\frac{\omega'/2}{\sin(\omega'/2)}, & \text{se } |\omega'| \leq \frac \pi L\\
0,& \text{se } \frac\pi L < |\omega'| \leq \pi
\end{cases} $$

Tale filtro può essere progettato utilizzando il [[8. Filtri FIR - Finite Impulse Response#^14b2ae|Metodo del campionamento in frequenza]].

Se l'ordine del filtro da progettare è infatti conosciuto (come nel nostro caso dove $N=  2LM + 1$), possiamo calcolare i pesi attraverso la IDFT a N punti:

$$\tilde d(k') = \frac 1N \sum_{i = -LM}^{LM}D(\omega_i')e^{j\omega_i'k'}, \quad -LM \leq k' \leq LM $$

Il filtro finestrato causale risulta come:

$$h(n') = \tilde d(n'-LM)w(n'), \quad 0 \leq n' \leq N-1$$

Dato che il filtro è progettato per salire gradualmente nella banda passante, per ottenere una vera attenuazione con kaiser dobbiamo progettare la finestra con un livello di attenuazione più alto.

Inoltre, dato che l'impulso deve essere a valori reali, dobbiamo rimpiazzare l'equazione scrivendola nella forma del coseno:

$$\tilde d(k') = \frac 1N \sum_{i = -LM}^{LM}D(\omega_i)\cos(\omega_i'k'), \quad -LM \leq k' \leq LM $$

![[freq_sampling.png]]
