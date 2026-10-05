# lezione\_2

Lavoreremo quasi solamente con robot su ruote, ma alcuni algoritmi sono utilizzabili anche con droni.
Ci sono numerose limitazioni, come la necessità di fare manovre per parcheggiare ed evitare ostacoli.

slide 6: ipotesi teoriche sul funzionamento della ruota:
velocità lineare: $v = \omega \cdot r$
raggio sterzata: $r = \frac v\omega$
diciamo che la posa è un vettore, anche se appartiene ad una varietà. per noi non è importante la differenza, lo diventa se lavoriamo con i droni.

slide 8: non avendo lo sterzo, le ruote per girare slittano

slide 10: progettare un sistema differenziale si può adattare agli altri 2 tipi

slide 12: la posa del robot è data da $x,y,\theta$
v ha un impatto immediato rispetto alle posizioni, infatti derivando la distanza tra il robot e il riferimento del world rispetto al tempo trovo la velocità.
avendo la posizione iniziale e conoscendo la storia degli input [v, w] posso integrare le equazioni differenziali e sapere dove mi trovo.

$$\begin{cases} \dot x = v\cos(\theta) \\ \dot y = v\sin(\theta)\\ \dot \theta = \omega\end{cases}$$

nessuna delle ipotesi nella slide 6 (inserisci link al capitolo) è vera, perché devo considerare il rumore. posso stimare la possa e poi correggerla basandomi sui sensori.

slide 15: runge-kutta di secondo ordine servono ad __approssimare__ ill modello nell'ambiente digitale.
Per calcolare lo spostamento futuro (t+1) di x e y calcolo la metà del cambiamento dell'angolo $\theta$, tutto moltiplicato per il tempo di stazionamento T.

slide 16: con il metodo di eulero uso solo i valori correnti. v e w nel tempo di stazionamento sono costanti, nella realtà non è cosi, sono quindi approssimati anche loro.

slide 18: nel periodo di controllo il modello si muove su un arco di circonferenza.
se assumo che il modello differenziale è esatto, allora il velocity motion model è corretto.
come detto prima assumo che v e w siano costanti nel tempo tra x e x', calcolo il raggio dell'arco di circonferenza con $r=\frac vw$

slide 19: il modello risultante è esatto, non ho quindi problemi legati alle approssimazioni.
a differenza di runge-kutta che prova a calcolare la configurazione futura, questo modello prende i dati della configurazione passata e calcola quella presente.
ci interessa studiare la posa che abbiamo adesso, basandoci sui segnali di controllo inviati all'istante precedente.

///dalla slide 23 non serve studiare, ma sono concetti utili da vedere, aggiungere al file chiamato "zz. Argomenti extra"
