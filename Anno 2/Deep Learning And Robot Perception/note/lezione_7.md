# lezione\_7

2026-10-06

slide 12: avvicinarsi fisicamente all'obiettivo produce risultati diversi rispetto al cambiare FOV (zoomare). Avvicinandoci il FOV resta lo stesso, quindi gli elementi nell'immagini avranno le stesse proporzioni, cambiare il fov porta a un cambiamento delle proporzioni.

slide 13: lo stesso oggetto con la stessa altezza, a causa dell'effetto della proiezione, se si trova più lontano risulterà più piccolo.

slide 18: la formula ci indica che più il punto è lontano più piccolo sarà sull'immagine.

slide 19: rappresentiamo il mondo 2d con 3 coordinate (il 3d sarebbe 4 coordinate).

slide 20: così posso esprimere la formula tramite moltiplicazioni di matrice e vettore.
Prima otteniamo fX, fY, Z, possiamo poi dividere per Z per ottenere le coordinate nel piano cartesiano.

slide 21: è impossibile tornare indietro all'ambiente 3d, se non abbiamo il punto 3d non abbiamo Z, e se non abbiamo Z non possiamo stabilire in quale punto dello spazio si trovava quel pixel.

$$X = \frac xf \cdot Z$$

L'idea della proiezione 3d è che se utilizzo un'altra immagine della stessa scena cambiando leggermente il punto di vista, e se riesco a riconoscere un oggetto in comune in quelle immagini, posso individuare il punto di intersezione e ricavare la Z (Triangolazione).

slide 22: devo considerare l'offset, perché con la formula assumo che l'origine dell'immagine sia al centro dell'immagine, quando in realtà l'origine si trova nell'angolo in alto a sinistra.

slide 23: devo quindi aggiungere questo offset.

slide 24: la mia projection matrix dipende quindi da 5 parametri diversi.

slide 30: calibriamo la camera così da riuscire a trovare k.

slide 32: questa procedura si chiama triangolazione, abbiamo bisogno dei parametri intrinsechi e estrinsechi (boh lo ha detto in inglese).
è una specie di features matching ma più complesso perché dobbiamo farlo per tutti i pixel.

slide 34: se conosco tutte le informazioni rilevanti, come la rotazione e la baseline, e in qualche modo conosco anche la profondità Z (vedremo dopo), posso facillmente ricostruire il punto.
la focal length è la distanza tra camera e piano.
La baseline B è la disparity?? non ho capito

slide 35: non ho capito come si ricava la disparity, se è spiegata in questa slide.
Il professore sta citando i descriptor, descrivendo ogni pixel basandoci sui suoi vicini, come per i keypoints. Il calcolo è quindi molto complesso in quanto ci sono milioni di pixel.

slide 38: baseline più grandi ci permettono di distinguere meglio la profondità degli oggetti.

slide 39: l'errore di disparità aumenta con il quadrato della profondità.

slide 44: non devo guardare a tutta l'immagine, devo solo guardare alla linea che viene proiettata dalla linea di proiezione dell'altra immagine. è impossibile che il pixel si trovi in un'altra posizione.

slide 46: il piano epipolare è definito dalle linee che connettono la proiezione del centro delle camere e il punto tridimensionale x. il punto p è l'intersezione tra la linea epipolare e la baseline.
la linea epipolare è l'intersezione tra il piano epipolare e il punto p.
la linea epipolare e il piano epipolare cambiano a seconda del punto tridimensionale.

slide 47: tutte le linee epipolari passano per l'epipolo, l'epipolo è fisso.
l'epipolo potrebbe essere nel piano dell'immagine, oppure all'esterno a seconda di come sono ruotate le telecamere.

slide 53: il world origin coincide con il centro della prima camera.

slide 54: in questo esempio assumiamo che la camera sia la stessa, quindi abbiamo la stessa calibration matrix.

slide 55: rappresento il punto X' come il primo X traslato e ruotato secondo la trasformazione della seconda camera.

slide 56: entrambi i raggi coincidono nel punto X, che è sconosciuto. i raggi ovviamente coincidono con i centri delle telecamere, perché è da dove vengono generati, e sappiamo a quale distanza si trovano i due centri.


slide 61: su camere posizionate in parallelo, la linea epipolare sarà orizzontale in quanto il punto verrà solo traslato in orizzontale.

slide 62: possiamo riscrivere la formula della retta come $$ax + by + c = 0 \to y =- \frac ab x - \frac cb \to y = mx+q$$

il vantaggio di questa forma è che posso riscriverla in forma di moltiplicazione tra vettori.
Definiamo una linea sul piano, e il punto q' deve trovarsi sulla linea.

slide 65: stiamo lavorando con il pixel q, che sarebbe la versione normalizzata di p. possiamo calcolare le coordinate p partendo dalla versione normalizzata q.
la differenza tra la matrice fondamentale e la matrice intrinseca (?) è la presenza degli intrinsechi.

dobbiamo tornare alle coordinate dei pixel perché iniziamo dalle coordinate dei pixel, ci servono le coordinate normalizzate solo per i calcoli.

$$p'^T \frac {K^{-1T} E K^{-1}}F p = 0$$
$p'^T F p =0$ coordinate pixel
$q'^T F q = 0$ coordinate normalizzate

slide 70: sappiamo che ogni punto dell'immagine 1 è collegato a ogni punto dell'immagine 2 tramite epipolar constraint.
Se non conosciamo F possiamo selezionare 2 punti sull'immagine che possiamo matchare per poi calcolare la F.


