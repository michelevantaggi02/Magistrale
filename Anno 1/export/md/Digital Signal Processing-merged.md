# 0. Introduzione

Libri consigliati:
- Orfanidis "Introduction to signal processing" ([download gratuito](https://rutgers.app.box.com/s/5vsu06pp556g9dfsdvayh4k50wqpataw))
- Oge Marques "Practical image and video processing using matlab" ([immagini gratuite](https://ogemarques.com/books/), [libgen](https://libgen.gl/edition.php?id=146257563))

L'esame è diviso in 2 parti:

1. Esercizi al pc su Matlab della durata di 3h. Complesso perché gli esercizi non sono esattamente come fatti a lezione, ti da un problema e devi capire tu come risolverlo (ex: devi capire se progettare un filtro FIR, o un equalizzatore parametrico, o devi effettuare una quantizzazione di un segnale). Puoi però usare qualsiasi strumento, appunti, internet ecc…
2. Orale a domanda secca da cui poi devi dire tutto il possibile, non ancora dato ma impossibile sbagliare (nel senso che se non la sai non puoi cambiare argomento e sei bocciato)



# 1. Quantizzazione

La quantizzazione è un'operazione non lineare e irreversibile che comporta sempre una perdita di informazione, mappando un segnale a valori continui su un insieme finito di livelli discreti.

Nell'elaborazione dei segnali, descriviamo l'effetto della quantizzazione tramite un __modello a rumore additivo__: il segnale quantizzato $x_Q(n)$ è visto come la somma tra il segnale campionato $x(n)$ e una componente di errore $e(n)$:

$$
x_Q(n) = x(n) + e(n) \quad \text{con } e(n) = x_Q(n) - x(n)
$$

Se il segnale varia nell'intera scala senza saturare e attraversa molti livelli di quantizzazione (ipotesi di Widrow/Bennett), possiamo approssimare statisticamente $e(n)$ come una sequenza di rumore bianco scorrelata dall'ingresso, a distribuzione uniforme in $[-\frac Q2, \frac Q2]$, con media nulla e varianza (potenza del rumore):

$$
\sigma_e^2 = E[e^2(n)] = \frac{Q^2}{12}
$$

dove $Q$ indica la __larghezza del livello__ (o passo di quantizzazione / risoluzione, indicato talvolta in letteratura con $\Delta$ o $\text{NFP}$).

> [!tip] Dither (Aggiunta Intenzionale di Rumore)
> La quantizzazione di per sé non aggiunge fisicamente rumore al segnale. Tuttavia, con segnali periodici o a bassa ampiezza (es. una sinusoide di ampiezza inferiore a $\frac Q2$ o audio a basso volume), l'errore $e(n)$ diventa fortemente correlato all'ingresso, generando una fastidiosa distorsione armonica nota come __granulation noise__.
> Per risolvere questo problema si introduce il __dither__: un rumore casuale a basso livello sommato intenzionalmente al segnale _prima_ del quantizzatore:
>
> $$
> x_Q(n) = Q(x(n) + d(n))
> $$
>
> Come dimostrato da __Orfanidis__ (_Capitolo 2, Sez. 2.5 "Analog and Digital Dither", pp. 69–77_), scegliendo un dither con densità di probabilità triangolare (_TPDF dither_) di ampiezza pari a due livelli di quantizzazione ($2Q$):
> - Si __linearizza__ il quantizzatore, eliminando del tutto le armoniche spurie e la correlazione tra errore e segnale.
> - La distorsione armonica viene trasformata in un innocuo fruscio di fondo stazionario (rumore bianco), pagando un incremento del rumore di fondo di 4.8 dB ($10\log_{10} 3$) per il TPDF dither (rispetto ai 3 dB del dither rettangolare RPDF).
> - Il dither si applica sia in forma __analogica__ (prima della conversione A/D) sia in forma __digitale__ (nella riquantizzazione o riduzione della lunghezza di parola, come nel mastering audio da 24 a 16 bit).

## Filtro Anti-Aliasing

![[immagini/ADC.svg|center mid]]

A monte del campionatore (ADC) dobbiamo sempre inserire un __filtro analogico passa-basso anti-aliasing__. Il suo compito è eliminare o attenuare drasticamente tutte le frequenze superiori alla frequenza di Nyquist ($\frac{f_s}2$, dove $f_s$ è la frequenza di campionamento, detta anche $f_c$), impedendo che si ripieghino irreversibilmente all'interno della banda utile del segnale sotto forma di aliasing.

![[immagini/filtro passa basso.svg|center small]]

- __BP__: Banda passante ($0 \le f \le f_{pass}$)
- __BT__: Banda di transizione ($f_{pass} < f < f_{stop}$)
- __BA__: Banda di arresto ($f \ge f_{stop}$, con $f_{stop} \le f_s - f_{pass}$)

> [!example]
> - La voce nella telefonia digitale tradizionale (standard ITU-T G.711 / PCM) ha una banda utile nominale di __300 Hz – 3400 Hz__ ed è campionata a $f_s = 8\text{ kHz}$.
> - Nelle fotocamere digitali l'aliasing è di tipo __spaziale__, causato dalla griglia discreta dei fotositi (pixel) che genera pattern moiré su trame fitte. Per evitarlo si inserisce un filtro ottico passa-basso (__OLPF__, tipicamente una lamina birifrangente di quarzo o niobato di litio) che sfoca leggermente i dettagli a frequenza spaziale troppo elevata. (I filtri IR-cut servono invece a schermare l'infrarosso termico per fedeltà cromatica, non per l'aliasing spaziale).

## Oversampling

Con __oversampling__ (sovracampionamento) si intende la tecnica in cui campioniamo il segnale analogico a una frequenza $f_s' = L \cdot f_s$ molto più alta del minimo di Nyquist ($L \gg 1$, con $L = 2\times, 4\times, 8\times, \dots$).

> [!important]
> L'oversampling __non elimina__ il filtro passa-basso analogico anti-aliasing, ma ne __semplifica enormemente i requisiti circuitali__.
> Spostando la prima replica spettrale a $f_s' = L f_s$, la banda di transizione del filtro analogico diventa larghissima (da $f_{max}$ fino a $L f_s - f_{max}$). Di conseguenza, non abbiamo più bisogno di un costoso e critico filtro analogico di ordine elevato (che introduce forti distorsioni di fase ed è sensibile alle tolleranze dei componenti), ma basta un semplice filtro analogico RC del 1° o 2° ordine.

La selettività accurata viene delegata interamente al dominio digitale:
1. Un __filtro passa-basso digitale__ taglia con precisione ideale tutte le frequenze oltre la banda base $f_{max}$ (i filtri digitali hanno fase perfettamente lineare, zero usura e nessuna deriva termica).
2. Viene eseguita la __decimazione__ (downsampling di un fattore $L$) per riportare la frequenza di campionamento al valore originario $f_s$.

![[immagini/oversampling.svg|center mid]]

- $f_s$: frequenza di campionamento base (rate di Nyquist)
- $f_s'$: frequenza di campionamento sovracampionata ($L \cdot f_s$)

L'oversampling porta anche un fondamentale guadagno sul rumore di quantizzazione (_Orfanidis, Sez. 2.2_): la potenza totale del rumore $\sigma_e^2 = \frac{Q^2}{12}$ si spalma uniformemente sulla banda estesa $[- \frac{L f_s}2, \frac{L f_s}2]$. Il filtro digitale successivo elimina il rumore fuori dalla banda utile, riducendo la potenza di rumore in banda di un fattore $L$:

$$
\sigma_{\text{in-band}}^2 = \frac{\sigma_e^2}{L} = \frac{Q^2}{12 L}
$$

Otteniamo così un incremento dell'SNR pari a $10 \log_{10}(L)\text{ dB}$, che equivale a un guadagno di __0.5 bit di risoluzione per ogni raddoppio della frequenza di campionamento__.

Nei sensori d'immagine l'oversampling spaziale si ottiene aumentando la densità dei pixel sul sensore. Per compensare la minor superficie di raccolta luce dei fotositi più piccoli, in fase di decimazione usiamo il __binning__, che combina il segnale di pixel adiacenti riducendo il rumore.

## Fixed Point

Formato di rappresentazione dei numeri in cui la posizione della virgola binaria è prefissata.
In formato senza segno (_unsigned_) con $D+1$ bit interi e $k$ bit frazionari (lunghezza totale della parola $B = D + 1 + k$ bit):

$$
N = \sum_{i = -k}^D b_i \cdot 2^i
$$

$$
N = b_D b_{D-1}\dots b_1 b_0 \, , \, b_{-1} b_{-2}\dots b_{-k}
$$

La posizione della virgola è un puro riferimento concettuale per noi: l'hardware tratta i registri come normali numeri interi, purché la posizione della virgola sia allineata tra gli operandi.

> [!example]
> Rappresentazione unsigned nell'intervallo $[0, 2)$ a 8 bit (formato UQ1.7):
> Abbiamo 1 bit per la parte intera ($D=0 \implies b_0$) e 7 bit per la frazione ($k=7 \implies b_{-1} \dots b_{-7}$):
>
> $$
> b_0 \, , \, b_{-1} b_{-2} b_{-3} b_{-4} b_{-5} b_{-6} b_{-7}
> $$
>
> _(Se mappati nei bit fisici di un registro a 8 bit $[a_7 \dots a_0]$, $a_7$ corrisponde al bit intero $b_0$ con peso $2^0$, mentre $a_6 \dots a_0$ corrispondono a $b_{-1} \dots b_{-7}$)._
>
> - Il valore minimo rappresentabile è __$0$__ (tutti i bit a zero).
> - Il __passo di risoluzione (LSB / quanto)__ è: $N_{FP} = Q = 2^{-7} = \frac 1{128} \approx 0.0078125$.
> - Il valore massimo rappresentabile è: $M_{FP} = 2 - N_{FP} = 2 - 2^{-7} \approx 1.9921875$.

Possiamo pensare ai numeri in virgola fissa come a una scala con gradini di ampiezza uniforme:

![[immagini/scala virgola fissa.svg|center big]]

Se rappresentiamo in digitale i segnali del mondo reale, emergono chiare limitazioni: l'errore assoluto è limitato ($\le \frac Q2$), ma per valori molto piccoli l'errore relativo cresce a dismisura.

> [!note]
> Nella maggioranza dei processori DSP reali (es. architetture Texas Instruments o ARM), i calcoli in virgola fissa si eseguono in __complemento a due__ (notazione Q con segno, es. Q15 o Q1.15 su 16 bit), dove il bit più significativo (MSB) ha peso negativo: $-b_D \cdot 2^D$.

## Gamma Dinamica

La gamma dinamica (__Dynamic Range__, DR) è il rapporto tra il valore massimo rappresentabile a fondo scala e la minima risoluzione (LSB):

$$
\frac{M_{FP}}{N_{FP}} = 2^B - 1 \approx 2^B = \frac RQ
$$

Espressa in decibel ($dB$):

$$
\text{DR}_{dB} = 20\log_{10}(2^B-1) \approx 20 \log_{10}(2^B) = B(20 \log_{10}2) \approx 6.02 B \text{ dB}
$$

L'unico modo per aumentare i decibel in virgola fissa è aumentare i bit: ogni bit aggiuntivo incrementa la gamma dinamica di circa __6 dB__ (ovvero ne __raddoppia__ l'ampiezza in scala lineare).

> [!important] Differenza tra Gamma Dinamica e SQNR
> Non dobbiamo confondere la Gamma Dinamica (rapporto tra estremi della scala) con il rapporto Segnale-Rumore di Quantizzazione (__SQNR__).
> Come illustrato in _Orfanidis (Cap. 2, Sez. 2.1)_, per un segnale sinusoidale a fondo scala:
>
> $$
> \text{SQNR} \approx 6.02 B + 1.76 \text{ dB}
> $$
>
> Il termine $+1.76\text{ dB}$ ($= 10\log_{10}(1.5)$) tiene conto del valore efficace (RMS) della sinusoide ($P_x = \frac{V_{pp}^2}8$) rispetto alla potenza del rumore di quantizzazione uniforme ($\sigma_e^2 = \frac{Q^2}{12}$).

## Floating Point

Il formato a virgola fissa ha una dinamica ristretta. Per gestire intervalli dinamici molto ampi mantenendo alta la precisione relativa è stato sviluppato il floating point, a fronte di un maggior costo hardware e computazionale.

Un numero in virgola mobile è espresso nella forma:

$$
x = (-1)^s \cdot M \cdot 2^e
$$

dove $s$ è il bit di segno, $M$ è il significante normalizzato ($M = 1.f \in [1, 2)$ per i numeri normalizzati, con $f \in [0, 1)$ campo frazionario) ed $e$ è l'esponente reale.

### Errore Assoluto Vs Errore Relativo

Il floating point è estremamente efficiente perché la densità dei numeri rappresentabili si adatta all'ordine di grandezza:
- Avvicina i numeri tra loro in prossimità dello zero e li allontana per valori grandi.
- L'__errore assoluto__ aumenta con il valore del numero.
- L'__errore relativo__ $\varepsilon_R = \frac{|\hat{x} - x|}{|x|}$ __non è costante__, ma oscilla entro ciascun intervallo di potenze ed è __superiormente limitato__ dall'_unit roundoff_ $u = 2^{-p}$ (pari a metà della _machine epsilon_ $\epsilon_{mach} = 2^{-(p-1)}$, con $p$ bit di significante):

$$
\varepsilon_R \le u = 2^{-p}
$$

> [!example] Esempio intuitivo in base 10 (con mantissa a 4 cifre ed esponente $e$):
>
> $$
> \begin{matrix*}[r]
> A = 0.5655 \cdot 10^e \\
> \varepsilon_A = 0.00005 \cdot 10^e
> \end{matrix*} \quad \implies \quad \varepsilon_R = \frac{0.00005 \cdot 10^e}{0.5655 \cdot 10^e} = \frac{0.00005}{0.5655} \approx 0.0088\%
> $$
>
> Se consideriamo invece il valore minimo normalizzato $0.1000 \cdot 10^e$, l'errore relativo massimo sale a $\frac{0.00005}{0.1000} = 0.05\%$. L'errore relativo quindi non è costante, ma è sempre rigorosamente confinato sotto il limite prefissato su tutta la scala.

### Standard IEEE 754

I due formati standard universali sono:
- __Float a 32 bit (Singola precisione)__: 1 bit segno, 8 bit esponente, 23 bit mantissa (24 bit di significante effettivo $p=24$ con bit intero implicito).
- __Double a 64 bit (Doppia precisione)__: 1 bit segno, 11 bit esponente, 52 bit mantissa (53 bit effettivi $p=53$).

L'esponente è memorizzato in forma polarizzata (_biased exponent_, intero unsigned $E$):

$$
e = E - \text{bias}
$$

Nel formato a 32 bit il bias vale __127__. Per i numeri normalizzati ($1 \le E \le 254$), i valori del campo $E$ coprono un intervallo di esponenti reali da __$-126$ a $+127$__.
Il massimo valore finito normalizzato è $x_{max} = (2 - 2^{-23}) \cdot 2^{127} \approx 2 \cdot 2^{127} = 2^{128}$, mentre il minimo normalizzato positivo è $x_{min} = 1.0 \cdot 2^{-126}$.
La gamma dinamica dei normalizzati di un float a 32 bit è quindi:

$$
\text{DR}_{\text{Float32}} = 20\log_{10}\left(\frac{x_{max}}{x_{min}}\right) \approx 20\log_{10}\left(\frac{2^{128}}{2^{-126}}\right) = 20\log_{10}(2^{254}) \approx 254 \cdot 6.02 \approx 1529 \text{ dB}
$$

superando i $1660\text{ dB}$ includendo i numeri subnormali.

### Valori Speciali IEEE 754

Le combinazioni estreme del campo esponente ($E=0$ ed $E=255$) sono riservate alla gestione di casi speciali:
- __Zero con segno__ ($+0, -0$): $E = 0, f = 0$.
- __Numeri denormalizzati / subnormali__: $E = 0, f \ne 0$. L'esponente reale è fissato convenzionalmente a $e = 1 - \text{bias} = -126$ con significante $0.f$; permettono il _gradual underflow_ continuo evitando salti bruschi a zero per valori inferiori a $2^{-126}$ (fino a $2^{-23} \cdot 2^{-126} = 2^{-149}$).
- __Infinito__ ($+\infty, -\infty$): $E = 255, f = 0$. Segnala overflow o divisioni per zero.
- __NaN (Not a Number)__: $E = 255, f \ne 0$. Risultato di operazioni matematiche indeterminate (come $\frac 00$ o $\sqrt{-1}$).



# 2. Quantizzazione Uniforme

![[immagini/conversione_adc.png|center mid]]

La conversione analogico-digitale (ADC) si compone di due stadi fondamentali: il campionamento temporale e la quantizzazione in ampiezza.
A monte del quantizzatore troviamo il circuito di campionamento e tenuta (__Sample and Hold__, S/H): l'interruttore campiona istantaneamente la tensione analogica a intervalli di campionamento $T$, mentre il condensatore interno mantiene (__hold__) costante tale tensione per l'intera durata della conversione, evitando che il segnale vari mentre il quantizzatore ne codifica il valore.

Un convertitore ADC uniforme è caratterizzato da un __range di fondo scala__ $R$ (la massima escursione di ampiezza accettata in ingresso), suddiviso equamente in $2^B$ __livelli di quantizzazione__, dove $B$ è il numero di bit del convertitore.

La distanza tra due livelli consecutivi prende il nome di __larghezza del livello__ (_quantization width_) o passo di quantizzazione (risoluzione $Q$ o $N_{FP}$):

$$
Q = \frac R{2^B} = N_{FP}
$$

che possiamo riscrivere nella forma:

$$
\frac RQ = 2^B
$$

![[immagini/quantizzazione_segnale.png|center mid]]

## ADC Bipolare E Unipolare

In base all'intervallo delle ampiezze gestite, distinguiamo due configurazioni principali di convertitore:

1. __ADC Bipolare__: accetta segnali con escursione positiva e negativa centrati attorno allo zero:

$$
-\frac R2 \le x(nT) < \frac R2
$$

In formato numerico standard (es. complemento a due su $B$ bit), i $2^B$ livelli discreti coprono l'intervallo da $-\frac R2$ a $\frac R2 - Q$. L'estremo superiore $\frac R2$ è escluso: il livello massimo rappresentabile è sempre $\frac R2 - Q$.

2. __ADC Unipolare__: accetta unicamente segnali positivi compresi tra lo zero e il fondo scala:

$$
0 \le x(nT) < R
$$

I livelli discreti associati sono $y_i = i \cdot Q$ per $i = 0, 1, \dots, 2^B-1$. Anche qui il limite superiore $R$ è escluso, e il livello massimo vale $R - Q$ _(nei quantizzatori unipolari simmetrici mid-riser con arrotondamento, i livelli di ricostruzione centrati negli intervalli sono $y_i = (i + 0.5)Q$ per preservare l'errore $|e| \le Q/2$ su tutto $[0, R)$)_.

Nella pratica ingegneristica, se il segnale analogico $x(t)$ possiede un intervallo di ampiezza non coincidente con quello dell'ADC, deve essere __precondizionato analogicamente__ (tramite circuiti con amplificatori operazionali che applicano opportuni offset e guadagni) per essere adattato all'intervallo del quantizzatore prescelto.

## Errore Di Quantizzazione

Definiamo __errore di quantizzazione__ $e(nT)$ lo scarto tra il campione quantizzato $x_Q(nT)$ e il campione continuo ideale $x(nT)$:

$$
e(nT) = x_Q(nT) - x(nT)
$$

o più semplicemente per un singolo campione $x$:

$$
e = x_Q - x
$$

### Arrotondamento Vs Troncamento

I due metodi principali per mappare un valore continuo sul livello discreto più vicino sono:
- __Arrotondamento (Rounding)__: associa il valore continuo al livello discreto a distanza minima. L'errore è simmetrico e compreso nell'intervallo:

$$
-\frac Q2 < e \le \frac Q2 \implies |e|_{\text{max}} = \frac Q2
$$

- __Troncamento (Truncation)__: taglia semplicemente i bit meno significativi, approssimando sempre per difetto. L'errore risulta asimmetrico e non positivo:

$$
-Q < e \le 0
$$

L'arrotondamento è la scelta d'elezione nel DSP perché non introduce alcun bias continuo ($\bar{e} = 0$) e produce una potenza di errore quattro volte inferiore rispetto alla media quadratica del troncamento ($\frac{Q^2}{12}$ contro $\frac{Q^2}3$).

### Metriche Di Errore Ed Errore RMS

L'errore massimo $e_{\text{max}} = \frac Q2$ rappresenta un limite superiore nel caso peggiore, ma costituisce una stima pessimistica dell'errore tipico.
Per quantificare l'errore medio e l'errore quadratico medio calcoliamo la media e la media quadratica sull'intervallo del quanto:

$$
\bar{e} = \frac 1Q \int_{-\frac Q2}^{\frac Q2} e\,\mathrm{d}e = 0 \quad (\text{media})
$$

$$
\overline{e^2} = \frac 1Q \int_{-\frac Q2}^{\frac Q2} e^2\,\mathrm{d}e = \left. \frac 1Q \frac{e^3}3 \right|_{-\frac Q2}^{\frac Q2} = \frac{Q^2}{12} \quad (\text{media quadratica})
$$

Poiché $\bar{e} = 0$ (metà dei valori viene arrotondata per eccesso e metà per difetto), la media non fornisce informazioni sull'ampiezza tipica dello scarto.
La metrica fondamentale adottata nei sistemi di elaborazione è la __radice dell'errore quadratico medio__ (__RMS__, _Root Mean Square_):

$$
e_{rms} = \sqrt{\overline{e^2}} = \frac Q{\sqrt{12}}
$$

### Modello Statistico Del Rumore Di Quantizzazione

Possiamo interpretare l'errore come una variabile casuale continua $e$ con __distribuzione uniforme__ nell'intervallo $[-\frac Q2, \frac Q2]$:

$$
p(e) = \begin{cases} \frac 1Q & \text{se } -\frac Q2 \le e \le \frac Q2 \\ 0 & \text{altrimenti} \end{cases}
$$

La costante $\frac 1Q$ assicura la corretta normalizzazione dell'area di probabilità:

$$
\int_{-\frac Q2}^{\frac Q2} p(e)\,\mathrm{d}e = 1
$$

I momenti statistici dell'errore (valore atteso) coincidono con le medie calcolate sull'intervallo del quanto (e, per l'ipotesi di ergodicità, con le medie temporali a lungo termine del segnale di errore):
- __Valore atteso (media)__:

$$
E[e] = \int_{-\frac Q2}^{\frac Q2} e \, p(e)\,\mathrm{d}e = 0
$$

- __Potenza media (varianza del rumore)__:

$$
\sigma_e^2 = E[e^2] = \int_{-\frac Q2}^{\frac Q2} e^2 \, p(e)\,\mathrm{d}e = \frac{Q^2}{12}
$$

Questa interpretazione probabilistica è alla base del __modello a rumore additivo__:

$$
x_Q(n) = x(n) + e(n)
$$

Pensiamo al segnale quantizzato $x_Q(n)$ come alla somma tra il segnale originale puro $x(n)$ e una sorgente di rumore additivo $e(n)$.

Sotto le __ipotesi di Widrow/Bennett__ (segnale ad ampia dinamica, che spazia su molti livelli $Q$ e a spettro largo), la sequenza $e(n)$ si comporta come un __rumore bianco stazionario__ con funzione di autocorrelazione impulsiva:

$$
R_{ee}(k) = E[e(n+k)e(n)] = \sigma_e^2 \delta(k) = \frac{Q^2}{12}\delta(k)
$$

ed è statisticamente __incorrelata__ con il segnale d'ingresso (cross-correlazione identicamente nulla):

$$
R_{ex}(k) = E[e(n+k)x(n)] = 0
$$

>[!warning] Limiti del Modello Additivo
>Il modello statistico cessa di essere valido quando il segnale varia lentamente o ha un'ampiezza molto ridotta (inferiore a $\frac Q2$). In quel caso l'errore $e(n)$ diventa periodico e fortemente correlato al segnale, manifestandosi come una sgradevole distorsione armonica (__granulation noise__).
>Come approfondito nel capitolo [[1. Quantizzazione#1. Quantizzazione|1. Quantizzazione]], questo problema si risolve introducendo il __dither__ (rumore casuale a basso livello sommato prima dell'ADC).

## Gamma Dinamica

> [!info]
> ![[1. Quantizzazione#Gamma Dinamica]]

$$
\text{DR} = \frac RQ = 2^B \approx \frac{M_{FP}}{N_{FP}} = 2^B - 1
$$

La __gamma dinamica__ (__Dynamic Range__, DR) quantifica il rapporto tra la massima escursione a fondo scala del segnale ($R$) e la minima variazione risolvibile ($Q$):

$$
\text{DR} = \frac RQ = 2^B
$$

Espressa in decibel ($dB$):

$$
\text{DR}_{\text{dB}} = 20\log_{10}\left(\frac RQ\right) = 20\log_{10}(2^B) = B \cdot (20\log_{10} 2) \approx 6.02 B\text{ dB}
$$

Ogni bit aggiuntivo del quantizzatore raddoppia la scala dinamica in ampiezza, incrementandola di circa __6.02 dB__.

## Rapporto Segnale-Rumore Di Quantizzazione (SQNR)

![[immagini/errore.svg|center mid]]

L'errore istantaneo è rigorosamente confinato entro un quanto di ampiezza:

$$
-\frac Q2 < e(n) \le \frac Q2
$$

Quando le ipotesi statistiche sono verificate, modelliamo l'errore come una sorgente di rumore additivo indipendente:

![[immagini/diagramma rumore.svg|center small]]

Il rapporto segnale-rumore di quantizzazione (__Signal-to-Quantization-Noise Ratio__, SQNR) misura la qualità del segnale convertito confrontando la potenza media del segnale utile $P_x$ con la potenza del rumore di quantizzazione $\sigma_e^2$:

$$
\text{SQNR} = \frac{P_x}{\sigma_e^2}
$$

In scala logaritmica decibel:

$$
\text{SQNR}_{\text{dB}} = 10\log_{10}\left(\frac{P_x}{\sigma_e^2}\right)
$$

dove la potenza del rumore di quantizzazione uniforme vale:

$$
\sigma_e^2 = \frac{Q^2}{12} = \frac{R^2}{12 \cdot 2^{2B}}
$$

### Derivazione dell'SQNR per Sinusoide a Fondo Scala

Consideriamo come segnale di prova una sinusoide pura a fondo scala, la cui escursione picco-picco copre l'intero range $R$ dell'ADC:

$$
x(t) = A \cos(\Omega t) \quad \text{con ampiezza di picco } A = \frac R2
$$

1. La __potenza media del segnale sinusoidale__ $P_x$ è data dal quadrato del suo valore efficace (RMS):

$$
P_x = \frac{A^2}2 = \frac{(R/2)^2}2 = \frac{R^2}8
$$

2. La __potenza del rumore di quantizzazione__ $\sigma_e^2$, ricordando che $Q = \frac{R}{2^B}$, vale:

$$
\sigma_e^2 = \frac{Q^2}{12} = \frac{R^2}{12 \cdot 2^{2B}}
$$

3. Calcoliamo il rapporto tra le due potenze in scala lineare:

$$
\frac{P_x}{\sigma_e^2} = \frac{\frac{R^2}8}{\frac{R^2}{12 \cdot 2^{2B}}} = \frac{12}8 \cdot 2^{2B} = 1.5 \cdot 2^{2B}
$$

4. Esprimendo il rapporto in decibel otteniamo la celebre formula fondamentale:

$$
\text{SQNR}_{\text{dB}} = 10\log_{10}\left(1.5 \cdot 2^{2B}\right) = 10\log_{10}(1.5) + 20 B \log_{10}(2)
$$

Poiché $10\log_{10}(1.5) \approx 1.7609\text{ dB}$ e $20\log_{10}(2) \approx 6.0206\text{ dB}$, ricaviamo:

$$
\text{SQNR}_{\text{dB}} \approx 6.02 B + 1.76\text{ dB}
$$

>[!important] Interpretazione Fisica dei Termini
>- Il fattore __$6.02 B$__ evidenzia che __ogni bit in più nell'ADC aumenta il rapporto segnale-rumore di circa 6 dB__ (dimezzando l'ampiezza del rumore rispetto al segnale).
>- Il termine costante __$+1.76\text{ dB}$__ riflette la forma d'onda del segnale (il fattore di cresta del coseno $k = \frac{A}{\sigma_x} = \sqrt{2}$, per cui $P_x = \frac{A^2}2$). Per segnali generici a pieno carico / fondo scala ($A = \frac R2$) con fattore di cresta $k$, l'espressione generale assume la forma:
>
>$$
>\text{SQNR}_{\text{dB}} = 6.02 B + 4.77 - 20\log_{10}(k)\text{ dB}
>$$



# 3. Quantizzazione Ottima

Il rapporto segnale-rumore di quantizzazione (SQNR) dipende strettamente dalla funzione di densità di probabilità (p.d.f.) del segnale. Nella realtà fisica la quasi totalità dei segnali di interesse non possiede una p.d.f. uniforme.

Ad esempio, il segnale vocale umano presenta una distribuzione tipicamente esponenziale simmetrica (Laplaciana, $p_x(x) \propto \mathrm{e}^{-\lambda|x|}$), caratterizzata da un'altissima probabilità di ampiezze vicine allo zero e code lunghe per i picchi rari. Se utilizziamo un quantizzatore uniforme lineare per la voce, i segnali di bassa intensità vengono penalizzati con un SQNR degradato e un rumore di quantizzazione intollerabile.

![[immagini/caratteristica ingresso-uscita.svg|center mid]]

## Quantizzatore Ottimo Di Max

L'obiettivo della quantizzazione ottima è massimizzare l'SQNR a parità di numero di bit $B$ (ovvero per un numero fissato di livelli $N = 2^B$), minimizzando la __distorsione quadratica media__ (__MSE__, _Mean Squared Error_):

$$
D = E[(x - x_Q)^2]
$$

Per raggiungere questo obiettivo dobbiamo ottimizzare congiuntamente due insiemi di parametri:
- $x_i$: le __soglie di decisione__ (_decision boundaries_), che delimitano gli intervalli di ampiezza in ingresso.
- $y_i$: i __livelli di ricostruzione__ (_output levels_), ovvero i valori discreti assegnati a ciascun intervallo.

Considerando una p.d.f. simmetrica $p_x(x) = p_x(-x)$, la distorsione totale $D$ può essere decomposta in tre contributi fondamentali:

$$
D = \underbrace{\int_{-x_1}^{x_1} x^2 p_x(x)\,\mathrm{d}x}_{\text{ZONA MORTA}} + \underbrace{2\sum_{n=1}^{M-1}\int_{x_n}^{x_{n+1}} (x - y_n)^2 p_x(x)\,\mathrm{d}x}_{\text{ZONA QUASI LINEARITÀ}} + \underbrace{2\int_{x_M}^{\infty} (x - y_M)^2 p_x(x)\,\mathrm{d}x}_{\text{ZONA SATURAZIONE}}
$$

- __Zona morta__ ($[-x_1, x_1]$): intervallo centrale attorno allo zero in cui l'uscita viene posta a $y_0 = 0$.
- __Zona attiva (quasi linearità)__ ($[x_n, x_{n+1}]$, per $n=1,\dots,M-1$ sul semiasse positivo): intervalli intermedi in cui il quantizzatore opera sui segnali a dinamica ordinaria.
- __Zona di saturazione__ ($[x_M, \infty)$): intervallo estremo di clipping, dove il segnale supera il fondo scala e viene troncato al livello massimo $y_M$. (Qui $M$ indica il numero di livelli sul semiasse positivo, con $M = N/2$).

### Condizioni Di Ottimalità: Centroide E Punto Medio

I valori ottimi di $x_i$ e $y_i$ che minimizzano la distorsione $D$ si ricavano annullando le derivate parziali $\frac{\partial D}{\partial y_i} = 0$ e $\frac{\partial D}{\partial x_i} = 0$:

1. __Condizione di Centroide__ ($\frac{\partial D}{\partial y_i} = 0$):

$$
y_i = \frac{\int_{x_{i-1}}^{x_i} x p_x(x)\,\mathrm{d}x}{\int_{x_{i-1}}^{x_i} p_x(x)\,\mathrm{d}x} = E[x \mid x_{i-1} \le x < x_i]
$$

Ciascun livello di uscita $y_i$ deve coincidere con il __centroide di probabilità__ (valore atteso condizionato) della rispettiva zona di decisione.

2. __Condizione di Punto Medio__ ($\frac{\partial D}{\partial x_i} = 0$):

$$
x_i = \frac{y_i + y_{i+1}}{2}
$$

Ciascuna soglia di decisione $x_i$ deve essere esattamente il __punto medio__ tra due livelli di ricostruzione adiacenti.

Poiché le due equazioni sono mutuamente accoppiate (spostando $y_i$ si spostano gli $x_i$ e viceversa), la soluzione ottima viene calcolata numericamente tramite un algoritmo iterativo fino a convergenza.

![[immagini/pdf_non_uniforme.png|center mid]]

### Limiti Pratici Di Max E Necessità Del Companding

Sebbene il quantizzatore di Max sia teoricamente ottimo, nella pratica ingegneristica presenta due grossi limiti:
1. __Complessità circuitale hardware__: richiede una scala di resistori disuguali calibrata ad-hoc, estremamente difficile e costosa da integrare in silicio rispetto a un ADC uniforme lineare.
2. __Sensibilità alla potenza del segnale__: le soglie ottime sono calcolate per una specifica p.d.f. con varianza $\sigma_x^2$ fissa. Se il volume del segnale varia (es. un parlante parla più a bassa voce o grida), il quantizzatore perde la sua ottimalità e le prestazioni decadono drasticamente.

Per superare questi limiti si adotta l'approccio del __companding__.

## Quantizzazione Non Uniforme E Companding

Invece di costruire un complicato ADC non uniforme in silicio, manteniamo un __normale ed economico ADC uniforme lineare__.
L'idea alla base del companding è __modificare la p.d.f.__ del segnale in ingresso tramite una trasformazione non lineare reversibile $\eta = g(x)$, in modo da renderla uniforme prima di applicare la quantizzazione lineare:

$$
\eta = g(x)
$$

Al termine della trasmissione, l'operazione inversa $x = g^{-1}(\eta)$ ripristinerà l'ampiezza originale del segnale. Il termine companding deriva appunto dalla fusione di __compressione__ ed __espansione__.

### Modifica Della p.d.f. Tramite Companding

La funzione di compressione $g(x)$ deve soddisfare quattro proprietà fondamentali:
1. Essere strettamente crescente e invertibile.
2. Essere dispari (antisimmetrica): $g(-x) = -g(x)$.
3. Mantenere lo zero: $g(0) = 0$.
4. Rispettare i limiti di fondo scala: $g(\infty) = \frac{R}{2}$ (o al massimo valore di saturazione).

Per la legge di trasformazione delle variabili casuali continue:

$$
p_\eta(\eta) = \left[ \frac{p_x(x)}{\left|\frac{\partial g(x)}{\partial x}\right|} \right]_{x = g^{-1}(\eta)}
$$

Affinché $p_\eta(\eta)$ risulti una distribuzione uniforme nell'intervallo di fondo scala $[- \frac{R}{2}, \frac{R}{2}]$, la sua densità deve essere costante e pari a $\frac{1}{R}$:

$$
p_\eta(\eta) = \frac{1}{R} \implies \frac{\partial g(x)}{\partial x} = R \cdot p_x(x)
$$

Integrando per ampiezze positive ($x \ge 0$):

$$
g(x) = R \int_0^x p_x(u)\,\mathrm{d}u
$$

> [!info] Connessione con la CDF (Probability Integral Transform)
> Per una p.d.f. simmetrica a media nulla, l'integrale sulle ampiezze positive $\int_0^x p_x(u)\,\mathrm{d}u$ rappresenta la probabilità cumulata a partire dallo zero, ovvero $F_X(x) - F_X(0) = F_X(x) - \frac{1}{2}$, dove $F_X(x)$ è la funzione di distribuzione cumulativa (__CDF__, _Cumulative Distribution Function_).
> Estendendo la trasformazione con antisimmetria e riscalando sull'escursione totale $R$:
>
> $$
> g(x) = R \left(F_X(x) - \frac{1}{2}\right) = R \cdot F_X(x) - \frac{R}{2}
> $$
>
> In base al _Teorema della Trasformata Integrale di Probabilità_, applicando la propria CDF a qualsiasi variabile aleatoria continua $X$, la variabile risultante $Y = F_X(X)$ ha __sempre distribuzione uniforme__ in $[0, 1]$.
>
> Nel trattamento delle immagini questa proprietà è il principio fondante dell'__equalizzazione dell'istogramma__ (dove la CDF empirica funge da curva di trasformazione). Nella telefonia vocale, poiché la CDF esatta varia da parlante a parlante e con il volume della voce, si preferisce utilizzare curve analitiche fisse e robuste (__$\mu$-law__ e __A-law__) che approssimano la forma della CDF garantendo un SQNR costante su oltre 30–40 dB di dinamica.

### Caso Di Studio: Segnale Vocale Con Distribuzione Laplaciana

Consideriamo il segnale vocale modellato con distribuzione esponenziale (Laplaciana):

$$
p_x(x) = \frac{\lambda}{2} \mathrm{e}^{-\lambda |x|} \quad \text{con } \lambda^2 = \frac{2}{\sigma_x^2}
$$

Per valori positivi $x > 0$:

$$
\frac{\partial g(x)}{\partial x} = R \cdot \frac{\lambda}{2} \mathrm{e}^{-\lambda x}
$$

Integrando tra $0$ e $x$:

$$
g(x) = \int_0^x R \frac{\lambda}{2} \mathrm{e}^{-\lambda u}\,\mathrm{d}u = \frac{R}{2} (1 - \mathrm{e}^{-\lambda x})
$$

Verifichiamo che la funzione rispetta i vincoli:
- Per $x = 0 \implies g(0) = 0$.
- Per $x \to \infty \implies g(\infty) = \frac{R}{2}$.

Invertendo la relazione per ricavare la legge di espansione al ricevitore:

$$
1 - \mathrm{e}^{-\lambda x} = \frac{2\eta}R \implies \mathrm{e}^{-\lambda x} = 1 - \frac{2\eta}R
$$

$$
x = g^{-1}(\eta) = -\frac 1\lambda \ln\left[1 - \frac{2\eta}R\right] \quad \text{con } 0 \le \eta < \frac{R}{2}
$$

Per simmetria dispari si ricavano i valori per le ampiezze negative.

### Implementazione dell'Amplificatore a Guadagno Variabile

Nel dominio analogico, l'operazione di compressione $g(x)$ si realizza mediante un __amplificatore a guadagno variabile__:

![[immagini/amplificatore a guadagno variabile.svg|center big]]

Il guadagno istantaneo dell'amplificatore è elevato per piccoli segnali (amplificando le ampiezze deboli) e decresce progressivamente per segnali ampi.
Poiché questo circuito introduce una forte distorsione non lineare, modifica radicalmente lo spettro in frequenza del segnale; di conseguenza non __può essere utilizzato__ nei sistemi in cui è richiesta un'__analisi spettrale__ lineare a monte del ricevitore.

## Implementazione Digitale Del Companding

Nei moderni sistemi di elaborazione digitale dei segnali il companding non viene implementato con amplificatori analogici, ma interamente nel dominio digitale:

![[immagini/companding_digitale.svg|center big]]

1. Il segnale analogico $x(t)$ viene acquisito tramite un ADC lineare ad alta risoluzione a $B'$ bit ($B' > B$, ad esempio 12 o 16 bit lineari), garantendo un elevato rapporto segnale-rumore di partenza.
2. I campioni a $B'$ bit vengono convertiti nel target compresso a $B$ bit (es. 8 bit) applicando la curva di compressione non lineare $\eta = g(x)$.

![[immagini/companding_digitale_esempio.svg|center big]]

Per evitare il calcolo in tempo reale di complesse funzioni logaritmiche non lineari, la curva $g(x)$ viene precalcolata e memorizzata all'interno di una tabella di consultazione rapida (__Look-Up Table__, LUT):

![[immagini/lookup table.svg|center mid]]

Questa tecnica di mappatura tramite LUT è modulare e può essere applicata direttamente anche a dati bidimensionali (come immagini e matrici video).

### Compressione Logaritmica: $\mu$-Law E A-Law

Nei sistemi di telecomunicazione e telefonia vocale si utilizzano tradizionalmente due standard di compressione logaritmica:
- __$\mu$-law__: adottata prevalentemente in Nord America e Giappone:

$$
\eta = g(x) = \text{sgn}(x) \frac{\ln(1 + \mu |x|)}{\ln(1 + \mu)} \quad \text{con } \mu = 255 \text{ e } |x| \le 1
$$

Nel limite per $\mu \to 0$ (applicando il teorema di de l'Hôpital o lo sviluppo di Taylor), la curva degenera nella caratteristica lineare uniforme $g(x) = x$.
- __A-law__: variante analoga adottata storicamente in Europa e a livello internazionale.

La compressione logaritmica consente di mantenere un rapporto SQNR pressoché costante su un'ampia gamma dinamica di potenze vocali, permettendo a un segnale compresso a soli 8 bit di eguagliare la qualità percettiva di una quantizzazione uniforme a 12 bit.

## Quantizzazione Non Lineare Nel Video Ed HDR

La quantizzazione non lineare trova ampia applicazione anche nell'elaborazione video e nelle immagini ad alta dinamica (__HDR__, _High Dynamic Range_):
- L'obiettivo principale in questo ambito non è massimizzare l'SQNR, ma estendere il più possibile la dinamica percepibile dall'occhio umano.
- I sensori delle telecamere moderne acquisiscono a 14–16 bit lineari unsigned.
- I codec e i canali di trasmissione standard lavorano tipicamente a 8–10 bit per motivi di banda.
- Si applica quindi una curva di compressione non lineare della dinamica (ispirata alla risposta percettiva logaritmica del sistema visivo umano) per distribuire i livelli di quantizzazione dove l'occhio è più sensibile.
- In fase di riproduzione il display applica la curva inversa per ripristinare la corretta scala di luminanza (i display di fascia alta sfruttano pannelli a 10–12 bit di dinamica).



# 4. Spettro in Frequenza - DTFT

La Trasformata di Fourier classica a tempo continuo (CTFT) non può essere calcolata direttamente su calcolatori digitali, poiché richiede segnali continui sia nel dominio del tempo sia nel dominio della frequenza.

Per l'elaborazione numerica dei segnali sono state introdotte due formulazioni fondamentali:
- __DTFT (Discrete-Time Fourier Transform)__: opera su sequenze discrete nel tempo $x(n)$ e produce uno spettro continuo $X(\omega)$. Non è calcolabile numericamente in macchina su tutti i punti perché la variabile frequenza $\omega$ rimane continua, ma costituisce lo strumento analitico primario per progettare e studiare filtri e sistemi lineari tempo-invarianti (LTI).
- __DFT (Discrete Fourier Transform)__: campiona anche l'asse delle frequenze in $N$ punti discreti $\omega_k = \frac{2\pi k}{N}$, rendendo la trasformata interamente numerica e implementabile tramite gli algoritmi rapidi FFT. La DFT non è una semplice approssimazione della DTFT, ma ne costituisce una _rappresentazione esatta_, a patto che la sequenza temporale abbia __durata finita__ ($L \le N$).

## Dalla Trasformata Continua Alle Trasformate Discrete

Confrontiamo la definizione classica continua con la trasformata a tempo discreto:

$$
\text{CTFT (tempo continuo)}:\quad x(t) \to X(f) = \int_{-\infty}^{+\infty} x(t) \mathrm{e}^{-j 2\pi f t}\,\mathrm{d}t \quad \text{oppure} \quad X(\Omega) = \int_{-\infty}^{+\infty} x(t) \mathrm{e}^{-j \Omega t}\,\mathrm{d}t \quad (\Omega = 2\pi f)
$$

$$
\text{DTFT (tempo discreto)}:\quad x(n) \to X(\omega) = \sum_{n=-\infty}^{\infty} x(n) \mathrm{e}^{-j\omega n} \quad \left(\omega = 2\pi \frac{f}{f_s}\right)
$$

> [!question] Come si definisce e si ricava la pulsazione digitale $\omega$ (e perché compare $f_s$ al denominatore)?
> Consideriamo un fasore elementare analogico alla frequenza fisica $f$ (in Hz):
>
> $$
> x_a(t) = \mathrm{e}^{j 2\pi f t} = \mathrm{e}^{j \Omega t} \quad \text{con } \Omega = 2\pi f \text{ [rad/s]}
> $$
>
> Quando campioniamo il segnale ad intervalli uniformi $T = \frac{1}{f_s}$ (dove $f_s$ è la frequenza di campionamento, detta anche $f_c$), poniamo $t = nT$:
>
> $$
> x(n) = x_a(t)\Big|_{t=nT} = \mathrm{e}^{j 2\pi f (nT)} = \mathrm{e}^{j \left(\frac{2\pi f}{f_s}\right) n} = \mathrm{e}^{j \omega n}
> $$
>
> Troviamo così la definizione della __pulsazione digitale (o frequenza normalizzata)__:
>
> $$
> \omega = \frac{2\pi f}{f_s} = 2\pi f T = \Omega T \quad [\text{rad/campione}]
> $$
>
> Per approfondire le condizioni di campionamento ideale, vedi [[Anno 1/Lezioni integrative DSP/1. Segnali#Campionamento|Lezioni integrative: Campionamento]].

## Frequenza Digitale ($\omega$) E Intervallo Di Nyquist

La frequenza digitale $\omega$ misura l'avanzamento di fase del segnale tra due campioni successivi ed è espressa in __radianti per campione__ ($\text{rad/campione}$).
Possiamo anche definire la __frequenza ciclica normalizzata__ $F$:

$$
F = \frac{f}{f_s} = \frac{\omega}{2\pi} \quad [\text{cicli/campione}]
$$

Poiché per qualsiasi numero intero $n$ vale $\mathrm{e}^{-j(\omega + 2\pi)n} = \mathrm{e}^{-j\omega n} \cdot \mathrm{e}^{-j 2\pi n} = \mathrm{e}^{-j\omega n}$, la DTFT è intrinsecamente __periodica di periodo $2\pi$__:

$$
X(\omega + 2\pi) = X(\omega)
$$

L'__intervallo fondamentale di Nyquist__ delle frequenze fisiche $[-\frac{f_s}2, \frac{f_s}2]$ corrisponde nelle unità di $\omega$ all'intervallo simmetrico:

$$
-\pi \le \omega \le \pi \quad (\text{ovvero } \omega \in [-\pi, \pi])
$$

oppure, equivalentemente nell'elaborazione numerica e negli algoritmi di calcolo, all'intervallo positivo:

$$
0 \le \omega < 2\pi \quad (\text{ovvero } \omega \in [0, 2\pi))
$$

### Periodizzazione Spettrale E Repliche Di Nyquist

Il campionamento temporale genera una replicazione periodica dello spettro analogico continuo originario $X_a(f)$.
Come dimostrato in _Orfanidis (Cap. 1, Sez. 1.5, eq. 1.5.14)_, la relazione esatta tra lo spettro continuo $X_a(f)$ e la DTFT $X(\omega)$ è espressa dalla __formula di sommatoria di Poisson__:

$$
X_s(f) = \frac{1}{T} \sum_{k=-\infty}^{\infty} X_a\left(f - k f_s\right)
$$

ovvero, in termini di pulsazione digitale normalizzata $\omega = 2\pi \frac{f}{f_s}$:

$$
X(\omega) = f_s \sum_{k=-\infty}^{\infty} X_a\left(\frac{\omega f_s}{2\pi} - k f_s\right) = \frac{1}{T} \sum_{k=-\infty}^{\infty} X_a\left(\frac{\omega - 2\pi k}{2\pi T}\right)
$$

Il campionamento genera infinite repliche dello spettro continuo centrate attorno a tutti i multipli interi della frequenza di campionamento $k f_s$.
Se il segnale continuo è a banda limitata ($f_{max} < \frac{f_s}2$) e rispetta il [[Anno 1/Lezioni integrative DSP/1. Segnali#^e56489|Teorema del Campionamento di Nyquist-Shannon]], le repliche spettrali non si sovrappongono: non vi è aliasing e all'interno dell'intervallo fondamentale $[-\pi, \pi]$ la DTFT riproduce fedelmente lo spettro analogico continuo originale, scalato per il fattore di ampiezza $f_s = \frac 1T$.

### Trasformata Inversa (IDTFT)

L'inversa della DTFT (__IDTFT__, _Inverse Discrete-Time Fourier Transform_) consente di recuperare perfettamente la sequenza temporale discreta $x(n)$ a partire dal suo spettro integrando su un unico periodo fondamentale di Nyquist:

$$
x(n) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(\omega) \mathrm{e}^{j\omega n}\,\mathrm{d}\omega
$$

L'equazione di sintesi esprime ogni campione $x(n)$ come una __combinazione lineare continua__ (integrale) di oscillazioni elementari a tempo discreto $\mathrm{e}^{j\omega n}$, in cui l'ampiezza complessa infinitesima di ciascuna componente armonica è pesata dal coefficiente spettrale $X(\omega)\,\frac{\mathrm{d}\omega}{2\pi}$.

## Proprietà Della DTFT

La DTFT eredita le proprietà della trasformata di Fourier continua, con la fondamentale particolarità della periodicità in $\omega$.

### Rappresentazione Polare E Simmetria Hermitiana

La DTFT di una sequenza $x(n)$ è in generale una funzione complessa di variabile reale $\omega$. Possiamo scriverla in forma cartesiana o polare:

$$
X(\omega) = \text{Re}[X(\omega)] + j\,\text{Im}[X(\omega)] = |X(\omega)| \mathrm{e}^{j \arg X(\omega)}
$$

dove $|X(\omega)|$ rappresenta lo __spettro di ampiezza__ (o modulo) e $\arg X(\omega)$ lo __spettro di fase__.

Per tutti i segnali fisici reali ($x(n) \in \mathbb{R}$), la DTFT soddisfa la __simmetria hermitiana__:

$$
X(-\omega) = X^*(\omega)
$$

Questo comporta quattro conseguenze fondamentali:
- Il modulo è __pari__: $|X(-\omega)| = |X(\omega)|$
- La fase è __dispari__: $\arg X(-\omega) = -\arg X(\omega)$
- La parte reale è __pari__: $\text{Re}[X(-\omega)] = \text{Re}[X(\omega)]$
- La parte immaginaria è __dispari__: $\text{Im}[X(-\omega)] = -\text{Im}[X(\omega)]$

>[!note] Implicazione Pratica
>Grazie alla simmetria hermitiana, per i segnali reali non occorre analizzare o memorizzare l'intero intervallo $[-\pi, \pi]$: tutte le informazioni fisiche sono contenute nell'intervallo monolatero $[0, \pi]$ (corrispondente alle frequenze da $0$ a $\frac{f_s}2$). La banda negativa $[-\pi, 0]$ è ridondante.

### Risposta Impulsiva E Risposta in Frequenza

La risposta impulsiva $h(n)$ di un sistema lineare tempo-invariante (LTI) è la sequenza in uscita generata quando in ingresso applichiamo l'__impulso unitario discreto__ (noto anche nel gergo ingegneristico come __impulso di Dirac discreto__, o formalmente __delta di Kronecker__ $\delta(n)$):

$$
\delta(n) = \begin{cases} 1 & \text{se } n = 0 \\ 0 & \text{se } n \ne 0 \end{cases}
$$

A differenza della delta di Dirac continua $\delta(t)$ (che è una distribuzione non limitata con area unitaria), nel dominio discreto $\delta(n)$ è un segnale ordinario con valore finito unitario in $n=0$.

La __risposta in frequenza__ $H(\omega)$ del sistema LTI coincide con la DTFT della sua risposta impulsiva:

$$
H(\omega) = \sum_{n=-\infty}^{\infty} h(n) \mathrm{e}^{-j\omega n}
$$

### Teorema Di Convoluzione E Filtraggio

La convoluzione lineare tra l'ingresso $x(n)$ e la risposta impulsiva $h(n)$ nel dominio del tempo corrisponde a una semplice __moltiplicazione algebrica__ nel dominio della frequenza:

$$
y(n) = h(n) * x(n) = \sum_{k=-\infty}^{\infty} h(k) x(n - k)
$$

Applicando la DTFT ad ambo i membri otteniamo:

$$
Y(\omega) = H(\omega) \cdot X(\omega)
$$

In modulo e fase:
- $|Y(\omega)| = |H(\omega)| \cdot |X(\omega)|$ (l'ampiezza dell'ingresso viene riscalata dal guadagno del filtro).
- $\arg Y(\omega) = \arg X(\omega) + \arg H(\omega)$ (la fase dell'ingresso viene traslata della risposta di fase del filtro).

### Teorema Di Parseval E Conservazione dell'Energia

Il __Teorema di Parseval__ stabilisce l'equivalenza tra l'energia totale della sequenza calcolata nel dominio del tempo e l'energia distribuita nel dominio spettrale.

Come formulato in _Orfanidis (Cap. 5, eq. 5.4.7)_, l'integrazione deve essere limitata a un __singolo periodo fondamentale__ $[-\pi, \pi]$:

$$
\sum_{n=-\infty}^{\infty} |x(n)|^2 = \frac{1}{2\pi} \int_{-\pi}^{\pi} |X(\omega)|^2\,\mathrm{d}\omega
$$

La grandezza $|X(\omega)|^2$ prende il nome di __densità spettrale di energia__ (ESD, _Energy Spectral Density_).
L'energia totale del segnale nel tempo equivale al valor medio dello spettro di energia $|X(\omega)|^2$ calcolato sul periodo fondamentale $[-\pi, \pi]$ (ovvero all'area sottesa dallo spettro di energia scalata per il fattore di normalizzazione $\frac{1}{2\pi}$).



# 5. Trasformata Discreta Di Fourier (DFT)

La __Discrete Fourier Transform (DFT)__ è una trasformata __esatta__ che permette di rappresentare ed elaborare un segnale discreto completamente in ambito numerico (digitale).

Mentre la [[4. Spettro in frequenza - DTFT|DTFT]] produce uno spettro a frequenza continua $\omega \in [-\pi, \pi]$, la DFT valuta lo spettro campionando l'intervallo $[0, 2\pi)$ in $N$ frequenze discrete equispaziate:

$$
\omega_k = \frac{2\pi}{N} k, \quad k = 0, \dots, N-1
$$

In termini di frequenza fisica analogica (in Hz), i punti di campionamento corrispondono a:

$$
f_k = \frac{k f_s}{N}
$$

Il problema operativo consiste nel determinare la griglia di frequenze $f_k$, ossia individuare il numero corretto di campioni $N$ per rappresentare adeguatamente il segnale.

Campionare in frequenza a passi discreti $\Delta\omega = \frac{2\pi}{N}$ implica che il segnale nel dominio del tempo debba essere a __durata finita__: non è possibile applicare la DFT a segnali a tempo discreto di durata infinita senza troncarli.

$$
\text{DTFT: } \quad X(\omega) = \sum_{n = -\infty}^{\infty} x(n) \mathrm{e}^{-j\omega n}, \quad \omega = \frac{2\pi f}{f_s}
$$

$$
\text{DFT: } \quad X(\omega_k) = \sum_{n = 0}^{N-1} x(n) \mathrm{e}^{-j \frac{2\pi}{N} k n}, \quad \text{con } x(n) = 0 \text{ per } n \notin \{0, \dots, N-1\}, \; k = 0, \dots, N-1
$$

^6ad93d

Se la sequenza temporale è strettamente limitata nell'intervallo $0 \le n \le N-1$, la DFT campiona esattamente la DTFT nei punti $\omega_k$ senza perdita di informazione.

Nulla vieta di considerare un segnale di lunghezza effettiva $L \le N$, con campioni non nulli solo per $0 \le n \le L-1$.

## IDFT (Trasformata Inversa)

La trasformata inversa (IDFT) consente di ricostruire esattamente i campioni temporali $x(n)$ a partire dai coefficienti spettrali $X(\omega_k)$:

$$
x(n) = \frac{1}{N} \sum_{k=0}^{N-1} X(\omega_k) \mathrm{e}^{j\omega_k n}, \quad n = 0, \dots, N-1
$$

Se valutata al di fuori dell'intervallo base $0 \le n \le N-1$, la formula della IDFT genera una replica __periodica__ di periodo $N$ della sequenza originaria, denotata con $\tilde{x}(n)$.

## Sovracampionamento in Frequenza

Se la sequenza ha durata $L$ e si sceglie una dimensione di trasformazione $N > L$, si ottiene un sovracampionamento in frequenza:

![[immagini/dft_oversampling.svg|center big]]

Si parla di sovracampionamento perché, partendo da $L$ campioni temporali, si calcolano $N > L$ campioni in frequenza, ottenendo più punti di quanti ne servirebbero per descrivere la sequenza originale.

Per segnali reali $x(n)$, i coefficienti spettrali soddisfano la __simmetria Hermitiana__ ($X(\omega_{N-k}) = X^*(\omega_k)$); è quindi sufficiente calcolare e memorizzare solo $\frac{N}{2} + 1$ valori indipendenti (assumendo $N$ pari, corrispondenti agli indici $k = 0, 1, \dots, N/2$).

## Zero-Padding

Quando si dispone di un segnale di lunghezza $L < N$, è possibile estendere la sequenza a $N$ campioni appendendo in coda $D = N - L$ zeri. Questa operazione prende il nome di __zero-padding__.

L'aggiunta di zeri __non modifica la DTFT__ del segnale, ma cambia la __DFT__, poiché quest'ultima valuta la medesima funzione continua su una griglia più fitta di frequenze:

$$
\begin{align}
X_D(\omega) &= \sum_{n = 0}^{L+D-1} x_D(n) \mathrm{e}^{-j\omega n} \\
&= \sum_{n = 0}^{L-1} x_D(n) \mathrm{e}^{-j \omega n} + \sum_{n = L}^{L+D-1} 0 \cdot \mathrm{e}^{-j\omega n} \\
&= \sum_{n = 0}^{L-1} x(n) \mathrm{e}^{-j\omega n} + 0 \\
&= X(\omega)
\end{align}
$$

Lo zero-padding funge da __interpolazione nel dominio della frequenza__: riduce la distanza tra i punti campionati $\Delta\omega = \frac{2\pi}{N}$, evitando che picchi spettrali cadano tra due righe adiacenti (effetto "picket-fence"), ma __non migliora la risoluzione fisica__ tra componenti frequenziali vicine, che rimane vincolata alla lunghezza originaria $L$.

## Complessità Della DFT Ed FFT

![[#^6ad93d]]

Applicando la formula di Eulero per esplicitare parte reale e immaginaria:

$$
x(n) \mathrm{e}^{-j\omega_k n} = x(n) \left(\cos(\omega_k n) - j \sin(\omega_k n)\right)
$$

Ipotizzando una sequenza reale $x(n) \in \mathbb{R}$:
- Per ciascun valore $\omega_k$ occorre eseguire $2L$ operazioni di moltiplicazione e accumulo reali (__MACS__), corrispondenti a $2L$ moltiplicazioni reali e $\approx 2L$ somme reali.
- Per l'intera DFT di dimensione $N$ sono necessari $2LN$ MACS reali, che diventano $2N^2$ MACS reali nel caso standard $L = N$.

Nel caso in cui $x(n)$ sia a valori complessi:
- Ciascun termine richiede 4 moltiplicazioni e 4 somme reali (4 MACS reali), portando il costo computazionale a $4N^2$ MACS reali (equivalenti a $N^2$ __moltiplicazioni complesse__).

> [!IMPORTANT] Algoritmo FFT (Fast Fourier Transform)
> L'algoritmo __FFT__ (Radix-2 Cooley-Tukey) riduce la complessità computazionale da $\mathcal{O}(N^2)$ a soli $\mathcal{O}(N \log_2 N)$ passaggi (richiedendo esattamente $\frac{N}{2} \log_2 N$ moltiplicazioni complesse e $N \log_2 N$ somme complesse), a condizione che la dimensione $N$ sia una potenza di due ($N = 2^m$).
> In ambito applicativo è quasi sempre preferibile estendere la sequenza tramite [[#Zero-Padding]] fino alla prima potenza di due utile ed eseguire una FFT, piuttosto che calcolare direttamente la DFT di lunghezza arbitraria.

## Convoluzione Lineare Con Sequenze Di Durata Finita

La convoluzione lineare tra una sequenza di ingresso $x(n)$ e la risposta impulsiva di un filtro FIR $h(n)$ di lunghezza $M$ (ossia di ordine $M-1$) è definita da:

$$
y(n) = x(n) \ast h(n) = \sum_{k=0}^{M-1} h(k) x(n - k)
$$

Se la sequenza in ingresso ha __durata finita__ pari a $L$ campioni:

$$
x(n) = 0 \quad \text{per } n < 0 \text{ e per } n \ge L, \quad L \gg M
$$

La sequenza di uscita $y(n)$ risulterà __più lunga__ rispetto alla sequenza di ingresso $x(n)$ a causa della memoria interna del filtro (lunghezza totale pari a $L + M - 1$ campioni), generando specifici __fenomeni di transitorio__.

### Fenomeni Di Transitorio

L'evoluzione temporale dell'uscita si suddivide in 3 fasi caratteristiche:
- __Transitorio di attacco__ ($0 \le n \le M-2$, durata $M-1$ campioni): si verifica quando la memoria del filtro (il registro a scorrimento dei campioni passati) è inizialmente vuota e comincia a riempirsi; il numero di campioni validi di $x(n)$ che concorrono al calcolo della sommatoria aumenta progressivamente da $1$ a $M$ man mano che occupano le celle di ritardo.
- __Risposta a regime__ ($M-1 \le n \le L-1$, durata $L-M+1$ campioni): una volta riempita completamente la memoria del filtro con $M$ campioni validi, i nuovi campioni scorrono rimpiazzando quelli più vecchi; l'elaborazione procede a pieno carico.
- __Transitorio di rilascio (coda)__ ($L \le n \le L+M-2$, durata $M-1$ campioni): quando la sequenza di ingresso si esaurisce ($x(n) = 0$), il registro interno continua a svuotarsi fornendo campioni residui in uscita; la fase si conclude quando tutti i ritardi interni tornano a zero.

## Convoluzione Circolare

Nella [[4. Spettro in frequenza - DTFT|DTFT]] il prodotto algebrico tra trasformate corrisponde alla convoluzione lineare nel tempo. Con la DFT, a causa della periodizzazione intrinseca introdotta dal campionamento in frequenza, il prodotto puntuale tra trasformate corrisponde invece a una __convoluzione circolare__ (o ciclica).

> [!IMPORTANT] Vincolo di Durata Finita
> Per applicare la DFT a sequenze temporali discrete è indispensabile che esse abbiano __durata finita__:
> - $x_1(n)$ di durata limitata a $L$ campioni ($0 \le n \le L-1$)
> - $x_2(n)$ di durata limitata a $M$ campioni ($0 \le n \le M-1$)

La convoluzione lineare tra $x_1(n)$ e $x_2(n)$ genera un segnale di lunghezza complessiva pari a $L + M - 1$. Affinché la convoluzione circolare calcolata tramite DFT coincida esattamente con la convoluzione lineare (evitando fenomeni di sovrapposizione ciclica o __aliasing temporale__), la dimensione $N$ della DFT deve soddisfare:

$$
N \ge L + M - 1
$$

Analiticamente, l'operazione di convoluzione circolare a $N$ punti $\circledast_N$ è definita nel dominio del tempo come:

$$
x_3(n) = x_1(n) \circledast_N x_2(n) = \sum_{m=0}^{N-1} x_1(m) x_2((n - m) \bmod N), \quad n = 0, \dots, N-1
$$

Le DFT a $N$ punti delle due sequenze (estese con zero-padding a lunghezza $N$) sono:

$$
\begin{aligned}
X_1(\omega_k) &= \text{DFT}_N\{x_1(n)\} \\
X_2(\omega_k) &= \text{DFT}_N\{x_2(n)\}
\end{aligned}
\qquad \text{per } k = 0, \dots, N-1
$$

Nel dominio della frequenza l'operazione corrisponde al prodotto algebrico termine a termine:

$$
x_3(n) = x_1(n) \circledast_N x_2(n) \quad \overset{\text{DFT}_N}{\longleftrightarrow} \quad X_3(\omega_k) = X_1(\omega_k) \cdot X_2(\omega_k)
$$

La DFT tratta implicitamente le sequenze come __periodiche__ di periodo $N$. Si parla di convoluzione circolare proprio perché uno dei due segnali viene ribaltato e fatto scorrere in modo circolare (modulo $N$) rispetto all'altro:

![[immagini/circ_conv_1.jpg|center small]] ![[immagini/circ_conv_2.jpg|center small]]



# 6. Finestratura

![[immagini/schema_blocchi_finestra.svg|center big]]

Nell'elaborazione numerica dei segnali, la catena di acquisizione e analisi spettrale prevede quattro passaggi fondamentali:
1. Progettazione del filtro passa-basso anti-aliasing in base alla banda utile del segnale analogico;
2. Progettazione del convertitore ADC in base alla dinamica e al rapporto segnale-rumore di quantizzazione (__SQNR__);
3. Progettazione della finestra temporale (__windowing__), che comporta inevitabilmente una perdita di risoluzione in frequenza e l'introduzione di dispersione spettrale;
4. Calcolo numerico della trasformata tramite algoritmi __DFT__ o __FFT__ con la precisione desiderata.

Nel mondo reale ogni segnale viene acquisito per un intervallo di tempo limitato $T_L = L \cdot T$. È quindi necessario studiare l'effetto della finestratura nel dominio della [[4. Spettro in frequenza - DTFT|DTFT]], poiché la [[5. Trasformata discreta di Fourier (DFT)|DFT]] opera intrinsecamente su sequenze a durata finita.

La finestra rettangolare ideale di lunghezza $L$ è definita da:

$$
w(n) = \begin{cases}
1, & 0 \le n \le L-1 \\
0, & \text{altrove}
\end{cases}
$$

Applicare la finestra al segnale discreto indefinito $x(n)$ equivale a eseguire un prodotto puntuale nel tempo:

$$
x_L(n) = x(n) \cdot w(n) = \begin{cases}
x(n), & 0 \le n \le L-1 \\
0, & \text{altrove}
\end{cases}
$$

Confrontando le rispettive DTFT:

$$
\begin{align}
X(\omega) &= \sum_{n=-\infty}^{\infty} x(n) \mathrm{e}^{-j\omega n} \\ \\
X_L(\omega) &= \sum_{n=0}^{L-1} x(n) \mathrm{e}^{-j\omega n} \\ \\
& X(\omega) \neq X_L(\omega)
\end{align}
$$

Dato che il prodotto nel dominio del tempo corrisponde alla convoluzione periodica nel dominio delle frequenze:

$$
x_L(n) = x(n) \cdot w(n) \quad \xleftrightarrow{\quad \text{DTFT} \quad} \quad X_L(\omega) = \frac{1}{2\pi} X(\omega) \circledast W(\omega)
$$

## Finestra Nel Dominio Delle Frequenze

Nel dominio della frequenza continua normalizzata $\omega$, il segnale finestrato $X_L(\omega)$ è dato dalla __convoluzione periodica__ (integrale di convoluzione su un periodo fondamentale di ampiezza $2\pi$):

$$
X_L(\omega) = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(\theta) W(\omega - \theta) \,\mathrm{d}\theta
$$

Per determinare lo spettro $W(\omega)$ della finestra rettangolare, calcoliamo la DTFT della sequenza $w(n)$:

> [!NOTE] Serie Geometrica
> Ricordando la somma notevole della serie geometrica troncata:
>
> $$
> \sum_{k=0}^{n} x^k = \frac{1 - x^{n+1}}{1 - x}
> $$

Esplicitando la sommatoria:

$$
\begin{align}
W(\omega) &= \sum_{n=-\infty}^{+\infty} w(n) \mathrm{e}^{-j\omega n} = \sum_{n=0}^{L-1} \mathrm{e}^{-j\omega n} \\
&= \frac{1 - \mathrm{e}^{-j\omega L}}{1 - \mathrm{e}^{-j\omega}} = \frac{\sin(\omega L / 2)}{\sin(\omega / 2)} \mathrm{e}^{-j\omega(L-1)/2}
\end{align}
$$

La funzione spettrale ottenuta è il __sinc periodico__ (nucleo di Dirichlet):
- Il termine d'ampiezza $\frac{\sin(\omega L / 2)}{\sin(\omega / 2)}$ presenta valore di picco $W(0) = L$ a centro banda ($\omega = 0$); il suo modulo determina il profilo dello spettro, caratterizzato da un __lobo principale__ centrale e da una serie di __lobi laterali__ (sidelobes);
- Il fattore di fase $\mathrm{e}^{-j\omega(L-1)/2}$ rappresenta il ritardo di gruppo costante introdotto dalla finestra causale centrata in $M = \frac{L-1}{2}$.

![[immagini/sidelobes.png|center mid]]

### Dispersione Spettrale (Spectral Leakage)

Il troncamento temporale netto genera il fenomeno della __dispersione spettrale__ (__frequency leakage__).

A causa della convoluzione con $W(\omega)$, l'energia di ciascuna riga sinusoidale del segnale originale non rimane concentrata sulla propria frequenza nominale, ma viene parzialmente "spalmata" sulle frequenze adiacenti attraverso i lobi laterali della finestra.

Se nel segnale sono presenti componenti sinusoidali con ampiezze molto disuguali, i lobi laterali di una sinusoide ad alta energia possono mascherare completamente una componente debole vicina.

### Risoluzione in Frequenza

La finestratura comporta inoltre una limitazione intrinseca sulla __risoluzione in frequenza__, definita come la minima distanza che due toni sinusoidali devono avere per essere distinti come due picchi separati nello spettro:

> [!IMPORTANT] Risoluzione in Frequenza
> La risoluzione fisica in frequenza è vincolata dalla durata finita dell'osservazione temporale $T_L = L \cdot T = \frac{L}{f_s}$:
>
> $$
> \Delta f = \frac{1}{T_L} = \frac{f_s}{L}
> $$

![[immagini/ris_frequenza.png|center mid]]

Se la distanza tra due righe spettrali è inferiore a $\Delta f$, i rispettivi lobi principali si fondono in un unico picco indistinguibile.

Per attenuare i lobi secondari e ridurre il leakage non è sufficiente aumentare $L$: occorre impiegare finestre temporali smussate che riducano gradualmente l'ampiezza ai bordi, eliminando la transizione a gradino.

## Finestre a Coseno Rialzato (Hamming E Hann)

Per attenuare i lobi laterali si utilizzano finestre ponderate basate sul coseno rialzato. La più diffusa è la __finestra di Hamming__:

$$
w(n) = \begin{cases}
0.54 - 0.46 \cos\left(\frac{2\pi n}{L-1}\right), & 0 \le n \le L-1 \\
0, & \text{altrove}
\end{cases}
$$

> [!NOTE] Relazione tra Hann e Hamming
> Entrambe appartengono alla famiglia delle finestre a coseno rialzato $w(n) = \alpha - \beta \cos\left(\frac{2\pi n}{L-1}\right)$:
> - La __finestra di Hann__ (o Hanning) adotta pesi uguali $\alpha = 0.5$, $\beta = 0.5$, azzerando esattamente i campioni agli estremi ($w(0) = w(L-1) = 0$);
> - La __finestra di Hamming__ adotta $\alpha = 0.54$, $\beta = 0.46$, lasciando un piccolo scalino ai bordi ottimizzato per cancellare quasi perfettamente il primo lobo secondario.

![[immagini/hamming.png|center mid]]

La finestra di Hamming porta l'attenuazione del lobo secondario a circa $-40\text{ dB}$ ( $-43\text{ dB}$ teorici, rispetto ai soli $-13\text{ dB}$ della finestra rettangolare), al prezzo di raddoppiare la larghezza del lobo principale ($c = 2$): la risoluzione in frequenza si dimezza a parità di campioni, ma per recuperare la separabilità richiesta è sufficiente aumentare la lunghezza $L$.

## Finestra Parametrica Di Kaiser

Le finestre fisse (come la rettangolare o la Hamming) offrono un valore di attenuazione rigido e non modificabile. La __finestra di Kaiser__ supera questo limite introducendo un parametro di forma $\alpha$ (denotato frequentemente come $\beta$ nella letteratura ingegneristica e in MATLAB) regolabile in modo continuo:

$$
w(n) = \frac{I_0\left(\alpha \sqrt{1 - \frac{(n-M)^2}{M^2}}\right)}{I_0(\alpha)}, \quad 0 \le n \le L-1, \quad M = \frac{L-1}{2}
$$

> [!NOTE] Funzione di Bessel $I_0$
> $I_0(x)$ è la funzione di Bessel modificata del primo tipo e di ordine zero.

Tramite le relazioni empiriche sviluppate da J. F. Kaiser (Orfanidis, Sez. 10.2), assegnati il livello desiderato di attenuazione dei lobi laterali $R$ (in dB positivi, $R > 0$) e la risoluzione spettrale richiesta $\Delta f_w$, è possibile ricavare l'ordine del filtro $M = L-1$ (e quindi la lunghezza finita $L = \lceil c f_s / \Delta f_w \rceil + 1$) e il parametro di forma $\alpha$:

$$
L - 1 = \frac{c f_s}{\Delta f_w} \iff \Delta f_w = \frac{c f_s}{L-1}
$$

Il fattore di allargamento del lobo principale $c$ è legato all'attenuazione $R$ da:

$$
c = \frac{6 (R + 12)}{155}
$$

Il parametro di forma $\alpha$ si calcola in base all'intervallo di attenuazione desiderato:

$$
\alpha = \begin{cases}
0, & R \le 13.26 \\
0.76609(R - 13.26)^{0.4} + 0.09834(R - 13.26), & 13.26 < R \le 60 \\
0.12438(R + 6.3), & 60 < R \le 120
\end{cases}
$$

> [!IMPORTANT] Limite di Applicabilità della Finestra di Kaiser
> Le formule empiriche di Kaiser sono calibrate per un intervallo di attenuazione fino a $120\text{ dB}$; per valori superiori a $120\text{ dB}$ le approssimazioni empiriche perdono precisione.

Per ridurre l'ampiezza dei lobi laterali (aumentare l'attenuazione $R$) è necessario incrementare il coefficiente $c$, con conseguente allargamento del lobo principale: a parità di risoluzione $\Delta f_w$, occorrerà quindi aumentare la lunghezza complessiva $L$ della sequenza.

### Tabella Comparativa Delle Finestre

|     Finestra     | Attenuazione Lobi Secondari $R$ (dB) | Fattore di Risoluzione ($c$) |
| :--------------: | :----------------------------------: | :--------------------------: |
| __Rettangolare__ |            $13\text{ dB}$            |             $1$              |
|   __Hamming__    |            $40\text{ dB}$            |             $2$              |
|    __Kaiser__    |           Variabile ($R$)            |    $\frac{6(R+12)}{155}$     |

> [!NOTE] Convenzione sull'Attenuazione $R$
> Nelle formule di Kaiser, $R$ è espresso come valore positivo in dB indicante la reiezione dei lobi secondari rispetto al lobo principale (corrispondente rispettivamente a un livello di $-13\text{ dB}$ per la rettangolare e $-40\text{ dB}$ per la Hamming).



# 7. Stima Spettrale Di Segnali Non Stazionari

Un segnale stazionario _non varia_ le proprie caratteristiche statistiche e spettrali nel tempo (ampiezza e frequenze rimangono costanti), a differenza di un segnale __non stazionario__ il cui contenuto spettrale evolve continuamente (es. voce umana, segnali musicali, segnali biomedici, segnali radar o sonar a modulazione di frequenza come i chirp).

Nell'analisi spettrale di segnali non stazionari emergono due esigenze applicative fondamentali:
1. __Spettro istantaneo__: determinare come varia il contenuto in frequenza del segnale istante per istante nel corso del tempo;
2. __Spettro medio__: valutare la distribuzione media dell'energia o della potenza lungo l'intera durata dell'osservazione.

## Segnali Stazionari a Tratti E Tempo Di Stazionarietà

Poiché la trasformata di Fourier classica ([[4. Spettro in frequenza - DTFT|DTFT]] e [[5. Trasformata discreta di Fourier (DFT)|DFT]]) integra il segnale lungo tutto il tempo fornendo una rappresentazione globale priva di localizzazione temporale, non è adatta a descrivere segnali le cui frequenze cambiano nel tempo.

Tuttavia, la quasi totalità dei segnali fisici reali non varia in modo istantaneo, ma può essere modellata come __stazionaria a tratti__.

> [!IMPORTANT] Tempo di Stazionarietà ($T_{\text{staz}}$)
> Si definisce __tempo di stazionarietà__ il massimo intervallo temporale entro il quale le proprietà statistiche e spettrali del segnale possono essere considerate ragionevolmente costanti.
> Ad esempio, per il segnale vocale umano il tempo di stazionarietà tipico è compreso tra $10$ e $20\text{ ms}$.

Sezionando il segnale continuo in intervalli di durata non superiore a $T_{\text{staz}}$, all'interno di ciascun frammento è possibile assumere l'ipotesi di stazionarietà e applicare gli strumenti classici dell'analisi di Fourier.

## Schema Di Acquisizione Ed Elaborazione

La catena di elaborazione per la stima spettrale di segnali non stazionari è riassunta nello schema a blocchi seguente:

![[immagini/schema_blocchi_stazionario.svg|center big]]

La pipeline si articola in cinque fasi consecutive:
1. __Filtro Anti-Aliasing (FAA)__: limita superiormente la banda del segnale analogico continuo $x(t)$, rendendolo a banda limitata entro la frequenza di Nyquist;
2. __Convertitore A/D__: campiona il segnale a frequenza di campionamento $f_s$ (periodo di campionamento $T = 1/f_s$), generando la sequenza discreta $x(n)$;
3. __Frame Blocking__: suddivide il flusso indefinito $x(n)$ in una successione di blocchi temporali (frame) di lunghezza $L$ campioni, con passo di avanzamento $M$ (hop size) tra un blocco e il successivo. Affinché ciascun blocco sia stazionario, la sua durata fisica deve rispettare il vincolo $\Delta t = L \cdot T = \frac{L}{f_s} \le T_{\text{staz}}$;
4. __Finestratura $w(n)$__: ciascun frame estratto viene moltiplicato per una [[6. Finestratura|funzione finestra]] (es. Hamming o Kaiser) per smussare le discontinuità ai bordi e limitare la dispersione spettrale (spectral leakage);
5. __Calcolo della DFT/FFT__: su ciascun blocco finestrato viene calcolata una DFT di dimensione $N$ (tipicamente con algoritmo FFT estendendo il blocco con eventuale zero-padding fino a una potenza di due).

## Short-Time Fourier Transform (STFT)

La __Short-Time Fourier Transform (STFT)__ formalizza matematicamente questo procedimento: non si tratta di una nuova trasformata astratta, ma di una sequenza di DFT calcolate su blocchi temporali consecutivi.

Per il generico blocco $m$-esimo di lunghezza $L$ estratto con passo di scorrimento $M$ (hop size) e finestrato con $w(n)$, la trasformata discreta a $N$ punti è definita da:

$$
X(k, m) = \sum_{n=0}^{L-1} x(m M + n) \, w(n) \, \mathrm{e}^{-j \frac{2\pi k}{N} n}, \quad k = 0, \dots, N-1
$$

dove:
- $m$ è l'indice discreto del frame temporale ($m = 0, \dots, K_{\text{tot}}-1$);
- $k$ è l'indice del bin di frequenza discreta ($k = 0, \dots, N-1$), corrispondente alla frequenza analogica $f_k = \frac{k f_s}{N}$;
- $w(n)$ è la finestra temporale di analisi di lunghezza $L$ ($0 \le n \le L-1$);
- $M$ è l'intervallo di avanzamento (hop size) in campioni tra blocchi successivi (con sovrapposizione se $M < L$);
- $L$ è la lunghezza in campioni di ciascun blocco temporale;
- $N$ è il numero di punti su cui viene calcolata la DFT/FFT ($N \ge L$).

Il risultato complessivo della STFT non è un singolo vettore spettrale, bensì una __matrice bidimensionale tempo-frequenza__ di dimensioni $N \times K_{\text{tot}}$, dove le righe indicizzano le frequenze discrete $k$ e le colonne indicizzano i blocchi temporali $m$.

### Informazioni Ricavabili Dalla Matrice Spettrale

La matrice tempo-frequenza $X(k, m)$ consente di risolvere direttamente i problemi conoscitivi iniziali:

- __Spettro Istantaneo__: corrisponde all'estrazione di una singola colonna $m$-esima della matrice $X(k, m)$. Fornisce l'istantanea del contenuto in frequenza del segnale nell'intervallo temporale occupato da quel determinato frame;
- __Spettrogramma__: è la rappresentazione visiva globale 2D dell'intensità energetica $|X(k, m)|^2$. L'asse orizzontale rappresenta l'evoluzione temporale ($m$), l'asse verticale rappresenta le frequenze ($k$), mentre l'intensità o il colore di ciascun pixel codifica la potenza associata a quella specifica coordinata tempo-frequenza;
- __Spettro Medio__: si calcola mediando sull'asse temporale (ovvero mediando su tutti i blocchi $m=0,\dots,K_{\text{tot}}-1$ per ciascuna frequenza $k$) i valori di potenza dello __spettrogramma__ $|X(k, m)|^2$:

$$
P_{\text{medio}}(k) = \frac{1}{K_{\text{tot}}} \sum_{m=0}^{K_{\text{tot}}-1} |X(k, m)|^2
$$

Fornisce una stima spettrale di potenza globale a lungo termine (equivalente al metodo di Welch per la stima della PSD), superando le fluttuazioni transitorie e preservando il contenuto energetico senza le cancellazioni distruttive di fase che deriverebbero dalla media diretta dei coefficienti complessi $X(k, m)$.

### Trade-Off Di Risoluzione Tempo-Frequenza

La scelta della dimensione del blocco $L$ introduce un vincolo di indeterminazione intrinseco (principio di indeterminazione tempo-frequenza di Heisenberg-Gabor):
- __Blocchi lunghi__ ($L$ elevato): aumentano la risoluzione in frequenza ($\Delta f = \frac{f_s}{L}$ diminuisce, lobi più stretti), ma degradano la risoluzione temporale $\Delta t = \frac{L}{f_s}$, con il rischio concreto di violare il tempo di stazionarietà $T_{\text{staz}}$ e mascherare transitori rapidi;
- __Blocchi corti__ ($L$ ridotto): garantiscono un'eccellente localizzazione temporale degli eventi transitori, ma peggiorano sensibilmente la risoluzione in frequenza, producendo lobi principali larghi che possono fondere righe spettrali adiacenti.

Nella pratica si sceglie $L$ come compromesso guidato dal tempo di stazionarietà $T_{\text{staz}}$ dell'applicazione, oppure si eseguono analisi multiscala con finestre di dimensioni differenti.



# 8. Filtri FIR - Finite Impulse Response

![[immagini/Filtri_FIR.svg|center mid]]

La progettazione di un filtro digitale con tagli perfettamente netti nella risposta in frequenza è fisicamente irrealizzabile, poiché richiederebbe una risposta impulsiva a durata temporale infinita e non causale.

## Comportamenti Di Non Idealità

In un filtro reale compaiono scostamenti inevitabili rispetto alla risposta ideale:
- Nella __banda passante__ ($0 \le f \le f_{\text{pass}}$), dove idealmente il guadagno dovrebbe valere $1$, la risposta oscilla attorno a $1$ con un'ondulazione massima detta __ripple di banda passante__ $\delta_{\text{pass}}$, mantenendosi nell'intervallo $[1 - \delta_{\text{pass}}, 1 + \delta_{\text{pass}}]$;
- Nella __banda di arresto__ ($f \ge f_{\text{stop}}$), dove idealmente il guadagno dovrebbe annullarsi a $0$, la risposta reale presenta oscillazioni residue contenute al di sotto di una soglia $\delta_{\text{stop}}$.

> [!IMPORTANT] Attenuazione in Banda di Arresto ($A_{\text{stop}}$)
> L'__attenuazione in banda di arresto__ quantifica l'abbattimento minimo (in dB) del segnale nella stopband rispetto al livello unitario della passband:
>
> $$A_{\text{stop}} = -20 \log_{10} \delta_{\text{stop}}$$

L'intervallo compreso tra la fine della banda passante $f_{\text{pass}}$ e l'inizio della banda di arresto $f_{\text{stop}}$ costituisce la __banda di transizione__:

$$
\Delta f = f_{\text{stop}} - f_{\text{pass}}
$$

> [!NOTE] Selettività dei Filtri
> Un filtro è detto __selettivo__ se presenta una banda di transizione $\Delta f$ molto stretta: più rapido è il passaggio tra banda passante e banda di arresto, maggiore è la selettività del filtro.

### Ritardo Di Gruppo E Linearità Della Fase

I filtri FIR a fase lineare introducono un ritardo temporale costante indipendente dalla frequenza:

$$
M = \frac{N - 1}{2}
$$

dove $N$ è il numero di coefficienti (lunghezza del filtro). Tale proprietà è fondamentale nelle applicazioni audio, biomedicali e di telecomunicazioni, poiché garantisce l'assenza di distorsione di fase: tutte le componenti armoniche attraversano il sistema subendo lo stesso ritardo.

## Progettare Un Filtro FIR - Metodo Delle Finestre

Il metodo delle finestre parte dalla specifica della risposta in frequenza ideale $D(\omega)$ e ne ricava la risposta impulsiva ideale $d(k)$ mediante l'[[4. Spettro in frequenza - DTFT#IDTFT|IDTFT]]:

$$
D(\omega) = \sum_{k=-\infty}^{\infty} d(k) \mathrm{e}^{-j\omega k} \iff d(k) = \frac{1}{2\pi} \int_{-\pi}^{\pi} D(\omega) \mathrm{e}^{j\omega k}\,\mathrm{d}\omega
$$

In generale, la risposta impulsiva ideale $d(k)$ ha estensione temporale infinita ed è simmetrica rispetto all'origine $k = 0$.

> [!EXAMPLE] Filtro Passa-Basso Ideale (LP)
> La risposta in frequenza ideale per un passa-basso con pulsazione di taglio $\omega_c$ è:
>
> $$
> D(\omega) = \begin{cases}
> 1, & |\omega| \le \omega_c \\
> 0, & \omega_c < |\omega| \le \pi
> \end{cases}
> $$
>
> Calcolando la trasformata inversa:
>
> $$
> \begin{align}
> d(k) &= \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} 1 \cdot \mathrm{e}^{j\omega k}\,\mathrm{d}\omega \\
> &= \left[ \frac{\mathrm{e}^{j\omega k}}{2\pi j k} \right]_{-\omega_c}^{\omega_c} = \frac{\mathrm{e}^{j\omega_c k} - \mathrm{e}^{-j\omega_c k}}{2\pi j k}
> \end{align}
> $$
>
> Applicando la formula di Eulero si ottiene la classica funzione campionatrice:
>
> $$
> d(k) = \frac{\sin(\omega_c k)}{\pi k}, \quad -\infty < k < \infty
> $$
>
> Nel centro di simmetria $k = 0$, applicando il limite notevole:
>
> $$
> d(0) = \frac{\omega_c}{\pi}
> $$
>
> Se la frequenza di taglio è scelta come frazione intera della frequenza di campionamento (es. $\omega_c = \frac{\pi}{L}$), i passaggi per lo zero della risposta impulsiva cadranno esattamente in corrispondenza dei multipli interi di $L$ ($k = \pm L, \pm 2L, \dots$).

> [!EXAMPLE] Altre Tipologie di Filtri Ideali
> ### Passa-Alto (HP)
> Sfruttando la __proprietà di complementarietà__ rispetto al filtro passa-basso:
>
> $$
> D_{\text{HP}}(\omega) = 1 - D_{\text{LP}}(\omega) \implies d_{\text{HP}}(k) = \delta(k) - d_{\text{LP}}(k)
> $$
>
> ### Passa-Banda (BP)
> Ottenuto dalla differenza tra due filtri passa-basso con frequenze di taglio $\omega_b > \omega_a$:
>
> $$
> D_{\text{BP}}(\omega) = D_{\text{LP}_b}(\omega) - D_{\text{LP}_a}(\omega)
> $$
>
> ### Arresta-Banda (BS / Notch)
> Complementare rispetto al passa-banda:
>
> $$
> D_{\text{BS}}(\omega) = 1 - D_{\text{BP}}(\omega)
> $$

### Causalità E Ritardo Nei Filtri FIR

Dal punto di vista della causalità temporale:
- Una sequenza è __causale__ se i suoi campioni sono nulli per indici temporali negativi ($n < 0$);
- Una sequenza è __anticausale__ se è non nulla solo per campioni passati e si esaurisce nell'istante di osservazione ($n \le 0$);
- Una sequenza è __mista (o non causale)__ se si estende sia prima che dopo l'origine dei tempi.

![[immagini/segnale_causale.svg|center small]] ![[immagini/segnale_anticausale.svg|center small]] ![[immagini/segnale_non_causale.svg|center small]]

La risposta ideale $d(k)$ ha estensione mista (non causale), estendendosi da $-\infty$ a $+\infty$. Se provassimo a calcolare l'uscita:

$$
y(n) = \sum_{k=-M}^{M} d(k) x(n-k) = \sum_{k=0}^{M} d(k) x(n-k) + \sum_{k=-M}^{-1} d(k) x(n-k)
$$

I termini con $k < 0$ (come $x(n - (-1)) = x(n + 1)$) richiederebbero campioni futuri del segnale, impossibili da acquisire in tempo reale.

Per rendere il filtro realizzabile occorre:
1. __Troncare la risposta impulsiva__ a un intervallo finito $-M \le k \le M$ di lunghezza $N = 2M + 1$;
2. __Traslare la risposta verso destra__ di $M$ campioni, rendendola causale al costo di introdurre un __ritardo puro__ di $M = \frac{N-1}{2}$ campioni.

> [!IMPORTANT] Ritardo dei Filtri FIR Simmetrici
> Un filtro FIR simmetrico a fase lineare di lunghezza $N = 2M + 1$ campioni produce __sempre__ un ritardo di gruppo pari a:
>
> $$M = \frac{N - 1}{2} \text{ campioni}$$

### Finestra Rettangolare E Troncamento

Il troncamento simmetrico equivale a considerare i campioni di $d(k)$ nell'intervallo $[-M, M]$:

$$
d(k) = \frac{1}{2\pi} \int_{-\pi}^{\pi} D(\omega) \mathrm{e}^{j\omega k}\,\mathrm{d}\omega, \quad -M \le k \le M
$$

Il vettore dei coefficienti troncati è:

$$
d = [d_{-M}, d_{-M+1}, \dots, d_{-1}, d_0, d_1, \dots, d_{M-1}, d_M]
$$

L'origine $k = 0$ coincide con il centro di simmetria $d_0$. Per rendere la sequenza causale si definisce il filtro $h(n)$ ritardando la sequenza di $M$ passi:

$$
h(n) = d(n - M), \quad n = 0, 1, \dots, N-1
$$

Il vettore risultante $h = [h_0, h_1, \dots, h_{N-1}]$ ha indici interamente non negativi.

Per un filtro passa-basso, la risposta impulsiva causale diventa:

$$
h(n) = d(n - M) = \frac{\sin(\omega_c (n - M))}{\pi (n - M)}, \quad n = 0, \dots, N-1
$$

Il segnale filtrato si ottiene tramite la convoluzione lineare a lunghezza finita:

$$
y(n) = \sum_{k=0}^{2M} h(k) x(n-k)
$$

Nel dominio della frequenza, il troncamento corrisponde alla somma finita:

$$
\hat{D}(\omega) = \sum_{k=-M}^{M} d(k) \mathrm{e}^{-j\omega k}
$$

La risposta in frequenza del filtro causale traslato $h(n)$ è:

$$
H(\omega) = \mathrm{e}^{-j\omega M} \hat{D}(\omega) = \mathrm{e}^{-j\omega M} \sum_{k=-M}^{M} d(k) \mathrm{e}^{-j\omega k}
$$

Dato che $d(k)$ è reale e simmetrica ($d(-k) = d(k)$), la sommatoria $\hat{D}(\omega)$ è una funzione puramente __reale e pari__ in $\omega$. La fase complessiva del filtro è quindi data da $\theta(\omega) = -M\omega$ nei tratti in cui $\hat{D}(\omega) > 0$, mentre presenta salti di $\pm \pi$ in corrispondenza dei cambi di segno di $\hat{D}(\omega)$ (fase lineare generalizzata):

$$
\theta(\omega) = -M\omega
$$

confermando la perfetta __linearità della fase__ e l'assenza di distorsione di fase (il ritardo di gruppo è rigorosamente costante: $\tau_g = - \frac{\mathrm{d}\theta}{\mathrm{d}\omega} = M$).

#### Approssimazione Del Filtro Ideale E Fenomeno Di Gibbs

Consideriamo come esempio un filtro passa-basso ideale con frequenza di taglio normalizzata $\omega_c = 0.3\pi$, troncato a due diverse lunghezze: $N = 41$ ($M = 20$) e $N = 121$ ($M = 60$).

Per la prima finestra ($N = 41$):

$$
h(n) = d(n - 20) = \frac{\sin(0.3\pi (n - 20))}{\pi (n - 20)}, \quad n = 0, \dots, 40
$$

Per la seconda finestra ($N = 121$):

$$
h(n) = d(n - 60) = \frac{\sin(0.3\pi (n - 60))}{\pi (n - 60)}, \quad n = 0, \dots, 120
$$

Il confronto tra le risposte impulsive:

![[immagini/FIR_rec_window_response.png|center big]]

E tra le rispettive risposte in frequenza:

![[immagini/FIR_rec_window_freq_res.png|center big]]

Le oscillazioni visibili nella risposta in frequenza derivano dal troncamento netto nel tempo ([[6. Finestratura#Finestra nel Dominio delle Frequenze|finestra rettangolare]]). La risposta complessiva è data dal prodotto nel tempo $h(n) = w(n) d(n-M)$, che nel dominio delle frequenze corrisponde alla convoluzione periodica:

$$
\begin{align}
H(\omega) &= \frac{1}{2\pi} \int_{-\pi}^{\pi} W(\omega - \omega') \mathrm{e}^{-j\omega' M} D(\omega')\,\mathrm{d}\omega' \\
&= \frac{1}{2\pi} \int_{-\omega_c}^{\omega_c} W(\omega - \omega') \mathrm{e}^{-j\omega' M}\,\mathrm{d}\omega'
\end{align}
$$

Dal confronto emergono tre proprietà fondamentali:
1. All'aumentare di $N$, la risposta $\hat{D}(\omega)$ converge puntualmente a $D(\omega)$ su quasi tutto l'intervallo;
2. La larghezza della banda di transizione $\Delta f$ diminuisce proporzionalmente a $1/N$;
3. In prossimità del salto di discontinuità a $\omega = \omega_c$, le oscillazioni non si riducono in ampiezza, ma mantengono una sovraelongazione costante pari a circa l'__8.9%__ (fenomeno di Gibbs). All'aumentare di $N$, le oscillazioni vengono schiacciate verso la discontinuità, concentrandosi in una regione di ampiezza infinitesima attorno a $\omega_c$ (un insieme limite di misura nulla), ma senza ridursi in ampiezza.

### Finestra Di Hamming

Per eliminare l'oscillazione residua dell'8.9% dovuta alla finestra rettangolare, si applica una finestra temporale a bordi smussati. Impiegando la __finestra di Hamming__ (finestra a coseno rialzato):

$$
w(n) = 0.54 - 0.46 \cos\left(\frac{2\pi n}{N-1}\right), \quad n = 0, 1, \dots, N-1
$$

La risposta impulsiva finestrata risulta:

$$
h(n) = w(n) d(n-M) = \left[ 0.54 - 0.46 \cos\left(\frac{2\pi n}{N-1}\right) \right] \cdot \frac{\sin(\omega_c (n - M))}{\pi (n - M)}
$$

![[immagini/FIR_hamming_ris_freq.png|center big]]

A parità di lunghezza $N$, la finestra di Hamming abbatte drasticamente il ripple in banda passante e di arresto (riducendolo a circa lo $0.2\%$, corrispondente a un'attenuazione $A_{\text{stop}} \approx 54\text{ dB}$), al prezzo di raddoppiare l'ampiezza della banda di transizione.

### Finestra Di Kaiser

La __finestra di Kaiser__ consente di svincolarsi dai valori fissi delle finestre classiche, offrendo il pieno controllo simultaneo sia sull'attenuazione in stopband che sulla larghezza di transizione:

$$
w(n) = \frac{I_0\left(\alpha \sqrt{1 - \frac{(n-M)^2}{M^2}}\right)}{I_0(\alpha)}, \quad 0 \le n \le N-1, \quad M = \frac{N-1}{2}
$$

(dove $I_0(\cdot)$ denota la funzione di Bessel modificata del primo tipo e di ordine zero).

Le specifiche di progetto del filtro sono definite tramite quattro parametri:
- $\delta_{\text{pass}}$: ondulazione massima tollerata in banda passante;
- $\delta_{\text{stop}}$: ondulazione massima tollerata in banda di arresto;
- $f_{\text{pass}}$: frequenza limite della banda passante;
- $f_{\text{stop}}$: frequenza iniziale della banda di arresto.

La frequenza di taglio $f_c$ e la banda di transizione $\Delta f$ valgono:

$$
f_c = \frac{1}{2}(f_{\text{pass}} + f_{\text{stop}}), \quad \Delta f = f_{\text{stop}} - f_{\text{pass}}
$$

In termini di pulsazioni normalizzate rispetto alla frequenza di campionamento $f_s$:

$$
\omega_{\text{pass}} = \frac{2\pi f_{\text{pass}}}{f_s}, \quad \omega_{\text{stop}} = \frac{2\pi f_{\text{stop}}}{f_s}, \quad \omega_c = \frac{2\pi f_c}{f_s}, \quad \Delta\omega = \frac{2\pi \Delta f}{f_s}
$$

I valori di attenuazione (in dB) sono calcolati da:

$$
A_{\text{pass}} = 20 \log_{10}\left(\frac{1 + \delta_{\text{pass}}}{1 - \delta_{\text{pass}}}\right), \quad A_{\text{stop}} = -20 \log_{10} \delta_{\text{stop}}
$$

Il metodo di Kaiser genera ondulazioni identiche nelle due bande; si dimensiona pertanto il filtro sul vincolo più stringente:

$$
\delta = \min(\delta_{\text{pass}}, \delta_{\text{stop}}) \implies A = -20 \log_{10}\delta, \quad \delta = 10^{-\frac{A}{20}}
$$

Di solito il vincolo più stringente è $\delta_{\text{stop}}$.

#### Parametro Di Forma $\alpha$

Nel progetto di filtri FIR il parametro di forma $\alpha$ è legato all'attenuazione $A$ dalle formule di Kaiser:

> [!WARNING] Differenza tra Filtri e Stima Spettrale
> Nel progetto dei filtri FIR il parametro $\alpha$ assume valori differenti rispetto alla stima spettrale, poiché l'effetto della finestra deriva dall'integrazione del suo spettro sulla banda di transizione:
>
> $$
> \alpha = \begin{cases}
> 0.1102(A - 8.7), & A \ge 50 \\
> 0.5842(A - 21)^{0.4} + 0.07886(A - 21), & 21 < A < 50 \\
> 0, & A \le 21
> \end{cases}
> $$

#### Banda Di Transizione E Lunghezza Del Filtro

La lunghezza del filtro $N$ e la banda di transizione $\Delta f$ sono legate dalla relazione:

$$
\Delta f = \frac{D f_s}{N - 1} \iff N - 1 = \frac{D f_s}{\Delta f}
$$

Il fattore numerico $D$ si ricava dall'attenuazione $A$:

$$
D = \begin{cases}
\frac{A - 7.95}{14.36}, & A > 21 \\
0.922, & A \le 21
\end{cases}
$$

### Algoritmo Di Progetto Del Filtro Con Finestra Di Kaiser

I passi operativi per il dimensionamento completo sono:
1. Calcolare $f_c$ e $\Delta f$ a partire dalle frequenze di specifica $f_{\text{pass}}$ e $f_{\text{stop}}$;
2. Determinare la pulsazione di taglio normalizzata $\omega_c = \frac{2\pi f_c}{f_s}$;
3. Calcolare i ripple $\delta_{\text{pass}}$ e $\delta_{\text{stop}}$ dai valori di attenuazione richiesti;
4. Identificare il vincolo peggiore $\delta = \min(\delta_{\text{pass}}, \delta_{\text{stop}})$ e calcolare l'attenuazione $A = -20 \log_{10}\delta$ in dB;
5. Calcolare i parametri $\alpha$ e $D$;
6. Ricavare la lunghezza del filtro $N = 1 + \frac{D f_s}{\Delta f}$ e arrotondarla all'intero __dispari__ successivo più vicino ($N = 2M + 1$);
7. Impostare il semi-ordine $M = \frac{N - 1}{2}$;
8. Calcolare i campioni della finestra di Kaiser $w(n)$ per $n = 0, \dots, N-1$;
9. Determinare la risposta impulsiva causale del filtro finestrato:

   $$h(n) = w(n) d(n-M) = w(n) \frac{\sin(\omega_c (n - M))}{\pi (n - M)}$$

   Nel centro di simmetria $n = M$, dato che $w(M) = 1$, vale esattamente:

   $$h(M) = \frac{\omega_c}{\pi}$$

## Metodo Del Campionamento in Frequenza

Quando la risposta desiderata $D(\omega)$ ha un profilo analitico complesso per cui non è agevole calcolare l'integrale della IDTFT in forma analitica chiusa, è possibile campionare la risposta in frequenza in $N$ punti equispaziati incorporando direttamente la fase lineare corrispondente al ritardo causale $M = \frac{N-1}{2}$:

$$
H(k) = D\left(\frac{2\pi k}{N}\right) \mathrm{e}^{-j \frac{2\pi k}{N} M}, \quad k = 0, 1, \dots, N-1
$$

Applicando una [[5. Trasformata discreta di Fourier (DFT)#IDFT|IDFT]] a $N$ punti sui campioni complessi $H(k)$, si ottiene direttamente la sequenza temporale causale $h(n)$ di lunghezza $N$:

$$
h(n) = \text{IDFT}\{H(k)\} = \frac{1}{N} \sum_{k=0}^{N-1} H(k) \mathrm{e}^{j \frac{2\pi}{N} k n}, \quad n = 0, 1, \dots, N-1
$$

La risposta in frequenza continua $H(\omega)$ interpola esattamente i campioni desiderati nelle frequenze discrete $\omega_k = \frac{2\pi k}{N}$. Per mitigare le oscillazioni di Gibbs tra i nodi campionati senza alterare l'interpolazione esatta tramite finestratura temporale, nella pratica di progetto si lasciano tipicamente uno o due campioni non vincolati nella banda di transizione, ottimizzandone numericamente l'ampiezza per massimizzare l'attenuazione in banda di arresto.

## Filtri a Sottobande

Un banco di filtri a sottobande scompone un segnale d'ingresso $x(n)$ con spettro $X(f)$ in un insieme di $K$ segnali distinti a banda ridotta $x_1(n), x_2(n), \dots, x_K(n)$.

![[immagini/banco_filtri_sottobanda.svg|center big]]

La condizione di ricostruzione perfetta per filtri causali impone che la somma delle uscite delle sottobande restituisca il segnale originale ritardato del ritardo di gruppo comune $M$:

$$
\sum_{i=1}^{K} x_i(n) = x(n - M)
$$

dove $M = \frac{N-1}{2}$ campioni.

Per garantire questa proprietà si impiega una batteria di $K$ filtri digitali complementari:

$$
h_1(n), h_2(n), \dots, h_K(n)
$$

I vincoli di progetto reali per il banco di filtri implicano che:
- Le bande di transizione siano __sovrapposte e complementari__: l'intervallo di transizione di un filtro coincide con l'intervallo di transizione del filtro contiguo, incrociandosi alla frequenza di taglio a $-6\text{ dB}$ (ossia $-3\text{ dB}$ di potenza);
- Nel caso della finestra di Kaiser, tutti i filtri del banco condividano la __stessa lunghezza__ $N$ (ossia lo stesso ordine $N-1$), garantendo il medesimo ritardo temporale $M = \frac{N-1}{2}$ su tutte le sottobande affinché le componenti possano essere ricomposte in fase;
- Tutti i filtri offrano la medesima attenuazione in banda di arresto.



# 9. Filtri IIR - Fondamenti E Trasformata Z

I filtri __IIR (Infinite Impulse Response)__ sono sistemi lineari tempo-invarianti (LTI) a tempo discreto caratterizzati da una risposta impulsiva $h(n)$ di durata teoricamente infinita.

A differenza dei filtri [[8. Filtri FIR - Finite Impulse Response|FIR]], la cui uscita dipende esclusivamente da un numero finito $N$ di campioni passati dell'ingresso:

$$
\begin{aligned}
\text{FIR: } \quad &h(n) = 0 \quad \text{per } n < 0 \text{ e per } n \ge N \\
&y(n) = \sum_{k=0}^{N-1} h(k) x(n-k)
\end{aligned}
$$

la risposta impulsiva di un filtro IIR è causale ma ha durata (supporto) teoricamente infinita:

$$
\begin{aligned}
\text{IIR: } \quad &h(n) = 0 \quad \text{per } n < 0, \quad \text{con supporto infinito per } n \ge 0 \\
&y(n) = \sum_{k=0}^{\infty} h(k) x(n-k)
\end{aligned}
$$

Nonostante la sommatoria sia infinita, i filtri IIR possono essere realizzati in modo esatto ed estremamente efficiente se ricondotti a una __equazione alle differenze ricorsiva__.

> [!EXAMPLE] L'Accumulatore Ideale
> L'accumulatore somma ricorsivamente tutti i campioni del segnale di ingresso:
>
> $$
> y(n) = \sum_{k=0}^{\infty} 1 \cdot x(n-k)
> $$
>
> Esplicitando i primi passi temporali:
>
> $$
> \begin{align*}
> x(0) &\to y(0) = x(0) \\
> x(1) &\to y(1) = x(1) + y(0) = x(1) + x(0) \\
> x(2) &\to y(2) = x(2) + y(1) = x(2) + x(1) + x(0) \\
> &\;\;\vdots \\
> x(n) &\to y(n) = x(n) + y(n-1)
> \end{align*}
> $$
>
> L'introduzione del termine di retroazione (__feedback__) $y(n-1)$ consente di calcolare una risposta infinita impiegando una singola operazione di memoria.

## Introduzione Alla Trasformata Z

La __Trasformata Z__ rappresenta l'equivalente a tempo discreto della trasformata di Laplace del dominio continuo. Essa consente di convertire le operazioni di convoluzione ed equazioni alle differenze in un'algebra polinomiale complessa.

Per una sequenza generica $x(n)$, la trasformata Z bilatera è definita da:

$$
X(z) = \sum_{n = -\infty}^{\infty} x(n) z^{-n} = \underbrace{\sum_{n=-\infty}^{-1} x(n) z^{-n}}_{\text{parte anticausale}} + \underbrace{\sum_{n=0}^{\infty} x(n) z^{-n}}_{\text{parte causale}}
$$

dove $z$ è una variabile complessa ($z \in \mathbb{C}$). Se la sequenza è puramente causale, la sommatoria contiene solo potenze negative di $z$; se è anticausale contiene solo potenze positive; se è mista (a due lati) include entrambe.

Applicando la trasformata Z alla risposta impulsiva $h(n)$ del sistema si ottiene la __funzione di trasferimento__ $H(z)$:

$$
H(z) = \sum_{n = -\infty}^{\infty} h(n) z^{-n}
$$

Se valutata sulla circonferenza di raggio unitario nel piano complesso ($z = \mathrm{e}^{j\omega}$), la trasformata Z coincide con la [[4. Spettro in frequenza - DTFT|DTFT]], fornendo la risposta in frequenza del filtro $H(\omega)$.

> [!NOTE] Funzione di Trasferimento nei Filtri FIR
> In un filtro FIR di lunghezza $N$, la funzione di trasferimento è un semplice polinomio in $z^{-1}$ di grado $N-1$, privo di poli non nulli (tutti i poli sono nell'origine $z = 0$, rendendolo un filtro di soli zeri).

### Proprietà Della Trasformata Z

Le tre proprietà fondamentali impiegate per l'analisi e la sintesi dei sistemi LTI sono:

- __Linearità__: la trasformata di una combinazione lineare di segnali è pari alla combinazione lineare delle rispettive trasformate:

  $$a_1 x_1(n) + a_2 x_2(n) \xrightarrow{\mathcal{Z}} a_1 X_1(z) + a_2 X_2(z)$$

- __Ritardo temporale__: ritardare una sequenza di $D$ campioni corrisponde a moltiplicare la sua trasformata per il fattore $z^{-D}$:

  $$x(n - D) \xrightarrow{\mathcal{Z}} z^{-D} X(z)$$

  Nel calcolo circuitale e negli algoritmi DSP, l'operatore $z^{-1}$ rappresenta fisicamente l'__elemento di memoria unitario__ (un registro di ritardo di un campione);
- __Convoluzione__: la convoluzione temporale tra ingresso e risposta impulsiva si trasforma in un semplice __prodotto algebrico polinomiale__ nel dominio Z:

  $$y(n) = x(n) \ast h(n) \iff Y(z) = H(z) \cdot X(z)$$

  Questa proprietà evita il calcolo oneroso della sommatoria di convoluzione nel tempo, consentendo di analizzare l'effetto del filtro tramite una moltiplicazione polinomiale.

#### Dalla Risposta Temporale Alla Forma Polinomiale

Grazie a queste proprietà, qualsiasi filtro FIR (noto tramite il vettore dei suoi coefficienti campionati) può essere convertito all'istante nella sua funzione di trasferimento polinomiale.

Consideriamo ad esempio due filtri:

$$
h_a = [2, 3, 5, 2], \quad h_b = [1, 0, 0, 0, -1]
$$

Ogni sequenza discreta può essere vista come una somma pesata di impulsi unitari ritardati:

$$
h_a(n) = 2\delta(n) + 3\delta(n-1) + 5\delta(n-2) + 2\delta(n-3)
$$

$$
h_b(n) = \delta(n) - \delta(n-4)
$$

Poiché la trasformata dell'impulso unitario vale:

$$
\delta(n) \xrightarrow{\mathcal{Z}} \sum_{n = -\infty}^{\infty} \delta(n) z^{-n} = \delta(0) z^{-0} = 1
$$

e per la proprietà del ritardo ogni impulso ritardato corrisponde a:

$$
\delta(n-k) \xrightarrow{\mathcal{Z}} z^{-k}
$$

i valori campionati del filtro diventano direttamente i __coefficienti del polinomio__ ordinati per potenze crescenti del ritardo $z^{-1}$:

$$
H_a(z) = 2 + 3z^{-1} + 5z^{-2} + 2z^{-3}, \quad H_b(z) = 1 - z^{-4}
$$

### Esempio Del Gradino Unitario

Il gradino unitario discreto $u(n)$ rappresenta l'attivazione permanente di un segnale costante a partire dall'origine dei tempi:

![[immagini/Gradino unitario.svg|center small]]

$$
u(n) = \begin{cases}
1, & n \ge 0 \\
0, & n < 0
\end{cases}
$$

Per calcolarne la trasformata Z in modo immediato, anziché risolvere una sommatoria infinita, si sfrutta una semplice relazione alle differenze: sottraendo al gradino la sua versione ritardata di un campione, tutti i campioni per $n \ge 1$ si annullano, isolando il solo impulso nell'origine $n = 0$:

![[immagini/Gradino unitario 1.svg|center small]]

$$
u(n) - u(n-1) = \delta(n)
$$

Applicando la trasformata Z a entrambi i membri sfruttando linearità e ritardo:

$$
X(z) - z^{-1} X(z) = 1
$$

Raccogliendo $X(z)$ a fattor comune si ottiene un'equazione algebrica elementare:

$$
X(z)(1 - z^{-1}) = 1 \implies X(z) = \frac{1}{1 - z^{-1}}
$$

> [!NOTE] Ambiguità Temporale dell'Espressione Algebrica
> La medesima espressione chiusa $\frac{1}{1 - z^{-1}}$ si otterrebbe anche trasformando la sequenza anticausale cambiata di segno $-u(-n-1)$. Questa ambiguità mostra concretamente perché l'espressione algebrica da sola non è sufficiente e rende indispensabile specificare la __Regione di Convergenza (ROC)__.

### Regione Di Convergenza (ROC) E Causalità

La Trasformata Z di un segnale a durata infinita è una serie di potenze:

$$
X(z) = \sum_{n=-\infty}^{\infty} x(n) z^{-n}
$$

A seconda del valore numerico assegnato alla variabile complessa $z$, questa sommatoria infinita può convergere a un valore finito oppure divergere a infinito.

La __Regione di Convergenza (ROC)__ è l'insieme dei punti del piano complesso $z$ per i quali la serie converge:

$$
\text{ROC} = \left\{ z \in \mathbb{C} \;\middle|\; \sum_{n=-\infty}^{\infty} |x(n)| |z|^{-n} < \infty \right\}
$$

> [!IMPORTANT] Perché la ROC è Indispensabile?
> La sola formula algebrica di $X(z)$ __non basta__ a identificare il segnale nel tempo. Due segnali temporali completamente differenti (ad esempio uno causale che evolve verso il futuro e uno anticausale che evolve verso il passato) possono dare origine esattamente alla __stessa formula algebrica__ per $X(z)$.
> La ROC è l'informazione complementare che scioglie questa ambiguità e rende la trasformata univocamente invertibile.

#### Proprietà Geometriche Della ROC

1. __Forma regolare__: la ROC è sempre formata da regioni con simmetria circolare (dischi interni, corone circolari anulari o regioni esterne a un cerchio), tutte centrate nell'origine $z = 0$;
2. __Assenza di poli__: la ROC __non contiene mai alcun polo__. Nei poli il denominatore di $X(z)$ si azzera e la funzione diverge a infinito ($X(z) \to \infty$); per definizione, la ROC comprende solo i punti in cui la serie assume un valore finito. I poli fungono quindi da barriere geometriche naturali che delimitano le frontiere della ROC.

> [!EXAMPLE] Esponenziale Causale Monolatero
> Data la sequenza causale $x(n) = p^n u(n) = (0.5)^n u(n)$ per $n \ge 0$:
>
> $$
> \begin{align}
> X(z) &= \sum_{n = -\infty}^{\infty} (0.5)^n u(n) z^{-n} = \sum_{n = 0}^{\infty} (0.5)^n z^{-n} = \sum_{n=0}^{\infty} (0.5 z^{-1})^n \\
> &= \frac{1}{1 - 0.5 z^{-1}} = \frac{z}{z - 0.5}
> \end{align}
> $$
>
> La serie geometrica converge se e solo se la ragione ha modulo minore di uno:
>
> $$
> |0.5 z^{-1}| < 1 \implies |z| > 0.5
> $$
>
> Il polo si trova in $z = 0.5$. La ROC è la regione esterna alla circonferenza che passa per il polo:
>
> $$
> \text{ROC} = \{z \in \mathbb{C} : |z| > 0.5\}
> $$

Generalizzando per un polo $p$ generico:

$$
p^n u(n) \xrightarrow{\mathcal{Z}} \frac{1}{1 - pz^{-1}}, \quad \text{con polo in } z = p \text{ e } \text{ROC: } |z| > |p|
$$

#### Confronto Tra Segnale Causale E Anticausale (Polo Singolo)

Se consideriamo invece il segnale anticausale $x(n) = -p^n u(-n-1)$, attivo solo per tempi passati ($n \le -1$), gli esponenti negativi $z^{-n}$ diventano potenze positive di $z$. La serie geometrica converge allora all'interno del cerchio:

$$
-p^n u(-n-1) \xrightarrow{\mathcal{Z}} \frac{1}{1 - pz^{-1}}, \quad \text{con polo in } z = p \text{ e } \text{ROC: } |z| < |p|
$$

L'espressione algebrica è identica a quella del caso causale, ma le regioni del piano in cui la serie converge sono separate e disgiunte:

![[immagini/roc_causale.svg|center small]] ![[immagini/roc_anticausale.svg|center small]]

- __Segnale Causale ($|z| > |p|$)__: la ROC si estende all'__esterno__ del cerchio del polo. Se il polo è interno al cerchio unitario ($|p| < 1$), la ROC racchiude la circonferenza unitaria $|z| = 1 \implies$ il sistema è __causale e stabile__;
- __Segnale Anticausale ($|z| < |p|$)__: la ROC è il __disco interno__ al polo. Se $|p| < 1$, la ROC esclude il cerchio unitario $\implies$ il sistema è __anticausale e instabile__.

#### Sistemi a Più Poli: Le Tre Topologie Della ROC

Quando un filtro presenta più poli (ad esempio due poli con $|p_1| < |p_2|$, come $|p_1| = 0.6$ e $|p_2| = 1.35$), le circonferenze concentriche associate a ciascun polo partizionano il piano complesso in tre regioni disgiunte:

![[immagini/roc_multipolo_causale.svg|center small]] ![[immagini/roc_multipolo_anulare.svg|center small]] ![[immagini/roc_multipolo_anticausale.svg|center small]]

1. __ROC Esterna ($|z| > |p_2|$)__:
   - È la regione all'esterno del polo di raggio massimo;
   - Tutti i poli cadono all'interno del bordo della ROC, quindi tutti i termini dell'inversa sono __causali__ ($u(n)$);
   - Se il polo massimo supera il cerchio unitario ($|p_2| > 1$), la ROC esclude $|z|=1 \implies$ __sistema causale ma instabile__;
2. __ROC Anulare / Due Lati ($|p_1| < |z| < |p_2|$)__:
   - È la corona circolare compresa tra i due poli;
   - Il polo interno $p_1$ genera un termine causale destro, mentre il polo esterno $p_2$ genera un termine anticausale sinistro: la risposta nel tempo è una sequenza __bilatera (mista a due lati)__;
   - Se la corona racchiude la circonferenza unitaria ($|p_1| < 1 < |p_2|$), la DTFT converge $\implies$ __sistema a due lati e stabile__;
3. __ROC Interna ($|z| < |p_1|$)__:
   - È il disco interno al polo di raggio minimo;
   - Tutti i poli cadono all'esterno della ROC, quindi tutti i termini dell'inversa sono __anticausali__ ($u(-n-1)$);
   - Poiché $|p_1| < 1$, il disco esclude il cerchio unitario $\implies$ __sistema anticausale e instabile__.

> [!IMPORTANT] Teorema di Stabilità BIBO e Regola di Progetto
> Un sistema LTI discreto è stabile in senso BIBO (Bounded-Input Bounded-Output) se e solo se la sua risposta impulsiva è assolutamente sommabile ($\sum |h(n)| < \infty$).
> Nel dominio Z, ciò equivale a richiedere che la __ROC includa interamente il cerchio unitario $|z| = 1$__ (condizione che garantisce la convergenza della DTFT).
>
> Unendo i due requisiti per un filtro fisico realizzabile ed elaborabile in tempo reale:
> 1. La __causalità__ impone che la ROC sia esterna al polo di raggio massimo: $|z| > \max |p_i|$;
> 2. La __stabilità__ impone che la ROC contenga il cerchio unitario $|z| = 1$, il che richiede $1 > \max |p_i|$.
> 
> Pertanto, un filtro IIR causale è stabile se e solo se __tutti i suoi poli cadono rigorosamente all'interno del cerchio unitario__ ($|p_i| < 1$).

### Relazione Tra Trasformata Z E DTFT

Valutando la trasformata Z lungo il cerchio unitario ($z = \mathrm{e}^{j\omega}$ con $\omega \in [-\pi, \pi]$):

$$
\left. X(z) \right|_{z = \mathrm{e}^{j\omega}} = \sum_{n = -\infty}^{\infty} x(n) \mathrm{e}^{-j\omega n} = X(\omega)
$$

La DTFT esiste ed è continua se e solo se il cerchio unitario $|z| = 1$ appartiene alla ROC.

#### Segnali Marginalmente Stabili

I segnali marginalmente stabili presentano poli collocati esattamente sulla circonferenza unitaria ($|p| = 1$), come nel caso delle oscillazioni sinusoidali permanenti. Per tali segnali la valutazione diretta diverge in corrispondenza della pulsazione del polo:

> [!EXAMPLE] Sinusoide Complessa Causale
> Consideriamo il segnale causale $x(n) = \mathrm{e}^{j\omega_0 n} u(n)$:
>
> $$
> X(z) = \frac{1}{1 - \mathrm{e}^{j\omega_0} z^{-1}}, \quad \text{ROC: } |z| > 1
> $$
>
> Poiché il polo $z = \mathrm{e}^{j\omega_0}$ giace sul cerchio unitario ($|z|=1$), la circonferenza unitaria costituisce la frontiera di convergenza della ROC. Nel senso delle distribuzioni (calcolando il limite per $r \to 1^+$ di $X(r \mathrm{e}^{j\omega})$), la DTFT del segnale causale include sia la parte razionale che una componente impulsiva:
>
> $$
> X(\omega) = \frac{1}{1 - \mathrm{e}^{-j(\omega - \omega_0)}} + \pi \sum_{k=-\infty}^{\infty} \delta(\omega - \omega_0 - 2\pi k)
> $$
>
> Il termine razionale si annulla a denominatore per $\omega = \omega_0$ facendolo divergere, mentre l'impulso di Dirac $\pi \delta(\omega - \omega_0)$ concentra la componente spettrale permanente (a differenza della sinusoide bilatera che ha peso $2\pi$).

## Pattern Poli-Zeri E Risposta in Frequenza

La funzione di trasferimento di un filtro a poli e zeri è espressa come rapporto tra due polinomi in $z^{-1}$:

$$
H(z) = \frac{N(z)}{D(z)} = \frac{b_0}{a_0} \frac{\prod_{i=1}^{M} (1 - z_i z^{-1})}{\prod_{j=1}^{N} (1 - p_j z^{-1})}
$$

La forma geometrica della risposta in frequenza $H(\omega)$ è determinata dalla disposizione dei poli $p_j$ e degli zeri $z_i$ sul piano complesso Z.

Per un sistema elementare del primo ordine con un singolo zero in $z = z_1$ e un singolo polo in $z = p_1$:

$$
H(z) = \frac{1 - z_1 z^{-1}}{1 - p_1 z^{-1}} = \frac{z - z_1}{z - p_1}
$$

Valutando sul cerchio unitario $z = \mathrm{e}^{j\omega}$:

$$
H(\omega) = \frac{\mathrm{e}^{j\omega} - z_1}{\mathrm{e}^{j\omega} - p_1} \implies |H(\omega)| = \frac{|\mathrm{e}^{j\omega} - z_1|}{|\mathrm{e}^{j\omega} - p_1|}
$$

![[immagini/poli_zeri.svg|center big]]

L'ampiezza $|H(\omega)|$ corrisponde al rapporto tra le distanze euclidee del punto corrente sul cerchio unitario $\mathrm{e}^{j\omega}$ dallo zero $z_1$ (a numeratore) e dal polo $p_1$ (a denominatore):
- Più il punto $\mathrm{e}^{j\omega}$ si avvicina a un polo interno al cerchio, più il denominatore si rimpicciolisce e la risposta $|H(\omega)|$ cresce generando un picco (risonanza);
- Più il punto $\mathrm{e}^{j\omega}$ si avvicina a uno zero posto sul cerchio unitario, più il numeratore tende a zero, creando una valle o un azzeramento perfetto (filtri notch).

Per guidare il posizionamento geometrico di poli e zeri è utile suddividere il cerchio unitario in settori angolari associati alle basse frequenze ($\omega \approx 0$), medie frequenze e alte frequenze ($\omega \approx \pi$):

![[immagini/cerchio_unitario.png|center mid]]

Ad esempio, per progettare un filtro passa-basso occorrerà posizionare i poli in prossimità del cerchio unitario nella zona a basse frequenze ($\omega \approx 0$) e gli zeri nella zona ad alte frequenze ($\omega \approx \pi$).

## Sviluppo in Fratti Parziali E Inversione Della Trasformata Z

L'inversione della trasformata Z consiste nel determinare la sequenza temporale $h(n)$ a partire dalla funzione razionale $H(z)$:

$$
H(z) = \frac{b_0 + b_1 z^{-1} + \dots + b_M z^{-M}}{a_0 + a_1 z^{-1} + \dots + a_N z^{-N}} = \frac{b_0}{a_0} \frac{\prod_{i=1}^{M} (1 - z_i z^{-1})}{\prod_{j=1}^{N} (1 - p_j z^{-1})}
$$

Il metodo più conveniente consiste nello scomporre $H(z)$ nella somma di fratti parziali del primo ordine associati ai singoli poli:

$$
H(z) = \frac{A_1}{1 - p_1 z^{-1}} + \frac{A_2}{1 - p_2 z^{-1}} + \dots + \frac{A_N}{1 - p_N z^{-1}}
$$

Una volta calcolati i residui $A_i$, ciascun termine elementare viene invertito temporalmente:

$$
\frac{A_i}{1 - p_i z^{-1}} \xrightarrow{\mathcal{Z}^{-1}} A_i p_i^n u(n) \quad (\text{per ROC causale } |z| > |p_i|)
$$

### Caso 1: Grado Del Numeratore Minore Del Denominatore ($M < N$)

Se il grado del numeratore è strettamente inferiore a quello del denominatore, l'espansione assume la forma diretta sopra indicata. Ciascun residuo $A_i$ viene calcolato isolando il fattore a denominatore e valutando la funzione nel polo corrispondente $z = p_i$:

$$
A_i = \left[ (1 - p_i z^{-1}) H(z) \right]_{z = p_i} = \left[ \frac{N(z)}{\prod_{j \neq i} (1 - p_j z^{-1})} \right]_{z = p_i}, \quad i = 1, \dots, N
$$

### Caso 2: Grado Del Numeratore Uguale Al Denominatore ($M = N$)

Se il grado del numeratore coincide con quello del denominatore, l'espansione in fratti parziali deve includere una costante additiva $A_0$:

$$
H(z) = A_0 + \sum_{i=1}^{N} \frac{A_i}{1 - p_i z^{-1}}
$$

Il termine costante $A_0$ corrisponde al valore asintotico per $z \to 0$ (o $z^{-1} \to \infty$):

$$
A_0 = \lim_{z \to 0} H(z) = \lim_{z^{-1} \to \infty} H(z) = \frac{b_M}{a_N}
$$

mentre i residui $A_i$ si calcolano con la medesima formula del Caso 1. Nel tempo, $A_0$ genera un impulso isolato $A_0 \delta(n)$.

### Caso 3: Grado Del Numeratore Maggiore Del Denominatore ($M > N$)

Se il grado del numeratore supera quello del denominatore ($M > N$), si esegue preliminarmente la divisione polinomiale tra $N(z^{-1})$ e $D(z^{-1})$ ordinati secondo le potenze decrescenti di $z^{-1}$, ricavando un polinomio quoziente $Q(z^{-1})$ di grado $M - N$ e un resto $R(z^{-1})$ di grado inferiore a $N$:

$$
N(z^{-1}) = Q(z^{-1}) D(z^{-1}) + R(z^{-1}) \implies H(z) = Q(z^{-1}) + \frac{R(z^{-1})}{D(z^{-1})}
$$

Il termine razionale residuo $\frac{R(z^{-1})}{D(z^{-1})}$ ha grado a numeratore strettamente inferiore al denominatore e può essere regolarmente scomposto in fratti parziali. Il quoziente polinomiale $Q(z^{-1}) = \sum_{k=0}^{M-N} q_k z^{-k}$ genera nel tempo una sequenza causale a supporto finito (FIR) formata da impulsi isolati $\sum_{k=0}^{M-N} q_k \delta(n-k)$.

### Poli Complessi Coniugati

Dato che i coefficienti del filtro sono a valori reali, i poli complessi compaiono sempre in coppie coniugate $p_1 = R_1 \mathrm{e}^{j\omega_1}$ e $p_1^* = R_1 \mathrm{e}^{-j\omega_1}$, con residui a loro volta coniugati $A_1 = B_1 \mathrm{e}^{j\alpha_1}$ e $A_1^* = B_1 \mathrm{e}^{-j\alpha_1}$:

$$
H(z) = \frac{A_1}{1 - p_1 z^{-1}} + \frac{A_1^*}{1 - p_1^* z^{-1}} + \dots
$$

Invertendo la coppia causale nel tempo:

$$
h_1(n) = A_1 p_1^n u(n) + A_1^* p_1^{*n} u(n) = 2 \operatorname{Re}[A_1 p_1^n] u(n)
$$

Esplicitando in forma polare:

$$
\operatorname{Re}[A_1 p_1^n] = \operatorname{Re}\left[ B_1 \mathrm{e}^{j\alpha_1} R_1^n \mathrm{e}^{j\omega_1 n} \right] = B_1 R_1^n \cos(\omega_1 n + \alpha_1)
$$

La risposta impulsiva reale associata alla coppia coniugata è quindi una sinusoide smorzata:

$$
h(n) = 2 B_1 R_1^n \cos(\omega_1 n + \alpha_1) u(n)
$$

Il fattore di decadimento esponenziale $R_1^n$ assicura la stabilità se il raggio del polo è strettamente minore di uno ($R_1 < 1$).

## Modalità Equivalenti per Descrivere I Filtri Digitali

Un sistema LTI a tempo discreto può essere descritto attraverso diverse rappresentazioni matematiche e operative tra loro perfettamente equivalenti:

![[immagini/descrizioni_filtri.png|center mid]]

La catena di progettazione collega direttamente:
1. Le specifiche di risposta in frequenza desiderata;
2. La funzione di trasferimento $H(z)$ sul piano complesso Z;
3. Il pattern geometrico di poli e zeri;
4. L'equazione alle differenze nel dominio temporale;
5. La struttura circuitale a blocchi (registri di ritardo $z^{-1}$, moltiplicatori e sommatori);
6. L'algoritmo di elaborazione del segnale per campioni.

> [!EXAMPLE] Conversione Completa tra Descrizioni
> Consideriamo il filtro del primo ordine definito dalla funzione di trasferimento:
>
> $$
> H(z) = \frac{5 + 2z^{-1}}{1 - 0.8z^{-1}}
> $$
>
> Poiché numeratore e denominatore hanno grado uguale ($M = N = 1$), applichiamo lo sviluppo in fratti parziali del Caso 2:
>
> $$
> H(z) = A_0 + \frac{A_1}{1 - 0.8z^{-1}}
> $$
>
> I coefficienti valgono:
>
> $$
> A_0 = \left. H(z) \right|_{z = 0} = \left. \frac{5z + 2}{z - 0.8} \right|_{z = 0} = \frac{2}{-0.8} = -2.5
> $$
>
> $$
> A_1 = \left[ (1 - 0.8z^{-1}) H(z) \right]_{z = 0.8} = \left. (5 + 2z^{-1}) \right|_{z = 0.8} = 5 + \frac{2}{0.8} = 7.5
> $$
>
> L'espressione decomposta è:
>
> $$
> H(z) = -2.5 + \frac{7.5}{1 - 0.8z^{-1}}
> $$
>
> Assumendo la causalità, la risposta impulsiva analitica è:
>
> $$
> h(n) = -2.5\delta(n) + 7.5(0.8)^n u(n)
> $$
>
> Per determinare l'equazione alle differenze ingresso-uscita, esplicitiamo la relazione tra le trasformate $Y(z) = H(z) X(z)$:
>
> $$
> (1 - 0.8z^{-1}) Y(z) = (5 + 2z^{-1}) X(z)
> $$
>
> Sviluppando i prodotti:
>
> $$
> Y(z) - 0.8z^{-1} Y(z) = 5X(z) + 2z^{-1} X(z)
> $$
>
> Applicando l'inversa della trasformata Z termine a termine, si ottiene l'__equazione alle differenze__:
>
> $$
> y(n) - 0.8y(n-1) = 5x(n) + 2x(n-1)
> $$
>
> Esplicitando il campione corrente in uscita $y(n)$:
>
> $$
> y(n) = 0.8y(n-1) + \underbrace{5x(n) + 2x(n-1)}_{\text{contributo feedforward (FIR)}}
> $$

In generale, ponendo convenzionalmente $a_0 = 1$, l'uscita di un filtro IIR è composta dalla combinazione pesata degli ingressi presenti e passati (parte FIR / feedforward) e dalla retroazione delle uscite precedentemente calcolate (parte IIR / feedback):

$$
y(n) = - \underbrace{\sum_{i=1}^{N} a_i y(n-i)}_{\text{retroazione IIR}} + \underbrace{\sum_{j=0}^{M} b_j x(n-j)}_{\text{filtro FIR}}
$$



# A. Filtri IIR - Risposta E Progettazione

Questo capitolo analizza la risposta dinamica dei filtri IIR nel dominio del tempo e della frequenza, approfondendo le metodologie di progettazione basate sul posizionamento geometrico di poli e zeri sul piano complesso Z per filtri del primo ordine (smoother), risuonatori del secondo ordine, equalizzatori parametrici, filtri notch e filtri a pettine.

## Risposta Sinusoidale a Regime

Data una sinusoide complessa persistente a frequenza angolare $\omega_0$:

$$
x(n) = \mathrm{e}^{j\omega_0 n}, \quad -\infty < n < +\infty
$$

applicando la convoluzione lineare con la risposta impulsiva $h(n)$ di un filtro IIR stabile:

$$
\begin{align}
y(n) &= \sum_{m=-\infty}^{\infty} h(m) x(n-m) = \sum_{m=-\infty}^{\infty} h(m) \mathrm{e}^{j\omega_0 (n-m)} \\
&= \mathrm{e}^{j\omega_0 n} \underbrace{\sum_{m=-\infty}^{\infty} h(m) \mathrm{e}^{-j\omega_0 m}}_{\text{DTFT } H(\omega_0)} = H(\omega_0) \mathrm{e}^{j\omega_0 n}
\end{align}
$$

L'uscita a regime permanente ha la medesima frequenza dell'ingresso, con ampiezza riscaldata dal modulo $|H(\omega_0)|$ e fase traslata di $\arg H(\omega_0)$:

$$
y(n) = |H(\omega_0)| \mathrm{e}^{j\left(\omega_0 n + \arg H(\omega_0)\right)}
$$

### Ritardo Di Fase E Ritardo Di Gruppo

Lo sfasamento introdotto dal filtro si traduce in un ritardo temporale:
- Il __ritardo di fase__ $d(\omega)$ misura il ritardo temporale subito dalla portante sinusoidale a frequenza $\omega$:

  $$d(\omega) = -\frac{\arg H(\omega)}{\omega} \iff \arg H(\omega) = -\omega d(\omega)$$

- Il __ritardo di gruppo__ $d_g(\omega)$ misura il ritardo temporale subito dall'inviluppo di modulazione di un pacchetto d'onda a banda stretta:

  $$d_g(\omega) = -\frac{\mathrm{d}}{\mathrm{d}\omega} \arg H(\omega)$$

Nei filtri FIR simmetrici di lunghezza $N$ campioni (ordine del filtro pari a $N-1$), limitatamente alle frequenze in cui la risposta in ampiezza è positiva, il ritardo è rigorosamente indipendente dalla frequenza ($d(\omega) = d_g(\omega) = D = \frac{N-1}{2}$), garantendo perfetta linearità della fase:

$$
\mathrm{e}^{j\omega n} \xrightarrow{\mathcal{H}} |H(\omega)| \mathrm{e}^{j\omega (n - D)}
$$

Nel caso dei filtri IIR, non è matematicamente possibile ottenere una fase perfettamente lineare sull'intero intervallo di Nyquist $[-\pi, \pi]$. È tuttavia possibile progettare filtri IIR che approssimino una fase lineare limitatamente alla banda passante (come i filtri a ritardo massimamente piatto di Bessel).

## Risposta Al Transitorio E Stabilità

Nel mondo reale ogni segnale viene applicato a partire da un istante iniziale ($n = 0$). L'ingresso sinusoidale è quindi causale:

$$
x(n) = \mathrm{e}^{j\omega_0 n} u(n) \xrightarrow{\mathcal{Z}} X(z) = \frac{1}{1 - \mathrm{e}^{j\omega_0} z^{-1}}, \quad \text{ROC: } |z| > 1
$$

Dato un filtro IIR causale e stabile con $M$ poli strettamente interni al cerchio unitario ($|p_i| < 1$):

$$
H(z) = \frac{N(z)}{(1 - p_1 z^{-1})(1 - p_2 z^{-1}) \dots (1 - p_M z^{-1})}
$$

La trasformata Z dell'uscita è:

$$
Y(z) = H(z) X(z) = \frac{N(z)}{\left(1 - \mathrm{e}^{j\omega_0} z^{-1}\right) \prod_{i=1}^{M} (1 - p_i z^{-1})}
$$

Scomponendo in fratti parziali:

$$
Y(z) = \frac{C}{1 - \mathrm{e}^{j\omega_0} z^{-1}} + \sum_{i=1}^{M} \frac{B_i}{1 - p_i z^{-1}}
$$

Il residuo $C$ associato al polo del segnale vale:

$$
C = \left[ (1 - \mathrm{e}^{j\omega_0} z^{-1}) Y(z) \right]_{z = \mathrm{e}^{j\omega_0}} = H(\mathrm{e}^{j\omega_0}) = H(\omega_0)
$$

Antitrasformando causalmente per $n \ge 0$:

$$
y(n) = \underbrace{H(\omega_0) \mathrm{e}^{j\omega_0 n}}_{\text{risposta a regime permanente}} + \underbrace{\sum_{i=1}^{M} B_i p_i^n}_{\text{risposta transitoria}}
$$

Poiché tutti i poli del filtro soddisfano $|p_i| < 1$, i termini $p_i^n$ decadono esponenzialmente a zero per $n \to \infty$:

$$
y(n) \to H(\omega_0) \mathrm{e}^{j\omega_0 n} \quad \text{per } n \to \infty
$$

Se anche un solo polo cadesse all'esterno del cerchio unitario ($|p_k| > 1$), il termine corrispondente $p_k^n$ divergerebbe esponenzialmente, rendendo il sistema incontrollabile e instabile.

### Costante Temporale Effettiva

La durata temporale del transitorio è determinata dal polo che decade più lentamente, ossia quello avente modulo massimo (__polo dominante__):

$$
\rho = \max_{i} |p_i|
$$

Fissata una soglia percentuale di tolleranza $\varepsilon$ (tipicamente l'1%, $\varepsilon = 0.01$), la __durata effettiva del transitorio__ $n_{\text{eff}}$ (numero di campioni necessari affinché il transitorio scenda al di sotto di $\varepsilon$) si ricava da:

$$
\rho^{n_{\text{eff}}} = \varepsilon \implies n_{\text{eff}} = \frac{\ln \varepsilon}{\ln \rho} = \frac{\ln(1/\varepsilon)}{\ln(1/\rho)}
$$

Più il polo dominante si avvicina alla circonferenza unitaria ($\rho \to 1$), più la costante temporale cresce e più lungo sarà il tempo di assestamento del filtro.

## Filtri Di Primo Ordine (Smoother)

I filtri di primo ordine (smoother) costituiscono i blocchi passa-basso o passa-alto elementari con un singolo polo e un singolo zero a valori reali:

$$
H(z) = \frac{G(1 + b z^{-1})}{1 - a z^{-1}}
$$

dove $a$ è la coordinata del polo sul semiasse reale positivo ($z = a$, con $0 < a < 1$ per stabilità causale) e lo zero del filtro è collocato in $z = -b$ (con $0 < b \le 1$ per posizionarlo sul semiasse reale negativo vicino a $\omega = \pi$).

Valutando la risposta in frequenza alle pulsazioni estreme dell'intervallo di Nyquist ($z = \mathrm{e}^{j0} = 1$ e $z = \mathrm{e}^{j\pi} = -1$):

$$
H(0) = \frac{G(1 + b)}{1 - a}
$$

$$
H(\pi) = \frac{G(1 - b)}{1 + a}
$$

Il rapporto di attenuazione tra la massima frequenza ($\pi$) e la frequenza continua ($0$) vale:

$$
\frac{H(\pi)}{H(0)} = \frac{(1 - b)(1 - a)}{(1 + b)(1 + a)}
$$

> [!EXAMPLE] Progetto di uno Smoother Passa-Basso
> Assegnate le specifiche:
> 1. Durata del transitorio: $n_{\text{eff}} = 20$ campioni con soglia $\varepsilon = 0.01$;
> 2. Rapporto di attenuazione: $\frac{H(\pi)}{H(0)} = \frac{1}{21}$.
> 
> Calcolo del polo $a$:
>
> $$
> a = \varepsilon^{1/n_{\text{eff}}} = (0.01)^{1/20} \approx 0.8
> $$
>
> Calcolo del parametro $b$ (zero in $z = -b = -0.4$):
>
> $$
> \frac{(1 - b)(1 - 0.8)}{(1 + b)(1 + 0.8)} = \frac{1}{21} \implies \frac{0.2(1 - b)}{1.8(1 + b)} = \frac{1}{21} \implies b = 0.4
> $$
>
> Calcolo del guadagno di normalizzazione a frequenza continua ($H(0) = 1$):
>
> $$
> H(0) = \frac{G(1 + 0.4)}{1 - 0.8} = \frac{1.4}{0.2} G = 7 G = 1 \implies G = \frac{1}{7} \approx 0.1429
> $$
>
> La funzione di trasferimento risultante è:
>
> $$
> H(z) = \frac{\frac{1}{7}(1 + 0.4z^{-1})}{1 - 0.8z^{-1}} \approx \frac{0.1429(1 + 0.4z^{-1})}{1 - 0.8z^{-1}}
> $$
>
> Esplicitando la relazione tra le trasformate $Y(z) = H(z) X(z)$:
>
> $$
> (1 - 0.8z^{-1}) Y(z) = 0.1429(1 + 0.4z^{-1}) X(z)
> $$
>
> Antitrasformando nel dominio temporale si ottiene l'equazione alle differenze:
>
> $$
> y(n) = 0.8y(n-1) + 0.1429\left(x(n) + 0.4x(n-1)\right)
> $$
>
> Questa struttura richiede solo 3 moltiplicazioni e accumuli (__MACS__) per ciascun campione elaborato.

## Filtri Di Secondo Ordine (Resonator)

I filtri __resonator__ di secondo ordine presentano una risposta in frequenza dominata da un picco risonante a una specifica frequenza nominale $\omega_0$:

![[immagini/resonator 1.png|center mid]]

Per posizionare la risonanza a $\omega = \omega_0$, si colloca una coppia di poli complessi coniugati sul piano Z a raggio $R$ ($0 < R < 1$):

$$
p = R \mathrm{e}^{j\omega_0}, \quad p^* = R \mathrm{e}^{-j\omega_0}
$$

La funzione di trasferimento è:

$$
H(z) = \frac{G}{(1 - R \mathrm{e}^{j\omega_0} z^{-1})(1 - R \mathrm{e}^{-j\omega_0} z^{-1})} = \frac{G}{1 + a_1 z^{-1} + a_2 z^{-2}}
$$

I coefficienti del denominatore si ricavano direttamente dalle relazioni trigonometriche:

$$
a_1 = -2R \cos\omega_0, \quad a_2 = R^2
$$

### Calcolo Del Guadagno Di Normalizzazione $G$

Per normalizzare il picco di risonanza al guadagno unitario ($|H(\omega_0)| = 1$, corrispondente a $0\text{ dB}$):

$$
|H(\omega_0)| = \frac{G}{|(1 - R)(1 - R \mathrm{e}^{-2j\omega_0})|} = 1
$$

da cui si ricava la formula analitica per il guadagno $G$:

$$
G = (1 - R) \sqrt{1 - 2R \cos(2\omega_0) + R^2}
$$

### Risposta in Modulo E Larghezza Di Banda a 3 dB

Il modulo quadro della risposta in frequenza è espresso da:

$$
|H(\omega)|^2 = \frac{G^2}{\left(1 - 2R \cos(\omega - \omega_0) + R^2\right) \left(1 - 2R \cos(\omega + \omega_0) + R^2\right)}
$$

La __larghezza di banda a metà potenza__ (frequenze a $-3\text{ dB}$, $\Delta\omega = \omega_2 - \omega_1$) è definita dalla condizione:

$$
|H(\omega)|^2 = \frac{1}{2} |H(\omega_0)|^2 = \frac{1}{2} \iff 20 \log_{10} \left| \frac{H(\omega)}{H(\omega_0)} \right| = -3\text{ dB}
$$

Per poli sufficientemente vicini al cerchio unitario ($R \approx 1$), la larghezza di banda è legata al raggio $R$ dalla relazione approssimata:

$$
\Delta\omega \simeq 2(1 - R)
$$

> [!IMPORTANT] Compromesso Risoluzione - Transitorio nel Resonator
> Più il raggio $R$ si avvicina a $1$:
> - Più la larghezza di banda $\Delta\omega$ si restringe, rendendo il picco risonante selettivo;
> - Più la costante temporale del transitorio $n_{\text{eff}}$ aumenta, rendendo lenta la risposta a variazioni dell'ingresso.

### Risposta Impulsiva Ed Equazione Alle Differenze

La risposta impulsiva causale analitica del risuonatore è:

$$
h(n) = \frac{G}{\sin\omega_0} R^n \sin(\omega_0 n + \omega_0), \quad n \ge 0
$$

L'equazione alle differenze ricorsiva per il calcolo in tempo reale è:

$$
y(n) = -a_1 y(n-1) - a_2 y(n-2) + G x(n)
$$

> [!EXAMPLE] Progetto Numerico di un Risuonatore
> Dati di specifica: frequenza di risonanza $f_0 = 500\text{ Hz}$, larghezza di banda $\Delta f = 32\text{ Hz}$, frequenza di campionamento $f_s = 10\text{ kHz}$.
>
> Calcolo delle frequenze normalizzate:
>
> $$
> \omega_0 = \frac{2\pi f_0}{f_s} = \frac{2\pi \cdot 500}{10000} = 0.1\pi
> $$
>
> $$
> \Delta\omega = \frac{2\pi \Delta f}{f_s} = \frac{2\pi \cdot 32}{10000} = 0.0064\pi \approx 0.02
> $$
>
> Determinazione del raggio $R$:
>
> $$
> 2(1 - R) = 0.02 \implies R = 0.99
> $$
>
> Calcolo dei coefficienti del filtro:
>
> $$
> a_1 = -2(0.99) \cos(0.1\pi) = -1.8831
> $$
>
> $$
> a_2 = (0.99)^2 = 0.9801
> $$
>
> $$
> G = (1 - 0.99) \sqrt{1 - 2(0.99)\cos(0.2\pi) + (0.99)^2} = 0.0062
> $$
>
> Funzione di trasferimento:
>
> $$
> H(z) = \frac{0.0062}{1 - 1.8831z^{-1} + 0.9801z^{-2}}
> $$

## Equalizzatore Parametrico

L'equalizzatore parametrico generalizza la struttura del risuonatore introducendo una coppia di zeri complessi coniugati allineati sulla stessa direzione angolare $\omega_0$ dei poli:

$$
z_1 = r \mathrm{e}^{j\omega_0}, \quad z_1^* = r \mathrm{e}^{-j\omega_0}
$$

dove $r$ ($0 \le r \le 1$) è il raggio degli zeri e $R$ ($0 \le R < 1$) è il raggio dei poli.

La funzione di trasferimento è:

$$
H(z) = \frac{(1 - r \mathrm{e}^{j\omega_0} z^{-1})(1 - r \mathrm{e}^{-j\omega_0} z^{-1})}{(1 - R \mathrm{e}^{j\omega_0} z^{-1})(1 - R \mathrm{e}^{-j\omega_0} z^{-1})} = \frac{1 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}
$$

con coefficienti:

$$
\begin{align}
b_1 &= -2r \cos\omega_0, & b_2 &= r^2 \\
a_1 &= -2R \cos\omega_0, & a_2 &= R^2
\end{align}
$$

Il comportamento in frequenza dipende dal confronto tra i due raggi:
- Se $r < R$: il polo è più vicino al cerchio unitario rispetto allo zero $\implies$ si ottiene un'__enfatizzazione (boost / guadagno in dB)__ attorno a $\omega_0$;
- Se $r > R$: lo zero è più vicino al cerchio unitario rispetto al polo $\implies$ si ottiene un'__attenuazione (cut / valle in dB)__ attorno a $\omega_0$.

![[immagini/eq_param_pole_zero_pattern.png|center mid]]

### Filtro Notch

Nel caso limite in cui gli zeri vengono posizionati esattamente sulla circonferenza unitaria ($r = 1$):

![[immagini/notch.png|center mid]]

la risposta in frequenza si annulla esattamente alla pulsazione $\omega_0$ ($|H(\omega_0)| = 0$). I coefficienti del numeratore diventano:

$$
b_1 = -2\cos\omega_0, \quad b_2 = 1
$$

$$
a_1 = R b_1 = -2R \cos\omega_0, \quad a_2 = R^2
$$

La funzione di trasferimento del filtro notch può essere espressa sinteticamente come:

$$
H(z) = \frac{1 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}} = \frac{N(z)}{N(R^{-1} z)}
$$

dove il numeratore fattorizzato è:

$$
N(z) = 1 - 2\cos\omega_0 z^{-1} + z^{-2} = (1 - \mathrm{e}^{j\omega_0} z^{-1})(1 - \mathrm{e}^{-j\omega_0} z^{-1})
$$

> [!NOTE] Guadagno in Banda Passante
> Per normalizzare esattamente a guadagno unitario a frequenza continua ($H(0) = 1$, $0\text{ dB}$), la funzione di trasferimento può essere moltiplicata per il fattore di scala:
>
> $$
> G_0 = \frac{1 + a_1 + a_2}{1 + b_1 + b_2} = \frac{1 - 2R\cos\omega_0 + R^2}{2(1 - \cos\omega_0)}
> $$

### Filtro a Pettine (Comb)

Il filtro a pettine estende il principio del notch all'annullamento simultaneo di un insieme di frequenze armoniche multiple. Per elaborare segnali reali a coefficienti reali, ogni polo o zero a frequenza $\omega_i$ deve essere accompagnato dal suo complesso coniugato $-\omega_i$.

Nel caso fondamentale in cui le $M$ frequenze siano armonicamente equispaziate sull'intera circonferenza ($\omega_k = \frac{2\pi k}{M}$ per $k = 0, \dots, M-1$), per la proprietà delle radici $M$-esime dell'unità ($\prod_{k=0}^{M-1} (1 - \mathrm{e}^{j \frac{2\pi k}{M}} z^{-1}) = 1 - z^{-M}$), il polinomio al numeratore collassa nella forma sparsa:

$$
N(z) = 1 - z^{-M}
$$

Il denominatore introduce poli collocati sulle stesse direzioni radiali degli zeri, ma ritirati all'interno del cerchio unitario al raggio $\rho$ ($0 < \rho < 1$):

$$
D(z) = N(\rho^{-1} z) = 1 - \rho^M z^{-M}
$$

La funzione di trasferimento del __filtro a pettine canonico__ assume così la forma computazionalmente ottimizzata:

$$
H(z) = \frac{1 - z^{-M}}{1 - \rho^M z^{-M}}
$$

implementabile in tempo reale mediante una singola linea di ritardo di lunghezza $M$ e una sola moltiplicazione per campione:

$$
y(n) = \rho^M y(n-M) + x(n) - x(n-M)
$$

Nel caso più generale di frequenze arbitrarie, la funzione di trasferimento espansa resta:

$$
H(z) = \frac{N(z)}{N(\rho^{-1} z)} = \frac{1 + b_1 z^{-1} + \dots + b_P z^{-P}}{1 + \rho b_1 z^{-1} + \dots + \rho^P b_P z^{-P}}
$$

dove $a_i = \rho^i b_i$. Se $\rho \lesssim 1$, le coppie polo-zero si stringono e le tacche di attenuazione diventano estremamente strette e selettive:

![[immagini/comb.png|center mid]]

> [!NOTE] Filtro a Pettine Inverso (Inverted Comb)
> Invertendo la posizione reciproca di poli e zeri (spingendo gli zeri all'interno rispetto ai poli), la funzione si capovolge trasformando le valli di soppressione in picchi di risonanza periodica:
>
> ![[immagini/comb_inverso.png|center mid]]



# B. Sistemi Multi-Rate

Questi sistemi si basano sui filtri FIR per effettuare __interpolazione, decimazione e rate conversion__.

Fino ad ora abbiamo analizzato soltanto sistemi single-rate, dove la frequenza di campionamento $f_s$ non cambia tra input e output.

I sistemi multi-rate lavorano __cambiando la frequenza di campionamento__ del segnale. Sono fondamentali, ad esempio, per convertire flussi digitali tra standard con frequenze diverse (come il passaggio da audio CD a $44.1\text{ kHz}$ ad audio DAT o broadcast a $48\text{ kHz}$).

![[immagini/esempi_multirate.png|center mid]]

Un sistema digitale multi-rate produce una frequenza di campionamento in uscita scalata di un fattore intero oppure di un rapporto razionale tra interi.

## Interpolazione

![[immagini/blocchi_interp.png|center mid]]

Nell'interpolazione aumentiamo la frequenza di campionamento di un fattore intero $L$ rispetto a quella iniziale $f_s$.

Invece di ricampionare fisicamente il segnale analogico ad altissima frequenza con un convertitore A/D, questo processo viene svolto __interamente nel dominio digitale__ mediante una sequenza di operazioni matematiche equivalenti.

![[immagini/ex_interp.svg|center big]]

Dato che la sequenza originaria a frequenza $f_{s1}$ rispetta pienamente il teorema del campionamento di Nyquist-Shannon, essa contiene già tutta l'informazione del segnale continuo; i nuovi campioni intermedi ad alta frequenza $f_{s2} = L f_{s1}$ possono quindi essere calcolati in modo esatto in digitale.

![[immagini/schema_upsampler.png|center mid]]

Nel campionamento discreto lo spettro del segnale diventa periodico nelle frequenze con periodo pari alla frequenza di campionamento. Per ricostruire o interpolare il segnale alla nuova frequenza, occorre un __filtro passa-basso digitale__ che isoli la banda base originaria eliminando le repliche periodiche.

![[immagini/filtro_interpolatore.png|center mid]]

La frequenza di campionamento $f_s'$ è più alta del necessario proprio per distanziare le repliche spettrali ed evitare che il filtro prenda componenti indesiderate appartenenti agli intervalli adiacenti.

### Tipi Di Impulso per l'Interpolazione

Nel processo di conversione digitale-analogica (D/A) e di ricostruzione continua, una sequenza discreta di campioni numerici $y[n]$ deve essere trasformata in una forma d'onda continua nel tempo $y(t)$.

Dal punto di vista fisico e sistemistico, ogni campione $y[n]$ viene trasformato nell'emissione di un __impulso elementare continuo__ $p(t - nT_s)$, centrato all'istante di campionamento $nT_s$ e con ampiezza scalata dal valore numerico del campione.

Il segnale analogico continuo risultante è la __superposizione__ (somma pesata) di tutti gli impulsi traslati nel tempo:

$$
y(t) = \sum_{n=-\infty}^\infty y[n] p(t - nT_s)
$$

- __Impulso ideale (Sinc)__: rappresenta l'interpolatore perfetto secondo il teorema di Nyquist-Shannon:

  $$
  p(t) = \frac{\sin(\frac\pi{T_s}t)}{\frac\pi{T_s}t} = \text{sinc}\left(\frac{t}{T_s}\right), \quad -\infty < t < \infty
  $$

  Nel dominio delle frequenze la sua trasformata di Fourier è un filtro passa-basso a gradino netto (__brick-wall__) con banda rigorosamente limitata a $[-f_s/2, f_s/2]$.
  Tuttavia, l'impulso ideale __non è fisicamente realizzabile__:
  1. Ha durata temporale infinita ($-\infty < t < \infty$), quindi per calcolare $y(t)$ in un dato istante richiederebbe tutti i campioni infiniti passati e futuri (sistema non causale a ritardo infinito).
  2. Richiederebbe un filtro analogico di ordine infinito con transizione istantanea a $f_s/2$, impossibile da costruire con componenti fisici reali (resistenze, condensatori, amplificatori operazionali).

Per questo motivo, nei convertitori reali si ricorre a forme di impulso elementari $p(t)$ a __durata finita e causali__, facilmente generabili dall'hardware analogico del DAC.

![[immagini/tipi_impulso.png|center mid]]

### Zero-Order Hold Interpolation (Impulso Rettangolare)

![[immagini/zero-hold.png|center mid]]

- __A cosa serve__: È la forma di impulso più semplice in assoluto ed è quella implementata nativamente da tutti i DAC standard a scala (__Zero-Order Hold__ o circuito sample-and-hold). Il convertitore mantiene costante la tensione in uscita al valore $y[n]$ per l'intera durata del periodo di campionamento $T_s$, aggiornandola a gradino solo all'arrivo del campione successivo.
- __Comportamento e limiti__: È immediato ed economico da costruire in hardware. Tuttavia:
  - Nel dominio del tempo genera una forma d'onda a scalini discontinua.
  - Nel dominio della frequenza ha uno spettro di tipo $\text{sinc}$ che decade lentamente (come $1/f$), lasciando passare consistenti repliche spettrali ad alta frequenza (immagini dello spettro).
  - Introduce una sensibile attenuazione progressiva in banda utile (__droop__ di Nyquist), che raggiunge circa $-3.92\text{ dB}$ (circa $4\text{ dB}$) in prossimità di $f_s/2$.

A meno di non operare a frequenze di campionamento molto elevate (sovracampionamento), la ricostruzione con solo impulso rettangolare produce un'accuratezza modesta.

### Interpolazione Lineare (Impulso Triangolare)

![[immagini/linear_interp.png|center mid]]

- __A cosa serve__: Collega i campioni adiacenti a coppie mediante segmenti rettilinei continui (First-Order Hold), eliminando i salti bruschi a gradino. La durata complessiva dell'impulso è pari al doppio del periodo di campionamento ($2T_s$).
- __Comportamento__: Nel dominio della frequenza corrisponde a una funzione $\text{sinc}^2$, con un decadimento asintotico proporzionale a $1/f^2$.
- Rispetto all'impulso rettangolare, il decadimento quadratico abbatte in maniera decisamente più rapida le repliche ad alta frequenza, migliorando l'approssimazione del segnale. Tuttavia, la sua generazione richiede circuiti analogici integratori di rampa più complessi, oppure calcoli numerici dedicati per determinare la pendenza tra campioni consecutivi.

### Interpolazione Parabolica (Impulso Parabolico)

![[immagini/interp_parab.png|center mid]]

- __A cosa serve__: Realizza un raccordo polinomiale del secondo ordine (spline quadratica) continuo sia nei valori sia nella derivata prima. La sua durata temporale è pari a quattro volte quella rettangolare ($4T_s$, ovvero il doppio di quella triangolare).
- __Comportamento__: Assume valore unitario in $t=0$ ($p(0)=1$) e presenta zeri di campionamento a $\pm T_s$ e $\pm 2 T_s$, eliminando gli spigoli vivi dell'interpolazione lineare. Nel dominio della frequenza decade come $1/f^3$, offrendo una soppressione eccellente delle repliche spettrali ad alta frequenza.
- La generazione analogica diretta di impulsi parabolici precisi è tuttavia circuitalmente onerosa e raramente impiegata nei convertitori fisici.

### Sovracampionamento per l'Interpolazione

Se il segnale originale non varia sensibilmente nell'arco della durata dell'impulso, la ricostruzione analogica risulta fedele anche con impulsi elementari.

Invece di costruire complessi circuiti analogici per generare impulsi triangolari o parabolici, la tecnologia moderna risolve il problema __spostando la complessità nel dominio digitale tramite il sovracampionamento (oversampling)__.

Un DAC a scala (ZOH), la cui risposta in frequenza normalizzata segue l'andamento $\frac{\sin x}{x}$, attenua parzialmente le repliche spettrali, mentre il filtro passa-basso analogico successivo ha il compito di rimuoverle completamente. La combinazione del DAC a scala con il filtro simula la ricostruzione ideale.

Il ricostruttore analogico ideale sarebbe un filtro passa-basso a gradino con frequenza di taglio a $f_s /2$, dotato di una transizione ripida tra banda passante e banda di arresto.

![[immagini/filtro_ricor.png|center mid]]

Nelle applicazioni audio ad alta fedeltà, per garantire una qualità eccellente con campionamento a frequenza di Nyquist ($f_s = 44.1\text{ kHz}$), si dovrebbe utilizzare un filtro analogico ad altissimo ordine, estremamente costoso, sensibile alle tolleranze dei componenti e suscettibile di distorsione di fase.

Un modo efficace per alleggerire i requisiti del filtro analogico consiste nell'__aumentare la frequenza di campionamento__. Questo allontana sensibilmente lo spazio tra le repliche spettrali adiacenti, consentendo di impiegare un filtro analogico passa-basso con banda di transizione molto ampia, semplice ed economico (del 1° o 2° ordine).

![[immagini/fir_oversampled.png|center mid]]

La medesima conclusione si riscontra nel dominio del tempo: all'aumentare della frequenza di campionamento i gradini del DAC a scala diventano talmente fitti e ravvicinati da approssimare visivamente e fisicamente la curva continua originale.

![[immagini/oversampling_id.png|center mid]]

Questo approccio risulterebbe però impratico se richiedesse di convertire fisicamente in analogico e ricampionare dall'inizio a frequenza più alta.

La soluzione consiste nell'eseguire il sovracampionamento interamente in digitale mediante un __filtro interpolatore digitale__, che riceve i campioni alla frequenza di base $f_s$ e genera campioni intermedi alla frequenza moltiplicata $f_s' = L f_s$.

Rispetto alla nuova frequenza di campionamento $f_s'$, lo spettro dei campioni a bassa rate si presenta come una serie di repliche periodiche all'interno dell'intervallo esteso.

>[!note]
>Il nuovo intervallo di Nyquist è definito rispetto alla frequenza sovracampionata:
>
>$$\left[-\frac{f_s'}{2}, \frac{f_s'}{2}\right]$$
>
>Al suo interno compaiono quindi $L-1$ repliche indesiderate dello spettro di base (immagini spettrali).

![[immagini/oversampling_interpolatore.png|center mid]]

Questo è esattamente lo spettro del segnale all'uscita del blocchetto upsampler (rate expander).

Applicando un filtro digitale passa-basso con frequenza di taglio $f_c = f_s / 2 = f_s' / (2L)$ (nell'esempio con $L=4$, taglio a $f_s' / 8$) operante alla nuova frequenza $f_s'$, è possibile __eliminare tutte le repliche spettrali interne in eccesso__. Lo spettro risultante coincide perfettamente con quello di un segnale campionato fin dall'origine alla frequenza più alta.

Il filtro digitale, essendo periodico in $f$ con periodo $f_s'$, non può eliminare le repliche centrate ai multipli di $f_s'$. Queste ultime, trovandosi ora a frequenze molto elevate e ben distanziate dalla banda base, vengono rimosse senza difficoltà dal semplice filtro analogico di ricostruzione posto all'uscita del DAC.

### Forma Diretta

![[immagini/blocchi_interpolatore.png|center mid]]

Dati i campioni a frequenza base $x(n)$, la sequenza espansa nel tempo $x_{\text{up}}(n')$ all'uscita dell'upsampler è definita come:

$$x_{\text{up}}(nL) = x(n)$$

$$x_{\text{up}}(nL + i) = 0, \quad i=1,\dots,L-1$$

I campioni ai multipli interi di $L$ mantengono il valore dei campioni originari, mentre l'upsampler inserisce $L-1$ zeri tra ciascuna coppia di campioni consecutivi.

![[immagini/campioni_upsampler.png|center mid]]

Normalmente l'analisi è confinata nell'intervallo di Nyquist di base, ma l'espansione temporale allarga l'intervallo di osservazione a $[-f_s'/2, f_s'/2]$, rendendo visibili le repliche spettrali che devono essere eliminate dal filtro passa-basso digitale.

I parametri di taglio del filtro interpolatore alla nuova frequenza di campionamento sono:

$$f_c = \frac{f_s}2 = \frac{f_s'}{2L}, \quad \omega_c' = \frac{2\pi f_c}{f_s'} = \frac \pi L$$

Il filtro FIR interpolatore deve avere un __guadagno in continua pari a $L$__ per preservare l'ampiezza nominale dei campioni originari ($y_{\text{up}}(nL) = x(n)$) e compensare la scalatura spettrale introdotta dall'espansione del rate.

### Tecnica Di Progettazione Polifase

Partendo dal filtro interpolatore FIR, la convoluzione per determinare la sequenza interpolata ad alta frequenza si scrive come:

$$y_{\text{up}}(n') = \sum_{k'=-LM}^{LM} d(k') x_{\text{up}}(n'-k') \quad \text{somma convoluzionale non causale}$$

dove la lunghezza del filtro simmetrico è $N = 2LM + 1$.

Calcolare direttamente questa convoluzione alla frequenza elevata $f_s'$ comporterebbe un elevato spreco di risorse, poiché la maggior parte dei campioni di $x_{\text{up}}$ ha valore nullo. Scomponendo il filtro in __$L$ sottofiltri polifase operanti in parallelo alla frequenza di base $f_s$__, si ottiene un risparmio computazionale pari a un fattore $L$.

Indicizzando i campioni di uscita intermedi tra $nL$ e $(n+1)L$ con $n' = nL + i$ (con $i = 0, \dots, L-1$):

$$y_{\text{up}}(nL+i) = \sum_{k'=-LM}^{LM} d(k') x_{\text{up}}(nL+i-k'), \quad i=0,\dots,L-1$$

Scomponendo anche l'indice dei coefficienti $k'$ nella base $L$ con $k' = kL + j$:

$$y_{\text{up}}(nL+i) = \sum_{k=-M}^{M-1}\sum_{j=0}^{L-1} d(kL+j) x_{\text{up}}((n-k)L + i - j), \quad i=0,\dots,L-1$$

Si noti che l'estremo superiore $k' = LM$ della sommatoria non compare esplicitamente poiché per il filtro interpolatore ideale a banda $\pi/L$ vale $d(LM) = 0$ (proprietà di annullamento della sinc nei multipli di $L$), per cui ciascun sottofiltro polifase ha esattamente $2M$ coefficienti non nulli.

Si definiscono quindi gli $L$ filtri polifase $d_i(k)$ come:

$$d_i(k) = d(kL+i), \quad -M\leq k\leq M-1$$

Il ramo di ordine $0$, $d_0(k)$, agisce come un semplice filtro passa-tutto (ritardo puro), preservando inalterati i campioni originali della sequenza a frequenza base.

Tenendo conto che i campioni $x_{\text{up}}$ sono non nulli solo quando l'argomento è multiplo di $L$ (cioè per $j = i$):

$$\begin{align} x_{\text{up}}((n-k)L) &= x(n-k) \\ x_{\text{up}}((n-k)L + i - j) &= 0 \quad (j \neq i)\end{align}$$

La doppia sommatoria collassa al solo termine con $j = i$:

$$\begin{align} y_{\text{up}}(nL+i) &= \sum_{k=-M}^{M-1} d_i(k) x_{\text{up}}((n-k)L) \\ &= \sum_{k=-M}^{M-1} d_i(k) x(n-k) = y_i(n), \quad i=0,\dots,L-1 \end{align}$$

Ciascun filtro polifase $d_i(k)$ calcola direttamente l'$i$-esimo campione interpolato lavorando unicamente sui campioni originari a frequenza $f_s$.

![[immagini/filtro_polifase.png|center mid]]

## Decimazione

La decimazione è l'operazione duale dell'interpolazione, ovvero la riduzione controllata della frequenza di campionamento da un valore più alto $f_s'$ a uno più basso $f_s'' = f_s' / M$.

>[!warning]
>Non bisogna confondere il semplice __sottocampionamento__ (scarto puro di campioni nel tempo) con la __decimazione__.
>Il sottocampionamento da solo provocherebbe inevitabilmente __aliasing__ se il segnale di partenza contiene frequenze superiori alla nuova frequenza di Nyquist $f_s''/2$.
>La decimazione corretta include sempre un __filtraggio passa-basso preventivo (anti-aliasing)__ prima dello scarto dei campioni.
>
>Soltanto nell'ipotesi in cui si decimi un segnale precedentemente interpolato con il medesimo fattore, decimazione e sottocampionamento possono coincidere.

### Decimatore Ideale

![[immagini/decimatore_ideale.svg|center big]]

Prima di sottocampionare di un fattore $M$, è indispensabile garantire che lo spettro del segnale sia confinato entro l'intervallo $[0, f_s''/2]$, inserendo un filtro passa-basso digitale con frequenza di taglio $f_c = f_s''/2 = f_s' / (2M)$.

L'eliminazione delle componenti spettrali comprese tra $f_s''/2$ e $f_s'/2$ rappresenta una perdita di informazione irreversibile, ma matematicamente obbligatoria per prevenire distorsioni da ripiegamento spettrale (aliasing).

![[immagini/blocchi_ideal_decim.png|center mid]]

>[!note]
>Poiché i filtri ideali brick-wall non sono realizzabili, si impiegano filtri FIR progettati ad esempio con finestra di Kaiser, fissando:
>
>$$f_{\text{pass}} < \frac{f_s''}{2}$$
>
>$$\Delta f = 2\left(\frac{f_s''}{2} - f_{\text{pass}}\right)$$
>
>dove $f_{\text{stop}} = f_s'' - f_{\text{pass}} > \frac{f_s''}{2}$.

Il costo computazionale nominale diretto richiederebbe $N$ moltiplicazioni per ciascun campione ad alta frequenza. Tuttavia, poiché il decimatore trattiene solo 1 campione su $M$ (scartandone $M-1$), implementando la struttura polifase i calcoli vengono eseguiti solo per i campioni in uscita, riducendo l'onere computazionale medio a $N/M$ operazioni per campione d'ingresso.

### ADC Basati Sulla Decimazione

![[immagini/adc_decim.png|center mid]]

L'architettura con decimazione offre due vantaggi determinanti nella progettazione degli stadi di conversione analogico-digitale (ADC):
- __Semplificazione del filtro analogico anti-aliasing__: campionando inizialmente ad altissima frequenza $f_s'$, il filtro analogico preliminare può avere una pendenza molto blanda e componenti a bassa precisione.
- __Miglioramento della risoluzione effettiva (SNR)__: l'ADC rapido a monte può operare con un numero inferiore di bit; il filtraggio passa-basso digitale e la successiva decimazione mediano il rumore di quantizzazione distribuito su una banda molto ampia, incrementando il rapporto segnale-rumore (guadagno di processo).

## Sample Rate Converter

$$f_s'' = \frac{L}{M} f_s = \frac{f_s'}{M}$$

Un convertitore di frequenza di campionamento arbitrario a rapporto razionale si realizza mediante la cascata di un __interpolatore per $L$__ seguito da un __decimatore per $M$__.

>[!important]
>L'ordine della cascata non è commutabile: la decimazione è un'operazione irreversibile e distruttiva di informazione spettrale. Occorre sempre eseguire __prima l'interpolazione__ per $L$ e successivamente la decimazione per $M$. Invertendo l'ordine, il decimatore eliminerebbe frequenze che l'interpolatore non potrebbe più recuperare.

L'architettura a cascata presenta un notevole vantaggio di semplificazione:

![[immagini/blocchi_rate_conv.svg|center big]]

Entrambi i filtri (filtro anti-imaging dell'interpolatore e filtro anti-aliasing del decimatore) si trovano interposti tra l'upsampler e il downsampler, e operano quindi alla __medesima frequenza intermedia__ $f_s' = L f_s$.

Essendo due sistemi LTI in serie, la loro risposta complessiva è data dal prodotto delle singole risposte in frequenza:

$$H(\omega') = H_1(\omega') \cdot H_2(\omega')$$

Trattandosi di due filtri ideali passa-basso con tagli rispettivamente pari a $\pi / L$ e $\pi / M$, il loro prodotto coincide con il filtro avente la __banda passante più stretta__. È quindi sufficiente implementare un __singolo filtro FIR digitale__ con frequenza di taglio:

$$\omega_c' = \frac{2\pi f_c}{f_s'} = \min\left(\frac \pi L, \frac \pi M\right) = \frac \pi{\max(L,M)}$$

A seconda che risulti $L > M$ (conversione verso l'alto o up-sampling netto) oppure $L < M$ (conversione verso il basso o down-sampling netto), il filtro unico assume le caratteristiche rispettivamente del filtro interpolatore o del filtro decimatore.

## Filtri Multi-Stadio

Quando i fattori di conversione $L$ o $M$ sono molto grandi, la transizione richiesta al filtro digitale diventa estremamente stretta, determinando un ordine del filtro $N$ eccessivamente alto e un costo computazionale proibitivo.

Per ottimizzare le risorse, la conversione viene scomposta in __più stadi in cascata__ con fattori intermedi molto più piccoli (tipicamente mantenuti sotto 10).

Nei convertitori sample-rate a rapporto razionale viene scomposto soltanto lo stadio che impone il vincolo di filtraggio più severo.

L'ordine di allocazione dei fattori intermedi segue una regola precisa:
- __Dal fattore più grande al più piccolo__ per gli interpolatori (in modo che i filtri a pendenza più ripida operino alle frequenze di campionamento più basse).
- __Dal fattore più piccolo al più grande__ per i decimatori (per massimizzare la reiezione prima di ridurre ulteriormente la frequenza).

![[immagini/multi_stadio.svg|center big]]

## Equalizzazione DAC

![[immagini/dac_eq_blocchi.png|center mid]]

La risposta impulsiva fisica di un DAC standard a ritenuta di ordine zero è un impulso rettangolare di durata pari al periodo di campionamento.

In un sistema con oversampling, l'uscita dell'interpolatore numerico viene inviata al DAC a scala operante alla frequenza sovracampionata $f_s'$.

In questo caso la sua risposta in frequenza normalizzata (al guadagno) è data da:

$$H_{\text{dac}}(f) = \frac{\sin(\pi f / f_s')}{\pi f / f_s'}e^{-j \pi f / f_s'}$$

Tale risposta introduce un'attenuazione progressiva (droop) all'interno dell'intervallo di Nyquist fino a circa $4\text{ dB}$.

Per un filtro interpolatore con fattore $L$ e frequenza di taglio $f_c = \frac{f_s}2 = \frac{f_s'}{2L}$, la massima attenuazione al bordo della banda passante utile risulta:

$$|H_{\text{dac}}(f_c)| = \left| \frac{\sin(\pi f / f_s')}{\pi f / f_s'}\right |_{f = \frac{f_s'}{2L}} = \frac{\sin(\pi / 2L)}{\pi / 2L}$$

- Per valori elevati di $L$ ($L \geq 16$), l'attenuazione al bordo banda diventa trascurabile (inferiore a frazioni di decibel) e tende a $0\text{ dB}$.
- Per valori moderati di $L$ (ad esempio per $L \leq 8$), l'attenuazione di diversi decibel è avvertibile; è quindi opportuno compensarla sagomando il filtro interpolatore con una __risposta inversa__ rispetto a quella del DAC nella banda passante.

![[immagini/disegno_eq_dac.png|center mid]]

Il filtro equalizzato ideale desiderato ha risposta in frequenza:

$$D(f) = \begin{cases} 
LD_{\text{eq}}(f), & \text{se } |f| \leq \frac{f_s}2\\
0,& \text{se } \frac{f_s}2 < |f| \leq \frac{f_s'}2
\end{cases}$$

dove $D_{\text{eq}}(f)$ rappresenta l'inversa dell'ampiezza di $H_{\text{dac}}(f)$, privata della fase per operare a valori reali.

Nel dominio delle frequenze discrete normalizzate:

$$D(\omega') = \begin{cases}
L\frac{\omega'/2}{\sin(\omega'/2)}, & \text{se } |\omega'| \leq \frac \pi L\\
0,& \text{se } \frac\pi L < |\omega'| \leq \pi
\end{cases} $$

Tale filtro FIR può essere progettato agevolmente mediante il [[8. Filtri FIR - Finite Impulse Response#^14b2ae|Metodo del campionamento in frequenza]].

Noti la lunghezza $N$ del filtro desiderato (con $N = 2LM + 1$) e i campioni di frequenza, i coefficienti impulsivi simmetrici si determinano mediante IDFT a $N$ punti:

$$\tilde d(k') = \frac 1N \sum_{i = -LM}^{LM}D(\omega_i')e^{j\omega_i'k'}, \quad -LM \leq k' \leq LM $$

Il filtro causale finestrato si ottiene applicando una finestra simmetrica centrata $w(n')$:

$$h(n') = \tilde d(n'-LM)w(n'), \quad 0 \leq n' \leq N-1$$

Dato che la risposta desiderata cresce verso l'alto ai bordi della banda passante per compensare la caduta del DAC, per garantire il livello di attenuazione desiderato nella banda di arresto con una finestra di Kaiser è necessario specificare un'attenuazione di progetto leggermente più severa.

Inoltre, per assicurare coefficienti a valori puramente reali e simmetrici, l'espressione della IDFT si semplifica nella forma a soli coseni:

$$\tilde d(k') = \frac 1N \sum_{i = -LM}^{LM}D(\omega_i')\cos(\omega_i'k'), \quad -LM \leq k' \leq LM $$

![[immagini/freq_sampling.png|center mid]]
