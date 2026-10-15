# lezione\_12

presentazione 021_1

slide 4: l'idea del particle filter è di approssimare il filtro di bayes stimando le possibili pose.

slide 5: il filtro lavora con 2 modelli fondamentali: il modello di moto che viene utilizzato per calcolare la prior, e il modello di misura che ci aiuta a calcolare il peso di ogni particella per fare il resampling.
le particelle quelle meno importanti vengono eliminate e quelle più pesanti vengono duplicate.
il peso viene calcolato solo sulle particelle esistenti, se non ci sono particelle nella zona a verosimiglianza alta le particelle avranno un peso basso, questo è un problema noto di questo approccio.

slide 10: l'importance resampling è rumoroso, genera una stima con una varianza elevata.
se un robot va in una posizione in cui non è presente nessuna particella, si perde. Questo caso si chiama particle deprivation, e la soluzione è di inserire delle particelle nella parte dove è bassa la probabilità.

da slide 26 argomenti extra.

presentazione 012_2
