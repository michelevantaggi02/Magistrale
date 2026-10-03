slide 3: l'obiettivo finale di molti compiti di computer vision è quello di calcolare la trasformazione delle immagini. è quindi il percorso inverso rispetto all'image processing

slide 5: la trasformazione di un'immagine prende la griglia rappresentante l'immagine e sposta o ruota, cambiando la posizione del contenuto. le tre famiglie di trasformazioni sono progressivamente più complesse, ed ognuna include la precedente.

slide 6: p' corrisponde al punto p dopo aver applicato le trasformazioni.

slide 7: le trasformazioni sono diverse dai filtri, i filtri cambiano i dettagli lasciandoli nella stessa posizione.
Nel warping i pixel restano gli stessi, ma vengono spostati.

slide 8: assumiamo che le trasformazioni che applichiamo siano globali, quindi per tutta l'immagine.
Esempio: se l'auto si muove verso destra e io scatto 2 immagini spostandomi verso sinistra avrò lo sfondo che seguirà una trasformazione diversa rispetto all'auto.
In questo caso è più difficile calcolare le trasformazioni, perché sono trasformazioni locali.

slide 11: Dopo aver scalato bisogna applicare l'interpolazione
//// INSERIRE IMMAGINE DI ESEMPIO DI INTERPOLAZIONE, L'IMMAGINE RAPPRESENTA UNA MATRICE CON DIMENSIONE RADDOPPIATA (DA 3X3 A 6X6) E 3 LINEE CHE PARTONO DALLA PRIMA RIGA DELLA MATRICE E VANNO ALLA PRIMA RIGA DELLA SECONDA, CON GLI SPAZI VUOTI RIEMPITI IN ROSSO E A FIANCO UNA LEGENDA CON SCRITTO "RIMASTI VUOTI/DA INTERPOLARE" O QUALSIASI COSA SIA GIUSTA INSERIRE

slide 13: lo shear è importante perché quando scatto la foto c'è una non-idealità nel sensore che causa questo effetto, devo quindi imparare a stimarlo partendo dall'immagine scattata per poterlo correggere.

slide 15: le trasformazioni lineari non cambiano l'origine.

slide 16: non hanno la proprietà commutativa, applicare prima una o prima un'altra ha effetti diversi

slide 19: in una trasformazione affine abbiamo 6  parametri

slide 22: le omografie sono un'altra classe di trasformazioni che vanno a cambiare anche il parallelismo delle linee

slide 24: le omografie vengono calcolate tramite l'ultima riga delle matrici affini, e ci forniscono un cambio di prospettiva

slide 25: ci sono molte omografie che generano lo stesso risultato nel mondo cartesiano, dobbiamo aggiungere delle limitazioni per evitare di avere un sistema che non  può essere risolto.

slide 32-33: avendo $p=(x_1, y_1)$ e $p'=(x_1', y_1')$ i match individuati, posso calcolare la trasformazione:
$$\begin{align}
x_1' = x_1 + t_x \to t_x = x_1'-x_1\\ y_1' = y_1 + t_y \to t_y = y_1' - y_1
\end{align}$$

il problema è che i match non sono perfetti, non ho 2 punti con esattamente la stessa descrizione.
Ogni match potrebbe dare una diversa opinione sulla trasformazione avvenuta, dobbiamo quindi tenere conto di tutti i match trovati, facendo ad esempio la media

slide 35: dobbiamo risolvere un problema di ottimizzazione, ovvero trovare il parametro $t$ che spiega al meglio la traslazione di ogni punto.

slide 38: ovviamente dopo tutti questi giri, il t ottimale è la media

slide 45: possiamo applicare i moltiplicatori di lagrange