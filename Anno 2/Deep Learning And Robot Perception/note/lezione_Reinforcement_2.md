slide 4: la parte "given the model" è in realtà la parte di "value iteration"

slide 9: non abbiamo bisogno di labels perché l'agente impara sulla propria esperienza.

slide 10: ha fatto l'esempio della mossa 37 di alphaGo nel 2016/17, dove la mossa che all'inizio è sembrata stupida ha portato alla vittoria di alphago

slide 11: possiamo modificare la epsilon durante l'addestramento, nei primi step preferiamo esplorare per poi abbassare gradualmente la epsilon e passare all'esploiting.

slide 12: possiamo sfruttare anche l'esperienza collezionata da altri agenti.
La differenza tra on e off policy, nel caso di on policy quando cambiamo la policy dobbiamo scartare tutti i dati precedenti, perché erano collezionati dalla vecchia versione della policy (SARSA), ma non ho bisogno di strutture di dati complesse, uso solo quello che imparo in questo episodio.
Nella off policy sfrutto anche le informazioni degli episodi precedenti, rendendo l'addestrammento più stabile.

slide 16: prima valutiamo la policy con la bellman equation iterativamente, poi la miglioriamo rendendola greedy.

slide 19: una possibilità è il temporal difference learning, non abbiamo bisogno di aspettare perché non abbiamo il modello, qua impariamo dalle nostre deduzioni. 
siamo ancora in un contesto tabulare(non ho capito che significa).

slide 20: l'obiettivo è di addestrare v così che fitti lo stato.
da definizione v(s) è la media del target, se abbiamo tutto possiamo individuare v in un unico step con la bellman equation.
il  problema è che non conosciamo p, l'intuizione è quindi di calcolare la media. Non abbiamo le probabilità ma sfruttiamo la strategia di update per calcolare la media p, che convergerà pian piano al valore reale v.

slide 21: il nostro target si muove, rendendo complesso l'addestramento.

slide 27: è molto difficile riempire tabelle molto grandi, quindi si rimpiazzano con delle funzioni parametrizzate. 
