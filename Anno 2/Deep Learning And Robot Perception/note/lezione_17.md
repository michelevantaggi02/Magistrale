slide 8: è difficile individuare un punto che abbia un senso.

slide 11: l'encoder deve essere in grado di ricostruire l'input che stiamo processando.
Se le feature che stiamo addestrando sono robuste, queste riescono a ricostruire l'intera immagine.

slide 12: la loss è un mean square error che compara l'input con la sua ricostruzione.
L'autoencoder può essere usato per qualsiasi cosa, anche immagini, video, qualsiasi informazione.

slide 25: l'idea è di modellare la prior distribution per stimare la probabilità.
anche utilizzando il teorema di probabilità totale è molto difficile stimare la probabilità, e calcolare l'integrale è estremamente complesso, in quanto avremo bisogno di tantissimi punti (circa 100^16 mi pare di aver capito per questo esempio).
se campioniamo z randomicamente, avremo immagini molto diverse e sparse, avendo quindi pochi punti con immagini candidate.
Non avremo quindi il segnale di supervisione per addestrare la rete.

slide 26: l'idea è di valutare codici che sappiamo provengano da immagini, invece di prenderli randomicamente (dato che molti non generano immagini valide).
sfruttiamo il teorema di bayes effettuare i calcoli usando la posterior.
di conseguenza possiamo sfruttare la posterior per selezionare le immagini valide e generare nuove immagini anch'esse valide.
Abbiamo però sempre il problema di dover stimare p(x).

slide 27: usiamo la parte di encoder per avvicinarci il più possibile alla posterior distribution.

slide 29-30: se prendiamo il valore atteso rispetto a q, dato che la prior non dipende da q avremo come risultato la funzione stessa.
il primo termine è il valore atteso della ricostruzione, ci dice la media delle immagini ricostruite

slide 31: possiamo calcolare la reconstruction e la kl alla prior, ma non possiamo calcolare quella alla posterior.
dato che la kl alla posterior è sempre positivo, possiamo assumere che la probabilità sia maggiore o uguale alla differenza tra i primi due termini. questa differenza viene chiamata ELBO.
cercare di massimizzare la ELBO ci permette anche di aumentare il valore della probabilità.

slide 47: l'idea è di convertire i pixel dell'immagine in token di un vocabolario.
addestriamo un codebook (un insieme di token), prendiamo uno di questi token a random e generiamo un'immagine pixel per pixel.

slide 48: 
