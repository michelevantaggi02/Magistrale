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
