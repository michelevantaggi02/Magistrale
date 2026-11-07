# lezione\_20

Limiti di kalman:
- costo computazionale (vettore delle incognite)
- fa solo position tracking

obiettivo di rao-blackwell: si vuole creare un filtro più efficiente, andando ad aggiornare separatamente la parte legata ad $x$ (la posa) ed $m$ (gli elementi della mappa)

il filtro di kalman ha dimensione pari a quelle della mappa

slide 14: il vero vantaggio computazionale di RB sta proprio nella produttoria (ha un costo lineare in base al numero di filtri)

slide 15: ogni particella tiene memorie di tutte le pose visistate, oltre a quella corrente.

il modello di evoluzione della mappa è l'identità, quindi la prior e posterior al passo precedente comandano sotto l'ipotesi di staticità della mappa (mi calcolo solo la posterior ad esempio, non ho capito bene).
dire che la mappa non cambi vuol dire che non ci sono elementi mobili nella mappa.

slide 17: passo 4 non è proprio un update delle misure

PROBLEMA DEL PARTICLE DEPRIVATION

slide 21: $z_{i,t} - h(x_t^k, \hat m_{j,t-1}^k)$ sia z che h devono essere rispetto lo stesso sistema di riferimento.
z è l'errore tra la retta che ho trovato (z_i, t) e quelllo ceh avrei dovuto vedere (h(\cdot))
la funzione h prende le coordinate nel sistema di riferimento globale e le converte in quelle del sistema di riferimento z_{i,t} (rototraslazione), quesot perché è tutto rappresentato rispetto al sistema z, cioè laser.

slide 24: le rette si localizzano bene ma non ci permettono navigazione.
GMapping invece consente la navigazione.
In kalman, per far evolvere una mappa basata su rette... boh