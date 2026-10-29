# lezione\_13

slide 2: Fino ad ora abbiamo gli strumenti per costruire un'architettura basata sulle cnn.
Negli anni sono uscite diverse tipologie di architetture standard che si sono rivelate particolarmente efficienti per risolvere determinati task, in genere quando andremo a costruire le nostre reti si parte da una di queste architetture standard e si adatta al nostro problema.

slide 5: Compararemo queste architetture sul task di riconoscimento di imagenet.

slide 8: output feature map size $(C_{in}, H_{in}, W_{in}) \to (C_{out}, \frac {H_{in} - k + 2P}5 + 1, \frac{W_{in} -K + 2P}5 -1$
number parameters: $C_{in} C_{out} kk + C_{out}$
number multiply-adds: $H_{out} W_{out} kk C_{in} C_{out}$

slide 10: $(C_{in} C_{out} \cdot 3 \cdot 3) 3 = C^2 27 < 48C^2$

slide 11: L'ultimo tensore è qualcosa del tipo: $(236,6,6)$, che se applicato il flatten diventa $(9216)$, applicando poi i layer densi diventa $4096 \cdot 9216 = 32M$, che hanno però meno moltiplicazioni MAC.

slide 12: l'idea è di utilizzare soltanto layer convoluzionali, lasciando come layer denso soltanto l'ultimo.
Per ogni layer definisco 4 parti, ogni parte ha il suo layer convoluzionale con filtri di dimensione diversa che guardano parti diversi dell'immagine e che possono girare in parallelo.

In questo caso abbiamo un problema di MAC ancora più accentuato rispetto a VGG.

slide 13: prima di dare ai kernel più grandi l'input, si passa per un layer convoluzionale 1x1 che abbassa il numero di valori in input. Così facendo il numero di MAC diminuisce sensibilmente (da 303M a 128M), e non perdiamo quasi nessuna informazione.

slide 14: il numero di parametri è molto più piccolo rispetto a VGG e alexnet, abbiamo un decimo dei MAC di VGG e l'accuratezza è molto meglio.

slide 16: dopo aver aggiunto moltissimi layer ci aspettavamo di avere più parametri, rischiando l'overfitting. Controintuitivamente però si è notato che anche l'errore di training stava aumentando.
Il problema era nel lato di ottimizzazione, perché come abbiamo visto le reti molto grandi hanno il problema del vanishing gradient. Ovviamente è presente anche l'exploding gradient ma come abbiamo visto si può affrontare clippando il gradiente.

slide 19: se consideriamo soltanto 20 layer di quella da 56, dovremo avere lo stesso identico risultato della rete da 20, perché la rete da 56 dovrebbe imparare __almeno__ le stesse cose.

slide 21: si chiama residual perché il risultato è la somma tra l'input e il blocco F(x).
Invece di avere la necessità di calcolare l'intera funzione dobbiamo solo calcolare i residui della funzione.

slide 23: è una scorciatoia perché ci permette di passare al blocco successivo mantenendo il gradiente alto.
Questa semplice somma ci permette quindi di non far sparire il gradiente, rendendo possibile l'addestramento di reti molto profonde.

slide 36: il blocco residuo ha accesso soltanto all'output del blocco precedente, ma non a quelli ancora prima, generando il problema di possibie perdita di feature.
Ogni blocco deve avere accesso a tutte le informazioni prodotte dai layer precedenti.

/// inserisci immagine: input matrice con 3 layer, connessa a un blocco convoluzione che fornisce 64 feature map, l'input si connette poi alle 64 prodotte come residuo così da avere per il prossimo blocco 67 mappe, il secondo blocco convoluzionale fornisce 64 feature map che si riconnette come residual block alle 67 mappe precedenti, fornendone quindi 131.

La concatenazione è come una scorciatoia, le 3 feature map delle 67 sono connesse alla scorciatoia (così come le 67 delle 131), permettendo al gradiente di accedere direttamente a tutte le mappe.
Mi porto dietro così più informazioni, mantenendo i vantaggi dei residual block.

slide 38: 