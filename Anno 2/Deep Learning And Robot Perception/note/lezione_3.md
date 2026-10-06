# lezione\_3

introduzione: Nel deep learning abbiamo solo i dati grezzi del segnale, a differenza del machine learning dove le features erano già fissate. Per i tipi di problemi che andremo a risolvere è meglio avere una rete neurale a fare il lavoro di estrazione delle features.

slide 5: Nessuno ti dice come le immagini sono traslate e ruotate tra loro. Dobbiamo quindi addestrare un modello in grado di estrarre le features (gli elementi in comune) e di associarle tra immagini diverse così da poterle accoppiare. In questo modo riusciamo a capire in che modo è avvenuto il cambiamento di posa degli elementi.

///// INSERIRE IMMAGINE DI ESEMPIO, CASETTA STILIZZATA CHE SI SPOSTA DAL LATO DESTRO AL SINISTRO DELL'IMMAGINE, CON UN CERCHIO SULLA PUNTA DEL TETTO

Devo riconoscere lo stesso punto nelle 2 immagini diverse, per poi calcolare lo spostamento.

slide 6: per stimare la traiettoria di un robot bisogna analizzare i diversi frame forniti dalla telecamera

slide 8: non possiamo utilizzare in generale i singoli pixel, perché specialmente in scene con colori piatti ci sono troppi pixel simili

slide 9-10: dobbiamo quindi individuare pixel particolari, inusuali, e scartare quelli presenti

slide 10: Il detector deve individuare lo stesso punto su immagini diverse, indipendentemente da cambiamenti di posizione, luminosità o blur. Il descriptor assegna una descrizione che sia univoca per quel punto.

//// INSERIRE STESSA IMMAGINE CASETTE DI PRIMA, CON PIÙ PUNTI CON UNA FRECCIA CHE PORTA AD UN VETTORE CHE RAPPRESENTA L'ARRAY FORNITO DAL DESCRIPTOR (ASTRATTO, GENERICO)

Analizzo i vettori e, se il descriptor è fatto bene, posso compararli e individuare quello più simile tra le 2 immagini.

Ovviamente bisogna considerare che tra le due immagini ci sono cambiamenti di luminosità, rotazione, scala, ecc..

slide 14: Le flat region sono impossibili da analizzare, perché non ci sono elementi particolari che possono essere presi in considerazione, su un'area abbastanza grande con una flat region ogni pixel potrebbe essere quello giusto, e questo non va bene.

Lo stesso discorso vale per gli edges, dato che lungo la stessa linea si possono avere più aree uguali.

Per il corner è invece più difficile trovare delle aree duplicate.

//// INSERIRE SEMPRE IMMAGINE CASETTE BASE (SENZA I VETTORI), DOVE SI FA UN ESEMPIO DI CORNER, FLAT E EDGE, PRENDENDO PUNTI DELL'IMMAGINE E CREANDO UN EFFETTO DI INGRANDIMENTO SUL QUADRATINO ANALIZZATO.

slide 18: il problema è che consideriamo l'angolo solo localmente, pensiamo che sia unico ma globalmente potrebbe non esserlo.

slide 19: nota per me, trovare il nome dell'algoritmo.

slide 20: l'idea è di calcolare l'errore muovendo la finestra all'interno dell'area. la matrice di errore ci permette di distinguere flat, edge e corner region. Un punto ben localizzato ha l'errore che cresce velocemente.

slide 25: Ci serve una finestra più grande perché con un solo pixel non riusciamo a vedere lo shift del corner. Non è sufficiente guardare solo il pixel centrale, bisogna calcolare la finestra di errore.

slide 31: possiamo osservare gli autovalori e autovettori di C, avremo il minimo e massimo autovalore, se entrambi sono sopra ad una threshold avremo un corner.

slide 37: nella pratica non calcoliamo gli autovalori, ma la traccia e il determinante.

slide 42: abbiamo due gaussiane: una per il filtro e una per pesare l'impatto di ogni pixel nell'analisi.

slide 46: aumentando entrambe (come in pratica) avremo meno punti, ma più robusti

slide 53: il contrasto è presente anche dopo aver calcolato il gradiente.

Harris non è invariante alla scala, perché la finestra non riesce a registrare correttamente cambiamenti di scala.
