# lezione\_6

## Pacco 006_3

slide 11: si assume che il robot sia puntiforme, nella realtà non lo è quindi per risolvere problemi con le collisioni si dilata la dimensione degli ostacoli.

slide 14: le mappe topologiche non le useremo. Vanno molto bene per pianificare un percorso ma non sappiamo i dettagli della mappa e non possiamo localizzarci.

## Pacco 006_2

slide 4: dopo il signal treatment abbiamo il nostro array di numeri, fare features extraction consiste nel calcolare la formula degli ostacoli individuati.

slide 11: si preferisce rappresentare la retta con le coordinate polari, perché mi baso sul sistema di riferimento dell'origine ed è quindi più robusto. Anche i punti usano le coordinate polari.

slide 12: assumiamo che ogni punto sia rumoroso

slide 16: le formule ci dicono quali sono i parametri $\alpha, r$ che rappresentano al meglio la retta data dall'insieme dei punti.

## Pacco 006_1

slide 22: la matrice è diagonale a due blocchi perché gli errori sono indipendenti tra loro, questa ipotesi non è corretta nella realtà ma è abbastanza buona da poterla applicare.

slide 26: - calcola la retta tra il primo e ultimo campione
- trova tra gli altri il punto più lontano, se è sopra una soglia spezza la retta in 2, passando per un punto
- ripete fino a che non restano soltanto punti sotto la soglia
- fonde le rette molto vicine tra loro
Il problema di questo algoritmo è che non associa i punti ad ogni retta, ma se ci servono solo le rette allora è un buon algoritmo.

slide 27: non ho capito niente. rappresento i punti come sinusoidi e trovo dove intersecano?

slide 29: anche con questo algoritmo non si capiscono quali punti appartengono ad una retta, ma trovo soltanto la retta. per capire quali punti la compongono devo memorizzarli per ogni intersezione, cosa utile da fare perché questo algoritmo trova solo una retta alla volta, posso quindi togliere i punti della retta individuata e ritentare per trovarne altre.

slide 31: prendo 2 punti a caso e calcolo la retta, calcolo poi le distanze di tutti gli altri punti dalla retta e quelli sotto la soglia ne appartengono. ripeto questo algoritmo un certo numero di volte o finché non trovo un insieme di punti abbastanza grande. Rimuovo poi i punti della retta individuata e ripeto fino a che non finisco i punti.

## Pacco 006_2_bayes

slide 10: nel contesto stocastico facciamo un'ipotesi markoviana, della storia passata ci interessa soltanto l'ultimo stato.

slide 11: anche le misure hanno le proprietà di markov, sono un caso particolare di hidden markov model.

slide 12: l'ipotesi markoviana deriva dal fatto che lo stato x_t+1 deriva solo da x_t e u_t+1 e non ci sono altri elementi entranti.
ogni volta che ho un problema di hmm, il filtro di bayes potrebbe essere una possibile soluzione.

slide 14: la belief a priori non ha il condizionamento sull'ultima misura della z

slide 15: il filtro di bayes è un algoritmo iterativo che prende in input la pdf della posizione e le ultime misure esterocettive e propriocettive, integro nello spazio delle pose ($\Omega$) al variare della posa preccedente x_t-1 la belief a posteriore moltiplicata per la state transition probability.
poi posso utilizzare z per aggiustare la posizione.
$\eta$ fattore di normalizzazione.
Questo algoritmo non si può implementare perché il numero delle pose è infinito, non concluderò mai il ciclo for, dobbiamo quindi discretizzare il cubo (lo spazio).
