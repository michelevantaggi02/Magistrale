slide 6: la state transition probability indica la probabilità  di cambiare stato.

slide 7: fissato un punto analizziamo la distribuzione e vediamo quanto è probabile quel punto (computazione di distribuzione).
(sampling) parto da un punto sull'asse y, calcolo la funzione inversa e trovo il campione che ci serve.
le distribuzioni in genere non sono gaussiane, useremo delle distribuzioni di riferimento del mondo reale. vedremo anche alcune distribuzioni teoriche gaussiane, ma non le useremo.

slide 8: aggiungo al segnale una componente di rumore gaussiano.
Mi serve il valore numerico della realizzazione della variabile aleatoria di interesse. per fare dist. comp. devo trovare valori di u_x validi per il modello, e poi cacolare v_x.
Se volessi usare lo stesso modello per fare sampling mi basta calcolare una realizzazione della gaussiana v_x e trovare la posa.

slide 10: Y = AX + V
C_y = A C_x A^T + C_V se c'è indipendennza.
F_x è un jacobiano.

slide 12: introduciamo i modelli stocastici perché il robot non riesce a rispettare i modelli deterministici. dobbiamo quindi riuscire a modellare l'incertezza.

slide 13: assumiamo che i comandi forniti al robot [v, w] non sono esatti, l'idea è quindi di "corrompere" questi comandi, non l'effetto del movimento.
assumiamo che le velocità siano corrotte con un rumore additivo (non necessariamente gaussiano) a media nulla.
La varianza deve essere proporzionale alla velocità a cui sto andando, se vado piano l'errore è più piccolo, se vado molto veloce è più probabile l'errore.


slide 18: quell'algoritmo di gauss funziona per il teorema del limite centrale.

slide 19: al punto (1,1) c'è la posa, gli altri punti sono pose calcolate con l'aggiunta del rumore.
nel caso in cui io abbia più "nuvolette" in zone diverse scelgo il cluster con più campioni (monte carlo).