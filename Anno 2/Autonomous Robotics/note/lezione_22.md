# lezione\_22

slide 4: fastslam è un algoritmo basato sulle particelle basato su rao-blackwell.
la posa viene stimata tramite un filtro particellare, e la mappa è condizionata dalla sua particella.
ogni elemento di mappa ha il suo filtro, e ogni particella ha la sua mappa.
ci sono un numero di filtri pari al numero di elementi sulla mappa.

non è presente un filtro di kalman per aggiornare la mappa, la mappa è formata da una griglia e si aggiorna un filtro che vedremo un seguito.

slide 6: gmapping è molto vecchio, era il filtro di riferimento di ROS 1, in ROS 2 ci sono più scelte, ma al momento vedremo questo.

slide 7: l'idea di Gmapping è che per fare la stima a priori non utilizziamo soltanto un modello di moto, ma un modello che si basa sulle particelle.

Lo scan matching significa associare due insiemi di dati omogenei (due scan).
Tramite questo associa le varie mappe scannerizzate in tempi diversi per effettuare la stima a priori della posa.

slide 8: effettua il resampling quando il numero N_{eff} (numero efficace di particelle) che non ho capito cosa sia, è minore di un certo valore T
C'è un errore nella formula $N_{eff} = \frac 1{N\sum(\tilde w_i)^2}$
Ed in realtà $N_{eff} \in [1, N]$

slide 12: questa è la probabilità con cui il robot si trovi su quella particella.

slide 15: una mappa nel mondo ros è in formato png, ogni pixel è una cella diversa.
la risoluzione 0.1 è la dimensione in metri della cella.
occupied_thresh indica la soglia per cui decidiamo se una cella della griglia è libera o occupata.

slide 18: in ros, dal punto di vista della localizzazione, ci sono 4 sistemi di riferimento:
base link è solidale a boh.
odom è dove si trova il robot secondo l'odometria, veloce ma tende a driftare.
map, da quello che ho capito, è la mappa creata in gmapping, quindi la mappa su cui lavoriamo.
earth è il sistema di riferimento solidale rispetto alla terra, ma non si usa praticamente mai.

vari algoritmi lavorano a livelli diversi, è importante quindi conoscerne le differenze

slide 20:
throttle_scans dice se esaminare tutte le scansioni laser oppure saltarne alcune. Per motivi che vedremo dopo nell'esempio questo aggiornamento non ci sarà e l'aggiornamento sarà legato allo spostamento.

slide 21:
i 4 parametri "s" definiscono il rumore nei modelli di moto, come succede spesso non c'è coerenza sul come un parametro è utilizzato nei segmenti di codice e sul come è descritto nella documentazione. In questo caso "r" e "t" vengono scambiati e c'è un po' di incoerenza.

linear e angular update indica la soglia di spostamento dopo cui lo scan matching viene effettuato.

slide 23-24: non vedremo cartographer al momento perché è basato su teoria che vedremo in futuro (graph slam).
Mantiene comunque il matching.

slide 25: Non si tratta quindi di filtraggio come il particle filter, ma è un problema di ottimizzazione.

da slide 26 in poi argomenti extra, affidarsi anche al file gmapping_didattico.pdf.