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


