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

### Sovracampionamento per l'interpolazione

Se il segnale originale non varia di molto nella durata dell'impulso è facile ottenere una buona ricostruzione.

Il sovracampionamento è una pratica comune per ottenere un segnale ricostruito accurato, utilizzando un DAC semplice.

Slide 15