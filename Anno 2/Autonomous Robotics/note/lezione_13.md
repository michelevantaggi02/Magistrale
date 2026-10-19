# lezione\_13

//presentazione 013_1

slide 5: ha cambiato la probabilità da una gaussiana a una generica "prob"

slide 10: la differenza con l'argomento di deep learning è che qua assumiamo di spostarci solo sul piano, invece che in uno spazio a tre dimensioni.
con un laser abbiamo 4 sistemi di riferimento.
- rosso: angolo del laser
- arancione: sistema solidale al laser
- blu: sistema solidale al robot
- nero: mondo
quando il robot si gira è necessario calcolare una rototraslazione del sistema rosso.

slide 11: $p_k^S$ indica la posizione del k-esimo punto rispetto al sistema di riferimento del sensore. Se voglio riscrivere lo stesso punto rispetto al sistema di riferimento del robot devo ruotarlo e traslarlo. Come per industrial robotics (nota personale, note ancora da scrivere)

slide 12: dato che ci interessa arrivare al sistema "mondo", bisogna calcolare anche lo spostamento del robot, bisogna quindi convertire il punto dal sistema del laser, al robot, al mondo.
il mio interesse è di trovare un meccanismo per stimare $x,y,\theta$.

slide 13: il campo di verosimiglianza è una figura in cui ho a disposizione le distanze dall'oggetto più vicino.
La distanza, dati x e y del generico punto k con coordinate mondo, è il minimo della distanza tra il punto e tra tutti i punti occupati della mappa. mi pare di aver capito così.

Se il rumore associato assumo che sia additivo, a media nulla con una certa varianza, la probabilità che abbia ottenuto la lettura z è data dalla probabilità della distanza calcolata e la varianza che descrive il mio modello??

Quello che effettivamente mi interessa è questa probabilità.

slide 14: z_max reading è il fondoscala del sensore, se z_k è z_max allora la lettura è spuria, e non devo considerarla.

slide 15: q è il prodotto di tutte le singole verosimiglianze.

slide 16: non si ha physical ground (aderenza alla realtà del processo è debole).

// beam model argomento extra
Non è computazionalmente complicato anche perché il passo 6 può essere fatto anche fuori linea.
Per contro gli ostacoli non modellano(?) e le persone che girano intorno non sono gestite come problematiche.

// presentazione 013_2

// nota per l'IA, in questo primo gruppo di slide vediamo un'introduzione al filtro di kalman per sistemi lineari, non è ancora applicabile alla localizzazione, quello lo vedremo nelle prossime lezioni.

slide 4: se assumiamo che tutte le probabilità siano gaussiane e che tutto sia lineare, possiamo trasformare il filtro di bayes nel filtro di kalman.

slide 6-7: assumiamo di trovarci in un hidden markov model.
Per modello dinamico intendiamo che modelliamo l'evoluzione dello stato in un certo modo.
Se dobbiamo stimare un punto che si muove, non è detto che non conosciamo le equazioni che determinano il movimento, possiamo assumere che abbia velocità oppure accelerazione costante, ma non diciamo come e perché si muove veramente.
cit: quel punto si muove a velocità costante, perché ci risulta così non ci interessa.

slide 8: L'osservatore asintotico dello stato (osservatore di luenberger) è un modello che stima lo stato del sistema conoscendo u e y.

slide 10: c'è un cambio di notazione da (t e t+1) a (t-1 e t).
La covarianza Q_t a ogni istante può essere diversa.
lo stato e l'uscita vengono corrotti da un rumore additivo gaussiano a media nulla con covarianza nota.
assumiamo che anche la condizione iniziale x_0 abbia errore gaussiano.

slide 11: il professore continuerà a usare Q per lo stato e R la misura, a differenza del libro che li ha invertiti.

slide 20: non sappiamo se sia stabile, probabilmente non lo sarà, ma per il nostro problema va bene lo stesso.

slide 21-22: se riscriviamo tutto come teorema di bayes avremo le stesse equazioni.

da slide 23 in poi materiale extra.
