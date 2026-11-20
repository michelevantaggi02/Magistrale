slide 6: gli algoritmi di visual slam vengono caratterizzati secondo 2 criteri:
- la quantità di pixel utilizzati: densi o sparsi
- diretti o indiretti: diretti lavoriamo con i pixel, indiretti si estraggono features dall'immagine.
slide 8: il gruppo di ricerca di Tardòs è quello che ha pensato ORB-SLAM, se vogliamo trovare altri paper sull'argomento sarebbe utile usare i suoi.

slide 14: il detector che estrae le feature si chiama ORB basato su altri due famosi feature detector e descriptor.
/// da riguardare, distinzione tra front-end e backend nello SLAM.
abbiamo quindi 3 fasi fatte da 3 thread diversi: tracking, local mapping e loop closing

slide 15: //// aggiungi spiegazione dell'immagine

slide 24: ORB-SLAM ci mette delle misure di lunghezza senza unità di misura, perché è monocolore. Non ha quindi la giusta scala.

slide 20: \pi(AP_c) rappresenta la rappresentazione del punto 3D nel piano dell'immagine.

Dato un pixel nell'immagine, \Xi mi dice quanto è distante il punto (l'inverso della distanza).
