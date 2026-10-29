# lezione\_15

slide 4: nel caso in cui w non sia a media nulla, posso andare a manipolare B per spostare la media di w e renderlo a media nulla.

slide 5: lo stimatore di kalman è ottimo nel mondo lineare. nei problemi di localizzazione, però, i modelli non sono lineari, bisogna quindi estendere il filtro di kalman.

slide 6: è l'estensione ai modelli non lineari del filtro di kalman, ma ancora non è adatto alla localizzazione.

slide 7-8: il fatto che il modello sia non lineare rende impossibile il calcolo in forma chiusa della covarianza.
Non sappiamo come evolve la covarianza nel contesto non lineare.
si usa quindi il modello non lineare per calcolare la stima, e si usa un'approssimazione del modello per la covarianza.
Dato che è un'approssimazione la covarianza non è esatta e si perde quindi tutta l'ottimalità del filtro di kalman.
Assumiamo che x_t è una funzione generica dello stato precedente e l'ingresso u e che il rumore w sia additivo rispetto all'ingresso.

abbiamo f e h per indicare che non sappiamo nulla della covarianza.

slide 9: la stima a priori è l'evoluzione della stima a posteriori al passo precedente.
Quando lo stato evolve, in realtà, evolve il valore atteso dello stato precedente, è quindi un modello deterministico che evolve una volta sola.

Quanto più la non linearità della covarianza è forte, tanto più è errata l'approssimazione lineare che applichiamo.

slide 10: una volta calcolata la prior calcola l'innovazione, la pesa per il guadagno L e stima a posteriori.

slide 11: il fatto che il modello sia non lineare perde la proprietà di gaussianità del rumore.
il rumore nel kalman lineare è stabile, in questo no.
per sensor fusion si intende che per lo stesso contesto si usano sensori che misurano informazioni diverse, e che vengono poi messe insieme per effettuare delle stime.

slide 12: nella covarianza approssimata abbiamo $F_u Q_t F_u^T$, ma se fossimo stati nel mondo lineare avremo avuto $P_{t|t-1} = AP_{t-1|t-1}A^T + Q_t$, dove non abbiamo la presenza della matrice $B$. 

Possiamo approssimare la formula di $x_t = f(x_{t-1}, u_t + w_t)$ come $\delta_{xt} = F_x \delta_{xt-1} + F_u(\delta_u + w_t)$, dove $F_x = \frac{\partial l}{\partial x} |_{x = \hat x_{t+1|t-1}, u = u_t}$ moltiplico $F_u$ per la variazione dell'ingresso e il rumore, così ottengo poi nella covarianza approssimata $F_uQ_tF_u^T$, perché in realtà nel caso lineare la formula sarebbe dovuta essere $P_{t|t-1} = AP_{t-1|t-1}A^T + IQ_tI^T$.

La parte relativa all'ingresso non è presente perché B è un termine deterministico che non sposta la covarianza.

slide 18: una volta ottenuta la stima a priori effettua il matching (correzione della stima). All'interno del matching c'è il calcolo dell'innovazione e soprattutto l'associazione tra le features.
In precedenza infatti assumevamo di sapere dove ci troviamo nella mappa, ma nella realtà non abbiamo informazioni riguardo la posizione.

/// stiamo paragonando il filtro di kalman con il filtro a istogramma, in kalman non abbiamo la sommatoria del motion model moltiplicato per la belief precedente perché è tutto descritto dalla gaussianità.
//// AMCL utilizza il campo di verosimiglianza per trovare dove si trova. il calcolo della dist è l'equivalente dell'associazione di kalman.

slide 19: assumo di essere nel mondo del differential drive, posso assumere di avere il velocity motion model deterministico.
Stiamo facendo evolvere il valore atteso della stima, quindi è deterministico.

Come prima assumo che il rumore entri additivamente ad u.

slide 20: le coppie in $z_t^i$ hanno coordinate relative al sistema di riferimento del sensore.

slide 22-23: prendo la i-esima lettura, e la j-esima retta della mappa. con h calcolo la retta nel sistema di riferimento laser, e a questo punto z - h è una differenza esatta, se fossero la stessa retta ho l'errore, ma non so se la retta j è quella che mi serve.

Sigma è esattamente la covarianza della z tilde che ho calcolato prima.

posso calcolare la distanza di mahalanobis, se sigma è la matrice d'identità ho la norma del vettore, mentre se sigma è diagonale ho la media pesata con le varianze omonime (la prima componente per z tilde la divido per la sua covarianza, ecc...).
Quella mu è adimensionale e rende confrontabili le quantità, perché normalizzo le informazioni in base alla loro varianza.

Ho costruito una coppia i,j e gli ho associato una distanza mu, se io fisso i e lo faccio per tutti i j posso decidere che l'associazione (matching) è fatta con la coppia più vicina.


slide 29: se uso uno dei primi due modelli la covarianza è non stazionaria, e di conseguenza anche il filtro.

//// per calcolare l'errore il confronto deve essere fatto rispetto allo stesso sistema di riferimento, devo quindi ricalcolare le rette e portarle al sistema di riferimento del laser.