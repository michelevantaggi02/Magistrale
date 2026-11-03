slide 3: la classificazione delle immagini funziona in genere quando hai un'immagine che rappresenta un singolo oggetto, se abbiamo più oggetti dobbiamo passare all'object detection.

Nella semantic segmentation non creiamo un bounding box dell'oggetto, ma analizziamo ogni pixel per riconoscere la silhouette.

l'instance segmentation è in grado di differenziare anche instanze diverse dello stesso oggetto.

Grazie alle cnn possiamo riconoscere la distanza del punto che genera il pixel  sfruttando le proporzioni dell'oggetto e altre informazioni come le ombre ecc..

slide 6: l'idea è di assegnare a ogni pixel un punteggio id una categoria.
in generale 

//// inserisci immagine schema a blocchi,  blocco I_1 immagine di dimensione HxW che va nel blocco CNN che va nel blocco di output che sono N matrici (feature map) per ogni classe (es: car, cat, house).

Per ogni pixel abbiamo che in ogni feature map la probabilità che quel pixel vada in quella categoria calcolata con la softmax.

Avremo l'output di dimensione HxWxN.

Dobbiamo classificare ogni pixel come appartenente a una classe.

La loss è semplicemente la somma su tutti i pixel del logaritmo della probabilità per ogni classe???

Se il mio modello mi da una score il cui logaritmo è inferiore a 1 (esponente 0) la somma andrà verso -infinito, con il cambio di segno aumenta la loss.

slide 8: una possibillità è di utilizzare una sliding window che usa una cnn con output di grandezza il numero di possibili categorie.
Non gli diamo quindi direttamente tutta l'immagine.

slide 9: se utilizziamo soltanto layer convoluzionali aumenta enormemente il requisito di memoria.
Un modo più conveniente è di utilizzare strides o pooling layer per contenere la memoria e successivamente riampiare la risoluzione.

slide 10: l'unpooling parte da una bassa risoluzione e crea una ad alta risoluzione. 

slide 11: il transposed convolutional layer usa lo stride per fare l'upsampling dell'immagine. L'unpooling viene quindi addestrato.

slide 13: in U-net le feature map dell'encoder sono condivise con il decoder, a differenza della pipeline convoluzionale che viene addestrata separatamente.
L'idea è che condividendo le mappe si possono ricostruire alcune delle informazioni che vengono perse quando si abbassa la risoluzione.

slide 15: si può sfruttare la stessa architettura per obiettivi diversi, come la profondità.

slide 17: vogliamo identificare un bounding box che riconosca un oggetto nell'immagine.
La prima cosa che possiamo fare è di assumere che l'immagine contenga un solo oggetto, possiamo quindi passare l'intera immagine e avere 2 risultati diversi, uno per il bounding box e uno per la classe.

//// inserisci schema a blocchi, primo blocco immagine in input con una tazza vista dall'alto, secondo blocco "resnet backbone", terzo blocco un cubo di 512 feature maps, quarto blocco Global average pooling (GAP)  che fornisce un vettore di 512, il vettore viene connesso a 2 teste (output, fully connected): una testa ha 4 neuroni che forniscono il corner e altezza e larghezza del bounding box (L2 loss che compara l'errore di posizione e dimensione del bounding box), la seconda testa ha N neuroni che rappresentano le varie classi (cross entropy loss).

i due gradienti diversi vengono poi sommati e vengono propagati fino alla backbone per fare anche fine tuning.

Questo funziona però assumendo di avere un solo  oggetto nell'immagine.
Se abbiamo molti oggetti una possibilità è di avere un massimo numero di oggetti e replicare gli output un numero di volte che decidiamo, ma non è la soluzione ottimale.

slide 19: spesso i bounding box vengono addestrati anche sulla precision e recall, per farlo usiamo una treshold nella IoU e diciamo che una predizione è corretta se l'intersezione è almeno 0.5.

slide 20: Questo algoritmo è pensato per fornire molti falsi positivi.
La region proposal non ci fornisce la classe degli oggetti, solo delle proposte su dove si trovano questi oggetti, bisogna quindi poi fare la classificazione.

Si effettua il warping e ogni regione viene inserita nella stessa CNN, usata per generare le feature map che venivano inserite in una SVM per la classificazione e un regressore lineare per rifinire il bounding box.
Il primo processo di training addestra i parametri della CNN, il secondo addestrava la SVM, e il terzo la regressione lineare.

slide 21: questa rete è quindi molto sconveniente, in quanto sia l'addestramento che l'inferenza impiegavano un tempo lungo (47 secondi di inferenza).

slide 22: per questo motivo viene proposta la fast R-cnn, che sposta la region proposal dopo l'estrazione delle feature.
Prima estraggo l'immagine, passo tutta l'immagine alla CNN e poi effettuo il cropping sulla feature map, il GAP viene sostituito con un ROI pooling layer.
A differenza della regione precedente utilizza la struttura con 2 gruppi di output uno per il bounding e uno per la classe, accelerando l'addestramento e l'inferenza.

slide 23: il ROI crea un output che ha sempre la stessa risoluzione indipendentemente dalla dimensione della regione proposta.
divide la regione in 9 celle e effettua il pooling sul valore massimo delle 9 celle.

//// inserisci immagine di esempio, immagine matrice 6x6, regioni proposte di 3x2 e 5x2, se il roi deve proporre 2 output sceglie le 2 celle con i 2 valori più alti, quindi clona le due regioni fuori, indica i 2 punti per regione maggiori e con delle frecce crea due regioni 2x1 che contengono questi valori massimi.

slide 25: faster R-cnn ha eliminato il region proposal non addestrato inserendolo direttamente nella rete, effettuando un brancing della rete con una parte di Region Proposal Network che  fornisce il riconoscimento di oggetto e il bounding box, quest'ultimo viene inserito nel roi pooling e viene poi eseguita la classificazione e il bounding box corretto.

slide 26: la region proposal network non prende punti a random, usa delle ancore che sono dei punti candidati dove poter iniziare a creare le bounding box.
è più semplice iniziare da dei punti candidati piuttosto che da una pagina vuota.
Questa è l'idea dietro altre famiglie di detector come i single shot detector.

slide 27: L'idea di yolo si basa sulle ancore.
divide l'immagine in 7x7 celle, in ogni cella yolo inizializza un insieme di candidati (le ancore), in genere un bounding box verticale e uno orizzontale, quindi 98 candidati per ogni immagine.
Affina quindi il bounding box e stima la classe.


slide 39: effettuo quindi prima la segmentazione e poi l'object detection, e li metto insieme.

