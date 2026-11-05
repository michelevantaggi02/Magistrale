questa lezione è stata fatta DOPO la lezione 15.
le slide citano le lezioni per numero, ma attento perché le slide spesso e volentieri non coincidono, (ad esempio all'interno di questa slide c'è scritto lecture 11, ma siamo alla lezione 14 e il file si chiama 14).
Se vuoi inserire delle citazioni ritrova l'argomento negli appunti e cita il capitolo, non la lezione.

slide 5: normalmente gli input sono indipendenti da quelli precedenti, la rete non tiene a mente nulla degli input precedenti.
non possiamo quindi utilizzarle per modellare correlazioni tra più input in diversi istanti di spazio o tempo.

slide 10: vogliamo inserire il concetto di memoria all'interno della rete.
Facciamo visualizzare alla rete un elemento alla volta, facendole però ricordare quello che ha visto.

slide 12: se abbiamo un set di parametri specifico per ogni istante di tempo ci riporta al problema denso (dato che abbiamo un numero finito di pesi).
L'altro problema è che il numero di parametri cresce e aumenta il rischio di overfitting.
Avere soltanto un numero finito di parametri permette alla rete di capire soltanto i parametri che realmente servono.

slide 13: L'aggiornamento di memoria è una funzione che prende il precedente istante di memoria e l'input corrente.
l'obiettivo di questa ricorrenza è quindi come detto di imparare soltanto quello che serve.
Ad esempio, se stiamo effettuando una traduzione di una frase, la rete potrebbe dimenticarsi di una parte di input per poter predire il significato di una parola successiva.

slide 14: la matrice U modella la relazione tra l'input e l'hidden state.
W non ho capito
V modella lo stato di memoria attuale e l'output.

U ovviamente ha un numero di righe uguale alle unità nascoste del layer (non ho capito quale layer).

slide 15: la preattivazione del layer corrente è W moltiplicato per lo stato precedente + U per l'input + il bias.

l'output di esempio è perché consideriamo il problema come classificazione, ma ovviamente dipende dal tipo di problema che stiamo affrontando.

slide 16: dato che i parametri sono condivisi, W, U e V hanno gli stessi parametri nel tempo, ma non è questo quello che vogliamo, vogliamo che questi parametri si comportino diversamente in base a cosa abbiamo in memoria.

Nella recurrent network abbiamo situazioni diverse in base al pattern che abbiamo scelto (in questo esempio many to many), abbiamo una loss value per ogni time step nella sequenza.

slide 17: la overall loss è la somma delle loss di ogni step.
Compariamo queste probabilità usando la cross entropy al tempo t???

slide 20: l'addestramento di una rete propaga il gradiente anche al passo temporale precedente, rendendo la back propagation più complessa, in quando modificando il passo temporale precedente cambia la memoria nel passo temporale attuale.

slide 21: la backpropagation va dal passo attuale fino all'origine temporale, quindi il gradiente deve passare per tutti gli stati fino al primo.

slide 22: V è il più semplice da calcolare perché non ci obbliga a indietreggare nel tempo.
La derivata parziale applica quindi la regola della catena solo per questi 3 layer.
Chiaramente bisogna effettuare la somma per tutte le classi.

slide 23: formula della parziale della softmax rispetto ad o.

slide 25-26: Quando calcoliamo al derivata ad ogni step, applichiamo la regola della catena, ma W influenza anche lo step temporale precedente quindi bisogna propagarlo fino all'inizio.

slide 49-52: nel gradiente abbiamo il prodotto di molti termini parziali fino all'origine temporale.
L'impatto di una parola che era all'inizio della frase, se il gradiente non raggiunge quel punto sarà 0, quindi parole molto lontane nel passato non avranno un impatto nella predizione corrente.

slide 53: l'exploding gradient può come detto in precedenza essere risolto con il clipping, e sempre come detto in precedenza il vero problema è il vanishing gradient.

slide 56: l'idea è la stessa di ResNET.
Long Short Term Memory è implementata utilizzando il cell state, una connessione dove il gradiente non è affetto più di tanto.
L'idea dietro LSTM è di utilizzare dei gate per ??????? influenzare? idk, soltanto timestep scelti.
In questo modo il gradiente è moltiplicato solo dal forget gate????

slide 57: l'idea è di imparare degli switch per decidere quali informazioni leggere, salvare e prendere???

slide 58: il forget gate decide cosa eliminare dalla memoria, è l'unico gate connesso al gradiente, e quindi in grado di abbassarlo.

slide 59: l'input gate ci fornisce nuove informazioni da aggiungere in memoria.
è composto da due moduli, una tangente iperbolica che crea un vettore che riassume l'input e lo stato di memoria precedente.
La sigmoide moltiplica quello che la tangente iperbolica produce, e decide quali parti aggiungere effettivamente alla memoria.
il risultato di questa formula viene aggiunto in memoria dal nodo di somma.
Rimuoviamo quindi le informazioni ridondanti e aggiungiamo di nuove.

slide 60: l'output gate prende lo stato, lo passa tramite la tangente iperbolica, e usa una sigmoide per decidere la predizione corrente e la memoria futura.

slide 64: la gated recurring unit serve a risparmiare un po' di parametri, nella pratica non ci sono grosse differenze tra i due e forniscono le stesse performance.
anche se GRU fa risparmiare memoria si preferisce usare LSTM.

slide 69: le recurrent network vengono ancora utilizzate per task un po' più semplici, perché per compiti più complessi come documenti enormi si preferiscono i transformer.
I transformer sono progettati con le recurrent network in mente, per migliorarne le criticità.

//// l'ultimissima parte è un'introduzione alla lezione successiva, non ho ancora le slides