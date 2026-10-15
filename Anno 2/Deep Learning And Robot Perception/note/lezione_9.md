# lezione\_9

slide 4: vogliamo ovviamente che il modello abbia buone performance sui dati di test.

slide 6: con gli strumenti studiati fino ad ora possiamo effettuare il riconoscimento soltanto tramite l'associazione, classifichiamo le immagini come gatto solo se hanno le features simili a quelle dei dati forniti.
Se proviamo però a associare un gatto grigio e uno arancione, il match fallisce perché si tratta si di gatti, ma di elementi completamente diversi.
L'obiettivo di questi strumenti è infatti quello di associare più immagini dello stesso oggetto, non di oggetti diversi.

slide 7: non è robusto impostare a mano delle regole per il riconoscimento. Magari stiamo usando delle immagini che ritraggono il gatto da dietro, non riuscendo a intravedere il muso.
Se scriviamo delle regole a mano queste risulteranno quindi non robuste.
L'alternativa è quindi di far imparare al modello di machine learning quali sono le features più adatte per il compito specifico.

slide 8: nella pipeline abbiamo due punti in cui le informazioni sono predette o trasformate:
nel feature extraction (o features transformation) le features vengono trasformate, nel machine learning abbiamo sempre definito le features come fissate dal principio, ma nella computer vision sta alla rete neurale prendere l'immagine e trasformarla in informazioni che può utilizzare.
utilizzando un descriptor perdiamo tutte le informazioni presenti nell'immagine iniziale, e assumiamo che le informazioni fornite siano abbastanza da poter descrivere l'intera immagine.

slide 9: SIFT è abbastanza bravo da trasformare la matrice dell'immagine in un features space che sia abbastanza facile da separare linearmente con un linear classifier.
Non possiamo inventare un algoritmo di sift diverso per ogni problema, perché porta a un grosso spreco di tempo e risorse.
L'idea di SIFT è che funziona bene per molti compiti generici.

slide 11: assumiamo di poter definire le features, invece che addestrarle.

slide 12: se compariamo i valori nella stessa posizione, avremo che non combaciano per niente. Paradossalmente l'immagine della nave risulta più simile in quanto ci sono più pixel blu nelle stesse posizioni.

slide 13: il nearest neighbor classifier avrà delle pessime performance.

slide 14: per ogni tipo di input abbiamo bisogno di rappresentazione, qualcosa che trasforma gli input in qualcosa che sia più robusto per la classificazione.
Abbiamo bisogno di qualcosa che dopo applicata la trasformazione distribuisce i punti linearmente in un modo che sia facilmente separabile.
voglio che sia anche robusto ai cambiamenti dei pixel, applicando delle trasformazioni lineari o non nell'immagine devo avere un features space abbastanza simile così da avere immagini della stessa categoria vicine e immagini di categorie diverse lontane da queste.

slide 15-16: SIFT non è corretto, perché è progettato per estrarre keypoints, non abbiamo una quantità fissa di features estratte dall'immagine.
Un algoritmo che osserva l'immagine nell'interezza e crea un vettore di features a partire dall'immagine completa è HOG.
il risultato di HOG può essere dato direttamente ad un classifier per classificare l'immagine.
HOG considera celle 4x4 e per ogni cella calcola il numero di … non ho capito…. e calcola la direzione di quella cella con il gradiente????
Questo viene ripetuto per ogni cella nell'immagine.
Ogni cella viene poi raggruppata in blocchi di 2x2 celle.
in hog le celle si sovrappongono di 1 pixel.
///// INSERIRE IMMAGINE DI ESEMPIO DI PIXEL, CELLE E BLOCCO

dato che le celle sono composte da un istogramma 4x4??? i blocchi saranno composti da un istogramma 2x2????

in totale l'istogramma contiene un vettore di dimensione 1764.

slide 17-18: se cambiamo il colore dell'auto, hog sarà lo stesso perché la differenza tra auto e sfondo è comunque presente e quindi la descrizione dell'immagine sarà simile.
ovviamente il descriptor deve dipendere dal problema che devo affrontare.
esempio: Se voglio che il modello differenzi la mia macchina da quella di un altra persona che ha la macchina dello stesso modello con colore diverso, hog non sarebbe in grado di distinguerle in quanto ignora la differenza di colore.

slide 19: un buon descriptor può fare la differenza nelle performance della classificazione, ma usare features fisse ha delle limitazioni.

slide 22: se la parte di features extraction è addestrabile posso ottenere un ulteriore miglioramento nelle performance, e posso anche addestrare in base al problema che devo risolvere.

il 95% dei parametri di una nn nel deep learning è la parte che si occupa di features extraction.

slide 25: in una rete a 2 layer il primo hidden layer è quello che si occupa di estrarre le features (representation learning)? non ho capito.

slide 28: nel deep learning ho bisogno di più di 2 layer (cita il teorema di approssimazione universale), il teorema dice che posso utilizzare il primo hidden layer per ricavare qualsiasi feature complessa e poi utilizzare il secondo per la classificazione.
Nella backpropagation il delta di quel layer dipende dal delta del layer prima? dopo? boh. il bias è delta?

slide 29: se non ho una non linearità avere più layer collassa in un unico layer lineare.

slide 31: c'è un video che mostra la separazione grazie alla ReLU.

slide 36: questa modalità di rappresentazione ovviamente ha dei limiti.

slide 39: aggiungere più dati quando la descrizione non è fatta bene non porta a risultati migliori.
Aggiungere più dati da beneficio quando addestriamo il features extractor.
Si possono applicare combinazioni di trasformazioni random alle varie immagini di input quando addestriamo il features extractor, così da fornirgli più esempi su cui addestrare.

slide 40: se mostriamo l'accuracy come funzione in base ai sample, la CNN è molto migliore rispetto alle altre strategie, perché parte da una accuratezza migliore e riesce a crescere molto di più rispetto alle altre.

slide 42: siamo quindi in grado di distinguere le due parti di rete neurale, quella che si occupa di rappresentazione e quella di classificazione.
Possiamo riutilizzare i layer di rappresentazione anche per task diversi, addestrando soltanto il classifier in base al problema.
Questa tecnica si chiama transfer learning.
/// inserire immagine di esempio transfer learning, diagramma a blocchi in cui abbiamo x entrante nel primo blocco F =(uguale con 3 linee) phi con scritto "frozen", una freccia che va verso il vecchio classifier cancellato con uscite T, S e un'altra freccia che va al nuovo classifier con uscite C,B.

slide 47: l'idea è di rendere la rete abbastanza grande da andare in overfitting, per poi utilizzare tecniche di regolarizzazione per sistemare la rete.
Creiamo una rete enorme così da avere una completa potenza di rappresentazione, per poi contenerla e utilizzarla con dei constraints di regularization.

Se siamo in underfitting dobbiamo aumentare la dimensione della rete, se siamo in overfitting dobbiamo effettuare la regolarizzazione. Il tutto fino a che non raggiungiamo un risultato accettabile.
Ci servono delle dashboard in realtime che ci mostrino il training, validation e test error così da poterlo analizzare mentre la rete viene addestrata.

slide 51-52-53: da ricordare che di solito si effettua lo zero centering e, se necessario, la standardizzazione. pca e whitening non si fanno molto spesso.

slide 55: con v < 1 se aggiungiamo troppi layer si ha il problema del vanishing gradient, dove nella backpropagation attraversando i layer il gradiente diminuisce sempre di più fino a diventare 0.
con v> 1 si ha il problema inverso, il gradiente aumenta progressivamente fino ad esplodere, questo problema è però più semplice da risolvere in quanto ci basta fare clipping sul gradiente per evitare che diventi troppo grande.
si tende comunque a preferire un valore di v simile a 1, anche se è difficile da poter ottenere.

slide 58: per affrontare il problema di v si possono anche modificare le activation function, dato che la derivata di queste è quella che causa il valore di v.
il problema della sigmoide e della tanh è la saturazione, in quanto ci fa perdere informazioni. Quando la rete ottiene un numero alto, vuol dire che quel numero è importante e saturandolo non gli diamo la giusta importanza.

//// inserire immagine di esempio di un singolo neurone, con 3 input in ingresso, sopra al neurone la formula $w^T h_{l-1} + b$, che si connette ad un box con la activation function (generica non specificata). nel neurone entra un'altra freccia dal basso con l'immagine di un corner, perché nell'esempio il neurone dovrebbe occuparsi di identificare i corner di un'immagine.

abbiamo 3 variazioni di ReLU: Leaky-ReLU, P-ReLU, GeLU
//// inserisci grafici che mostrano le funzioni descritte

il parametro alpha in Leaky-ReLU indica quanto deve scendere la parte negativa, ed è un parametro che dobbiamo impostare. serve perché per ogni neurone che fornisce un valore negativo ReLU fornisce sempre 0, e calcolare il gradiente non porta nessun risultato, che di per se non è una brutta cosa dato che possiamo utilizzarli per spegnere alcuni neuroni che non ci servono, ma alcune volte non vogliamo utilizzare questa tecnica e ci possono servire dei valori negativi per evitare la morte di troppi neuroni.

la slope in P-ReLU è un parametro di ottimizzazione, quindi può essere addestrato aggiungendo complessità alla rete.

GeLU viene utilizzato nelle reti transformer e si è rilevato abbastanza utile per reti molto grandi.

nella maggior parte dei casi utilizzeremo ReLU base, GeLU per le reti transformer, le altre non si vedono molto spesso.

slide 61-62-63: nelle reti neurali non possiamo impostare tutto a 0, perché al primo passo la loss sarebbe enorme avendo come primo risultato sempre 0 e l'aggiornamento aggiornerà tutti i neuroni allo stesso modo. per rompere la simmetria l'inizializzazione della rete neurale deve essere random.

slide 64: bisogna compensare per la varianza impostando sigma quadro. in questo modo la varianza resta la stessa.

slide 66: spread compensation

slide 69: calcoliamo la media e la deviazione standard, centriamo sullo 0 e normalizziamo. la batch normalization ci da due parametri, gamme e beta, che possono essere addestrati. 