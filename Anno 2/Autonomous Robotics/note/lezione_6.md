# lezione_6

2026-10-05

slide 15-16: questo schema è solo concettuale (non si può implementare) perché è impossibile calcolare tutte le possibili pose nello spazio.
Assumendo infatti che il nostro spazio delle pose sia il pavimento, $x_t$ è qualsiasi punto del pavimento, con aggiunto l'angolo $\theta$. Dovremo quindi esplorare tutti gli infiniti punti dello spazio.
Come se non bastasse al punto 2 bisogna pure calcolare un integrale. Se fossero note le forme analitiche della state transition probability e della beliefe si potrebbe calcolare l'integrale in forma chiusa.
Queste funzioni non sono però note in forma chiusa, e bisogna quindi esplorare tutti i punti.

slide 18: dobbiamo modellare il legame tra $x_t$ e $z_t$, e il legame tra $x_{t-1}, u_t, x_t$

slide 20: la probabilità è 0.8 perché non sono sicuro che la spinta applicata funzionerà, avrò quindi uno 0.2 di probabilità che resti chiusa dopo aver effettuato la spinta.

slide 21: sto usando il filtro per capire il valore reale della variabile.
L'integrale diventa una sommatoria, la probabilità di avere un x_1 generico eseguendo una certa azione è dato dalla somma dei possibili stati precedenti moltiplicati per le probabilità di quegli stati, non ho capito.
Il dato propriocettivo è fissato, poiché non faccio nulla lo stato della porta non cambia.
Il nostro modello prova a capire le implicazioni di quel comando (?)

slide 22: Se non facciamo nulla, la probabilità che abbiamo calcolato, che sarebbe la prior, è data dal fatto che abbiamo creato il modello assumendo che la porta non avrebbe cambiato stato da sola, se così fosse avrei ottenuto probabilità diverse.

slide 23: passiamo poi dalla prior alla posterior. Per ogni possibile stato al passo 1 prendiamo ogni possibile theta e lo moltiplichiamo per la belief che abbiamo calcolato.
La probabilità che la porta sia aperta è eta (che ancora non sappiamo) per la probabilità di aver misurato la porta aperta (che diamo per sicura visto che la misuriamo) moltiplicato per la belief a priori che la porta sia aperta.

slide 24: Bisogna però calcolare il fattore di normalizzazione per fare in modo che la somma delle probabilità sia 1.

slide 25: abbiamo dovuto fare molti calcoli con un modellino "banale", avevamo 2 variabili di stato, due valori esterocettivi e due valori propriocettivi.
Non è saggio assumere che la porta sia aperta, con un errore quasi del 2% non è accettabile, si dovrebbe seguire il paradigma sei-sigma.
si chiama sei-sigma perché la coda a sei sigma di una gaussiana ha quella probabilità.

slide 27: abbiamo quindi visto che il filtro di bayes è un ciclo in cui si calcola la belief a priori e la belief a posteriori in continuazione.
$\eta$ è il nostro 1/p(y).

slide 28: nel primo passaggio ho applicato il teorema di bayes scambiando x_t e z_t.
Se vale l'ipotesi markoviana di stato completo la verosimiglianza di una certa misura dipende solo dallo stato precedente, non da tutti gli stati, rimane quindi la verosimiglianza di quella misura in base alla posa.
p(x_t | z_1:t-1, u_1:t) è la belief a priori, ovvero la riga 3 dell'algoritmo del filtro di bayes.
Quindi, ciò che so all'istante t è tutto quello di cui ho bisogno, perché delle misure precedenti non mi serve nulla.

slide 29: per dimostrare il filtro di bayes applico il teorema della probabilità totale.
dato che sto lavorando con l'ipotesi markoviana di stato completo, la dipendenza dagli z non conta (in rosso), e la posso buttare, lasciando solo la state transition probability.
u_t è quello che mi porta da x_t-1 a x_t, la probabilità dello stato precedente non può dipendere da quello che  mi porta allo stato successivo, lo posso quindi togliere lasciando u_1:t-1.

slide 30: se è tutto gaussiano, non devo calcolare sempre la belief, perché mi basta aggiornare il valore medio e la varianza.

slide 31: ricordo che l'ipotesi markoviana non vale nella realtà. 