# lezione\_16

slide 8: ci serve per migliorare le informazioni in memoria e avere migliori performance.

slide 21: in questa situazione non abbiamo un gradiente in quanto la softmax azzera tutti gli altri valori, di conseguenza non possiamo aggiornare i pesi.

slide 22: assumiamo che siano indipendenti e con media 0, la varianza è quindi la somma di tutte le varianze, che sono 1, e la somma d_k volte è d_k.
per evitare l'effetto di appiattimento della softmax all'aumentare del numero di parametri (?) lo dividiamo per la radice del numero di parametri.
in questo modo non si appiattisce tutto a 0.

slide 25: il vettore delle query è lo stato del decoder, le key e value sono gli stati dell'encoder.
Partono dal vettore input e creano questi vettori usando delle matrici. Abbiamo bisogno di tre mappe diverse perché in genere quello che cerchiamo non è necessariamente l'output layer. 

slide 29: 
////inserisci immagine, "the" "robot" "grasps" messi in colonna, ognuno con una freccia che genera il vettore di lunghezza d, vengono moltiplicati e si genera quindi una matrice Nxd che genera i vettori Q = XW_q, K=XW_k, V=XW_v
W_q \in R^{dxd_k}
spiega che K e V in genere hanno invece dimensioni diverse da Q.

slide 30: propaghiamo le informazioni delle altre parole a seconda dell'attenzione di quelle parole impilando più layer di attenzione. componiamo l'attenzione layer dopo layer.

slide 31: la differenza tra il layer denso e il convoluzionale hanno parametri fissi, mentre il self attention ha parametri diversi.
lo svantaggio è che più token ho, più lavoro devo fare.

slide 33: uno dei limiti è che l'attenzione perde totalmente l'ordine dei token, se calcoliamo una permutazione dell'input, l'output avrà una permutazione senza cambiare parametri.
L'attention layer non ha senso dell'ordine, non srotoliamo la sequenza e abbiamo quindi questa perdita.

slide 36: associamo ad ogni parola l'indice della parola nel vocabolario, non utilizziamo il vocabolario intero, ma cerchiamo di limitarlo alle parole più comuni, rimuovendo quelle meno utilizzate.
Per le parole più rare le dividiamo in sottotoken, "grasps" viene diviso in "grasp" e "s".
Esistono anche token speciali tipo \<START\>  e \<STOP\>.

slide 37: si calcola quindi un embedding che prende un vettore sparso e genera una versione densa di quel vettore.

////genera immagini, due piani cartesiani, il primo è il token space, con assi x_1 y_1, dove dog e cat sono lontani tra loro, una freccia rappresentante l'embedding va nel embedding space con assi d_1 d_2, dove dog e cat sono vicini tra loro

slide 39: 
////aggiungi immagine, "the" genera un vettore di embedding [0.2, 0.1, -0.3] che sommato al vettore position (inserisci la formula) p_0,0 = sin(10000^{-28/3} 0) = 0, p_0,1 = cos(10000^{-28/3} 0) = 1, stessa cosa per la parola robot, che genera il vettore embedding [0.1, 0.1, -0.4] che sommato al vettore posizione (solo prima formula) p_1,1 = sin(1 1)

slide 43: il decoder non ha accesso alle parole future, quando calcoliamo il self attention del decoder le parole a cui ha accesso sono soltanto quelle passate.
L'unico caso in cui ha accesso a quelle future è durante il training, ma dobbiamo mascherarle per impedirgli di addestrarsi guardando le parole future, mettendo l'attenzione a 0 tramite una maschera.

impostiamo la score a -infinito per avere la softmax a 0.
L'encoder invece ha accesso a tutta la frase, ed è quindi in grado di osservare le parole future per capirne il significato.

slide 45: un token potrebbe avere bisogno di più di una singola attenzione, ma la softmax fornisce un'attenzione unica.

slide 46: l'idea è quindi di aggiungere più teste all'attention layer, ognuna con i suoi parametri diversi, che ottiene una parte dell'embedding vector.
W_o ha lo stesso ruolo della matrice 1x1 nelle reti convoluzionali.

slide 49: di solito si sceglie un numero tra 8 e 16 teste, ovviamente abbiamo anche il bottleneck delle memorie.

slide 52: il transformer è una pila di attention layer con delle aggiunte.

slide 53: Abbiamo sempre il vanishing gradient, quindi si prende da resnet le connessioni residue.

slide 55: il transformer usa anche layer densi.

slide 65: il sample delle probabilità è il motivo per cui per lo stesso input gli llm producono risposte diverse.

slide 75: Una volta estratta e vettorizzata la patch abbiamo un equivalente dell'embedding vector, che può essere quindi mandato al visual transformer.

slide 76: possiamo utilizzare un layer convoluzionale con kernel della stessa dimensione della patch.

/// tornato a slide 69

slide 77: il ruolo del class token è quello di contenere le informazioni semantiche per effettuare la classificazione.

slide 87: questi metodi forniscono un grosso effetto di regolarizzazione, diminuendo la probabilità di overfitting.

slide 88: Si inizia addestrando il transformer con meno token (usando patch più grandi) e si effettua poi fine tuning con patch più piccole, e quindi un numero di token maggiore.

slide 89: l'attention layer può decidere quante informazioni locali utilizzare ad ogni layer.

slide 92: Il vision transformer divide l'immagine in patch 16x16, quindi la visione dell'immagine manca di alcuni dettagli perché utilizziamo patch molto grandi.
Vogliamo quindi avere più patch di dimensione minore, il problema è che la complessità aumenta quadraticamente (quindi con il quadrato dei token).

