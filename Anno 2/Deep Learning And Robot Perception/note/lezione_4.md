slide 3: dobbiamo riuscire a rilevare i punti di interesse unici che possono essere descritti facilmente

slide 5: una buona identity card potrebbe essere la matrice della finestra del punto.

slide 17: il problema di scala è presente sia dal lato detector che dal lato descriptor

slide 19: L'idea è quella di identificare anche la dimensione del KP, e di stimare anche l'orientamento così da poter adattare la finestra di conseguenza

slide 20: SIFT (Scale Invariant Features Transform) ha come obiettivo quello di riconoscere questi cambiamenti. Estrae i KP (Il detector è scale invariant), calcola l'orientamento e descrive i kp individuati (quindi è invariante anche il descriptor).

slide 24: se applichiamo una funzione a versioni dell'immagine sfocate diversamente, e questa funzione risponde diversamente ad ogni variazione, possiamo individuare la scala caratteristica di quel dettaglio.

slide 25: cambiando la scala abbiamo che la funzione risponde allo stesso modo usando un kernel più piccolo, se fatta bene la differenza di scala sarà data dai picchi della risposta.

slide 27: possiamo quindi stimare sigma per stimare la scala e la dimensione della finestra.

slide 28: la funzione deve avere un unico massimo ben definito

slide 29: la derivata seconda ci fornisce un blob in corrispondenza di angoli

slide 30: se cambi la scala della gaussiana il picco si abbassa e diventa meno chiaro, per risolvere moltiplichiamo il risultato per sigma al quadrato

slide 35: una versione meno costosa del LoG usando la differenza tra 2 gaussiane

slide 36: SIFT aggiunge un'altra operazione calcolando la hessian matrix

slide 42: l'idea è che l'orientamento del gradiente è un buon inizio per capire l'orientamento del corner.

slide 43: il picco si sposta secondo l'orientamento dell'immagine.

slide 60: eseguendo SIFT su due immagini diverse ottengo due vettori diversi, devo quindi poi matchare i vari punti dei due vettori per individuare i cambi di posizione

slide 63: la threshold a 1 indica che accettiamo tutti i possibili match. Abbassare la soglia fa diminuire enormemente il numero di match sbagliati, a scapito di pochi match giusti eliminati.