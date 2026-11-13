# lezione\_23

slide 4: le prime soluzioni di slam erano EKF, rao-blackwell è venuto dopo ed è stato applicato a gmapping.
rao-blackwell usa lo scan matching, che è un approccio diverso.

oggi vediamo un altro approccio ancora, il graph slam.

slide 5: l'obiettivo è di individuare una soluzione ottima, che racconti la migliore configurazione possibile tenendo conto le misurazioni che sono state raccolte.

slide 6: assumiamo di avere una sequenza di pose, arrivati alla posa 5 scopriamo di essere tornati alla stessa posa 2. possiamo sfruttare quindi questi loop e queste informazioni per stimare meglio la posa.

L'idea è collegare il dato propriocettivo (la freccia blu) che collega le pose, con il modello di moto.

slide 7: è in grado di fare una determinata misura in base agli elementi di mappa.
Da ogni posa il robot prende delle misure, possiamo quindi aggiungere un ulteriore arco che collega una posa ad un elemento di mappa.
è quindi presente un vincolo, o termine di errore, che rappresenta il modello di misura (o la misura?).
Se non diciamo all'algoritmo da dove è partito il robot, dato che ho solo dati relativi (u dice di quanto mi sono spostato, z dice la posizione relativa di una x con un elemento di mappa), non riuscirei a capire dove mi trovo veramente.
Aggiungere la posa iniziale vincola il grafo a partire da un punto determinato, è quindi presente un vincolo che fissa la libertà di movimento rigido (gauge freedom).

slide 8: il termine generico indicato con tau è la posa corrente.
La differenza tra dove siamo e dove prevederebbe il modello è l'errore associato all'arco.
dobbiamo minimizzare l'errore.
al successivo spostamento avrò una struttura simile alla precedente, con un nuovo errore che dipenderà dai valori scelti di x.
Negli archi di misura ho la stessa situazione, perché ho un valore stimato per m_1, ho un valore stimato per la posa, e nei modelli di misura, la funzione h applicato alla posa e a un modello di mappa mi dice quale misura dovrei ottenere.
La h(x_t,m) mi da un valore che devo confrontare con la z, dando quindi l'errore z_t - h(x_t, m), che devo sempre minimizzare.
Minimizzare tutti gli errori mi darà la soluzione del nostro problema di slam, in quanto ci darà il risultato con l'errore minore possibile.
Assumiamo che ogni singolo termine di errore sia gaussiano.
L'errore pesato per l'incertezza equivale alla distanza di mahalanobis (o come si chiama).

Si chiama graph slam perché è un problema di slam rappresentato tramite un grafo con del rumore.

slide 9: ogni molla sta in uno stato di equilibrio incompatibile con gli altri.
le molle applicano forze l'una sulle altre fino ad assestarsi e raggiungere un punto di equilibrio.

slide 10: una volta che abbiamo x-f e z-h, facciamo semplicemente la somma di tutti i termini.
Viene fuori J, un funzionale di costo, J^* è la funzione che minimizza il termine di errore.
La difficoltà è che f non è lineare, di conseguenza anche J non è lineare e può quindi avere più minimi locali.
Anche h è non lineare, stesso problema.
posso effettuare le sommatorie perché assumo indipendenza tra le misurazioni.

slide 10: la matrice di informazione è l'inversa della matrice di covarianza.
L'errore odometrico o di moto è la differenza tra la posa a un certo istante e il modello di moto.
L'errore di misura assume corrispondenze note (quando facciamo una misura sappiamo a quale elemento di mappa appartiene quella misura, in realtà dobbiamo determinarlo in qualche modo)

slide 12: il contesto generale viene chiamato "grafi a fattori" (factor graph), che sono grafi bipartiti (ci sono 2 classi di nodi, ogni arco collega un nodo di una classe a un nodo di un'altra classe). I nodi fattori sono quelli dove sono presenti i dati misurati.
I nodi tondi sono le pose o gli elementi di mappa.
in questo grafo phi_1 contiene il modello di moto, il fattore che sta tra x_1 e m_1 contiene il modello di misura.
è importante per la risoluzione il fatto che la struttura di questo grafo è sparsa.

slide 13: cerchiamo di minimizzare la probabilità congiunta.

da slide 17 in poi vengono da probabilistic robotics.

slide 23: inizializzo il modello, lo linearizzo, lo riduco eliminando gli elementi di mappa e lo risolvo.

slide 24: in termini di grafo ho 2 cammini per andare da x_1 a x_2, ho quello diretto con il suo modello, ma anche il cammino che passa per l'elemento di mappa.
Assorbo le informazioni di quel cammino nel legame tra x_1 e x_2, cancellando quindi un pezzo di storia (la riga m_1), arricchendo di contenuti l'interazione x_1 x_2.
m_3 è  un cammino da x_2 a x_3, ma anche da x_3 a x_4, ma anche da x_2 a x_4, si potenziano quindi i vari cammini, ma si aggiunge anche un altro link da x_2 a x_4.

La struttura dati si è ridotta quindi a un pose graph, che rappresenta solo le pose, ma l'errore si è articolato in quanto ho anche l'errore di z.

Sono legate coppie di pose che non sono in successione diretta, in quanto ci sono elementi di mappa che vedo da entrambe le pose.
