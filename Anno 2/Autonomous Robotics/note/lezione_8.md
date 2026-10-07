# lezione\_8

L'histogram filter è un modo per calcolare i filtri di bayes.

slide 3: la caratteristica computazionale è il principale limite di questo filtro, devo fare un ciclo for per infiniti punti nello spazio.
L'idea che sta dietro l'histogram filter è quello di campionare lo spazio delle pose.

slide 7: x_k non è il valore al passo attuale, ma è un punto nello spazio delle pose che il robot potrebbe assumere.

slide 8: ho essenzialmente riscritto il filtro di bayes in forma discreta.
sto esaminando tutte le possibili pose in cui sono adesso e le valuto con le possibili pose del passo precedente.
nel pratico la state transition probability diventa il nostro motion model.