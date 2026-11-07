# lezione\_19

/////AR_Lec_019_1_SLAM_ProblemFormulation.pdf

SLAM = non si ha l'ipotesi che la mappa sia nota

il robot ha bisogno di confrontare l'insieme delle pose,che gli sono state fornite, con la posa reale.

odometria: stima di quanto si è spostato il robot in due momenti diversi (quanta strada ha percorso in relazione alla terna $(x,y,z)$)

Dentro lo slam le informazioni sono ancora di tipo metrico.

slide 6: si dice che il sistema mondo all'accensione comincia con il sistema di riferimento personale a $t=0$.

L'ellisse intorno al ppunto m_0 rappresenta l'incertezza di misura.

slide 8: l'incertezza di m_1 e m_2 è maggiore, questo perché si sommano le incertezze della sua posa e quella di misura.

differenze con problema di localizzazione:
1. non si ha la mappa
2. ...

slide 12: ogni m_i indica il beacon i-esimo nella mappa.
Si assume che la mappa sia statica, cioè le posizioni degli elementi non cambiano.

slide 16:  il parametro m influenza le pose, ma non è influenzato da nulla

FRONTEND: livello di gestione dei sensori
BACKEND: pose di stime della mappa che lavora in maniera indipendente rispetto all'elaborazione dei dati e generazione della mappa.

/////AR_Lec_019_2_SLAM-EKF_SLAM.pdf
