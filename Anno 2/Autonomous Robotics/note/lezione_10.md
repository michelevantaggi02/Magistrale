# lezione\_10

slide 4: è fatto in 3 parti:
1. ciclo che scorre tutte le possibili pose
2. belief a priori
3. belief a posteriori / passo di correzione
Noi lo utilizziamo per la localizzazione, ma approcci simili si usano per molti algoritmi che si basano su informazioni enterocettive e esterocettive.

slide 5: salta

slide 6: assumiamo di fare sampling secondo la curva rossa, i campioni quindi avranno quella distribuzione di probabilità.
Per l'uniforme mi aspetto 2 nuvolette di punti intorno ai due massimi.

slide 11: il particle filter riesce a generare campioni di variabile aleatoria pur non conoscendo esattamente la distribuzione.

slide 17: nell'histogram, il primo grafo ha una curva data dal velocity motion model.
Nel particle il primo grafo indica tutte le possibili pose del robot.
Dobbiamo trovare il modo con cui calcolare la posterior, e al passo successivo dobbiamo ricalcolare la distribuzione a priori (resampling)

slide 19: a parità di u, ogni particella si muove in modo leggermente diverso,  perché appartengono a un modello stocastico.

slide 20: la parte di generazione della posterior funziona utilizzando il fattore di importanza (peso della particella).
dopo aver calcolato tutti i fattori di importanza delle particelle si effettua il resampling.

slide 21: ogni particella ha bisogno di sampling perché si sposta, e di distribution computation perché il suo peso viene calcolato tramite una tecnica di questo tipo.

 slide 22: x calligrafico è l'insieme delle particelle.

slide 25: le particelle molto pesanti sono più probabili da prendere, quelle meno pesanti invece sono meno probabili.
Se ho a disposizione il peso di una particella, le metto tutte insieme, genero le variabili aleatorie uniformi e faccio il resampling.
se ho 100 particelle tutte uguali, la probabilità sarà uguale ma calcolare, ma al passo 4 dell'algoritmo il particle filter mi genera risultati leggermente diversi in quanto utilizzo un modello stocastico che aggiunge rumore.

slide da 27 a 30: materiale supplementare

slide 34-35: non svolgere, lezione futura.