# lezione\_12

slide 1: fino ad ora abbiamo visto reti completamente connesse, o dense, dove ogni neurone è collegato a tutti i neuroni successivi, ed ogni collegamento ha il suo peso.

slide 10: si comporta similmente ad un filtro di sobel, può essere utilizzato per individuare bordi.

slide 11: se compariamo i filtri di sobel contro i layer addestrati tipici dei primi layer di una cnn, possiamo osservare che non ci sono molte differenze. è molto peculiare il fatto che i pesi addestrati hanno fornito un filtro molto simile ai sobel senza averglielo esplicitamente chiesto.

slide 12: possiamo implementare la convoluzione in modo simile alla moltiplicazione tra matrici, soltanto che abbiamo gli stessi parametri riutilizzati per neuroni diversi, inoltre la matrice è sparsa.
uno dei vantaggi immediati è che abbiamo meno parametri per lo stesso numero di unità.
L'altro vantaggio è che quindi compiamo meno operazioni.
Quando scegliamo una cnn layer introduciamo un inductive bias, per obbligare la rete a osservare solo feature locali, permettendoci di identificarle indipendentemente dalla loro posizione.

slide 14: non tutte le unità nascoste sono connesse con tutte le unità del layer successivo, le connessioni sono ridotte.
un neurone dei convolutional layer è connesso solo a un subset dei neuroni del layer successivo.
il numero di neuroni del layer precedente che un neurone vede si chiama recceptive field, o kernel size.

/// inserire immagine di esempio receptive field, con 3 layer da 7 neuroni ognuno, esempio solo dei 3 neuroni centrali del primo layer (il receptive field) connessi al neurone centrale del secondo layer, il neurone del secondo layer è connesso ai 3 neuroni centrali del terzo layer

un neurone è quindi connesso soltanto a k neuroni locali.

slide 16: per riconoscere una feature nell'immagine non ci serve osservare tutto l'insieme, ci basta prendere un piccolo vicinato di pixel.
in questo modo possiamo anche diminuire drasticamente il numero di parametri.

slide 17-18:
//// inserire immagine di esempio di receptive field, con 3 layer da 5 neuroni ciascuno, si ha un kernel da 3 neuroni e si disegni la piramide che compone i pesi del neurone centrale al terzo layer, quindi i primi 3 neuroni connessi al secondo neurone del layer 2, i neuroni da 2 a 4 connessi al 3 neurone del layer 2, i neuroni da 3 a 5 connessi al 4 neurone del layer 2, e i neuroni 2 3 4 del layer 2 connessi al 3 neurone del layer 3.

slide 19: posso riutilizzare gli stessi pesi per neuroni diversi, implementando effettivamente una convoluzione, così da risparmiare il numero di parametri (per un kernel di 3, ho 3 parametri invece che 9).

slide 20: un corner è un corner indipendentemente dalla sua posizione nell'immagine, le sue features sono locali, quindi non ha senso avere parametri diversi per punti diversi dell'immagine, mi basta usare sempre gli stessi parametri.

slide 22: in questo esempio prendo in considerazione un'immagine a scala di grigi, senza colori.
in genere le cnn performano estremamente meglio rispetto alle architetture dense.

slide 28: l'output è diverso se si applica la rotazione, bisogna quindi addestrare dei filtri che siano robusti a questo problema.

slide 31: non cambia nulla se l'immagine ha 3 colori, dobbiamo solo considerare che l'immagine abbia 3 matrici.
abbiamo  diversi modi per applicare il kernel a queste matrici: possiamo utilizzare il kernel per calcolare  la stessa posizione sulle 3 matrici, ma ha più senso avere filtri diversi in base al canale di input.
il kernel diventa quindi un piccolo cubo composto da 3 matrici, piazzamo quindi questo cubo e calcoliamo, il risultato sarà comunque una matrice singola e la convoluzione viene calcolata tramite questa struttura solida.

////valuta se usare l'immagine a slide 32 oppure: inserisci immagine di esempio di 3 matrici di immagine 5x5 messe una dietro l'altra con un cubo 3x3x3 che rappresenta il kernel cubico nell'angolo in alto a sinistra delle matrici. con una freccia che conduce alla cella in alto a destra di una matrice chiamata feature map 5x5

slide 34: in base al task dobbiamo decidere se utilizzare immagini a colori o in scala di grigi, perché la rete potrebbe addestrarsi a riconoscere elementi di uno specifico colore, dando più importanza a un canale piuttosto che agli altri, se non sappiamo qualora il colore sia importante o meno è sempre opportuno fornire più esempi possibili, ad esempio con auto di colori diversi per poter rendere la rete meno dipendente dai colori e più da altre informazioni.

slide 35: possiamo addestrare feature map diverse per feature diverse, ad esempio per identificare corner con forme diverse.
in un layer convoluzionale avremo un insieme di feature map, impilate e se osserviamo sono lo stesso oggetto matematico delle immagini (tensori).
Il numero di filtri, e quindi di feature, è un iperparametro delle cnn. 

slide 36: decidiamo separatamente per ogni layer il numero di feature. ogni layer ottiene tutte le feature del layer precedente.

//// inserisci immagine di esempio, immagine casetta, primo layer convoluzionale identifica i 4 angoli di un quadrato, il secondo layer individua il quadrato che corrisponde alle mura della casetta. per ogni layer inserisci sia la forma da individuare di esempio che la feature map associata, quindi il corner in alto a destra avrà un punto della feature map in alto a destra e così via anche per il quadrato.

slide 45: ReLU è sempre presente. 