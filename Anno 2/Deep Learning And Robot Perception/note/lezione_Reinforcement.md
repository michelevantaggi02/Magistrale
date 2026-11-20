cap 1.2: indica quanto buono è uno stato secondo la nostra funzione.

la value function indica il ritorno atteso da uno stato secondo una data policy.

//// immagine esempio: griglia 4x4, voglio calcolare il return dello stato s_1 che è rappresentato dalla cella in basso a sinistra. mi muovo con una freccia di 1 in alto, poi 1 a detra, poi 2 in alto fino al goal state. in un altra occasione mi muovo prima a destra poi in alto poi 2 volte a destra e 2 volte in alto (non c'è scritto goal state). ci sono dei -1  in ogni cella esplorata ma non ho capito perché.

La policy era però di andare sempre in alto, ma dato che è stocastica ho dei comportamenti inattesi??

La value function di uno stato è il valore atteso su tutti i possibili sample di traiettorie che posso ottenere dalla funzione di transizione.

cambio la policy per rendere la value function la più alta possibile per ogni stato del mio problema.

la mega probabilità modella la probabilità della serie di passi che servono per raggiungere il risultato a partire dallo stato s.
ovvero la probabilità che tutti quegli stati, azioni e reward hanno a partire dallo stato iniziale s.

applicando la regola di markov e la regola della catena abbiamo che $\sum_{traj} g_t$ (secondo step della mega formula non ho voglia di scrivere) ho scomposto il value in bohhhhh.

al quarto step cambio il modo con cui esprimo g_t in (r_{t+1} + \gamma g_{t+1}) lasciando il resto invariato.

da s_t mi posso muovere in s_{t+1} = s_1 oppure s_2 oppure s_3, e questo è stocastico dipende dalla state transition probability.

lo step 5 è conveniente perché posso tirare fuori la somma di r_{t+1} e anche le altre probabilità che non dipendono da s_{t+1} (quindi le probabilità che non dipendono dalla prossima traiettoria????)

////fai attenzione agli step ricontrolla per bene le formule, sto perdendo il conto delle righe e tutto il resto.

l'espressione finale si chiama equazione di bellman per la state value function.

il valore di uno stato è composto di 2 parti:
1. la moltiplicazione della probabilità per r (immediate reward)
2. la moltiplicazione della probabilità per il valore del prossimo stato (return from the future)

la action value function è una funzione dello stato e dell'azione.
prendiamo il valore atteso della policy, avendo lo stato s e l'azione a.

nel reinforcement learning è più semplice lavorare con la action value function.

selezioniamo l'azione solo dallo stato iniziale, le azioni successive devono comunque essere prese dalla policy.
Il motivo per cui lavorare con q invece che con t nonostante siano simili lo vedremo in futuro.

cap 1.2.2:

//// immagine di esempio è la figura 1.10 del pdf.
assumiamo che dal primo calcolo che il mondo è deterministico e la policy pure. Questo significa che la probabilità \pi(a=RIGHT | S_3) = 1, \pi(a \noteq RIGHT | S_3) = 0, P(S_4, r=1 | S_3, RIGHT) = 1, P(S\noteq S_4, r \noteq 1 | S_3, RIGHT) = 0.

$v_\pi(S_1) = 1 \cdot 1 \cdot[0 + \gamma \cdot v_\pi(S_3) = 0 + \gamma v_\pi(S_3)$ 
$v_\pi(S_2) = 1 + \gamma v_\pi(S_4)$
ecc...
usiamo queste equazioni per trovare i valori di tutti gli stati.

considerando invece il mondo stocastico della figura 1.11

se calcoliamo di nuovo abbiamo:
$v_\pi(s_1) = 0.4[0 + \gamma v_\pi(s_3)] + 0.5[-1 + \gamma v_\pi(s_2)]$
c'è il 50% di probabilità di andare in una o nell'altra direzione.

quello che cambia è l'azione verso il prossimo stato, devo quindi sommare 2 direzioni diverse.

se risolviamo di nuovo le equazioni avremo che v_\pi(s_1) = 8.5$, che è meno del valore che abbiamo nel mondo deterministico, perché ci da una possibilità di andare nello stato con reward -1 (da quello che ho capito è questo il motivo per cui si abbassa = 8.5$, che è meno del valore che abbiamo nel mondo deterministico, perché ci da una possibilità di andare nello stato con reward -1 (da quello che ho capito è questo il motivo per cui si abbassa))

cap 1.2.3:
formula in versione vettoriale per calcolare tutti gli stati dello spazio degli stati S.

cap 1.2.4:
se k tende a infinito avremo che v_k tenderà alla soluzione in forma chiusa

cap 2:

DEFINIZIONE DELLA POLICY OTTIMALE:
una policy \pi^* è ottima se v_{\pi^*}(s) \geq v_\pi(s), \forall s \in S e per ogni altra policy \pi \in \Pi(s)
è quindi ottima se la state value function di quella policy è maggiore per tutti gli stati di tutte le altre possibili policy.
dobbiamo trovare queste 3 cose:
- existence: 
- uniqueness:
- algorithm: 
Per questo introduciamo la bellman optimality equation (BOE)
v(s) = max_{\pi(s) \in \Pi(s)} \sum_a \..... formula 2.1

cap 2.1:
formula vettoriale

la bellman optimality equation è una funzione di v con risultato v, è quindi una mappa non lineare tra v e se stessa

cap 2.2:
fixed point: data una funzione f(v) dove (condizione) un punto v^* viene chiamato fixed point quando la funzione valutata in quel punto è quel punto stesso.
contraction mapping: data una funzione f(v), f è una contraction mapping se esiste \gamma \in (0,1) tale che: $||f(v_1) - f(v_2)|| \leq \gamma ||v_1 - v_2||$
è un modo matematico per dire che la funzione contrae gli intervalli, prende un intervallo nel dominio e lo rende più piccolo nel codominio.

teorema contraction mapping:
per ogni funzione f(v), dove f mappa R a se stesso, se f è una contraction mapping, allora:
- existence: esiste un fixed point v^* tale che f(v^*) = v^*
- uniqueness: v^* è unico
- algorithm: v_{k+1} = f(v) allora v_k \to  v^* per k \to \infty \forall v_0.

teorema: la BOE è una contraption mapping, non lo dimostreremo.

per trovare il fixed point mi basta utilizzare la soluzione iterativa del boe.

una volta raggiungo v^* possiamo calcolare la policy ottimale sostituendo v^* nella BOE:
$\pi^* = argmax_{\pi \in \Pi}(r_\pi + \gamma P_\pi v^*)$
possiamo ottenere la policy ottima usando una strategia greedy.

 
