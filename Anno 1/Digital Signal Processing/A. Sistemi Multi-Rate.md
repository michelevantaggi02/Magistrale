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
