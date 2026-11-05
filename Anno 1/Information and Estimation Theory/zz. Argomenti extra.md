# zz. Argomenti extra

Questo documento raccoglie dimostrazioni analitiche estese, passaggi algebrici dettagliati e modelli matematici collaterali del corso di __Information and Estimation Theory__ non presenti letteralmente nelle presentazioni sintetiche dei docenti, ma fondamentali nella letteratura scientifica di riferimento (Steven M. Kay, _Fundamentals of Statistical Signal Processing_, Vol. I & II; Thomas M. Cover & Joy A. Thomas, _Elements of Information Theory_).

Ogni sezione è puntualmente richiamata dai capitoli primari di lezione tramite wikilink dedicati.

## Dimostrazione del Limite Inferiore di Cramer-Rao (CRLB)

La derivazione formale della disuguaglianza del CRLB scalare poggia sull'applicazione della __disuguaglianza di Cauchy-Schwarz__ a due variabili aleatorie opportune definite nello spazio delle osservazioni $\mathcal{X}$.

Sia $\hat{\theta} = g(\mathbf{x})$ uno stimatore non polarizzato del parametro deterministico $\theta$, per cui:

$$
\mathbb{E}[\hat{\theta}] = \int_{\mathcal{X}} g(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = \theta \quad \forall \theta
$$

Definiamo la funzione di score:

$$
S(\mathbf{x}; \theta) = \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} = \frac{1}{f_{\mathbf{x}}(\mathbf{x}; \theta)} \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta}
$$

Sotto la condizione di regolarità, il valore atteso dello score è nullo:

$$
\mathbb{E}[S(\mathbf{x}; \theta)] = \int_{\mathcal{X}} \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \mathrm{d}\mathbf{x} = \frac{\partial}{\partial \theta} \int_{\mathcal{X}} f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = \frac{\partial}{\partial \theta} (1) = 0
$$

La varianza dello score coincide con l'Informazione di Fisher $I(\theta)$:

$$
\text{Var}\{S(\mathbf{x}; \theta)\} = \mathbb{E}\left[ S^2(\mathbf{x}; \theta) \right] = I(\theta)
$$

### Calcolo della Covarianza tra Stimatore e Score

Calcoliamo la covarianza tra lo stimatore $\hat{\theta}$ e la funzione di score $S(\mathbf{x}; \theta)$:

$$
\text{Cov}\{\hat{\theta}, S\} = \mathbb{E}\left[ (\hat{\theta} - \theta)(S - \mathbb{E}[S]) \right] = \mathbb{E}\left[ (\hat{\theta} - \theta) \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right]
$$

Esplicitiamo l'integrale:

$$
\text{Cov}\{\hat{\theta}, S\} = \int_{\mathcal{X}} (g(\mathbf{x}) - \theta) \frac{1}{f_{\mathbf{x}}(\mathbf{x}; \theta)} \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = \int_{\mathcal{X}} (g(\mathbf{x}) - \theta) \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \mathrm{d}\mathbf{x}
$$

Spezziamo l'integrale nei due addendi:

$$
\text{Cov}\{\hat{\theta}, S\} = \int_{\mathcal{X}} g(\mathbf{x}) \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \mathrm{d}\mathbf{x} - \theta \int_{\mathcal{X}} \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \mathrm{d}\mathbf{x}
$$

Il secondo integrale è nullo per la condizione di regolarità. Nel primo integrale, invertendo l'ordine di derivazione e integrazione:

$$
\int_{\mathcal{X}} g(\mathbf{x}) \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \mathrm{d}\mathbf{x} = \frac{\partial}{\partial \theta} \int_{\mathcal{X}} g(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = \frac{\partial}{\partial \theta} (\mathbb{E}[\hat{\theta}])
$$

Poiché lo stimatore $\hat{\theta}$ è non polarizzato, $\mathbb{E}[\hat{\theta}] = \theta$, per cui:

$$
\frac{\partial}{\partial \theta} (\theta) = 1 \implies \text{Cov}\{\hat{\theta}, S\} = 1
$$

La covarianza tra un qualsiasi stimatore non polarizzato e la funzione di score vale identicamente $1$.

### Applicazione della Disuguaglianza di Cauchy-Schwarz

Per due variabili aleatorie arbitrarie $U$ e $V$, la disuguaglianza di Cauchy-Schwarz stabilisce che il quadrato della loro covarianza è limitato superiormente dal prodotto delle loro varianze:

$$
\text{Cov}^2\{U, V\} \le \text{Var}\{U\} \text{Var}\{V\}
$$

Ponendo $U = \hat{\theta}$ e $V = S(\mathbf{x}; \theta)$:

$$
\text{Cov}^2\{\hat{\theta}, S\} \le \text{Var}\{\hat{\theta}\} \text{Var}\{S\}
$$

Sostituendo i valori ricavati:

$$
1^2 \le \text{Var}\{\hat{\theta}\} \cdot I(\theta)
$$

Poiché l'Informazione di Fisher è non negativa ($I(\theta) > 0$), dividendo per $I(\theta)$ otteniamo la disuguaglianza di Cramer-Rao:

$$
\text{Var}\{\hat{\theta}\} \ge \frac{1}{I(\theta)}
$$

### Condizione di Uguaglianza ed Efficienza

La disuguaglianza di Cauchy-Schwarz diventa un'uguaglianza se e solo se le due variabili aleatorie $(U - \mathbb{E}[U])$ e $(V - \mathbb{E}[V])$ sono proporzionali tra loro con probabilità $1$, ovvero esiste una costante $k(\theta)$ non dipendente da $\mathbf{x}$ tale che:

$$
S(\mathbf{x}; \theta) = k(\theta) (\hat{\theta} - \theta)
$$

Calcoliamo la covarianza sotto questa condizione di proporzionalità:

$$
\text{Cov}\{\hat{\theta}, S\} = \mathbb{E}\left[ (\hat{\theta} - \theta) \cdot k(\theta)(\hat{\theta} - \theta) \right] = k(\theta) \text{Var}\{\hat{\theta}\}
$$

Sapendo che $\text{Cov}\{\hat{\theta}, S\} = 1$ e che al raggiungimento del bound $\text{Var}\{\hat{\theta}\} = \frac{1}{I(\theta)}$:

$$
1 = k(\theta) \cdot \frac{1}{I(\theta)} \implies k(\theta) = I(\theta)
$$

Sostituendo $k(\theta) = I(\theta)$, la condizione necessaria e sufficiente affinché l'uguaglianza sia raggiunta diventa:

$$
\frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} = I(\theta) (\hat{\theta} - \theta)
$$

Se riusciamo a esprimere la derivata prima della log-verosimiglianza come il prodotto di una funzione $I(\theta)$ per una differenza $(\hat{\theta} - \theta)$ in cui $\hat{\theta} = g(\mathbf{x})$ non dipende da $\theta$, allora $\hat{\theta} = g(\mathbf{x})$ è l'__MVU estimator efficiente__.

## Identità tra la Prima e la Seconda Derivata dell'Informazione di Fisher

Dimostriamo l'equivalenza fondamentale per il calcolo dell'Informazione di Fisher:

$$
\mathbb{E}\left[ \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right)^2 \right] = -\mathbb{E}\left[ \frac{\partial^2 \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta^2} \right]
$$

Partiamo dalla condizione di regolarità:

$$
\int_{\mathcal{X}} \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = 0
$$

Deriviamo entrambi i membri rispetto al parametro $\theta$:

$$
\frac{\partial}{\partial \theta} \int_{\mathcal{X}} \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = 0
$$

Portando la derivata sotto il segno di integrale ed applicando la regola del prodotto di derivazione:

$$
\int_{\mathcal{X}} \left( \frac{\partial^2 \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta^2} f_{\mathbf{x}}(\mathbf{x}; \theta) + \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \frac{\partial f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right) \mathrm{d}\mathbf{x} = 0
$$

Ricordando che $\frac{\partial f}{\partial \theta} = f \cdot \frac{\partial \ln f}{\partial \theta}$, il secondo termine dentro l'integrale diventa:

$$
\frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \cdot \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} f_{\mathbf{x}}(\mathbf{x}; \theta) \right) = \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right)^2 f_{\mathbf{x}}(\mathbf{x}; \theta)
$$

Sostituendo nell'equazione:

$$
\int_{\mathcal{X}} \frac{\partial^2 \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta^2} f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} + \int_{\mathcal{X}} \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right)^2 f_{\mathbf{x}}(\mathbf{x}; \theta) \mathrm{d}\mathbf{x} = 0
$$

Riconoscendo gli operatori di valore atteso:

$$
\mathbb{E}\left[ \frac{\partial^2 \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta^2} \right] + \mathbb{E}\left[ \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right)^2 \right] = 0
$$

Isolando il secondo momento otteniamo la tesi:

$$
I(\theta) = \mathbb{E}\left[ \left( \frac{\partial \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta} \right)^2 \right] = -\mathbb{E}\left[ \frac{\partial^2 \ln f_{\mathbf{x}}(\mathbf{x}; \theta)}{\partial \theta^2} \right]
$$

## Disuguaglianza tra Elementi della FIM Inversa e Complemento di Schur

Nel caso vettoriale, la disuguaglianza fondamentale tra l'elemento diagonale della matrice di informazione di Fisher inversa e il reciproco dell'elemento della matrice originaria:

$$
[\mathbf{I}^{-1}(\boldsymbol{\theta})]_{i, i} \ge \frac{1}{[\mathbf{I}(\boldsymbol{\theta})]_{i, i}}
$$

spiega perché la stima congiunta di più parametri incogniti comporti sempre una varianza minima maggiore (o al più uguale) rispetto al caso in cui tutti gli altri parametri siano noti a priori.

### Dimostrazione Algebrica Tramite Inversione a Blocchi

Senza perdita di generalità, isoliamo il primo parametro $\theta_1$ partizionando a blocchi la matrice simmetrica e definita positiva $\mathbf{I} \in \mathbb{R}^{P \times P}$:

$$
\mathbf{I} = \begin{bmatrix} i_{11} & \mathbf{i}_{12}^T \\ \mathbf{i}_{12} & \mathbf{I}_{22} \end{bmatrix}
$$

dove $i_{11} = [\mathbf{I}]_{11} > 0$ è uno scalare, $\mathbf{i}_{12} \in \mathbb{R}^{P-1}$ è il vettore delle informazioni incrociate tra $\theta_1$ e i restanti parametri, e $\mathbf{I}_{22} \in \mathbb{R}^{(P-1) \times (P-1)}$ è il blocco principale relativo ai parametri secondari (anch'esso definito positivo).

Applicando la formula di inversione a blocchi per matrici (identità del complemento di Schur), l'elemento in posizione $(1, 1)$ della matrice inversa $\mathbf{I}^{-1}$ è dato esattamente da:

$$
[\mathbf{I}^{-1}]_{11} = \frac{1}{i_{11} - \mathbf{i}_{12}^T \mathbf{I}_{22}^{-1} \mathbf{i}_{12}}
$$

Analizziamo il termine sottrattivo al denominatore:
1. Poiché la matrice $\mathbf{I}$ è definita positiva, la sottomatrice $\mathbf{I}_{22}$ è definita positiva $\implies$ la sua inversa $\mathbf{I}_{22}^{-1}$ è anch'essa definita positiva.
2. La forma quadratica associata a una matrice definita positiva è sempre non negativa per qualsiasi vettore:

$$
\mathbf{i}_{12}^T \mathbf{I}_{22}^{-1} \mathbf{i}_{12} \ge 0
$$

con uguaglianza a zero se e solo se $\mathbf{i}_{12} = \mathbf{0}$ (ovvero quando $\theta_1$ è ortogonale/scorrelato rispetto a tutti gli altri parametri).

Di conseguenza, il denominatore è limitato superiormente da $i_{11}$:

$$
i_{11} - \mathbf{i}_{12}^T \mathbf{I}_{22}^{-1} \mathbf{i}_{12} \le i_{11}
$$

Prendendo il reciproco (poiché entrambi i membri sono strettamente positivi per la definita positività di $\mathbf{I}$):

$$
\frac{1}{i_{11} - \mathbf{i}_{12}^T \mathbf{I}_{22}^{-1} \mathbf{i}_{12}} \ge \frac{1}{i_{11}}
$$

Sostituendo $[\mathbf{I}^{-1}]_{11}$ e $i_{11} = [\mathbf{I}]_{11}$:

$$
[\mathbf{I}^{-1}]_{11} \ge \frac{1}{[\mathbf{I}]_{11}}
$$

L'uguaglianza $[\mathbf{I}^{-1}]_{ii} = \frac{1}{[\mathbf{I}]_{ii}}$ si verifica se e solo se la colonna e la riga dei termini di accoppiamento sono nulle ($\mathbf{i}_{12} = \mathbf{0}$), ovvero quando la matrice di informazione di Fisher è diagonale a blocchi e i parametri non interferiscono statisticamente tra loro nella stima.

## Dimostrazione del Teorema di Gauss-Markov per il BLUE Vettoriale

Consideriamo il modello lineare vettoriale per le osservazioni $\mathbf{x} \in \mathbb{R}^N$:

$$
\mathbf{x} = \mathbf{H}\boldsymbol{\theta} + \mathbf{w}
$$

dove $\boldsymbol{\theta} \in \mathbb{R}^P$ è il vettore dei parametri deterministici incogniti, $\mathbf{H} \in \mathbb{R}^{N \times P}$ è la matrice di osservazione a rango pieno colonna $\text{rk}(\mathbf{H}) = P \le N$, e $\mathbf{w}$ è un vettore aleatorio di rumore a media nulla $\mathbb{E}[\mathbf{w}] = \mathbf{0}$ e matrice di covarianza $\text{Cov}\{\mathbf{w}\} = \mathbf{C}_{\mathbf{w}\mathbf{w}} = \mathbf{C}_{\mathbf{x}\mathbf{x}}$ simmetrica e strettamente definita positiva.

Il __Teorema di Gauss-Markov__ afferma che lo stimatore:

$$
\hat{\boldsymbol{\theta}}_{\text{BLUE}} = (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H})^{-1} \mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{x}
$$

è il migliore stimatore lineare non polarizzato nel senso che, per qualunque altro stimatore lineare non polarizzato $\tilde{\boldsymbol{\theta}} = \mathbf{B}\mathbf{x}$, la differenza tra le rispettive matrici di covarianza $\mathbf{C}_{\tilde{\boldsymbol{\theta}}} - \mathbf{C}_{\hat{\boldsymbol{\theta}}_{\text{BLUE}}}$ è una matrice __semidefinita positiva__.

### Dimostrazione Tramite Decomposizione dell'Operatore Lineare

Sia $\tilde{\boldsymbol{\theta}} = \mathbf{B}\mathbf{x}$ un generico stimatore lineare, con $\mathbf{B} \in \mathbb{R}^{P \times N}$.
Affinché $\tilde{\boldsymbol{\theta}}$ sia non polarizzato per qualsiasi valore del parametro $\boldsymbol{\theta}$, deve valere:

$$
\mathbb{E}[\tilde{\boldsymbol{\theta}}] = \mathbf{B} \mathbb{E}[\mathbf{x}] = \mathbf{B} \mathbf{H} \boldsymbol{\theta} = \boldsymbol{\theta} \quad \forall \boldsymbol{\theta} \iff \mathbf{B}\mathbf{H} = \mathbf{I}_P
$$

Definiamo la matrice dei coefficienti ottima del BLUE:

$$
\mathbf{A} = (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H})^{-1} \mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1}
$$

Si verifica immediatamente che $\mathbf{A}$ soddisfa il vincolo di non polarizzazione:

$$
\mathbf{A}\mathbf{H} = (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H})^{-1} (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H}) = \mathbf{I}_P
$$

Possiamo esprimere la generica matrice $\mathbf{B}$ come la somma della matrice ottima $\mathbf{A}$ e di una matrice di scostamento $\mathbf{D} \in \mathbb{R}^{P \times N}$:

$$
\mathbf{B} = \mathbf{A} + \mathbf{D}
$$

Imponendo il vincolo di non polarizzazione su $\mathbf{B}$:

$$
\mathbf{B}\mathbf{H} = (\mathbf{A} + \mathbf{D})\mathbf{H} = \mathbf{A}\mathbf{H} + \mathbf{D}\mathbf{H} = \mathbf{I}_P + \mathbf{D}\mathbf{H} = \mathbf{I}_P \iff \mathbf{D}\mathbf{H} = \mathbf{0}
$$

La matrice di deviazione $\mathbf{D}$ deve quindi avere le righe ortogonali a tutte le colonne della matrice $\mathbf{H}$.

Calcoliamo ora la matrice di covarianza di $\tilde{\boldsymbol{\theta}}$:

$$
\mathbf{C}_{\tilde{\boldsymbol{\theta}}} = \text{Cov}\{\mathbf{B}\mathbf{x}\} = \mathbf{B} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{B}^T = (\mathbf{A} + \mathbf{D}) \mathbf{C}_{\mathbf{x}\mathbf{x}} (\mathbf{A} + \mathbf{D})^T
$$

Espandendo il prodotto matriciale:

$$
\mathbf{C}_{\tilde{\boldsymbol{\theta}}} = \mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{A}^T + \mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T + \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{A}^T + \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T
$$

Esaminiamo i termini incrociati. Sostituendo la definizione esplicita di $\mathbf{A}$:

$$
\mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T = (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H})^{-1} \mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T = (\mathbf{H}^T \mathbf{C}_{\mathbf{x}\mathbf{x}}^{-1} \mathbf{H})^{-1} \mathbf{H}^T \mathbf{D}^T
$$

Poiché per la condizione di non polarizzazione $\mathbf{D}\mathbf{H} = \mathbf{0}$, trasponendo si ha $\mathbf{H}^T \mathbf{D}^T = (\mathbf{D}\mathbf{H})^T = \mathbf{0}^T = \mathbf{0}$. Di conseguenza:

$$
\mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T = \mathbf{0} \quad \text{e analogamente} \quad \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{A}^T = (\mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T)^T = \mathbf{0}
$$

I termini incrociati si annullano identicamente. L'espressione della covarianza si riduce a:

$$
\mathbf{C}_{\tilde{\boldsymbol{\theta}}} = \mathbf{A} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{A}^T + \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T = \mathbf{C}_{\hat{\boldsymbol{\theta}}_{\text{BLUE}}} + \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T
$$

Sottraendo la matrice di covarianza del BLUE:

$$
\mathbf{C}_{\tilde{\boldsymbol{\theta}}} - \mathbf{C}_{\hat{\boldsymbol{\theta}}_{\text{BLUE}}} = \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T
$$

Poiché $\mathbf{C}_{\mathbf{x}\mathbf{x}}$ è una matrice simmetrica e definita positiva ($\mathbf{C}_{\mathbf{x}\mathbf{x}} > 0$), per qualunque vettore arbitrario $\mathbf{c} \in \mathbb{R}^P \setminus \{\mathbf{0}\}$ si ha:

$$
\mathbf{c}^T (\mathbf{C}_{\tilde{\boldsymbol{\theta}}} - \mathbf{C}_{\hat{\boldsymbol{\theta}}_{\text{BLUE}}}) \mathbf{c} = \mathbf{c}^T \mathbf{D} \mathbf{C}_{\mathbf{x}\mathbf{x}} \mathbf{D}^T \mathbf{c} = (\mathbf{D}^T \mathbf{c})^T \mathbf{C}_{\mathbf{x}\mathbf{x}} (\mathbf{D}^T \mathbf{c}) \ge 0
$$

La differenza $\mathbf{C}_{\tilde{\boldsymbol{\theta}}} - \mathbf{C}_{\hat{\boldsymbol{\theta}}_{\text{BLUE}}}$ è pertanto una matrice semidefinita positiva. L'uguaglianza alla minima varianza si ottiene se e solo se $\mathbf{D}^T \mathbf{c} = \mathbf{0}$ per ogni $\mathbf{c}$, il che implica $\mathbf{D} = \mathbf{0}$, ossia $\mathbf{B} = \mathbf{A}$.

Questo dimostra in modo costruttivo e inequivocabile che $\hat{\boldsymbol{\theta}}_{\text{BLUE}}$ minimizza la varianza di qualsiasi combinazione lineare dei parametri $\mathbf{c}^T \boldsymbol{\theta}$, sancendo l'unicità e l'ottimalità globale del BLUE nella classe lineare.

## Proprietà Geometriche della Matrice di Proiezione Ortogonale nei Minimi Quadrati

Nel contesto della stima deterministica ai minimi quadrati per il modello lineare $\mathbf{x} = \mathbf{H}\boldsymbol{\theta} + \mathbf{e}$, con $\mathbf{H} \in \mathbb{R}^{N \times P}$ di rango colonna pieno $P \le N$, la stima del segnale utile $\hat{\mathbf{s}}$ è ottenuta proiettando il vettore delle osservazioni $\mathbf{x}$ sul sottospazio generato dalle colonne di $\mathbf{H}$ (indicato con $\mathcal{R}(\mathbf{H})$):

$$
\hat{\mathbf{s}} = \mathbf{H}\hat{\boldsymbol{\theta}}_{\text{LSE}} = \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \mathbf{x} = \mathbf{P}_{\mathbf{H}} \mathbf{x}
$$

La matrice $\mathbf{P}_{\mathbf{H}} = \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \in \mathbb{R}^{N \times N}$ gode di proprietà algebriche e geometriche fondamentali:

### Simmetria

La matrice di proiezione ortogonale coincide con la sua trasposta:

$$
\mathbf{P}_{\mathbf{H}}^T = \left( \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \right)^T = (\mathbf{H}^T)^T \left( (\mathbf{H}^T\mathbf{H})^{-1} \right)^T \mathbf{H}^T = \mathbf{H} (\mathbf{H}^T\mathbf{H})^{-1} \mathbf{H}^T = \mathbf{P}_{\mathbf{H}}
$$

### Idempotenza

Applicare la proiezione più volte consecutivamente equivale ad applicarla una volta sola:

$$
\mathbf{P}_{\mathbf{H}}^2 = \mathbf{P}_{\mathbf{H}} \mathbf{P}_{\mathbf{H}} = \left( \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \right) \left( \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \right) = \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1} (\mathbf{H}^T\mathbf{H}) (\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T = \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T = \mathbf{P}_{\mathbf{H}}
$$

Di conseguenza, per induzione $\mathbf{P}_{\mathbf{H}}^k = \mathbf{P}_{\mathbf{H}}$ per qualsiasi intero positivo $k \ge 1$.

### Complemento Ortogonale

La matrice che proietta sul complemento ortogonale $\mathcal{R}(\mathbf{H})^\perp$ è definita da $\mathbf{P}_{\mathbf{H}}^\perp = \mathbf{I}_N - \mathbf{P}_{\mathbf{H}}$. Essa è a sua volta simmetrica e idempotente:

$$
(\mathbf{P}_{\mathbf{H}}^\perp)^T = (\mathbf{I}_N - \mathbf{P}_{\mathbf{H}})^T = \mathbf{I}_N - \mathbf{P}_{\mathbf{H}} = \mathbf{P}_{\mathbf{H}}^\perp
$$

$$
(\mathbf{P}_{\mathbf{H}}^\perp)^2 = (\mathbf{I}_N - \mathbf{P}_{\mathbf{H}})(\mathbf{I}_N - \mathbf{P}_{\mathbf{H}}) = \mathbf{I}_N - 2\mathbf{P}_{\mathbf{H}} + \mathbf{P}_{\mathbf{H}}^2 = \mathbf{I}_N - 2\mathbf{P}_{\mathbf{H}} + \mathbf{P}_{\mathbf{H}} = \mathbf{I}_N - \mathbf{P}_{\mathbf{H}} = \mathbf{P}_{\mathbf{H}}^\perp
$$

Inoltre, i due operatori di proiezione sono tra loro mutuamente ortogonali:

$$
\mathbf{P}_{\mathbf{H}} \mathbf{P}_{\mathbf{H}}^\perp = \mathbf{P}_{\mathbf{H}} (\mathbf{I}_N - \mathbf{P}_{\mathbf{H}}) = \mathbf{P}_{\mathbf{H}} - \mathbf{P}_{\mathbf{H}}^2 = \mathbf{P}_{\mathbf{H}} - \mathbf{P}_{\mathbf{H}} = \mathbf{0}
$$

### Traccia e Rango

Sfruttando la proprietà ciclica dell'operatore traccia $\text{tr}(\mathbf{A}\mathbf{B}) = \text{tr}(\mathbf{B}\mathbf{A})$:

$$
\text{tr}(\mathbf{P}_{\mathbf{H}}) = \text{tr}\left( \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \right) = \text{tr}\left( (\mathbf{H}^T\mathbf{H})^{-1} \mathbf{H}^T \mathbf{H} \right) = \text{tr}(\mathbf{I}_P) = P
$$

Poiché per una matrice di proiezione ortogonale gli autovalori possono valere unicamente $0$ oppure $1$, la traccia eguaglia la somma degli autovalori non nulli e coincide esattamente con il rango della matrice:

$$
\text{rk}(\mathbf{P}_{\mathbf{H}}) = \text{tr}(\mathbf{P}_{\mathbf{H}}) = P \quad \text{e} \quad \text{rk}(\mathbf{P}_{\mathbf{H}}^\perp) = \text{tr}(\mathbf{I}_N - \mathbf{P}_{\mathbf{H}}) = N - P
$$

### Decomposizione dell'Energia (Teorema di Pitagora)

Poiché il vettore delle osservazioni si decompone ortogonalmente nella componente di segnale e nel residuo:

$$
\mathbf{x} = \hat{\mathbf{s}} + \hat{\mathbf{e}} = \mathbf{P}_{\mathbf{H}} \mathbf{x} + \mathbf{P}_{\mathbf{H}}^\perp \mathbf{x}
$$

calcolando la norma euclidea al quadrato dell'osservazione:

$$
\|\mathbf{x}\|^2 = \mathbf{x}^T \mathbf{x} = (\hat{\mathbf{s}} + \hat{\mathbf{e}})^T (\hat{\mathbf{s}} + \hat{\mathbf{e}}) = \|\hat{\mathbf{s}}\|^2 + \|\hat{\mathbf{e}}\|^2 + 2\hat{\mathbf{s}}^T \hat{\mathbf{e}}
$$

Poiché $\hat{\mathbf{s}}^T \hat{\mathbf{e}} = (\mathbf{P}_{\mathbf{H}}\mathbf{x})^T (\mathbf{P}_{\mathbf{H}}^\perp \mathbf{x}) = \mathbf{x}^T \mathbf{P}_{\mathbf{H}}^T \mathbf{P}_{\mathbf{H}}^\perp \mathbf{x} = \mathbf{x}^T \mathbf{0} \mathbf{x} = 0$, si ha la perfetta conservazione dell'energia:

$$
\|\mathbf{x}\|^2 = \|\hat{\mathbf{s}}\|^2 + \|\hat{\mathbf{e}}\|^2
$$

La norma al quadrato dell'errore minimo (il valore ottimo della funzione di costo $J(\hat{\boldsymbol{\theta}}_{\text{LSE}})$) può essere calcolata direttamente mediante:

$$
J_{\min} = \|\hat{\mathbf{e}}\|^2 = \mathbf{x}^T \mathbf{P}_{\mathbf{H}}^\perp \mathbf{x} = \mathbf{x}^T (\mathbf{I}_N - \mathbf{P}_{\mathbf{H}}) \mathbf{x} = \|\mathbf{x}\|^2 - \mathbf{x}^T \mathbf{H}(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T \mathbf{x}
$$

## Teorema di Zehna e Invarianza del MLE per Funzioni Non Biunivoche

La proprietà di invarianza per trasformazioni continue è una delle caratteristiche distintive dello stimatore di massima verosimiglianza rispetto agli stimatori non polarizzati a minima varianza.

Sia $\hat{\boldsymbol{\theta}}_{\text{MLE}}$ lo stimatore di massima verosimiglianza di un parametro vettoriale $\boldsymbol{\theta} \in \Theta \subseteq \mathbb{R}^P$, ottenuto massimizzando la verosimiglianza $L(\boldsymbol{\theta}) = f_{\mathbf{x}}(\mathbf{x}; \boldsymbol{\theta})$.

Desideriamo trovare lo stimatore di massima verosimiglianza per una funzione vettoriale o scalare dei parametri:

$$
\boldsymbol{\alpha} = \mathbf{g}(\boldsymbol{\theta}), \quad \mathbf{g}: \Theta \to \Omega \subseteq \mathbb{R}^K
$$

dove la mappa $\mathbf{g}$ non è necessariamente invertibile né biunivoca (ad esempio la funzione modulo, elevamento al quadrato, o proiezioni a dimensione inferiore $K < P$).

### Definizione di Funzione di Verosimiglianza Indotta

Poiché la trasformazione può essere non iniettiva, a un generico valore $\boldsymbol{\alpha} \in \Omega$ può corrispondere un intero insieme di parametri $\boldsymbol{\theta}$ nella controimmagine:

$$
\mathbf{g}^{-1}(\boldsymbol{\alpha}) = \{ \boldsymbol{\theta} \in \Theta : \mathbf{g}(\boldsymbol{\theta}) = \boldsymbol{\alpha} \}
$$

La funzione di verosimiglianza indotta per il parametro $\boldsymbol{\alpha}$, introdotta da Peter W. Zehna (1966), è definita come l'estremo superiore (o massimo) della verosimiglianza originale su tutti i punti della controimmagine:

$$
\bar{L}(\boldsymbol{\alpha}) = \sup_{\boldsymbol{\theta} \in \mathbf{g}^{-1}(\boldsymbol{\alpha})} L(\boldsymbol{\theta}) = \sup_{\{ \boldsymbol{\theta} \in \Theta : \mathbf{g}(\boldsymbol{\theta}) = \boldsymbol{\alpha} \}} f_{\mathbf{x}}(\mathbf{x}; \boldsymbol{\theta})
$$

### Dimostrazione del Teorema di Invarianza

Lo stimatore di massima verosimiglianza di $\boldsymbol{\alpha}$ è definito per costruzione come il valore che massimizza la verosimiglianza indotta su $\Omega$:

$$
\hat{\boldsymbol{\alpha}}_{\text{MLE}} = \arg \max_{\boldsymbol{\alpha} \in \Omega} \bar{L}(\boldsymbol{\alpha})
$$

Sostituendo la definizione di $\bar{L}(\boldsymbol{\alpha})$:

$$
\max_{\boldsymbol{\alpha} \in \Omega} \bar{L}(\boldsymbol{\alpha}) = \max_{\boldsymbol{\alpha} \in \Omega} \left[ \sup_{\boldsymbol{\theta} \in \mathbf{g}^{-1}(\boldsymbol{\alpha})} L(\boldsymbol{\theta}) \right] = \sup_{\boldsymbol{\theta} \in \Theta} L(\boldsymbol{\theta})
$$

L'estremo superiore sull'intera partizione dello spazio $\Theta$ coincide con il massimo globale della funzione di verosimiglianza originaria $L(\boldsymbol{\theta})$, che per definizione è raggiunto nel punto $\hat{\boldsymbol{\theta}}_{\text{MLE}}$:

$$
\sup_{\boldsymbol{\theta} \in \Theta} L(\boldsymbol{\theta}) = L(\hat{\boldsymbol{\theta}}_{\text{MLE}})
$$

Sia $\boldsymbol{\alpha}^* = \mathbf{g}(\hat{\boldsymbol{\theta}}_{\text{MLE}})$. Poiché $\hat{\boldsymbol{\theta}}_{\text{MLE}} \in \mathbf{g}^{-1}(\boldsymbol{\alpha}^*)$, per la definizione di verosimiglianza indotta:

$$
\bar{L}(\boldsymbol{\alpha}^*) = \sup_{\boldsymbol{\theta} \in \mathbf{g}^{-1}(\boldsymbol{\alpha}^*)} L(\boldsymbol{\theta}) \ge L(\hat{\boldsymbol{\theta}}_{\text{MLE}})
$$

D'altra parte, poiché $\bar{L}(\boldsymbol{\alpha}) \le L(\hat{\boldsymbol{\theta}}_{\text{MLE}})$ per ogni $\boldsymbol{\alpha} \in \Omega$, deve necessariamente valere l'uguaglianza:

$$
\bar{L}(\boldsymbol{\alpha}^*) = L(\hat{\boldsymbol{\theta}}_{\text{MLE}}) = \max_{\boldsymbol{\alpha} \in \Omega} \bar{L}(\boldsymbol{\alpha})
$$

Di conseguenza, il punto di massimo della verosimiglianza indotta è esattamente:

$$
\hat{\boldsymbol{\alpha}}_{\text{MLE}} = \boldsymbol{\alpha}^* = \mathbf{g}(\hat{\boldsymbol{\theta}}_{\text{MLE}})
$$

Questo dimostra in piena generalità che per qualunque funzione $\mathbf{g}$, anche non biunivoca, la stima di massima verosimiglianza del parametro trasformato si ottiene applicando direttamente la trasformazione alla stima di massima verosimiglianza dei parametri originari.

## Ottimalità della Media a Posteriori per il Criterio MMSE

Nel paradigma bayesiano, il parametro da stimare $\theta$ è modellato come una variabile aleatoria avente densità di probabilità a priori $f_\theta(\theta)$. Il criterio di stima a minimo errore quadratico medio (__MMSE__, _Minimum Mean Square Error_) definisce la funzione di costo bayesiana (__BMSE__, _Bayesian Mean Square Error_):

$$
B_{\text{MSE}}(\hat{\theta}) = \mathbb{E}_{\mathbf{x}, \theta}\left[ (\theta - \hat{\theta}(\mathbf{x}))^2 \right] = \int_{\mathcal{X}} \int_{\Theta} (\theta - \hat{\theta}(\mathbf{x}))^2 f_{\mathbf{x}, \theta}(\mathbf{x}, \theta) \mathrm{d}\theta \mathrm{d}\mathbf{x}
$$

Dimostriamo in modo rigoroso e costruttivo che lo stimatore che minimizza globalmente il $B_{\text{MSE}}$ per qualsiasi realizzazione campionaria $\mathbf{x}$ è la __media a posteriori__ $\mathbb{E}[\theta \mid \mathbf{x}]$.

### Dimostrazione Tramite Decomposizione del Valore Atteso Condizionato

Fattorizziamo la densità di probabilità congiunta secondo la regola di Bayes:

$$
f_{\mathbf{x}, \theta}(\mathbf{x}, \theta) = f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x}) f_{\mathbf{x}}(\mathbf{x})
$$

Sostituendo nell'espressione del BMSE e invertendo l'ordine di integrazione per il teorema di Fubini-Tonelli:

$$
B_{\text{MSE}}(\hat{\theta}) = \int_{\mathcal{X}} \left[ \int_{\Theta} (\theta - \hat{\theta}(\mathbf{x}))^2 f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x}) \mathrm{d}\theta \right] f_{\mathbf{x}}(\mathbf{x}) \mathrm{d}\mathbf{x} = \mathbb{E}_{\mathbf{x}}\left[ \mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \hat{\theta}(\mathbf{x}))^2 \mid \mathbf{x} \right] \right]
$$

Poiché la densità marginale dei dati $f_{\mathbf{x}}(\mathbf{x}) \ge 0$ è non negativa ovunque, la minimizzazione dell'integrale esterno su $\mathcal{X}$ equivale a minimizzare l'integrale interno condizionato per ogni singolo valore fissato del vettore osservato $\mathbf{x}$:

$$
\min_{\hat{\theta}(\mathbf{x})} \mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \hat{\theta}(\mathbf{x}))^2 \mid \mathbf{x} \right] = \min_{\hat{\theta}(\mathbf{x})} \int_{\Theta} (\theta - \hat{\theta}(\mathbf{x}))^2 f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x}) \mathrm{d}\theta
$$

Definiamo la media a posteriori $\mu_{\theta \mid \mathbf{x}} = \mathbb{E}[\theta \mid \mathbf{x}] = \int_{\Theta} \theta f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x}) \mathrm{d}\theta$. Aggiungiamo e sottraiamo $\mu_{\theta \mid \mathbf{x}}$ all'interno del quadrato dell'errore:

$$
\theta - \hat{\theta}(\mathbf{x}) = (\theta - \mu_{\theta \mid \mathbf{x}}) + (\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))
$$

Sviluppiamo il quadrato del binomio:

$$
(\theta - \hat{\theta}(\mathbf{x}))^2 = (\theta - \mu_{\theta \mid \mathbf{x}})^2 + (\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))^2 + 2 (\theta - \mu_{\theta \mid \mathbf{x}})(\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))
$$

Calcoliamo il valore atteso condizionato rispetto alla PDF a posteriori $f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x})$:

$$
\mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \hat{\theta}(\mathbf{x}))^2 \mid \mathbf{x} \right] = \mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \mu_{\theta \mid \mathbf{x}})^2 \mid \mathbf{x} \right] + (\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))^2 + 2 (\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x})) \mathbb{E}_{\theta \mid \mathbf{x}}\left[ \theta - \mu_{\theta \mid \mathbf{x}} \mid \mathbf{x} \right]
$$

Il termine incrociato si annulla identicamente per definizione di media condizionata:

$$
\mathbb{E}_{\theta \mid \mathbf{x}}\left[ \theta - \mu_{\theta \mid \mathbf{x}} \mid \mathbf{x} \right] = \mathbb{E}_{\theta \mid \mathbf{x}}[\theta \mid \mathbf{x}] - \mu_{\theta \mid \mathbf{x}} = \mu_{\theta \mid \mathbf{x}} - \mu_{\theta \mid \mathbf{x}} = 0
$$

Otteniamo quindi l'identità fondamentale:

$$
\mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \hat{\theta}(\mathbf{x}))^2 \mid \mathbf{x} \right] = \text{Var}\{\theta \mid \mathbf{x}\} + (\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))^2
$$

dove $\text{Var}\{\theta \mid \mathbf{x}\} = \mathbb{E}_{\theta \mid \mathbf{x}}\left[ (\theta - \mu_{\theta \mid \mathbf{x}})^2 \mid \mathbf{x} \right]$ rappresenta la varianza della PDF a posteriori, la quale non dipende dalla scelta dello stimatore $\hat{\theta}(\mathbf{x})$.

Poiché $(\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}))^2 \ge 0$, il valore minimo dell'errore quadratico condizionato si ottiene se e solo se tale termine quadratico si annulla:

$$
\mu_{\theta \mid \mathbf{x}} - \hat{\theta}(\mathbf{x}) = 0 \iff \hat{\theta}_{\text{MMSE}}(\mathbf{x}) = \mu_{\theta \mid \mathbf{x}} = \mathbb{E}[\theta \mid \mathbf{x}]
$$

Il valore minimo del BMSE raggiungibile dallo stimatore ottimo è pari al valore atteso della varianza a posteriori:

$$
B_{\text{MSE}}(\hat{\theta}_{\text{MMSE}}) = \mathbb{E}_{\mathbf{x}}\left[ \text{Var}\{\theta \mid \mathbf{x}\} \right] = \int_{\mathcal{X}} \sigma_{\theta \mid \mathbf{x}}^2 f_{\mathbf{x}}(\mathbf{x}) \mathrm{d}\mathbf{x}
$$

Nel caso vettoriale $\boldsymbol{\theta} \in \mathbb{R}^P$, la medesima minimizzazione applicata a ciascuna componente scalare conduce immediatamente a $\hat{\boldsymbol{\theta}}_{\text{MMSE}} = \mathbb{E}[\boldsymbol{\theta} \mid \mathbf{x}]$, con matrice di errore bayesiano pari al valor medio della matrice di covarianza a posteriori $\mathbf{C}_{\boldsymbol{\theta} \mid \mathbf{x}}$.

## Aggiornamento Gaussiano e Completamento del Quadrato per la Stima Bayesiana DC

Consideriamo il modello di misura scalare con rumore bianco Gaussiano:

$$
x[n] = \theta + w[n], \quad n = 0, \dots, N-1, \quad w[n] \sim \mathcal{N}(0, \sigma^2) \quad \text{i.i.d.}
$$

con parametro incognito avente distribuzione a priori Gaussiana:

$$
\theta \sim \mathcal{N}(\mu_\theta, \sigma_\theta^2)
$$

Vogliamo determinare la forma analitica esatta della PDF a posteriori $f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x})$.

### Derivazione dell'Esponente e Regola delle Precisioni

Applicando il teorema di Bayes, la densità a posteriori è proporzionale al prodotto tra la verosimiglianza condizionata e la prior:

$$
f_{\theta \mid \mathbf{x}}(\theta \mid \mathbf{x}) \propto f_{\mathbf{x} \mid \theta}(\mathbf{x} \mid \theta) f_\theta(\theta)
$$

Esplicitiamo le distribuzioni gaussiane:

$$
f_{\mathbf{x} \mid \theta}(\mathbf{x} \mid \theta) = \frac{1}{(2\pi \sigma^2)^{N/2}} \exp\left( -\frac{1}{2\sigma^2} \sum_{n=0}^{N-1} (x[n] - \theta)^2 \right)
$$

$$
f_\theta(\theta) = \frac{1}{\sqrt{2\pi \sigma_\theta^2}} \exp\left( -\frac{1}{2\sigma_\theta^2} (\theta - \mu_\theta)^2 \right)
$$

Isoliamo l'esponente totale $Q(\theta)$ (trascurando i fattori indipendenti da $\theta$):

$$
Q(\theta) = -\frac{1}{2} \left[ \frac{(\theta - \mu_\theta)^2}{\sigma_\theta^2} + \frac{\sum_{n=0}^{N-1} (x[n] - \theta)^2}{\sigma^2} \right]
$$

Sviluppiamo la sommatoria nel secondo addendo:

$$
\sum_{n=0}^{N-1} (x[n] - \theta)^2 = \sum_{n=0}^{N-1} x^2[n] - 2\theta \sum_{n=0}^{N-1} x[n] + N\theta^2 = \sum_{n=0}^{N-1} x^2[n] - 2N\bar{x}\theta + N\theta^2
$$

dove $\bar{x} = \frac{1}{N}\sum_{n=0}^{N-1} x[n]$ è la media campionaria. Raggruppiamo i termini quadratici e lineari in $\theta$ nell'espressione $-2 Q(\theta)$:

$$
-2 Q(\theta) = \frac{\theta^2 - 2\mu_\theta \theta + \mu_\theta^2}{\sigma_\theta^2} + \frac{N\theta^2 - 2N\bar{x}\theta + \sum x^2[n]}{\sigma^2}
$$

$$
-2 Q(\theta) = \left( \frac{1}{\sigma_\theta^2} + \frac{N}{\sigma^2} \right) \theta^2 - 2 \left( \frac{\mu_\theta}{\sigma_\theta^2} + \frac{N\bar{x}}{\sigma^2} \right) \theta + \text{costante}
$$

Definiamo la precisione a priori $\lambda_\theta = \frac{1}{\sigma_\theta^2}$ e la precisione dei dati $\lambda_{\text{data}} = \frac{N}{\sigma^2}$. La precisione a posteriori $\lambda_{\theta \mid \mathbf{x}} = \frac{1}{\sigma_{\theta \mid \mathbf{x}}^2}$ è data dalla somma algebrica delle precisioni:

$$
\frac{1}{\sigma_{\theta \mid \mathbf{x}}^2} = \frac{1}{\sigma_\theta^2} + \frac{N}{\sigma^2} \implies \sigma_{\theta \mid \mathbf{x}}^2 = \frac{1}{\frac{1}{\sigma_\theta^2} + \frac{N}{\sigma^2}} = \frac{\sigma_\theta^2 \frac{\sigma^2}{N}}{\sigma_\theta^2 + \frac{\sigma^2}{N}}
$$

Completando il quadrato per la media a posteriori $\mu_{\theta \mid \mathbf{x}}$:

$$
-2 Q(\theta) = \frac{1}{\sigma_{\theta \mid \mathbf{x}}^2} \left[ \theta^2 - 2 \sigma_{\theta \mid \mathbf{x}}^2 \left( \frac{\mu_\theta}{\sigma_\theta^2} + \frac{N\bar{x}}{\sigma^2} \right) \theta \right] + \text{costante} = \frac{(\theta - \mu_{\theta \mid \mathbf{x}})^2}{\sigma_{\theta \mid \mathbf{x}}^2} + \text{costante}'
$$

da cui:

$$
\mu_{\theta \mid \mathbf{x}} = \sigma_{\theta \mid \mathbf{x}}^2 \left( \frac{\mu_\theta}{\sigma_\theta^2} + \frac{N\bar{x}}{\sigma^2} \right) = \frac{\frac{\sigma^2}{N}}{\sigma_\theta^2 + \frac{\sigma^2}{N}} \mu_\theta + \frac{\sigma_\theta^2}{\sigma_\theta^2 + \frac{\sigma^2}{N}} \bar{x}
$$

La PDF a posteriori è pertanto una Gaussiana univariata esatta $\mathcal{N}(\mu_{\theta \mid \mathbf{x}}, \sigma_{\theta \mid \mathbf{x}}^2)$, e la media condizionata $\mu_{\theta \mid \mathbf{x}}$ è una combinazione convessa ottimale tra la media a priori $\mu_\theta$ e la media campionaria dei dati $\bar{x}$.

## Lemma di Inversione Matriciale di Woodbury e Forme Duali dell'LMMSE

Nel modello vettoriale lineare bayesiano $\mathbf{x} = \mathbf{H}\boldsymbol{\theta} + \mathbf{w}$, con $\boldsymbol{\theta} \in \mathbb{R}^P$ e $\mathbf{x} \in \mathbb{R}^N$ ($N \ge P$), dove $\boldsymbol{\theta}$ e $\mathbf{w}$ sono incorrelati con medie e covarianze $(\boldsymbol{\mu}_{\boldsymbol{\theta}}, \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}})$ e $(\mathbf{0}, \mathbf{C}_{\mathbf{w}\mathbf{w}})$, lo stimatore lineare LMMSE assume due forme algebriche equivalenti che differiscono per la dimensione della matrice da invertire.

### Dimostrazione dell'Identità di Woodbury

Il __Lemma di Inversione Matriciale__ (formula di Sherman-Morrison-Woodbury) stabilisce che per matrici di dimensioni compatibili:

$$
(\mathbf{A} + \mathbf{B}\mathbf{C}\mathbf{D})^{-1} = \mathbf{A}^{-1} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} \mathbf{D}\mathbf{A}^{-1}
$$

Verifichiamo l'identità moltiplicando a destra il secondo membro per $(\mathbf{A} + \mathbf{B}\mathbf{C}\mathbf{D})$:

$$
\left[ \mathbf{A}^{-1} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} \mathbf{D}\mathbf{A}^{-1} \right] (\mathbf{A} + \mathbf{B}\mathbf{C}\mathbf{D})
$$

Espandendo i quattro prodotti matriciali:

$$
= \mathbf{I} + \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} \mathbf{D} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} \mathbf{D}\mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D}
$$

Raccogliamo a fattor comune a sinistra $\mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1}$ e a destra $\mathbf{C}\mathbf{D}$:

$$
= \mathbf{I} + \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} \left[ \mathbf{I} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B}\mathbf{C} \right] \mathbf{D}
$$

Notando che $[\mathbf{I} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B}\mathbf{C}] = [\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B}]\mathbf{C}$:

$$
= \mathbf{I} + \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} - \mathbf{A}^{-1}\mathbf{B} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B})^{-1} (\mathbf{C}^{-1} + \mathbf{D}\mathbf{A}^{-1}\mathbf{B}) \mathbf{C}\mathbf{D}
$$

$$
= \mathbf{I} + \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} - \mathbf{A}^{-1}\mathbf{B} \mathbf{I} \mathbf{C}\mathbf{D} = \mathbf{I} + \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} - \mathbf{A}^{-1}\mathbf{B}\mathbf{C}\mathbf{D} = \mathbf{I}
$$

L'identità è così rigorosamente dimostrata.

### Applicazione alle Due Forme dell'LMMSE

Nel modello lineare vettoriale:
- Vettore valor medio osservato: $\boldsymbol{\mu}_{\mathbf{x}} = \mathbf{H}\boldsymbol{\mu}_{\boldsymbol{\theta}}$.
- Matrice di covarianza incrociata: $\mathbf{C}_{\boldsymbol{\theta}\mathbf{x}} = \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}} \mathbf{H}^T$.
- Matrice di covarianza delle osservazioni: $\mathbf{C}_{\mathbf{x}\mathbf{x}} = \mathbf{H}\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T + \mathbf{C}_{\mathbf{w}\mathbf{w}}$.

La prima forma dello stimatore LMMSE opera nello spazio dei dati ($N$ dimensioni) ed è data da:

$$
\hat{\boldsymbol{\theta}}_{\text{LMMSE}} = \boldsymbol{\mu}_{\boldsymbol{\theta}} + \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T (\mathbf{H}\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T + \mathbf{C}_{\mathbf{w}\mathbf{w}})^{-1} (\mathbf{x} - \mathbf{H}\boldsymbol{\mu}_{\boldsymbol{\theta}})
$$

Tale forma richiede l'inversione di una matrice $N \times N$.

Applicando l'identità di Woodbury a $(\mathbf{H}\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T + \mathbf{C}_{\mathbf{w}\mathbf{w}})^{-1}$ ponendo $\mathbf{A} = \mathbf{C}_{\mathbf{w}\mathbf{w}}$, $\mathbf{B} = \mathbf{H}$, $\mathbf{C} = \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}$ e $\mathbf{D} = \mathbf{H}^T$:

$$
(\mathbf{C}_{\mathbf{w}\mathbf{w}} + \mathbf{H}\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T)^{-1} = \mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1} - \mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H} (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}
$$

Moltiplicando a sinistra per $\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T$:

$$
\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T (\mathbf{C}_{\mathbf{w}\mathbf{w}} + \mathbf{H}\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T)^{-1} = \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1} - \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H} (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}
$$

Raccogliendo a fattor comune a destra il termine $(\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}$:

$$
= \left[ \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}} (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H}) - \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H} \right] (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}
$$

$$
= \left[ \mathbf{I}_P + \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H} - \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H} \right] (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}
$$

$$
= (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}
$$

Si ottiene così la __seconda forma duale__ dello stimatore LMMSE, operante nello spazio dei parametri ($P$ dimensioni):

$$
\hat{\boldsymbol{\theta}}_{\text{LMMSE}} = \boldsymbol{\mu}_{\boldsymbol{\theta}} + (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1} \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1} (\mathbf{x} - \mathbf{H}\boldsymbol{\mu}_{\boldsymbol{\theta}})
$$

e la relativa matrice di errore bayesiano BMSE:

$$
\mathbf{C}_{\boldsymbol{\epsilon}} = (\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} + \mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1}
$$

### Vantaggi Computazionali e Connessione con il BLUE Classico

1. __Efficienza Computazionale__: Quando il numero di osservazioni campionarie $N$ è molto maggiore del numero di parametri $P$ ($N \gg P$), calcolare l'inversa di ordine $P$ nella seconda forma richiede un costo $O(P^3)$ drasticamente inferiore al costo $O(N^3)$ della prima forma.
2. __Connessione col Limite Classico__: Nel limite in cui la conoscenza a priori diventa infinitamente vaga (distribuzione non informativa o diffusa, $\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}} \to \infty \implies \mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} \to \mathbf{0}$), la seconda forma collassa esattamente su:

$$
   \lim_{\mathbf{C}_{\boldsymbol{\theta}\boldsymbol{\theta}}^{-1} \to \mathbf{0}} \hat{\boldsymbol{\theta}}_{\text{LMMSE}} = (\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1}\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1} \mathbf{x} = \hat{\boldsymbol{\theta}}_{\text{BLUE}}
$$

   e la matrice di BMSE converge alla matrice di covarianza del BLUE classico $(\mathbf{H}^T\mathbf{C}_{\mathbf{w}\mathbf{w}}^{-1}\mathbf{H})^{-1}$. L'approccio classico emerge dunque come il caso limite dell'approccio bayesiano privo di informazione a priori.

## Dimostrazione Rigorosa del Teorema Fondamentale di Neyman-Pearson

Nel contesto della teoria della decisione binaria per ipotesi semplici, consideriamo due ipotesi statistiche:

$$
H_0: \mathbf{x} \sim f_{\mathbf{x}}(\mathbf{x}; H_0) \quad \text{vs} \quad H_1: \mathbf{x} \sim f_{\mathbf{x}}(\mathbf{x}; H_1)
$$

Il criterio di Neyman-Pearson formula il problema di progetto del rilevatore ottimo come la massimizzazione vincolata della probabilità di rilevazione $P_{\text{D}}$ imponendo che la probabilità di falso allarme non superi una costante prefissata $\alpha \in (0, 1)$:

$$
\max_{\mathcal{R}_1 \subseteq \mathcal{X}} P_{\text{D}} = \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x}; H_1) \mathrm{d}\mathbf{x} \quad \text{sotto il vincolo} \quad P_{\text{FA}} = \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} = \alpha
$$

dove $\mathcal{R}_1$ indica la regione di decisione in cui si accetta l'ipotesi $H_1$ ($\hat{H} = H_1$), mentre il complemento $\mathcal{R}_0 = \mathcal{X} \setminus \mathcal{R}_1$ corrisponde all'accettazione dell'ipotesi nulla $H_0$.

### Dimostrazione Variazionale tramite Moltiplicatori di Lagrange

Definiamo la funzione obiettivo lagrangiana introducendo il moltiplicatore scalare $\lambda$:

$$
F(\mathcal{R}_1, \lambda) = P_{\text{D}} - \lambda (P_{\text{FA}} - \alpha) = \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x}; H_1) \mathrm{d}\mathbf{x} - \lambda \left[ \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} - \alpha \right]
$$

Raggruppando gli integrali estesi alla medesima regione di decisione $\mathcal{R}_1$:

$$
F(\mathcal{R}_1, \lambda) = \int_{\mathcal{R}_1} \left[ f_{\mathbf{x}}(\mathbf{x}; H_1) - \lambda f_{\mathbf{x}}(\mathbf{x}; H_0) \right] \mathrm{d}\mathbf{x} + \lambda \alpha
$$

Poiché il termine $\lambda \alpha$ è una costante indipendente dalla scelta geometrica della regione $\mathcal{R}_1$, per massimizzare l'integrale dobbiamo includere in $\mathcal{R}_1$ tutti e soli i punti dello spazio dei campioni $\mathbf{x} \in \mathcal{X}$ per i quali la funzione integranda risulta strettamente positiva:

$$
f_{\mathbf{x}}(\mathbf{x}; H_1) - \lambda f_{\mathbf{x}}(\mathbf{x}; H_0) > 0
$$

Poiché $f_{\mathbf{x}}(\mathbf{x}; H_0) > 0$ quasi ovunque sul supporto, dividendo per $f_{\mathbf{x}}(\mathbf{x}; H_0)$:

$$
\frac{f_{\mathbf{x}}(\mathbf{x}; H_1)}{f_{\mathbf{x}}(\mathbf{x}; H_0)} - \lambda > 0 \iff \frac{f_{\mathbf{x}}(\mathbf{x}; H_1)}{f_{\mathbf{x}}(\mathbf{x}; H_0)} > \lambda
$$

Definendo la soglia scalare $\gamma = \lambda$ (con $\gamma > 0$) e il __Rapporto di Verosimiglianza__ (_Likelihood Ratio_):

$$
L(\mathbf{x}) = \frac{f_{\mathbf{x}}(\mathbf{x}; H_1)}{f_{\mathbf{x}}(\mathbf{x}; H_0)}
$$

la regola decisionale ottimale che massimizza la potenza del test è data dal __Likelihood Ratio Test (LRT)__:

$$
L(\mathbf{x}) \underset{H_0}{\overset{H_1}{\gtrless}} \gamma
$$

dove la soglia $\gamma$ è determinata univocamente risolvendo l'equazione integrale del vincolo:

$$
P_{\text{FA}} = \int_{\{\mathbf{x} : L(\mathbf{x}) > \gamma\}} f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} = \alpha
$$

### Dimostrazione di Ottimalità Assoluta (Lemma di Neyman-Pearson)

Dimostriamo che per qualunque altra regola di decisione concorrente definita da una regione $\mathcal{R}_1'$ avente probabilità di falso allarme ammissibile $P_{\text{FA}}' \le \alpha$, la probabilità di rilevazione $P_{\text{D}}'$ non può mai superare $P_{\text{D}}$.

Indichiamo con $\phi(\mathbf{x})$ la funzione indicatrice della regione ottima $\mathcal{R}_1$ e con $\phi'(\mathbf{x})$ quella della regione concorrente $\mathcal{R}_1'$:

$$
\phi(\mathbf{x}) = \begin{cases} 1 & \mathbf{x} \in \mathcal{R}_1 \\ 0 & \mathbf{x} \in \mathcal{R}_0 \end{cases}, \quad \phi'(\mathbf{x}) = \begin{cases} 1 & \mathbf{x} \in \mathcal{R}_1' \\ 0 & \mathbf{x} \in \mathcal{R}_0' \end{cases}
$$

Consideriamo la quantità puntuale:

$$
\Delta(\mathbf{x}) = [f_{\mathbf{x}}(\mathbf{x}; H_1) - \gamma f_{\mathbf{x}}(\mathbf{x}; H_0)] [\phi(\mathbf{x}) - \phi'(\mathbf{x})]
$$

Analizziamo il segno di $\Delta(\mathbf{x})$ per qualsiasi valore di $\mathbf{x} \in \mathcal{X}$:
1. Se $\mathbf{x} \in \mathcal{R}_1$: allora $f_{\mathbf{x}}(\mathbf{x}; H_1) - \gamma f_{\mathbf{x}}(\mathbf{x}; H_0) > 0$. Poiché $\phi(\mathbf{x}) = 1$ e $\phi'(\mathbf{x}) \in \{0, 1\}$, la differenza vale $\phi(\mathbf{x}) - \phi'(\mathbf{x}) \ge 0$. Il prodotto è quindi non negativo: $\Delta(\mathbf{x}) \ge 0$.
2. Se $\mathbf{x} \in \mathcal{R}_0$: allora $f_{\mathbf{x}}(\mathbf{x}; H_1) - \gamma f_{\mathbf{x}}(\mathbf{x}; H_0) \le 0$. Poiché $\phi(\mathbf{x}) = 0$ e $\phi'(\mathbf{x}) \in \{0, 1\}$, la differenza vale $\phi(\mathbf{x}) - \phi'(\mathbf{x}) \le 0$. Il prodotto di due termini non positivi è non negativo: $\Delta(\mathbf{x}) \ge 0$.

Pertanto, $\Delta(\mathbf{x}) \ge 0$ identicamente per ogni $\mathbf{x} \in \mathcal{X}$. Integrando sull'intero spazio campionario:

$$
\int_{\mathcal{X}} [f_{\mathbf{x}}(\mathbf{x}; H_1) - \gamma f_{\mathbf{x}}(\mathbf{x}; H_0)] [\phi(\mathbf{x}) - \phi'(\mathbf{x})] \mathrm{d}\mathbf{x} \ge 0
$$

Espandendo i termini dell'integrale:

$$
\int_{\mathcal{X}} \phi(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_1) \mathrm{d}\mathbf{x} - \int_{\mathcal{X}} \phi'(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_1) \mathrm{d}\mathbf{x} - \gamma \left[ \int_{\mathcal{X}} \phi(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} - \int_{\mathcal{X}} \phi'(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} \right] \ge 0
$$

Riconoscendo le definizioni delle probabilità di rilevazione e falso allarme:

$$
(P_{\text{D}} - P_{\text{D}}') - \gamma (P_{\text{FA}} - P_{\text{FA}}') \ge 0 \implies P_{\text{D}} - P_{\text{D}}' \ge \gamma (P_{\text{FA}} - P_{\text{FA}}')
$$

Poiché per ipotesi la regola ottima satura il vincolo $P_{\text{FA}} = \alpha$ mentre la regola concorrente soddisfa $P_{\text{FA}}' \le \alpha$, si ha $P_{\text{FA}} - P_{\text{FA}}' \ge 0$. Essendo $\gamma > 0$, il secondo membro è non negativo:

$$
P_{\text{D}} - P_{\text{D}}' \ge 0 \implies P_{\text{D}} \ge P_{\text{D}}'
$$

Questo certifica in modo universale e incondizionato che nessun rilevatore binario avente probabilità di falso allarme minore o uguale ad $\alpha$ può conseguire una probabilità di rilevazione superiore a quella del Likelihood Ratio Test di Neyman-Pearson.

## Derivazione Analitica della Funzione Q e Proprietà per il Calcolo delle Probabilità d'Errore

Nel calcolo analitico delle prestazioni dei rilevatori in presenza di rumore Gaussiano, la probabilità che una variabile normale standard superi una determinata soglia è espressa tramite la __funzione Q__ (nota anche come coda destra della distribuzione Gaussiana standard):

$$
Q(z) = \frac{1}{\sqrt{2\pi}} \int_z^{+\infty} \exp\left( -\frac{u^2}{2} \right) \mathrm{d}u
$$

Essa è collegata alla funzione d'errore complementare Gaussiana $\text{erfc}(x) = \frac{2}{\sqrt{\pi}}\int_x^{+\infty} e^{-t^2}\mathrm{d}t$ tramite la sostituzione $u = t\sqrt{2}$:

$$
Q(z) = \frac{1}{2} \text{erfc}\left( \frac{z}{\sqrt{2}} \right)
$$

### Proprietà Fondamentali

1. __Valori notevoli e limiti__:

$$
   Q(-\infty) = 1, \quad Q(0) = \frac{1}{2}, \quad Q(+\infty) = 0
$$

2. __Simmetria__:
   In virtù della parità della densità Gaussiana normale:

$$
   Q(-z) = 1 - Q(z)
$$

3. __Monotonia e Derivata__:
   La funzione è strettamente decrescente su $\mathbb{R}$. Applicando il teorema fondamentale del calcolo integrale:

$$
   \frac{\mathrm{d}Q(z)}{\mathrm{d}z} = -\frac{1}{\sqrt{2\pi}} \exp\left( -\frac{z^2}{2} \right) < 0 \quad \forall z \in \mathbb{R}
$$

   Di conseguenza, la funzione ammette funzione inversa $Q^{-1}: (0, 1) \to \mathbb{R}$ anch'essa strettamente decrescente e biunivoca.

## Dimostrazione Analitica della Pendenza e Concavità della Curva ROC

La curva ROC (_Receiver Operating Characteristic_) descrive la traiettoria parametrica della probabilità di rilevazione $P_{\text{D}}(\gamma)$ in funzione della probabilità di falso allarme $P_{\text{FA}}(\gamma)$ al variare della soglia decisionale $\gamma \in [0, +\infty)$ per il test del rapporto di verosimiglianza:

$$
L(\mathbf{x}) = \frac{f_{\mathbf{x}}(\mathbf{x}; H_1)}{f_{\mathbf{x}}(\mathbf{x}; H_0)} \underset{H_0}{\overset{H_1}{\gtrless}} \gamma
$$

Dimostriamo in modo rigoroso due proprietà fondamentali della curva ROC per l'LRT:
1. La pendenza locale della retta tangente in ogni punto coincide esattamente con il valore della soglia $\gamma$: $\frac{\mathrm{d}P_{\text{D}}}{\mathrm{d}P_{\text{FA}}} = \gamma$.
2. La curva ROC dell'LRT è strettamente concava verso il basso: $\frac{\mathrm{d}^2 P_{\text{D}}}{\mathrm{d}P_{\text{FA}}^2} \le 0$.

### Identità Fondamentale tra le Distribuzioni del Rapporto di Verosimiglianza

Sia $l = L(\mathbf{x})$ la variabile aleatoria scalare corrispondente alla statistica di test LRT, avente densità di probabilità $f_l(l; H_0)$ sotto $H_0$ e $f_l(l; H_1)$ sotto $H_1$.
Valutiamo il momento di ordine $n$ di $l$ sotto l'ipotesi alternativa $H_1$:

$$
\mathbb{E}[l^n \mid H_1] = \int_{\mathcal{X}} L^n(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_1) \mathrm{d}\mathbf{x}
$$

Moltiplicando e dividendo l'integrando per $f_{\mathbf{x}}(\mathbf{x}; H_0)$:

$$
\mathbb{E}[l^n \mid H_1] = \int_{\mathcal{X}} L^n(\mathbf{x}) \frac{f_{\mathbf{x}}(\mathbf{x}; H_1)}{f_{\mathbf{x}}(\mathbf{x}; H_0)} f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} = \int_{\mathcal{X}} L^n(\mathbf{x}) L(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x}
$$

$$
\mathbb{E}[l^n \mid H_1] = \int_{\mathcal{X}} L^{n+1}(\mathbf{x}) f_{\mathbf{x}}(\mathbf{x}; H_0) \mathrm{d}\mathbf{x} = \mathbb{E}[l^{n+1} \mid H_0]
$$

Riscrivendo l'uguaglianza in termini delle densità unidimensionali della variabile aleatoria $l$:

$$
\int_0^{+\infty} l^n f_l(l; H_1) \mathrm{d}l = \int_0^{+\infty} l^{n+1} f_l(l; H_0) \mathrm{d}l = \int_0^{+\infty} l^n [l f_l(l; H_0)] \mathrm{d}l
$$

Poiché tale identità sussiste per qualunque intero $n \ge 0$, per l'unicità del problema dei momenti le due funzioni integrande devono coincidere quasi ovunque:

$$
f_l(l; H_1) = l f_l(l; H_0) \iff \frac{f_l(l; H_1)}{f_l(l; H_0)} = l
$$

La densità del rapporto di verosimiglianza sotto $H_1$ è data dalla densità sotto $H_0$ riscalata linearmente per il valore $l$ stesso.

### Calcolo della Pendenza della Curva ROC

Esprimiamo le probabilità operative come integrali della densità della statistica di test rispetto alla soglia $\gamma$:

$$
P_{\text{D}}(\gamma) = \text{Pr}\{l > \gamma \mid H_1\} = \int_\gamma^{+\infty} f_l(l; H_1) \mathrm{d}l
$$

$$
P_{\text{FA}}(\gamma) = \text{Pr}\{l > \gamma \mid H_0\} = \int_\gamma^{+\infty} f_l(l; H_0) \mathrm{d}l
$$

Applicando il teorema di Leibniz per la derivazione di un integrale rispetto all'estremo inferiore:

$$
\frac{\mathrm{d}P_{\text{D}}}{\mathrm{d}\gamma} = -f_l(\gamma; H_1) = -\gamma f_l(\gamma; H_0)
$$

$$
\frac{\mathrm{d}P_{\text{FA}}}{\mathrm{d}\gamma} = -f_l(\gamma; H_0)
$$

Applicando la regola della catena per derivare $P_{\text{D}}$ rispetto a $P_{\text{FA}}$:

$$
\frac{\mathrm{d}P_{\text{D}}}{\mathrm{d}P_{\text{FA}}} = \frac{\frac{\mathrm{d}P_{\text{D}}}{\mathrm{d}\gamma}}{\frac{\mathrm{d}P_{\text{FA}}}{\mathrm{d}\gamma}} = \frac{-\gamma f_l(\gamma; H_0)}{-f_l(\gamma; H_0)} = \gamma
$$

La derivata prima della curva ROC in ogni punto corrisponde esattamente alla soglia $\gamma$ del test LRT. L'equazione della retta tangente alla ROC nel punto $(\alpha, \beta) = (P_{\text{FA}}(\gamma), P_{\text{D}}(\gamma))$ è pertanto:

$$
P_{\text{D}} - \beta = \gamma (P_{\text{FA}} - \alpha) \implies P_{\text{D}} = \gamma P_{\text{FA}} + \beta - \gamma \alpha
$$

### Dimostrazione della Concavità

Valutiamo la derivata seconda della curva ROC:

$$
\frac{\mathrm{d}^2 P_{\text{D}}}{\mathrm{d}P_{\text{FA}}^2} = \frac{\mathrm{d}}{\mathrm{d}P_{\text{FA}}}\left( \frac{\mathrm{d}P_{\text{D}}}{\mathrm{d}P_{\text{FA}}} \right) = \frac{\mathrm{d}\gamma}{\mathrm{d}P_{\text{FA}}} = \frac{1}{\frac{\mathrm{d}P_{\text{FA}}}{\mathrm{d}\gamma}} = \frac{1}{-f_l(\gamma; H_0)} = -\frac{1}{f_l(\gamma; H_0)}
$$

Poiché la densità di probabilità è non negativa ovunque ($f_l(\gamma; H_0) \ge 0$), la derivata seconda è non positiva:

$$
\frac{\mathrm{d}^2 P_{\text{D}}}{\mathrm{d}P_{\text{FA}}^2} \le 0 \quad \forall \gamma \in (0, +\infty)
$$

Questo dimostra che la curva ROC di qualsiasi test LRT è __strettamente concava verso il basso__.
Al crescere di $P_{\text{FA}}$ (che corrisponde a diminuire la soglia $\gamma$ da $+\infty$ a $0$), la pendenza $\gamma$ decresce monotonicamente: per ogni incremento di falso allarme concesso, il guadagno marginale in rilevazione $\Delta P_{\text{D}}$ si riduce progressivamente (rendimenti marginali decrescenti).

## Derivazione Completa del Rischio di Bayes e Struttura a Costo Minimo

Nel problema di decisione bayesiana binaria, a ciascun esito decisionale è associato un costo economico o operativo $C_{ij} \in \mathbb{R}$, definito come il costo sostenuto decidendo per l'ipotesi $\hat{H} = H_i$ quando lo stato reale del sistema è $H_j$ ($i, j \in \{0, 1\}$).

La matrice dei costi assume la forma:

$$
\mathbf{C} = \begin{bmatrix} C_{00} & C_{01} \\ C_{10} & C_{11} \end{bmatrix}
$$

dove in condizioni naturali il costo di una decisione errata supera il costo della corrispondente decisione corretta:

$$
C_{10} > C_{00} \quad \text{e} \quad C_{01} > C_{11}
$$

### Espressione del Rischio Medio

Il __Rischio di Bayes__ $R$ è definito come il valore atteso del costo:

$$
R = \mathbb{E}[C] = \sum_{i=0}^1 \sum_{j=0}^1 C_{ij} \text{Pr}\{\hat{H} = H_i, H_j\} = \sum_{i=0}^1 \sum_{j=0}^1 C_{ij} \text{Pr}\{\hat{H} = H_i \mid H_j\} \text{Pr}\{H_j\}
$$

Espandendo esplicitamente i quattro addendi:

$$
R = C_{00} \text{Pr}\{\hat{H} = H_0 \mid H_0\} \text{Pr}\{H_0\} + C_{10} \text{Pr}\{\hat{H} = H_1 \mid H_0\} \text{Pr}\{H_0\} + C_{01} \text{Pr}\{\hat{H} = H_0 \mid H_1\} \text{Pr}\{H_1\} + C_{11} \text{Pr}\{\hat{H} = H_1 \mid H_1\} \text{Pr}\{H_1\}
$$

Esprimendo le probabilità condizionate mediante $P_{\text{FA}}$ e $P_{\text{D}}$:
- $\text{Pr}\{\hat{H} = H_1 \mid H_0\} = P_{\text{FA}}$, $\text{Pr}\{\hat{H} = H_0 \mid H_0\} = 1 - P_{\text{FA}}$.
- $\text{Pr}\{\hat{H} = H_1 \mid H_1\} = P_{\text{D}}$, $\text{Pr}\{\hat{H} = H_0 \mid H_1\} = 1 - P_{\text{D}}$.

Sostituendo:

$$
R = C_{00} (1 - P_{\text{FA}}) \text{Pr}\{H_0\} + C_{10} P_{\text{FA}} \text{Pr}\{H_0\} + C_{01} (1 - P_{\text{D}}) \text{Pr}\{H_1\} + C_{11} P_{\text{D}} \text{Pr}\{H_1\}
$$

Raggruppiamo i termini costanti indipendenti dalla partizione decisionale in una costante $K$:

$$
K = C_{00} \text{Pr}\{H_0\} + C_{01} \text{Pr}\{H_1\}
$$

Il rischio si riscrive come:

$$
R = K + (C_{10} - C_{00}) P_{\text{FA}} \text{Pr}\{H_0\} - (C_{01} - C_{11}) P_{\text{D}} \text{Pr}\{H_1\}
$$

### Minimizzazione Integrale del Rischio

Esplicitiamo le definizioni integrali di $P_{\text{FA}}$ e $P_{\text{D}}$ estese alla regione critica $\mathcal{R}_1$:

$$
R = K + (C_{10} - C_{00}) \text{Pr}\{H_0\} \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x} \mid H_0) \mathrm{d}\mathbf{x} - (C_{01} - C_{11}) \text{Pr}\{H_1\} \int_{\mathcal{R}_1} f_{\mathbf{x}}(\mathbf{x} \mid H_1) \mathrm{d}\mathbf{x}
$$

Combinando gli integrali:

$$
R = K + \int_{\mathcal{R}_1} \left[ (C_{10} - C_{00}) \text{Pr}\{H_0\} f_{\mathbf{x}}(\mathbf{x} \mid H_0) - (C_{01} - C_{11}) \text{Pr}\{H_1\} f_{\mathbf{x}}(\mathbf{x} \mid H_1) \right] \mathrm{d}\mathbf{x}
$$

Per minimizzare $R$, dobbiamo includere nella regione di decisione $\mathcal{R}_1$ tutti e soli i punti $\mathbf{x} \in \mathcal{X}$ che rendono la funzione integranda strettamente negativa:

$$
(C_{10} - C_{00}) \text{Pr}\{H_0\} f_{\mathbf{x}}(\mathbf{x} \mid H_0) - (C_{01} - C_{11}) \text{Pr}\{H_1\} f_{\mathbf{x}}(\mathbf{x} \mid H_1) < 0
$$

Portando il secondo termine a destra:

$$
(C_{01} - C_{11}) \text{Pr}\{H_1\} f_{\mathbf{x}}(\mathbf{x} \mid H_1) > (C_{10} - C_{00}) \text{Pr}\{H_0\} f_{\mathbf{x}}(\mathbf{x} \mid H_0)
$$

Poiché per ipotesi $(C_{01} - C_{11}) > 0$ e $\text{Pr}\{H_1\} > 0$, dividendo ambo i membri:

$$
\frac{f_{\mathbf{x}}(\mathbf{x} \mid H_1)}{f_{\mathbf{x}}(\mathbf{x} \mid H_0)} > \frac{(C_{10} - C_{00}) \text{Pr}\{H_0\}}{(C_{01} - C_{11}) \text{Pr}\{H_1\}}
$$

Si ottiene così la regola ottima del __Likelihood Ratio Test con soglia bayesiana__:

$$
L(\mathbf{x}) = \frac{f_{\mathbf{x}}(\mathbf{x} \mid H_1)}{f_{\mathbf{x}}(\mathbf{x} \mid H_0)} \underset{H_0}{\overset{H_1}{\gtrless}} \gamma_{\text{Bayes}}
$$

con soglia ottima scalare:

$$
\gamma_{\text{Bayes}} = \frac{(C_{10} - C_{00}) \text{Pr}\{H_0\}}{(C_{01} - C_{11}) \text{Pr}\{H_1\}}
$$

### Relazione con la Probabilità a Posteriori (Odds a Posteriori)

Moltiplicando ambo i membri della disuguaglianza per $\frac{\text{Pr}\{H_1\}}{\text{Pr}\{H_0\}}$:

$$
\frac{f_{\mathbf{x}}(\mathbf{x} \mid H_1) \text{Pr}\{H_1\}}{f_{\mathbf{x}}(\mathbf{x} \mid H_0) \text{Pr}\{H_0\}} > \frac{C_{10} - C_{00}}{C_{01} - C_{11}}
$$

Ricordando che per la formula di Bayes $\text{Pr}\{H_i \mid \mathbf{x}\} = \frac{f_{\mathbf{x}}(\mathbf{x} \mid H_i)\text{Pr}\{H_i\}}{f_{\mathbf{x}}(\mathbf{x})}$:

$$
\frac{\text{Pr}\{H_1 \mid \mathbf{x}\}}{\text{Pr}\{H_0 \mid \mathbf{x}\}} \underset{H_0}{\overset{H_1}{\gtrless}} \frac{C_{10} - C_{00}}{C_{01} - C_{11}}
$$

Il rilevatore a minimo rischio di Bayes confronta il rapporto tra le probabilità a posteriori delle due ipotesi (_posterior odds_) con il rapporto tra i costi differenziali netti dei due tipi di errore.
Nel caso particolare in cui le decisioni corrette siano a costo nullo ($C_{00} = C_{11} = 0$) e gli errori siano penalizzati con costo unitario uniforme ($C_{10} = C_{01} = 1$), la soglia vale $\frac{1 - 0}{1 - 0} = 1$, e la regola collassa esattamente sul rilevatore __MAP__ ($\text{Pr}\{H_1 \mid \mathbf{x}\} > \text{Pr}\{H_0 \mid \mathbf{x}\}$), dimostrando che la minimizzazione della probabilità d'errore è un caso speciale di rischio bayesiano simmetrico.

## Ottimalità del Criterio MAP per Ipotesi Multiple e Partizione dello Spazio

Nel problema di decisione statistica tra $M > 2$ ipotesi alternative $H_0, H_1, \dots, H_{M-1}$, si dispone di una distribuzione a priori nota:

$$
\text{Pr}\{H_j\} = \pi_j > 0, \qquad \sum_{j=0}^{M-1} \pi_j = 1
$$

e di densità condizionate $f(\mathbf{x} \mid H_j)$ su $\mathbb{R}^N$. Una regola decisionale corrisponde a una partizione dello spazio campionario $\mathbb{R}^N$ in $M$ regioni disgiunte $R_0, R_1, \dots, R_{M-1}$, tali per cui:

$$
R_i \cap R_j = \emptyset \quad \forall i \neq j, \qquad \bigcup_{i=0}^{M-1} R_i = \mathbb{R}^N
$$

con la convenzione che si decide l'ipotesi $\hat{H} = H_i$ se e solo se l'osservazione $\mathbf{x} \in R_i$.

Si assegni la matrice dei costi $C_{ij}$ associata al decidere $H_i$ quando lo stato reale è $H_j$, con la condizione naturale $C_{ij} > C_{jj}$ per ogni $i \neq j$. Il rischio medio di Bayes è:

$$
R = \sum_{i=0}^{M-1} \sum_{j=0}^{M-1} C_{ij} \, \text{Pr}\{\hat{H} = H_i \mid H_j\} \, \text{Pr}\{H_j\} = \sum_{i=0}^{M-1} \sum_{j=0}^{M-1} C_{ij} \, \pi_j \int_{R_i} f(\mathbf{x} \mid H_j) \, \mathrm{d}\mathbf{x}
$$

Scambiando la sommatoria con l'integrale:

$$
R = \sum_{i=0}^{M-1} \int_{R_i} \left[ \sum_{j=0}^{M-1} C_{ij} \, \pi_j \, f(\mathbf{x} \mid H_j) \right] \mathrm{d}\mathbf{x}
$$

Il termine tra parentesi quadre rappresenta il costo medio condizionato di decidere per la regione $R_i$ dato $\mathbf{x}$:

$$
c_i(\mathbf{x}) = \sum_{j=0}^{M-1} C_{ij} \, \pi_j \, f(\mathbf{x} \mid H_j)
$$

Poiché le regioni $\{R_i\}$ formano una partizione disgiunta e completa di $\mathbb{R}^N$, per minimizzare la somma complessiva $R = \sum_{i=0}^{M-1} \int_{R_i} c_i(\mathbf{x}) \, \mathrm{d}\mathbf{x}$ è necessario e sufficiente assegnare ciascun singolo punto $\mathbf{x} \in \mathbb{R}^N$ alla regione $R_k$ che minimizza il costo locale $c_k(\mathbf{x})$:

$$
\mathbf{x} \in R_k \iff c_k(\mathbf{x}) < c_i(\mathbf{x}) \quad \forall i \neq k
$$

### Caso Speciale: Costi Uniformi 0-1 e Probabilità d'Errore

Nel caso in cui le decisioni corrette abbiano costo nullo e tutti gli errori siano equiparati a costo unitario:

$$
C_{jj} = 0, \qquad C_{ij} = 1 \quad \forall i \neq j
$$

il costo locale $c_i(\mathbf{x})$ diventa:

$$
c_i(\mathbf{x}) = \sum_{j \neq i} \pi_j \, f(\mathbf{x} \mid H_j) = \sum_{j=0}^{M-1} \pi_j \, f(\mathbf{x} \mid H_j) - \pi_i \, f(\mathbf{x} \mid H_i) = f(\mathbf{x}) - \pi_i \, f(\mathbf{x} \mid H_i)
$$

dove $f(\mathbf{x}) = \sum_{j=0}^{M-1} \pi_j f(\mathbf{x} \mid H_j)$ è la densità marginale incondizionata delle osservazioni.

Sostituendo nell'espressione del rischio globale $R$:

$$
R = \sum_{i=0}^{M-1} \int_{R_i} \left[ f(\mathbf{x}) - \pi_i \, f(\mathbf{x} \mid H_i) \right] \mathrm{d}\mathbf{x} = \sum_{i=0}^{M-1} \int_{R_i} f(\mathbf{x}) \, \mathrm{d}\mathbf{x} - \sum_{i=0}^{M-1} \int_{R_i} \pi_i \, f(\mathbf{x} \mid H_i) \, \mathrm{d}\mathbf{x}
$$

Poiché $\bigcup_{i=0}^{M-1} R_i = \mathbb{R}^N$ e i sottoinsiemi sono disgiunti:

$$
\sum_{i=0}^{M-1} \int_{R_i} f(\mathbf{x}) \, \mathrm{d}\mathbf{x} = \int_{\mathbb{R}^N} f(\mathbf{x}) \, \mathrm{d}\mathbf{x} = 1
$$

Pertanto il rischio coincide con la probabilità totale d'errore $P_e$:

$$
P_e = R = 1 - \sum_{i=0}^{M-1} \int_{R_i} \pi_i \, f(\mathbf{x} \mid H_i) \, \mathrm{d}\mathbf{x}
$$

Il termine sottratto all'unità rappresenta la __probabilità di decisione corretta__ $P_c$:

$$
P_c = \sum_{i=0}^{M-1} \int_{R_i} \pi_i \, f(\mathbf{x} \mid H_i) \, \mathrm{d}\mathbf{x}
$$

Minimizzare l'errore $P_e$ equivale a massimizzare $P_c$. Per massimizzare la somma degli integrali su regioni disgiunte che ricoprono $\mathbb{R}^N$, ogni punto $\mathbf{x}$ deve essere assegnato alla regione $R_k$ per cui l'integrando $\pi_k f(\mathbf{x} \mid H_k)$ è massimo:

$$
\mathbf{x} \in R_k \iff \pi_k \, f(\mathbf{x} \mid H_k) > \pi_i \, f(\mathbf{x} \mid H_i) \quad \forall i \neq k
$$

Dividendo ambo i membri per la densità marginale comune $f(\mathbf{x}) > 0$, per il teorema di Bayes si ha $\text{Pr}\{H_i \mid \mathbf{x}\} = \frac{\pi_i f(\mathbf{x} \mid H_i)}{f(\mathbf{x})}$. Dunque:

$$
\mathbf{x} \in R_k \iff \text{Pr}\{H_k \mid \mathbf{x}\} > \text{Pr}\{H_i \mid \mathbf{x}\} \quad \forall i \neq k
$$

La regola ottima seleziona l'ipotesi con la massima probabilità a posteriori (__MAP__), provando rigorosamente che il decisore a minima probabilità d'errore coincide sempre con il rilevatore MAP per qualunque numero arbitrario di ipotesi $M \ge 2$.

## Teorema di Wilks e Proprietà Asintotiche del GLRT

Nel test di ipotesi composte, la densità di probabilità dei dati dipende da vettori di parametri incogniti:

$$
H_0: \boldsymbol{\theta} \in \boldsymbol{\Theta}_0, \qquad H_1: \boldsymbol{\theta} \in \boldsymbol{\Theta}_1
$$

Si consideri il caso nidificato in cui $\boldsymbol{\Theta}_0$ è un sottospazio di dimensione $p$ all'interno dello spazio parametrico $\boldsymbol{\Theta}_1$ di dimensione $p + r$, con $r \ge 1$ gradi di libertà aggiuntivi sotto l'ipotesi alternativa $H_1$.

La statistica del Generalized Likelihood Ratio Test (__GLRT__) è definita da:

$$
L_G(\mathbf{x}) = \frac{\sup_{\boldsymbol{\theta} \in \boldsymbol{\Theta}_1} f(\mathbf{x}; \boldsymbol{\theta})}{\sup_{\boldsymbol{\theta} \in \boldsymbol{\Theta}_0} f(\mathbf{x}; \boldsymbol{\theta})} = \frac{f(\mathbf{x}; \hat{\boldsymbol{\theta}}_1)}{f(\mathbf{x}; \hat{\boldsymbol{\theta}}_0)}
$$

dove $\hat{\boldsymbol{\theta}}_0$ e $\hat{\boldsymbol{\theta}}_1$ sono gli stimatori di massima verosimiglianza vincolati rispettivamente a $\boldsymbol{\Theta}_0$ e a $\boldsymbol{\Theta}_1$.

Si consideri la statistica due volte il log-rapporto di verosimiglianza:

$$
T_{\text{GLRT}}(\mathbf{x}) = 2 \ln L_G(\mathbf{x}) = 2 \left[ \ln f(\mathbf{x}; \hat{\boldsymbol{\theta}}_1) - \ln f(\mathbf{x}; \hat{\boldsymbol{\theta}}_0) \right]
$$

### Dimostrazione del Teorema di Wilks

Si espanda in serie di Taylor la log-verosimiglianza $\ln f(\mathbf{x}; \boldsymbol{\theta})$ attorno al vero valore del parametro $\boldsymbol{\theta}^* \in \boldsymbol{\Theta}_0$:

$$
\ln f(\mathbf{x}; \boldsymbol{\theta}) \approx \ln f(\mathbf{x}; \boldsymbol{\theta}^*) + \left[ \nabla_{\boldsymbol{\theta}} \ln f(\mathbf{x}; \boldsymbol{\theta}^*) \right]^T (\boldsymbol{\theta} - \boldsymbol{\theta}^*) - \frac{1}{2} (\boldsymbol{\theta} - \boldsymbol{\theta}^*)^T \mathbf{I}_N(\boldsymbol{\theta}^*) (\boldsymbol{\theta} - \boldsymbol{\theta}^*)
$$

dove $\mathbf{I}_N(\boldsymbol{\theta}^*)$ è la matrice di informazione di Fisher per le $N$ osservazioni indipendenti.

Nel punto di massimo $\hat{\boldsymbol{\theta}}$, il gradiente si annulla:

$$
\nabla_{\boldsymbol{\theta}} \ln f(\mathbf{x}; \hat{\boldsymbol{\theta}}) = \mathbf{0} \implies \nabla_{\boldsymbol{\theta}} \ln f(\mathbf{x}; \boldsymbol{\theta}^*) \approx \mathbf{I}_N(\boldsymbol{\theta}^*) (\hat{\boldsymbol{\theta}} - \boldsymbol{\theta}^*)
$$

Sostituendo questa relazione nell'espansione quadratica:

$$
\ln f(\mathbf{x}; \hat{\boldsymbol{\theta}}) - \ln f(\mathbf{x}; \boldsymbol{\theta}^*) \approx \frac{1}{2} (\hat{\boldsymbol{\theta}} - \boldsymbol{\theta}^*)^T \mathbf{I}_N(\boldsymbol{\theta}^*) (\hat{\boldsymbol{\theta}} - \boldsymbol{\theta}^*)
$$

Applicando questa approssimazione quadratica separatamente per il massimo non vincolato $\hat{\boldsymbol{\theta}}_1 \in \boldsymbol{\Theta}_1$ e per il massimo vincolato $\hat{\boldsymbol{\theta}}_0 \in \boldsymbol{\Theta}_0$, e sottraendo i due sviluppi, il termine $\ln f(\mathbf{x}; \boldsymbol{\theta}^*)$ si elide:

$$
T_{\text{GLRT}}(\mathbf{x}) \approx (\hat{\boldsymbol{\theta}}_1 - \boldsymbol{\theta}^*)^T \mathbf{I}_{N,1}(\boldsymbol{\theta}^*) (\hat{\boldsymbol{\theta}}_1 - \boldsymbol{\theta}^*) - (\hat{\boldsymbol{\theta}}_0 - \boldsymbol{\theta}^*)^T \mathbf{I}_{N,0}(\boldsymbol{\theta}^*) (\hat{\boldsymbol{\theta}}_0 - \boldsymbol{\theta}^*)
$$

Sotto l'ipotesi nulla $H_0$, per le proprietà asintotiche del MLE (consistenza e normalità asintotica), il vettore scostamento $(\hat{\boldsymbol{\theta}}_1 - \boldsymbol{\theta}^*)$ converge in distribuzione a una normale multivariata a media nulla:

$$
\sqrt{N} (\hat{\boldsymbol{\theta}}_1 - \boldsymbol{\theta}^*) \xrightarrow{d} \mathcal{N}\left( \mathbf{0}, \, \mathbf{I}_1^{-1}(\boldsymbol{\theta}^*) \right)
$$

La forma quadratica associata a uno spazio di dimensione $p + r$ vincolata a un sottospazio di dimensione $p$ proietta il vettore gaussiano sullo spazio ortogonale di dimensione $r = \dim(\boldsymbol{\Theta}_1) - \dim(\boldsymbol{\Theta}_0)$.
Per il teorema di Cochran, la differenza tra le due forme quadratiche indipendenti converge asintoticamente alla somma di $r$ variabili normali standard al quadrato indipendenti:

$$
T_{\text{GLRT}}(\mathbf{x}) = 2 \ln L_G(\mathbf{x}) \xrightarrow{d} \chi_r^2 \quad \text{sotto } H_0 \quad (\text{per } N \to \infty)
$$

Questo risultato fondamentale è noto come __Teorema di Wilks__ (1938). Il parametro $r$ rappresenta la differenza tra il numero di parametri liberi sotto $H_1$ e sotto $H_0$.

### Comportamento sotto l'Ipotesi Alternativa $H_1$

Quando è vera l'ipotesi alternativa $H_1$ e il parametro reale $\boldsymbol{\theta}_1^* \notin \boldsymbol{\Theta}_0$, lo scostamento presenta un valore atteso non nullo rispetto alla restrizione vincolata $\boldsymbol{\Theta}_0$. In questo caso, la distribuzione asintotica della statistica GLRT è una variabile aleatoria chi-quadro non centrale:

$$
T_{\text{GLRT}}(\mathbf{x}) \xrightarrow{d} \chi_r'^2(\lambda) \quad \text{sotto } H_1
$$

dove il __parametro di non centralità__ $\lambda$ è proporzionale all'energia del segnale utile pesata dall'informazione di Fisher:

$$
\lambda = (\boldsymbol{\theta}_1^* - \boldsymbol{\theta}_0^*)^T \mathbf{I}_N(\boldsymbol{\theta}^*) (\boldsymbol{\theta}_1^* - \boldsymbol{\theta}_0^*)
$$

Nel caso speciale del rilevamento di un livello DC incognito $A \neq 0$ immerso in rumore bianco gaussiano:
- Sotto $H_0$: $A = 0$ (spazio parametrico di dimensione $0$, ovvero $p = 0$).
- Sotto $H_1$: $A \neq 0$ (spazio parametrico di dimensione $1$, ovvero $p + r = 1 \implies r = 1$).

La statistica GLRT assume la forma esatta:

$$
T_{\text{GLRT}}(\mathbf{x}) = 2 \ln L_G(\mathbf{x}) = \frac{N \hat{A}_{\text{MLE}}^2}{\sigma_w^2} = \left( \frac{\sqrt{N} \bar{x}}{\sigma_w} \right)^2
$$

Poiché $\frac{\sqrt{N} \bar{x}}{\sigma_w} \sim \mathcal{N}(0, 1)$ sotto $H_0$, il quadrato di una normale standard ha esattamente per definizione distribuzione chi-quadro centrale a 1 grado di libertà:

$$
T_{\text{GLRT}}(\mathbf{x}) \sim \chi_1^2 \quad \text{sotto } H_0
$$

Sotto $H_1$, la variabile $\frac{\sqrt{N} \bar{x}}{\sigma_w}$ ha media non nulla pari a:

$$
\mathbb{E}\left[ \frac{\sqrt{N} \bar{x}}{\sigma_w} \right] = \frac{\sqrt{N} A}{\sigma_w} = d
$$

e varianza unitaria. Di conseguenza, il suo quadrato ha distribuzione chi-quadro non centrale a 1 grado di libertà con parametro di non centralità:

$$
\lambda = d^2 = \frac{N A^2}{\sigma_w^2} = \text{SNR}
$$

ovvero:

$$
T_{\text{GLRT}}(\mathbf{x}) \sim \chi_1'^2\left( \frac{N A^2}{\sigma_w^2} \right) \quad \text{sotto } H_1
$$

Questo conferma come la teoria asintotica generale di Wilks coincida esattamente con la distribuzione esatta a campioni finiti per il modello gaussiano lineare.

## Dimostrazione Assiomatica dell'Unicità dell'Entropia di Shannon-Khinchin

Nel suo articolo fondativo del 1948, Claude Shannon pose il problema di determinare se esista un'unica misura funzionale che quantifichi l'incertezza associata a una distribuzione di probabilità discreta su un insieme finito di $m$ eventi mutuamente esclusivi. Successivamente Aleksandr Khinchin (1957) ne formalizzò la struttura assiomatica.

Si consideri una famiglia di funzioni simmetriche $H_m(p_1, p_2, \dots, p_m)$ definite sul simplesso probabilistico standard:

$$
\Delta_m = \left\{ (p_1, \dots, p_m) \in \mathbb{R}^m \;\middle|\; p_i \ge 0, \; \sum_{i=1}^m p_i = 1 \right\}
$$

Si impongano i seguenti quattro assiomi fondamentali:

1. __Continuità__: Per ogni $m \ge 2$, la funzione $H_m(p_1, \dots, p_m)$ è continua rispetto a tutte le sue variabili sul simplesso $\Delta_m$.
2. __Monotonia stretta per distribuzioni uniformi__: Indicando con $A(m) = H_m\left(\frac{1}{m}, \dots, \frac{1}{m}\right)$ l'incertezza associata a una scelta equiprobabile tra $m$ alternative, la funzione $A(m)$ è strettamente crescente rispetto a $m$:

$$
A(m+1) > A(m) \quad \forall m \ge 1
$$

3. __Assioma di Raggruppamento (o Composizione)__: Se una scelta viene suddivisa in passi successivi, l'incertezza complessiva è la somma ponderata delle incertezze dei singoli passi:

$$
H_m(p_1, p_2, \dots, p_m) = H_{m-1}(p_1 + p_2, p_3, \dots, p_m) + (p_1 + p_2) \, H_2\left( \frac{p_1}{p_1+p_2}, \, \frac{p_2}{p_1+p_2} \right)
$$

4. __Normalizzazione__: Si fissa la scala di misura imponendo:

$$
H_2\left(\frac{1}{2}, \, \frac{1}{2}\right) = 1 \quad \text{bit}
$$

### Dimostrazione del Teorema di Unicità

La dimostrazione si articola in quattro passi costruttivi.

#### Passo 1: Proprietà moltiplicativa per potenze di interi

Si consideri una distribuzione uniforme su un alfabeto di $s^k$ simboli equiprobabili, con $s, k \in \mathbb{N}_{\ge 2}$.
Suddividendo gli $s^k$ elementi in $s$ gruppi disgiunti, ciascuno composto da $s^{k-1}$ elementi, per l'assioma di composizione l'incertezza totale è pari all'incertezza di selezionare uno degli $s$ gruppi, più l'incertezza condizionata di individuare l'elemento all'interno del gruppo selezionato (identica per tutti gli $s$ gruppi):

$$
A(s^k) = A(s) + A(s^{k-1})
$$

Applicando ricorsivamente questa relazione per $k$ volte si ottiene l'identità fondamentale:

$$
A(s^k) = k \, A(s)
$$

#### Passo 2: Derivazione della forma logaritmica per distribuzioni uniformi

Si considerino due interi arbitrari $m, l \ge 2$. Per ogni intero $n \ge 1$, esiste sempre un unico intero $k \ge 0$ tale per cui:

$$
m^k \le l^n < m^{k+1}
$$

Applicando il logaritmo naturale (funzione strettamente crescente):

$$
k \ln m \le n \ln l < (k+1) \ln m \implies \frac{k}{n} \le \frac{\ln l}{\ln m} < \frac{k+1}{n}
$$

da cui discende:

$$
\left| \frac{\ln l}{\ln m} - \frac{k}{n} \right| < \frac{1}{n}
$$

Parallelamente, per l'assioma di monotonia stretta ($A(a) \le A(b) \iff a \le b$):

$$
A(m^k) \le A(l^n) \le A(m^{k+1})
$$

Sfruttando la proprietà moltiplicativa ricavata nel Passo 1 ($A(s^k) = k A(s)$):

$$
k \, A(m) \le n \, A(l) \le (k+1) \, A(m) \implies \frac{k}{n} \le \frac{A(l)}{A(m)} \le \frac{k+1}{n}
$$

da cui:

$$
\left| \frac{A(l)}{A(m)} - \frac{k}{n} \right| \le \frac{1}{n}
$$

Combinando le due disuguaglianze tramite la disuguaglianza triangolare:

$$
\left| \frac{A(l)}{A(m)} - \frac{\ln l}{\ln m} \right| \le \left| \frac{A(l)}{A(m)} - \frac{k}{n} \right| + \left| \frac{k}{n} - \frac{\ln l}{\ln m} \right| < \frac{2}{n}
$$

Poiché questa relazione deve sussistere per qualsiasi valore di $n \in \mathbb{N}$, passando al limite per $n \to \infty$ il membro destro tende a zero, imponendo:

$$
\frac{A(l)}{A(m)} = \frac{\ln l}{\ln m} \implies \frac{A(l)}{\ln l} = \frac{A(m)}{\ln m} = C
$$

dove $C > 0$ è una costante positiva universale. Ne consegue che:

$$
A(m) = C \ln m = \log_b m \qquad \left( b = e^{1/C} \right)
$$

Imponendo l'assioma di normalizzazione $A(2) = H_2(1/2, 1/2) = 1$, si fissa univocamente la base del logaritmo a $b = 2$, ottenendo $A(m) = \log_2 m$.

#### Passo 3: Estensione a distribuzioni con probabilità razionali

Si consideri una distribuzione di probabilità in cui tutte le probabilità $p_i$ sono numeri razionali:

$$
p_i = \frac{n_i}{N}, \qquad n_i \in \mathbb{N}, \quad N = \sum_{i=1}^m n_i
$$

Si consideri un sistema ausiliario con $N$ eventi equiprobabili, ciascuno con probabilità $1/N$. L'incertezza totale è $A(N) = \log_2 N$.
Si raggruppino gli $N$ eventi in $m$ macro-eventi, dove il gruppo $i$-esimo contiene esattamente $n_i$ eventi. Per l'assioma di raggruppamento iterato:

$$
A(N) = H_m(p_1, \dots, p_m) + \sum_{i=1}^m p_i \, A(n_i)
$$

Sostituendo la forma logaritmica per le distribuzioni uniformi:

$$
\log_2 N = H_m(p_1, \dots, p_m) + \sum_{i=1}^m p_i \log_2 n_i
$$

Isolando $H_m(p_1, \dots, p_m)$ e ricordando che $\sum_{i=1}^m p_i = 1$:

$$
H_m(p_1, \dots, p_m) = \log_2 N - \sum_{i=1}^m p_i \log_2 n_i = \sum_{i=1}^m p_i \log_2 N - \sum_{i=1}^m p_i \log_2 n_i
$$

Raggruppando i logaritmi:

$$
H_m(p_1, \dots, p_m) = \sum_{i=1}^m p_i \left( \log_2 N - \log_2 n_i \right) = - \sum_{i=1}^m p_i \log_2 \left( \frac{n_i}{N} \right) = - \sum_{i=1}^m p_i \log_2 p_i
$$

#### Passo 4: Estensione a distribuzioni reali per continuità

Poiché l'insieme dei numeri razionali $\mathbb{Q} \cap [0, 1]$ è denso nell'intervallo reale $[0, 1]$, per qualsiasi vettore di probabilità reale $\mathbf{p} \in \Delta_m$ esiste una successione di vettori a componenti razionali $\mathbf{p}^{(k)} \in \Delta_m \cap \mathbb{Q}^m$ tale che $\lim_{k \to \infty} \mathbf{p}^{(k)} = \mathbf{p}$.
In virtù dell'assioma 1 (continuità di $H_m$ su $\Delta_m$), passando al limite per $k \to \infty$:

$$
H_m(p_1, \dots, p_m) = \lim_{k \to \infty} H_m(p_1^{(k)}, \dots, p_m^{(k)}) = \lim_{k \to \infty} \left[ - \sum_{i=1}^m p_i^{(k)} \log_2 p_i^{(k)} \right] = - \sum_{i=1}^m p_i \log_2 p_i
$$

La forma $H(X) = -\sum_{i=1}^m p_i \log_2 p_i$ è pertanto l'unica funzione che soddisfa simultaneamente i requisiti assiomatici di una misura quantitativa di informazione.

## Calcolo Asintotico dell'Entropia di Poisson con Approssimazione di Stirling

Si consideri una variabile aleatoria discreta $X$ distribuita secondo una legge di Poisson con parametro di intensità $\lambda > 0$ ($X \sim \text{Pois}(\lambda)$):

$$
p(k) = \text{Pr}\{X = k\} = \frac{\lambda^k e^{-\lambda}}{k!}, \qquad k = 0, 1, 2, \dots
$$

Si intende determinare il comportamento asintotico dell'entropia di Shannon di $X$ al divergere del parametro di intensità ($\lambda \to \infty$), dimostrando analiticamente come essa converga all'entropia di una distribuzione gaussiana continua avente la medesima varianza.

### Sviluppo Esatto dell'Entropia

Per definizione di entropia in unità naturali (nats):

$$
H_e(X) = - \sum_{k=0}^\infty p(k) \ln p(k)
$$

Esplicitando il logaritmo della probabilità di Poisson:

$$
\ln p(k) = \ln\left( \frac{\lambda^k e^{-\lambda}}{k!} \right) = k \ln \lambda - \lambda - \ln(k!)
$$

Sostituendo nell'espressione dell'entropia:

$$
H_e(X) = - \sum_{k=0}^\infty p(k) \left[ k \ln \lambda - \lambda - \ln(k!) \right] = - (\ln \lambda) \sum_{k=0}^\infty k \, p(k) + \lambda \sum_{k=0}^\infty p(k) + \sum_{k=0}^\infty p(k) \ln(k!)
$$

Ricordando che per la distribuzione di Poisson:

$$
\sum_{k=0}^\infty p(k) = 1, \qquad \mathbb{E}[X] = \sum_{k=0}^\infty k \, p(k) = \lambda
$$

si ottiene:

$$
H_e(X) = - \lambda \ln \lambda + \lambda + \mathbb{E}[\ln(X!)]
$$

### Sviluppo del Fattoriale tramite la Formula di Stirling

Per quantificare il termine $\mathbb{E}[\ln(X!)]$, si utilizza la formula asintotica di Stirling per il fattoriale:

$$
k! = \sqrt{2\pi k} \left(\frac{k}{e}\right)^k \left( 1 + O(1/k) \right)
$$

Prendendo il logaritmo naturale:

$$
\ln(k!) = k \ln k - k + \frac{1}{2}\ln(2\pi k) + O(1/k)
$$

Applicando l'operatore speranza matematica:

$$
\mathbb{E}[\ln(X!)] = \mathbb{E}[X \ln X] - \mathbb{E}[X] + \frac{1}{2}\mathbb{E}[\ln(2\pi X)] + O(1/\lambda)
$$

Essendo $\mathbb{E}[X] = \lambda$, l'entropia diventa:

$$
H_e(X) = -\lambda \ln \lambda + \lambda + \mathbb{E}[X \ln X] - \lambda + \frac{1}{2}\mathbb{E}[\ln(2\pi X)] + O(1/\lambda)
$$

I due termini lineari $\lambda$ e $-\lambda$ si elidono rigorosamente:

$$
H_e(X) = -\lambda \ln \lambda + \mathbb{E}[X \ln X] + \frac{1}{2}\mathbb{E}[\ln(2\pi X)] + O(1/\lambda)
$$

### Espansione in Serie di Taylor dei Valori Attesi

Si definisca lo scostamento aleatorio dalla media $\delta = X - \lambda$. Per le proprietà dei momenti della variabile di Poisson:

$$
\mathbb{E}[\delta] = 0, \qquad \mathbb{E}[\delta^2] = \text{Var}(X) = \lambda, \qquad \mathbb{E}[\delta^3] = \lambda, \qquad \mathbb{E}[\delta^4] = 3\lambda^2 + \lambda
$$

Si espanda la funzione $g(X) = X \ln X$ in serie di Taylor attorno al valore atteso $\lambda$:

$$
g(X) = (\lambda + \delta) \ln(\lambda + \delta) = (\lambda + \delta) \left[ \ln \lambda + \ln\left(1 + \frac{\delta}{\lambda}\right) \right]
$$

Sfruttando lo sviluppo in serie $\ln(1 + u) = u - \frac{u^2}{2} + \frac{u^3}{3} - \dots$ per $u = \delta/\lambda$:

$$
\ln\left(1 + \frac{\delta}{\lambda}\right) = \frac{\delta}{\lambda} - \frac{\delta^2}{2\lambda^2} + O\left(\frac{\delta^3}{\lambda^3}\right)
$$

Moltiplicando per $(\lambda + \delta)$:

$$
g(X) = (\lambda + \delta)\ln \lambda + (\lambda + \delta)\left[ \frac{\delta}{\lambda} - \frac{\delta^2}{2\lambda^2} + O\left(\frac{\delta^3}{\lambda^3}\right) \right]
$$

$$
g(X) = \lambda \ln \lambda + \delta \ln \lambda + \delta - \frac{\delta^2}{2\lambda} + \frac{\delta^2}{\lambda} + O\left(\frac{\delta^3}{\lambda^2}\right) = \lambda \ln \lambda + \delta(1 + \ln \lambda) + \frac{\delta^2}{2\lambda} + O\left(\frac{\delta^3}{\lambda^2}\right)
$$

Calcolando il valore atteso ed elidendo il termine lineare $\mathbb{E}[\delta] = 0$:

$$
\mathbb{E}[X \ln X] = \lambda \ln \lambda + \frac{\mathbb{E}[\delta^2]}{2\lambda} + O(1/\lambda) = \lambda \ln \lambda + \frac{\lambda}{2\lambda} + O(1/\lambda) = \lambda \ln \lambda + \frac{1}{2} + O(1/\lambda)
$$

Analogamente, si sviluppa in serie il termine logaritmico $\frac{1}{2}\ln(2\pi X)$:

$$
\frac{1}{2}\ln(2\pi X) = \frac{1}{2}\ln(2\pi(\lambda + \delta)) = \frac{1}{2}\ln(2\pi \lambda) + \frac{1}{2}\ln\left(1 + \frac{\delta}{\lambda}\right) = \frac{1}{2}\ln(2\pi \lambda) + \frac{\delta}{2\lambda} - \frac{\delta^2}{4\lambda^2} + \dots
$$

Prendendo il valore atteso:

$$
\frac{1}{2}\mathbb{E}[\ln(2\pi X)] = \frac{1}{2}\ln(2\pi \lambda) - \frac{\lambda}{4\lambda^2} + \dots = \frac{1}{2}\ln(2\pi \lambda) + O(1/\lambda)
$$

### Sintesi Asintotica Finale

Sostituendo i due valori attesi nell'espressione di $H_e(X)$:

$$
H_e(X) = -\lambda \ln \lambda + \left[ \lambda \ln \lambda + \frac{1}{2} + O(1/\lambda) \right] + \left[ \frac{1}{2}\ln(2\pi \lambda) + O(1/\lambda) \right]
$$

I termini $-\lambda \ln \lambda$ e $+\lambda \ln \lambda$ si elidono esattamente:

$$
H_e(X) = \frac{1}{2} + \frac{1}{2}\ln(2\pi \lambda) + O(1/\lambda) = \frac{1}{2}\ln(e) + \frac{1}{2}\ln(2\pi \lambda) + O(1/\lambda) = \frac{1}{2}\ln(2\pi e \lambda) + O(1/\lambda) \quad \text{nat}
$$

Convertendo la misura in base 2 (bit):

$$
H(X) = \frac{H_e(X)}{\ln 2} = \frac{1}{2}\log_2(2\pi e \lambda) + O\left(\frac{1}{\lambda}\right) \quad \text{bit}
$$

Poiché per il teorema del limite centrale $X \sim \text{Pois}(\lambda)$ converge per $\lambda \to \infty$ a una variabile gaussiana con media $\lambda$ e varianza $\sigma^2 = \lambda$, la cui entropia differenziale è esattamente $\frac{1}{2}\log_2(2\pi e \sigma^2)$, questo risultato prova analiticamente che l'entropia della distribuzione discreta di Poisson coincide asintoticamente con l'entropia della gaussiana equivalente.

## Dimostrazione Analitica della Disuguaglianza Log-Sum e Convessità Congiunta della Divergenza KL

### Enunciazione della Disuguaglianza Log-Sum

Siano date due sequenze finite di numeri reali non negativi $a_1, a_2, \dots, a_n$ e $b_1, b_2, \dots, b_n$, con $a_i \ge 0$ e $b_i \ge 0$ per ogni $i \in \{1, \dots, n\}$. La __disuguaglianza log-sum__ afferma che:

$$
\sum_{i=1}^n a_i \log \frac{a_i}{b_i} \ge \left( \sum_{i=1}^n a_i \right) \log \frac{\sum_{i=1}^n a_i}{\sum_{i=1}^n b_i}
$$

con uguaglianza se e solo se i rapporti $\frac{a_i}{b_i}$ sono costanti per tutti gli indici $i$ per cui $a_i > 0$, ovvero se esiste una costante $c > 0$ tale che $a_i = c \, b_i$.

Si adottano le usuali convenzioni di continuità fondate sul limite $\lim_{t \to 0^+} t \log t = 0$:
- $0 \log 0 = 0$
- $0 \log \frac{0}{0} = 0$
- $a \log \frac{a}{0} = +\infty$ per ogni $a > 0$
- $0 \log \frac{0}{b} = 0$ per ogni $b > 0$

### Dimostrazione Analitica tramite la Disuguaglianza di Jensen

Senza perdita di generalità, si considerino inizialmente $a_i > 0$ e $b_i > 0$ per ogni $i$. Si definisce la funzione reale di variabile reale $f: (0, +\infty) \to \mathbb{R}$:

$$
f(t) = t \log t
$$

Per stabilire la convessità di $f(t)$, si calcola la derivata prima rispetto alla base naturale (la scelta della base del logaritmo modifica solo un fattore moltiplicativo positivo $\frac{1}{\ln 2}$):

$$
f'(t) = \frac{d}{dt} (t \ln t) = \ln t + t \cdot \frac{1}{t} = 1 + \ln t
$$

Calcolando la derivata seconda:

$$
f''(t) = \frac{d}{dt} (1 + \ln t) = \frac{1}{t}
$$

Poiché $t > 0$, si ha $f''(t) > 0$ per ogni $t \in (0, +\infty)$. Di conseguenza, la funzione $f(t) = t \log t$ è __strettamente convessa__ su tutto il semiasse reale positivo.

Si applica ora la disuguaglianza di Jensen per funzioni convesse in forma pesata. Dati $n$ pesi normalizzati $\alpha_i \ge 0$ tali che $\sum_{i=1}^n \alpha_i = 1$ e $n$ punti $t_i > 0$, la disuguaglianza asserisce che:

$$
\sum_{i=1}^n \alpha_i f(t_i) \ge f\left( \sum_{i=1}^n \alpha_i t_i \right)
$$

Si scelgono specificamente i pesi $\alpha_i$ e le coordinate $t_i$ come segue:

$$
\alpha_i = \frac{b_i}{\sum_{j=1}^n b_j}, \qquad t_i = \frac{a_i}{b_i}
$$

Si osserva immediatamente che i coefficienti $\alpha_i$ costituiscono una valida combinazione convessa:

$$
\alpha_i \ge 0, \qquad \sum_{i=1}^n \alpha_i = \sum_{i=1}^n \frac{b_i}{\sum_{j=1}^n b_j} = \frac{\sum_{i=1}^n b_i}{\sum_{j=1}^n b_j} = 1
$$

Sostituendo $\alpha_i$ e $t_i$ nel membro sinistro della disuguaglianza di Jensen e moltiplicando entrambi i membri per la costante scalare positiva $\sum_{j=1}^n b_j$:

$$
\sum_{j=1}^n b_j \sum_{i=1}^n \alpha_i f(t_i) = \sum_{j=1}^n b_j \sum_{i=1}^n \left( \frac{b_i}{\sum_{j=1}^n b_j} \right) f\left( \frac{a_i}{b_i} \right) = \sum_{i=1}^n b_i f\left( \frac{a_i}{b_i} \right)
$$

Esplicitando $f(t) = t \log t$:

$$
\sum_{i=1}^n b_i f\left( \frac{a_i}{b_i} \right) = \sum_{i=1}^n b_i \left( \frac{a_i}{b_i} \log \frac{a_i}{b_i} \right) = \sum_{i=1}^n a_i \log \frac{a_i}{b_i}
$$

Si valuta ora l'argomento della funzione $f$ a secondo membro:

$$
\sum_{i=1}^n \alpha_i t_i = \sum_{i=1}^n \left( \frac{b_i}{\sum_{j=1}^n b_j} \right) \left( \frac{a_i}{b_i} \right) = \frac{\sum_{i=1}^n a_i}{\sum_{j=1}^n b_j}
$$

Applicando la funzione $f$ e riscalando per $\sum_{j=1}^n b_j$:

$$
\left( \sum_{j=1}^n b_j \right) f\left( \sum_{i=1}^n \alpha_i t_i \right) = \left( \sum_{j=1}^n b_j \right) f\left( \frac{\sum_{i=1}^n a_i}{\sum_{j=1}^n b_j} \right) = \left( \sum_{j=1}^n b_j \right) \left( \frac{\sum_{i=1}^n a_i}{\sum_{j=1}^n b_j} \log \frac{\sum_{i=1}^n a_i}{\sum_{j=1}^n b_j} \right)
$$

I fattori $\sum_{j=1}^n b_j$ si semplificano algebricamente:

$$
\left( \sum_{j=1}^n b_j \right) f\left( \sum_{i=1}^n \alpha_i t_i \right) = \left( \sum_{i=1}^n a_i \right) \log \frac{\sum_{i=1}^n a_i}{\sum_{j=1}^n b_j}
$$

Combinando i risultati ottenuti, si perviene esattamente alla formulazione della disuguaglianza log-sum:

$$
\sum_{i=1}^n a_i \log \frac{a_i}{b_i} \ge \left( \sum_{i=1}^n a_i \right) \log \frac{\sum_{i=1}^n a_i}{\sum_{i=1}^n b_i}
$$

Essendo $f$ strettamente convessa, l'uguaglianza in Jensen vale se e solo se tutti i punti $t_i$ sono identici, cioè $t_1 = t_2 = \dots = t_n$, il che implica:

$$
\frac{a_i}{b_i} = c \quad \forall i \in \{1, \dots, n\}
$$

Se alcuni $a_i$ o $b_i$ sono nulli, la validità discende immediatamente considerando il supporto $\{i : a_i > 0\}$ ed estendendo per continuità tramite i limiti dichiarati.

### Convessità Congiunta della Divergenza di Kullback-Leibler

Siano $(p_1, q_1)$ e $(p_2, q_2)$ due coppie distinte di funzioni di massa di probabilità definite sul medesimo alfabeto discreto $\mathcal{X}$. Per ogni scalare $\lambda \in [0, 1]$, si definiscano le distribuzioni mistura:

$$
p_\lambda(x) = \lambda p_1(x) + (1-\lambda) p_2(x), \qquad q_\lambda(x) = \lambda q_1(x) + (1-\lambda) q_2(x)
$$

Il teorema di __convessità congiunta__ stabilisce che la divergenza relativa $D(p \parallel q)$ è convessa nella coppia $(p, q)$:

$$
D(p_\lambda \parallel q_\lambda) \le \lambda D(p_1 \parallel q_1) + (1-\lambda) D(p_2 \parallel q_2)
$$

#### Dimostrazione

Per ciascun elemento fissato $x \in \mathcal{X}$, si applica la disuguaglianza log-sum con $n = 2$ termini, ponendo:

$$
a_1 = \lambda p_1(x), \quad a_2 = (1-\lambda) p_2(x), \quad b_1 = \lambda q_1(x), \quad b_2 = (1-\lambda) q_2(x)
$$

Le somme delle due coppie valgono:

$$
a_1 + a_2 = \lambda p_1(x) + (1-\lambda) p_2(x) = p_\lambda(x)
$$

$$
b_1 + b_2 = \lambda q_1(x) + (1-\lambda) q_2(x) = q_\lambda(x)
$$

La disuguaglianza log-sum applicata al punto $x$ assume la forma:

$$
(a_1 + a_2) \log \frac{a_1 + a_2}{b_1 + b_2} \le a_1 \log \frac{a_1}{b_1} + a_2 \log \frac{a_2}{b_2}
$$

Sostituendo le definizioni esplicite:

$$
p_\lambda(x) \log \frac{p_\lambda(x)}{q_\lambda(x)} \le \lambda p_1(x) \log \frac{\lambda p_1(x)}{\lambda q_1(x)} + (1-\lambda) p_2(x) \log \frac{(1-\lambda) p_2(x)}{(1-\lambda) q_2(x)}
$$

I fattori positivi $\lambda$ e $(1-\lambda)$ all'interno dei logaritmi si elidono:

$$
p_\lambda(x) \log \frac{p_\lambda(x)}{q_\lambda(x)} \le \lambda p_1(x) \log \frac{p_1(x)}{q_1(x)} + (1-\lambda) p_2(x) \log \frac{p_2(x)}{q_2(x)}
$$

Sommando la relazione puntuale su tutti gli elementi $x \in \mathcal{X}$:

$$
\sum_{x \in \mathcal{X}} p_\lambda(x) \log \frac{p_\lambda(x)}{q_\lambda(x)} \le \lambda \sum_{x \in \mathcal{X}} p_1(x) \log \frac{p_1(x)}{q_1(x)} + (1-\lambda) \sum_{x \in \mathcal{X}} p_2(x) \log \frac{p_2(x)}{q_2(x)}
$$

Riconoscendo le definizioni formali di divergenza di Kullback-Leibler in ciascun membro:

$$
D(p_\lambda \parallel q_\lambda) \le \lambda D(p_1 \parallel q_1) + (1-\lambda) D(p_2 \parallel q_2)
$$

Il risultato dimostra in modo rigoroso e autosufficiente la convessità congiunta della divergenza relativa.

## Dimostrazione Rigorosa della Disuguaglianza di Fano

### Modello di Stima e Catena di Markov

Si consideri una sorgente informativa discreta rappresentata da una variabile aleatoria $X$ a valori nell'alfabeto finito $\mathcal{X}$, con distribuzione di probabilità marginale $p(x) = \text{Pr}\{X = x\}$. La variabile $X$ viene trasmessa attraverso un canale o osservata mediante una variabile aleatoria correlata $Y \in \mathcal{Y}$ secondo la distribuzione condizionata $p(y \mid x)$.

A partire dalla sola osservazione $Y$, un ricevitore o stimatore costruisce una stima $\hat{X} = g(Y)$, dove $g: \mathcal{Y} \to \hat{\mathcal{X}}$ può essere una funzione sia deterministica sia randomizzata. Per la struttura del processo di elaborazione, la stima $\hat{X}$ dipende da $X$ esclusivamente per il tramite di $Y$, originando la catena di Markov:

$$
X \longrightarrow Y \longrightarrow \hat{X}
$$

Si definisce l'evento di errore di stima e la corrispondente probabilità d'errore $P_e$:

$$
P_e = \text{Pr}\{ \hat{X} \neq X \}
$$

### Variabile Indicatrice d'Errore ed Espansione dell'Entropia Congiunta

Per quantificare analiticamente la relazione tra l'entropia a posteriori $H(X \mid Y)$ e la probabilità d'errore $P_e$, si introduce la variabile aleatoria binaria indicatrice d'errore $E$:

$$
E = \begin{cases} 1 & \text{se } \hat{X} \neq X \\ 0 & \text{se } \hat{X} = X \end{cases}
$$

La distribuzione di probabilità di $E$ è bernoulliana: $\text{Pr}\{E = 1\} = P_e$ e $\text{Pr}\{E = 0\} = 1 - P_e$. L'entropia della variabile $E$ coincide con la funzione di entropia binaria:

$$
H(E) = H_B(P_e) = -P_e \log_2 P_e - (1 - P_e) \log_2(1 - P_e)
$$

Si considera l'entropia congiunta condizionata $H(E, X \mid \hat{X})$ e la si sviluppa in due modi distinti sfruttando la regola della catena per l'entropia condizionata.

#### Primo Sviluppo della Catena

Condizionando inizialmente rispetto a $X$ dato $\hat{X}$:

$$
H(E, X \mid \hat{X}) = H(X \mid \hat{X}) + H(E \mid X, \hat{X})
$$

Poiché $E$ è una funzione deterministica della coppia $(X, \hat{X})$ (l'indicatrice confronta l'uguaglianza tra $X$ e $\hat{X}$), noti $X$ e $\hat{X}$ il valore di $E$ è deterministico e privo di incertezza:

$$
H(E \mid X, \hat{X}) = 0
$$

Pertanto, il primo sviluppo restituisce:

$$
H(E, X \mid \hat{X}) = H(X \mid \hat{X})
$$

#### Secondo Sviluppo della Catena

Condizionando inizialmente rispetto a $E$ dato $\hat{X}$:

$$
H(E, X \mid \hat{X}) = H(E \mid \hat{X}) + H(X \mid E, \hat{X})
$$

Si analizzano separatamente i due addendi:
1. Poiché il condizionamento non può incrementare l'entropia:

$$
   H(E \mid \hat{X}) \le H(E) = H_B(P_e)
$$

2. Il secondo termine si espande mediante la definizione di valore atteso condizionato:

$$
   H(X \mid E, \hat{X}) = \text{Pr}\{E = 0\} H(X \mid E = 0, \hat{X}) + \text{Pr}\{E = 1\} H(X \mid E = 1, \hat{X})
$$

   - Nel caso $E = 0$, si ha per definizione $\hat{X} = X$. Condizionatamente a $(E = 0, \hat{X} = \hat{x})$, la variabile $X$ assume l'unico valore deterministico $\hat{x}$ con probabilità 1. Di conseguenza:

$$
     H(X \mid E = 0, \hat{X}) = 0
$$

   - Nel caso $E = 1$, si ha $X \neq \hat{X}$. Sapendo che $\hat{X} = \hat{x}$, la variabile $X$ può assumere valori soltanto nel sottoinsieme complementare $\mathcal{X} \setminus \{\hat{x}\}$, la cui cardinalità è limitata superiormente da $|\mathcal{X}| - 1$. L'entropia di una distribuzione discreta a supporto finito è massimizzata dalla distribuzione uniforme sulla cardinalità del supporto:

$$
     H(X \mid E = 1, \hat{X}) \le \log_2(|\mathcal{X}| - 1)
$$

Sostituendo queste valutazioni nel secondo addendo:

$$
H(X \mid E, \hat{X}) \le (1 - P_e) \cdot 0 + P_e \log_2(|\mathcal{X}| - 1) = P_e \log_2(|\mathcal{X}| - 1)
$$

Sommando i due termini:

$$
H(E, X \mid \hat{X}) \le H_B(P_e) + P_e \log_2(|\mathcal{X}| - 1)
$$

### Uguaglianza dei Due Sviluppi e Applicazione della DPI

Uguagliando il primo e il secondo sviluppo di $H(E, X \mid \hat{X})$:

$$
H(X \mid \hat{X}) \le H_B(P_e) + P_e \log_2(|\mathcal{X}| - 1)
$$

Poiché $X \longrightarrow Y \longrightarrow \hat{X}$ costituisce una catena di Markov, la __Data Processing Inequality__ (DPI) garantisce che nessuna elaborazione a valle possa incrementare l'informazione mutua:

$$
I(X; \hat{X}) \le I(X; Y)
$$

Esprimendo l'informazione mutua in termini di entropia marginale e condizionata:

$$
H(X) - H(X \mid \hat{X}) \le H(X) - H(X \mid Y)
$$

Sottraendo $H(X)$ da entrambi i membri e invertendo il segno:

$$
H(X \mid \hat{X}) \ge H(X \mid Y)
$$

Concatenando le disuguaglianze, si ottiene la forma rigorosa e generale della __disuguaglianza di Fano__:

$$
H(X \mid Y) \le H(X \mid \hat{X}) \le H_B(P_e) + P_e \log_2(|\mathcal{X}| - 1)
$$

Se l'alfabeto delle decisioni dello stimatore $\hat{\mathcal{X}}$ non è vincolato a coincidere con $\mathcal{X}$, la maggiorazione sull'entropia residua d'errore assume la forma più rilassata $\log_2 |\mathcal{X}|$, conducendo a:

$$
H(X \mid Y) \le H_B(P_e) + P_e \log_2 |\mathcal{X}|
$$

### Forme Indebolite e Limite Inferiore Esplicito su $P_e$

Poiché l'entropia binaria soddisfa la limitazione universale $H_B(P_e) \le 1$ bit (raggiunta per $P_e = \frac{1}{2}$), si può maggiorare $H_B(P_e)$ con 1:

$$
H(X \mid Y) \le 1 + P_e \log_2 |\mathcal{X}|
$$

Risolvendo algebricamente rispetto alla probabilità d'errore $P_e$:

$$
P_e \ge \frac{H(X \mid Y) - 1}{\log_2 |\mathcal{X}|}
$$

Tale limite inferiore stabilisce che se l'entropia equivoca $H(X \mid Y)$ supera 1 bit, è teoricamente impossibile annullare la probabilità d'errore, indipendentemente dalla complessità computazionale dello stimatore impiegato.

### Condizione di Raggiungibilità dell'Uguaglianza

Si consideri lo scenario privo di osservazioni ($Y = \emptyset$), in cui la stima deve avvenire a priori. Sia $X \in \{1, 2, \dots, m\}$ con probabilità ordinate in modo decrescente $p_1 \ge p_2 \ge \dots \ge p_m$. La regola di decisione ottima a minima probabilità d'errore stima sistematicamente la classe più probabile $\hat{X} = 1$, ottenendo:

$$
P_e = 1 - p_1
$$

In questo contesto, la disuguaglianza di Fano diventa:

$$
H(X) \le H_B(P_e) + P_e \log_2(m - 1)
$$

L'uguaglianza viene conseguita esattamente se e solo se la distribuzione a priori è uniforme su tutte le $m - 1$ classi rimanenti, ovvero:

$$
p(x) = \left( 1 - P_e, \, \frac{P_e}{m-1}, \, \frac{P_e}{m-1}, \, \dots, \, \frac{P_e}{m-1} \right)
$$

In tal caso, calcolando esplicitamente l'entropia di Shannon:

$$
H(X) = -(1 - P_e)\log_2(1 - P_e) - \sum_{i=2}^m \frac{P_e}{m-1} \log_2 \frac{P_e}{m-1}
$$

$$
H(X) = -(1 - P_e)\log_2(1 - P_e) - P_e \left[ \log_2 P_e - \log_2(m - 1) \right] = H_B(P_e) + P_e \log_2(m - 1)
$$

Ciò dimostra analiticamente la stretta ottimalità del limite di Fano nel caso peggiore.

## Dimostrazione Analitica del Teorema AEP tramite Disuguaglianza di Chebyshev sulla Varianza della Sorpresa

> [!NOTE] Riferimento al Capitolo di Teoria
> Trattazione teorica, intuizione ed esempi applicativi in [[8. Proprietà di Equipartizione Asintotica (AEP)]].

### Enunciazione del Teorema

Siano date $n$ variabili aleatorie discrete $X_1, X_2, \dots, X_n$ indipendenti e identicamente distribuite (i.i.d.) secondo la funzione di massa di probabilità $p(x) = \text{Pr}\{X = x\}$ definita sull'alfabeto finito $\mathcal{X}$, con entropia di Shannon:

$$
H(X) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x)
$$

Il __Teorema della Proprietà di Equipartizione Asintotica__ (Asymptotic Equipartition Property, AEP) stabilisce che la densità di sorpresa empirica normalizzata converge in probabilità all'entropia teorica della sorgente:

$$
-\frac{1}{n} \log_2 p(X_1, X_2, \dots, X_n) \xrightarrow{P} H(X) \quad \text{per } n \to \infty
$$

ovvero, per ogni $\epsilon > 0$ arbitrariamente prefissato:

$$
\lim_{n \to \infty} \text{Pr}\left\{ \left| -\frac{1}{n} \log_2 p(X_1, X_2, \dots, X_n) - H(X) \right| \ge \epsilon \right\} = 0
$$

### Dimostrazione Analitica

Poiché le variabili aleatorie $X_1, \dots, X_n$ sono mutuamente indipendenti, la probabilità congiunta della sequenza osservata fattorizza esattamente nel prodotto delle singole probabilità marginali:

$$
p(X_1, X_2, \dots, X_n) = \prod_{i=1}^n p(X_i)
$$

Applicando l'operatore logaritmico in base 2 e normalizzando per il fattore $-\frac{1}{n}$:

$$
-\frac{1}{n} \log_2 p(X_1, X_2, \dots, X_n) = -\frac{1}{n} \log_2 \left( \prod_{i=1}^n p(X_i) \right) = \frac{1}{n} \sum_{i=1}^n \left( -\log_2 p(X_i) \right)
$$

Si introducono le nuove variabili aleatorie reali $Y_i$:

$$
Y_i = -\log_2 p(X_i), \quad i \in \{1, 2, \dots, n\}
$$

Poiché le $X_i$ sono i.i.d. e ogni $Y_i$ è una trasformazione deterministica misurabile della rispettiva variabile $X_i$, anche le variabili $Y_1, Y_2, \dots, Y_n$ costituiscono una sequenza di variabili aleatorie indipendenti e identicamente distribuite.

#### Calcolo dei Momenti di Primo e Secondo Ordine

Si valuta il valore atteso della variabile generica $Y_i$:

$$
\mathbb{E}[Y_i] = \mathbb{E}[-\log_2 p(X_i)] = \sum_{x \in \mathcal{X}} p(x) \left( -\log_2 p(x) \right) = -\sum_{x \in \mathcal{X}} p(x) \log_2 p(x) = H(X)
$$

Si calcola ora la varianza di $Y_i$:

$$
\sigma_Y^2 = \text{Var}(Y_i) = \mathbb{E}\left[ (Y_i - \mathbb{E}[Y_i])^2 \right] = \sum_{x \in \mathcal{X}} p(x) \left( -\log_2 p(x) - H(X) \right)^2
$$

Poiché l'alfabeto $\mathcal{X}$ ha cardinalità finita $|\mathcal{X}| < \infty$ e per ogni $x$ tale che $p(x) > 0$ la quantità $\log_2 p(x)$ è un numero reale finito, la sommatoria è composta da un numero finito di termini limitati. Di conseguenza:

$$
\sigma_Y^2 < \infty
$$

#### Statistica della Media Campionaria e Disuguaglianza di Chebyshev

La quantità oggetto del teorema corrisponde alla media campionaria delle variabili $Y_i$:

$$
\bar{Y}_n = \frac{1}{n} \sum_{i=1}^n Y_i = -\frac{1}{n} \log_2 p(X_1, \dots, X_n)
$$

Per la linearità del valore atteso:

$$
\mathbb{E}[\bar{Y}_n] = \frac{1}{n} \sum_{i=1}^n \mathbb{E}[Y_i] = \frac{1}{n} \cdot n H(X) = H(X)
$$

Sfruttando la mutua indipendenza delle variabili $Y_i$, la varianza della somma è pari alla somma delle varianze:

$$
\text{Var}(\bar{Y}_n) = \text{Var}\left( \frac{1}{n} \sum_{i=1}^n Y_i \right) = \frac{1}{n^2} \sum_{i=1}^n \text{Var}(Y_i) = \frac{1}{n^2} \cdot n \sigma_Y^2 = \frac{\sigma_Y^2}{n}
$$

Si applica la disuguaglianza di Chebyshev alla variabile aleatoria $\bar{Y}_n$ rispetto alla deviazione $\epsilon > 0$:

$$
\text{Pr}\left\{ |\bar{Y}_n - \mathbb{E}[\bar{Y}_n]| \ge \epsilon \right\} \le \frac{\text{Var}(\bar{Y}_n)}{\epsilon^2}
$$

Sostituendo la media e la varianza calcolate:

$$
\text{Pr}\left\{ \left| -\frac{1}{n} \log_2 p(X_1, \dots, X_n) - H(X) \right| \ge \epsilon \right\} \le \frac{\sigma_Y^2}{n \epsilon^2}
$$

Eseguendo il limite per $n \to \infty$ con $\epsilon > 0$ e $\sigma_Y^2 < \infty$ fissati:

$$
\lim_{n \to \infty} \text{Pr}\left\{ \left| -\frac{1}{n} \log_2 p(X_1, \dots, X_n) - H(X) \right| \ge \epsilon \right\} \le \lim_{n \to \infty} \frac{\sigma_Y^2}{n \epsilon^2} = 0
$$

Poiché la probabilità è non negativa, per il teorema del confronto dei limiti:

$$
\lim_{n \to \infty} \text{Pr}\left\{ \left| -\frac{1}{n} \log_2 p(X_1, \dots, X_n) - H(X) \right| \ge \epsilon \right\} = 0
$$

La disuguaglianza di Chebyshev fornisce non solo la convergenza in probabilità, ma anche una delimitazione quantitativa della velocità di decadimento dell'errore asintotico nell'ordine di $O(1/n)$.

## Dimostrazione del Teorema di Cardinalità Minima per Insiemi ad Alta Probabilità

> [!NOTE] Riferimento al Capitolo di Teoria
> Trattazione teorica, intuizione ed esempi applicativi in [[8. Proprietà di Equipartizione Asintotica (AEP)]].

### Enunciazione del Teorema

Siano $X_1, X_2, \dots, X_n$ variabili aleatorie discrete i.i.d. $\sim p(x)$ con entropia $H(X)$. Per ogni $n$, sia $B_\delta^{(n)} \subset \mathcal{X}^n$ un sottoinsieme arbitrario dello spazio delle sequenze tale da concentrare una probabilità non inferiore a $1 - \delta$, con $\delta \in (0, 1/2)$:

$$
\text{Pr}\{B_\delta^{(n)}\} \ge 1 - \delta
$$

Allora, per qualsiasi $\epsilon > 0$ e per $n$ sufficientemente grande, la cardinalità dell'insieme $B_\delta^{(n)}$ soddisfa:

$$
\frac{1}{n} \log_2 |B_\delta^{(n)}| > H(X) - 2\epsilon
$$

ovvero, all'ordine primario nell'esponente:

$$
|B_\delta^{(n)}| \doteq 2^{n H(X)}
$$

Nessun sottoinsieme dello spazio campionario può concentrare la quasi totalità della massa probabilistica impiegando un numero di sequenze asintoticamente inferiore a $2^{n H(X)}$.

### Dimostrazione Analitica

Si consideri l'intersezione tra l'insieme arbitrario ad alta probabilità $B_\delta^{(n)}$ e l'insieme tipico $A_\epsilon^{(n)}$. La probabilità dell'unione di due eventi soddisfa:

$$
\text{Pr}\{B_\delta^{(n)} \cup A_\epsilon^{(n)}\} = \text{Pr}\{B_\delta^{(n)}\} + \text{Pr}\{A_\epsilon^{(n)}\} - \text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} \le 1
$$

Riorganizzando i termini:

$$
\text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} \ge \text{Pr}\{B_\delta^{(n)}\} + \text{Pr}\{A_\epsilon^{(n)}\} - 1
$$

Per ipotesi $\text{Pr}\{B_\delta^{(n)}\} \ge 1 - \delta$. Inoltre, per il Teorema dell'Insieme Tipico, per qualsiasi $\epsilon > 0$ esiste un intero $n_0$ tale che per ogni $n \ge n_0$:

$$
\text{Pr}\{A_\epsilon^{(n)}\} > 1 - \epsilon
$$

Sostituendo queste due delimitazioni inferiori:

$$
\text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} \ge (1 - \delta) + (1 - \epsilon) - 1 = 1 - \delta - \epsilon
$$

Poiché per ipotesi $\delta < 1/2$, scegliendo $\epsilon < 1/2 - \delta$ si garantisce che $1 - \delta - \epsilon > 0$.

D'altra parte, per definizione di insieme tipico $A_\epsilon^{(n)}$, ciascuna sequenza $x^n \in A_\epsilon^{(n)}$ possiede una probabilità vincolata superiormente da:

$$
p(x^n) \le 2^{-n(H(X) - \epsilon)}
$$

Poiché $B_\delta^{(n)} \cap A_\epsilon^{(n)} \subseteq A_\epsilon^{(n)}$, tale maggiorazione sussiste per ogni elemento dell'intersezione. Valutando la probabilità dell'intersezione come somma discreta:

$$
\text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} = \sum_{x^n \in B_\delta^{(n)} \cap A_\epsilon^{(n)}} p(x^n) \le \sum_{x^n \in B_\delta^{(n)} \cap A_\epsilon^{(n)}} 2^{-n(H(X) - \epsilon)}
$$

La quantità sommata è costante rispetto all'indice della sommatoria, pertanto:

$$
\text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} \le |B_\delta^{(n)} \cap A_\epsilon^{(n)}| \cdot 2^{-n(H(X) - \epsilon)}
$$

Poiché l'intersezione è contenuta in $B_\delta^{(n)}$, si ha banalmente $|B_\delta^{(n)} \cap A_\epsilon^{(n)}| \le |B_\delta^{(n)}|$. Di conseguenza:

$$
\text{Pr}\{B_\delta^{(n)} \cap A_\epsilon^{(n)}\} \le |B_\delta^{(n)}| \cdot 2^{-n(H(X) - \epsilon)}
$$

Concatenando il limite inferiore probabilistico con la maggiorazione analitica:

$$
1 - \delta - \epsilon \le |B_\delta^{(n)}| \cdot 2^{-n(H(X) - \epsilon)}
$$

Moltiplicando ambo i membri per il fattore positivo $2^{n(H(X) - \epsilon)}$:

$$
|B_\delta^{(n)}| \ge (1 - \delta - \epsilon) \cdot 2^{n(H(X) - \epsilon)}
$$

Applicando il logaritmo in base 2 ad entrambi i membri:

$$
\log_2 |B_\delta^{(n)}| \ge n(H(X) - \epsilon) + \log_2(1 - \delta - \epsilon)
$$

Dividendo l'intera disuguaglianza per la lunghezza della sequenza $n$:

$$
\frac{1}{n} \log_2 |B_\delta^{(n)}| \ge H(X) - \epsilon + \frac{1}{n} \log_2(1 - \delta - \epsilon)
$$

Poiché $1 - \delta - \epsilon > 0$ è una costante strettamente positiva indipendente da $n$, la quantità $\log_2(1 - \delta - \epsilon)$ è una costante finita. Pertanto:

$$
\lim_{n \to \infty} \frac{1}{n} \log_2(1 - \delta - \epsilon) = 0
$$

Esiste quindi un indice $n_1$ tale che per ogni $n \ge n_1$:

$$
\frac{1}{n} \log_2(1 - \delta - \epsilon) > -\epsilon
$$

Ne discende che per ogni $n \ge \max(n_0, n_1)$:

$$
\frac{1}{n} \log_2 |B_\delta^{(n)}| > H(X) - 2\epsilon
$$

Questo risultato dimostra in modo rigoroso e inconfutabile che l'insieme tipico $A_\epsilon^{(n)}$ possiede la cardinalità minima (al primo ordine dell'esponente) tra tutti i possibili sottoinsiemi ad alta probabilità dello spazio delle sequenze.

## Dimostrazione Analitica della Convergenza di Cesàro e dell'Uguaglianza dei Tassi di Entropia

### Lemma di Monotonia dell'Entropia Condizionata

Sia $\{X_i\}_{i=-\infty}^{+\infty}$ un processo stocastico discreto stazionario a valori nell'alfabeto finito $\mathcal{X}$. Si definisce la sequenza delle entropie condizionate temporali:

$$
a_n = H(X_n \mid X_{n-1}, X_{n-2}, \dots, X_1), \quad n \ge 1
$$

__Lemma__: La successione $\{a_n\}_{n=1}^\infty$ è non crescente in $n$:

$$
a_{n+1} \le a_n \quad \forall n \ge 1
$$

e converge a un limite finito non negativo, indicato con $H'(\mathcal{X})$.

#### Dimostrazione

Per definizione di $a_{n+1}$:

$$
a_{n+1} = H(X_{n+1} \mid X_n, X_{n-1}, \dots, X_1)
$$

Poiché il condizionamento non può incrementare l'entropia ("information can't hurt"), rimuovendo la prima osservazione $X_1$ dal set di condizionamento si ottiene la maggiorazione:

$$
H(X_{n+1} \mid X_n, X_{n-1}, \dots, X_1) \le H(X_{n+1} \mid X_n, X_{n-1}, \dots, X_2)
$$

Sfruttando l'invarianza per traslazione temporale garantita dall'ipotesi di stazionarietà del processo, si applica uno shift temporale unitario all'indietro (con $l = -1$):

$$
H(X_{n+1} \mid X_n, X_{n-1}, \dots, X_2) = H(X_n \mid X_{n-1}, X_{n-2}, \dots, X_1) = a_n
$$

Ne discende la disuguaglianza:

$$
a_{n+1} \le a_n
$$

La successione $\{a_n\}$ è monotona non crescente. Poiché per l'entropia di variabili discrete vale $a_n \ge 0$ per ogni $n$, la successione è inferiormente limitata da zero. Per il teorema fondamentale di esistenza del limite per successioni monotone e limitate, esiste finito il limite:

$$
H'(\mathcal{X}) = \lim_{n \to \infty} H(X_n \mid X_{n-1}, \dots, X_1)
$$

### Teorema delle Medie di Cesàro

__Teorema (Cesàro)__: Sia data una successione di numeri reali $\{a_n\}_{n=1}^\infty$ convergente al limite $a \in \mathbb{R}$ per $n \to \infty$:

$$
\lim_{n \to \infty} a_n = a
$$

Allora la successione delle medie aritmetiche campionarie $\{b_n\}_{n=1}^\infty$, definita da:

$$
b_n = \frac{1}{n} \sum_{i=1}^n a_i
$$

converge anch'essa al medesimo limite $a$:

$$
\lim_{n \to \infty} b_n = a
$$

#### Dimostrazione

Sia fissato un parametro reale $\epsilon > 0$ arbitrario. Poiché $\lim_{n \to \infty} a_n = a$, per definizione di limite esiste un indice intero $N_0 = N_0(\epsilon)$ tale che:

$$
|a_i - a| < \frac{\epsilon}{2} \quad \forall i > N_0
$$

Si valuta lo scostamento tra la media campionaria $b_n$ e il valore limite $a$ per qualunque $n > N_0$:

$$
|b_n - a| = \left| \frac{1}{n} \sum_{i=1}^n a_i - a \right| = \left| \frac{1}{n} \sum_{i=1}^n (a_i - a) \right|
$$

Scomponendo la sommatoria nei primi $N_0$ termini e nei successivi $n - N_0$ termini e applicando la disuguaglianza triangolare:

$$
|b_n - a| \le \frac{1}{n} \sum_{i=1}^{N_0} |a_i - a| + \frac{1}{n} \sum_{i=N_0+1}^n |a_i - a|
$$

Si analizzano separatamente i due addendi:
1. La quantità $S_0 = \sum_{i=1}^{N_0} |a_i - a|$ è una costante finita e indipendente da $n$. Di conseguenza, per $n \to \infty$ si ha $\frac{S_0}{n} \to 0$. Esiste quindi un indice $N_1$ tale che per ogni $n > N_1$:

$$
   \frac{1}{n} \sum_{i=1}^{N_0} |a_i - a| < \frac{\epsilon}{2}
$$

2. Nel secondo termine, ciascun addendo soddisfa $|a_i - a| < \frac{\epsilon}{2}$, dunque:

$$
   \frac{1}{n} \sum_{i=N_0+1}^n |a_i - a| < \frac{1}{n} \sum_{i=N_0+1}^n \frac{\epsilon}{2} = \frac{n - N_0}{n} \frac{\epsilon}{2} < \frac{\epsilon}{2}
$$

Scegliendo $n > \max(N_0, N_1)$, combinando le due maggiorazioni si ottiene:

$$
|b_n - a| < \frac{\epsilon}{2} + \frac{\epsilon}{2} = \epsilon
$$

Ciò dimostra analiticamente che $\lim_{n \to \infty} b_n = a$.

### Dimostrazione dell'Uguaglianza $H(\mathcal{X}) = H'(\mathcal{X})$

Si consideri il tasso di entropia medio per simbolo $H(\mathcal{X})$ definito da:

$$
H(\mathcal{X}) = \lim_{n \to \infty} \frac{1}{n} H(X_1, X_2, \dots, X_n)
$$

Applicando la regola della catena per l'entropia congiunta multivariata:

$$
H(X_1, X_2, \dots, X_n) = \sum_{i=1}^n H(X_i \mid X_{i-1}, \dots, X_1)
$$

Dividendo per la lunghezza della sequenza $n$:

$$
\frac{1}{n} H(X_1, X_2, \dots, X_n) = \frac{1}{n} \sum_{i=1}^n H(X_i \mid X_{i-1}, \dots, X_1)
$$

Si riconosce che il secondo membro è esattamente la media campionaria di Cesàro $b_n = \frac{1}{n}\sum_{i=1}^n a_i$ associata alla sequenza dei termini condizionati $a_i = H(X_i \mid X_{i-1}, \dots, X_1)$.

Poiché per il primo lemma la successione $\{a_i\}$ converge al limite $H'(\mathcal{X})$, per il Teorema di Cesàro anche la sequenza delle medie $b_n$ converge al medesimo valore:

$$
\lim_{n \to \infty} \frac{1}{n} H(X_1, \dots, X_n) = \lim_{n \to \infty} \frac{1}{n} \sum_{i=1}^n a_i = H'(\mathcal{X})
$$

Di conseguenza, per qualsiasi processo stocastico stazionario, entrambi i limiti esistono finiti e coincidono:

$$
H(\mathcal{X}) = H'(\mathcal{X})
$$

## Derivazione Rigorosa della Distribuzione Stazionaria e dell'Entropy Rate per il Random Walk su Grafi

### Modello di Random Walk su Grafo Connesso Non Orientato

Sia $G = (V, E)$ un grafo finito, connesso e non orientato, privo di nodi isolati e privo di cappi ($W_{ii} = 0$). A ciascun ramo $(i, j) \in E$ è associato un peso non negativo simmetrico $W_{ij} = W_{ji} \ge 0$, con la convenzione $W_{ij} = 0$ se $(i, j) \notin E$.

Si definisce il __grado pesato__ del vertice $i \in V$:

$$
d_i = \sum_{j \in V} W_{ij}
$$

Il peso complessivo del grafo è dato dalla somma dei gradi di tutti i nodi:

$$
2m = \sum_{i \in V} d_i = \sum_{i \in V} \sum_{j \in V} W_{ij}
$$

Una particella esegue una passeggiata aleatoria sui nodi del grafo. Trovandosi nel nodo $i$, la particella seleziona il nodo di arrivo $j$ con probabilità proporzionale al peso del ramo corrispondente. Gli elementi della matrice di transizione di stato $\mathbf{P} = [P_{ij}]$ sono dati da:

$$
P_{ij} = \text{Pr}\{X_{n+1} = j \mid X_n = i\} = \frac{W_{ij}}{d_i}
$$

Si verifica immediatamente che $\mathbf{P}$ è una valida matrice stocastica:
- $P_{ij} \ge 0$ per ogni $i, j \in V$;
- Per ciascuna riga $i$:

$$
  \sum_{j \in V} P_{ij} = \sum_{j \in V} \frac{W_{ij}}{d_i} = \frac{1}{d_i} \sum_{j \in V} W_{ij} = \frac{d_i}{d_i} = 1
$$

### Determinazione della Distribuzione Stazionaria e Reversibilità

Si considera il vettore di probabilità $\boldsymbol{\mu} = [\mu_i]_{i \in V}$ proporzionale ai gradi pesati dei singoli nodi:

$$
\mu_i = \frac{d_i}{2m} = \frac{d_i}{\sum_{k \in V} d_k}
$$

#### Verifica della Condizione di Punto Fisso $\boldsymbol{\mu} \mathbf{P} = \boldsymbol{\mu}$

Si calcola la componente $j$-esima del prodotto vettore-matrice:

$$
(\boldsymbol{\mu} \mathbf{P})_j = \sum_{i \in V} \mu_i P_{ij} = \sum_{i \in V} \left( \frac{d_i}{2m} \right) \left( \frac{W_{ij}}{d_i} \right) = \frac{1}{2m} \sum_{i \in V} W_{ij}
$$

Poiché la matrice dei pesi è simmetrica ($W_{ij} = W_{ji}$ per l'ipotesi di grafo non orientato):

$$
\sum_{i \in V} W_{ij} = \sum_{i \in V} W_{ji} = d_j
$$

Sostituendo:

$$
(\boldsymbol{\mu} \mathbf{P})_j = \frac{d_j}{2m} = \mu_j
$$

Ciò prova che $\boldsymbol{\mu}$ è una distribuzione stazionaria della catena di Markov.

#### Condizione di Bilancio Dettagliato (Reversibilità)

Si valuta la probabilità del flusso stazionario tra lo stato $i$ e lo stato $j$:

$$
\mu_i P_{ij} = \left( \frac{d_i}{2m} \right) \left( \frac{W_{ij}}{d_i} \right) = \frac{W_{ij}}{2m}
$$

Simmetricamente, il flusso inverso vale:

$$
\mu_j P_{ji} = \left( \frac{d_j}{2m} \right) \left( \frac{W_{ji}}{d_j} \right) = \frac{W_{ji}}{2m}
$$

Dato che $W_{ij} = W_{ji}$, si ha l'uguaglianza identica per ogni coppia di nodi $(i, j)$:

$$
\mu_i P_{ij} = \mu_j P_{ji}
$$

La catena di Markov associata al random walk su grafo non orientato è pertanto intrinsecamente __reversibile__, garantendo che la dinamica stocastica mantenga le stesse proprietà statistiche sotto inversione dell'asse temporale.

### Calcolo in Forma Chiusa dell'Entropy Rate

L'entropy rate di una catena di Markov stazionaria è dato dalla media dell'entropia di transizione condizionata pesata dalla distribuzione stazionaria:

$$
H(\mathcal{X}) = H(X_2 \mid X_1) = -\sum_{i \in V} \mu_i \sum_{j \in V} P_{ij} \log_2 P_{ij}
$$

Sostituendo le espressioni esplicite di $\mu_i$ e $P_{ij}$:

$$
H(\mathcal{X}) = -\sum_{i \in V} \left( \frac{d_i}{2m} \right) \sum_{j \in V} \left( \frac{W_{ij}}{d_i} \right) \log_2 \left( \frac{W_{ij}}{d_i} \right)
$$

Semplificando il fattore scalare $d_i$:

$$
H(\mathcal{X}) = -\frac{1}{2m} \sum_{i \in V} \sum_{j \in V} W_{ij} \log_2 \left( \frac{W_{ij}}{d_i} \right)
$$

Scomponendo il logaritmo del quoziente:

$$
H(\mathcal{X}) = -\frac{1}{2m} \sum_{i \in V} \sum_{j \in V} W_{ij} \left( \log_2 W_{ij} - \log_2 d_i \right)
$$

$$
H(\mathcal{X}) = -\frac{1}{2m} \sum_{i \in V} \sum_{j \in V} W_{ij} \log_2 W_{ij} + \frac{1}{2m} \sum_{i \in V} \left( \sum_{j \in V} W_{ij} \right) \log_2 d_i
$$

Poiché $\sum_{j \in V} W_{ij} = d_i$, il secondo termine si semplifica:

$$
H(\mathcal{X}) = \frac{1}{2m} \sum_{i \in V} d_i \log_2 d_i - \frac{1}{2m} \sum_{i \in V} \sum_{j \in V} W_{ij} \log_2 W_{ij}
$$

#### Casi Particolari Notevoli

1. __Grafo Non Pesato ($W_{ij} \in \{0, 1\}$)__:
   I termini $W_{ij} \log_2 W_{ij}$ si annullano sia per $W_{ij} = 0$ (per continuità $0\log 0 = 0$) sia per $W_{ij} = 1$ ($\log 1 = 0$). Di conseguenza:

$$
   H(\mathcal{X}) = \frac{1}{2m} \sum_{i \in V} d_i \log_2 d_i
$$

   dove $2m$ coincide con il doppio del numero totale di archi $|E|$.
2. __Grafo Regolare di Grado $d$ ($d_i = d \quad \forall i \in V$)__:
   Ciascun nodo ha il medesimo grado $d$. Sostituendo:

$$
   H(\mathcal{X}) = \frac{1}{2m} \sum_{i \in V} d \log_2 d = \frac{\log_2 d}{2m} \sum_{i \in V} d = \frac{\log_2 d}{2m} \cdot 2m = \log_2 d \quad \text{bit/passo}
$$

   A ciascun passo, la particella sceglie uniformemente tra i $d$ vicini disponibili, generando un'incertezza massima pari a $\log_2 d$ bit.

## Delimitazione dell'Entropy Rate per Funzioni di Catene di Markov e Modelli Nascosti

### Enunciazione del Teorema del Sandwich

Sia $\{X_i\}_{i=1}^\infty$ una catena di Markov stazionaria definita su alfabeto finito $\mathcal{X}$ con distribuzione stazionaria e matrice di transizione note. Sia $Y_i = \phi(X_i)$ un processo stocastico ottenuto applicando una funzione deterministica $\phi: \mathcal{X} \to \mathcal{Y}$ a ciascun stato della catena.

Sebbene il processo $\{Y_i\}$ in generale __non sia una catena di Markov__ (poiché lo stato passato di $Y$ può contenere memoria remota sugli stati non osservabili di $X$), esso eredita la proprietà di stazionarietà da $\{X_i\}$, rendendo ben definito il suo entropy rate:

$$
H(\mathcal{Y}) = \lim_{n \to \infty} H(Y_n \mid Y_{n-1}, \dots, Y_1)
$$

__Teorema (Delimitazione di Shannon-Cover per Funzioni di Catene di Markov)__: Per ogni intero $n \ge 1$:

$$
H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1) \le H(\mathcal{Y}) \le H(Y_n \mid Y_{n-1}, \dots, Y_1)
$$

e per $n \to \infty$:

$$
\lim_{n \to \infty} H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1) = H(\mathcal{Y}) = \lim_{n \to \infty} H(Y_n \mid Y_{n-1}, \dots, Y_1)
$$

### Dimostrazione Analitica

Si considerano separatamente i due rami della delimitazione:

#### Ramo Superiore

Per la proprietà generale secondo cui il condizionamento non incrementa l'entropia, la successione $\{H(Y_n \mid Y_{n-1}, \dots, Y_1)\}$ è monotona non crescente in $n$. Ne consegue immediatamente che ciascun elemento della successione maggiora il limite asintotico:

$$
H(\mathcal{Y}) \le H(Y_n \mid Y_{n-1}, \dots, Y_1) \quad \forall n \ge 1
$$

#### Ramo Inferiore

Si valuta l'entropia condizionata includendo la condizione iniziale della catena di Markov $X_1$:

$$
H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1)
$$

Per la proprietà di Markovità di $\{X_i\}$, noto lo stato $X_1$, la sequenza futura $(X_2, \dots, X_n)$ (e dunque anche le sue funzioni deterministiche $(Y_2, \dots, Y_n)$) è condizionatamente indipendente dall'intera traiettoria passata prima del tempo 1, ovvero $(Y_0, Y_{-1}, \dots, Y_{-k})$. Di conseguenza:

$$
H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1) = H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1, Y_0, Y_{-1}, \dots, Y_{-k})
$$

Applicando la regola di riduzione dell'entropia per condizionamento rispetto a $X_1$:

$$
H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1, Y_0, \dots, Y_{-k}) \le H(Y_n \mid Y_{n-1}, \dots, Y_1, Y_0, \dots, Y_{-k})
$$

Il membro destro rappresenta l'entropia condizionata del processo $\{Y\}$ data una storia passata di lunghezza $n + k$. Facendo tendere $k \to \infty$, per la stazionarietà del processo tale quantità converge esattamente all'entropy rate $H(\mathcal{Y})$:

$$
\lim_{k \to \infty} H(Y_n \mid Y_{n-1}, \dots, Y_{-k}) = H(\mathcal{Y})
$$

Dunque:

$$
H(Y_n \mid Y_{n-1}, \dots, Y_1, X_1) \le H(\mathcal{Y})
$$

#### Convergenza a Cascata (Chiusura del Sandwich)

La differenza tra il limite superiore e il limite inferiore corrisponde all'informazione mutua condizionata tra $X_1$ e $Y_n$ data la traiettoria intermedia:

$$
H(Y_n \mid Y^{n-1}) - H(Y_n \mid Y^{n-1}, X_1) = I(X_1; Y_n \mid Y_{n-1}, \dots, Y_1)
$$

Espandendo la mutua informazione congiunta:

$$
I(X_1; Y_1, \dots, Y_n) = \sum_{k=1}^n I(X_1; Y_k \mid Y^{k-1}) \le H(X_1) < \infty
$$

Essendo la serie a termini non negativi superiormente limitata dall'entropia finita dello stato iniziale $H(X_1) \le \log_2 |\mathcal{X}| < \infty$, il termine generale della serie deve necessariamente convergere a zero:

$$
\lim_{n \to \infty} I(X_1; Y_n \mid Y_{n-1}, \dots, Y_1) = 0
$$

Ciò prova che:

$$
\lim_{n \to \infty} \left[ H(Y_n \mid Y^{n-1}) - H(Y_n \mid Y^{n-1}, X_1) \right] = 0
$$

I due rami convergono esattamente al medesimo valore $H(\mathcal{Y})$, consentendo di stimare numericamente l'entropy rate di processi a stati nascosti e modelli HMM con precisione arbitraria prefissata.


## Dimostrazione Integrale del Teorema di McMillan per Codici Univocamente Decodificabili

Il Teorema di Kraft stabilisce che per qualsiasi codice istantaneo (o prefisso) su un alfabeto codice di dimensione $D$, le lunghezze delle parole di codice $l_1, l_2, \dots, l_m$ devono necessariamente soddisfare la disuguaglianza $\sum_{i=1}^m D^{-l_i} \le 1$. Il Teorema di McMillan (1956) estende tale risultato fondamentale all'intera classe, significativamente più ampia, dei codici univocamente decodificabili.

### Enunciato del Teorema di McMillan

Sia $C: \mathcal{X} \to \mathcal{D}^*$ un codice univocamente decodificabile definito su una sorgente a $m$ simboli con lunghezze delle parole di codice $l_1, l_2, \dots, l_m$ su un alfabeto di cardinalità $D$. Allora la sommatoria delle lunghezze soddisfa la disuguaglianza di Kraft:

$$
\sum_{i=1}^m D^{-l_i} \le 1
$$

### Dimostrazione Analitica (Metodo delle Potenze Polinomiali di Karush)

Si consideri la quantità $S = \sum_{i=1}^m D^{-l_i}$ elevata a una potenza intera arbitraria $k \ge 1$:

$$
S^k = \left( \sum_{i=1}^m D^{-l_i} \right)^k = \sum_{i_1=1}^m \sum_{i_2=1}^m \dots \sum_{i_k=1}^m D^{-(l_{i_1} + l_{i_2} + \dots + l_{i_k})}
$$

Ciascun termine all'interno della sommatoria multipla corrisponde a una specifica sequenza di $k$ simboli di sorgente $x_{i_1} x_{i_2} \dots x_{i_k}$, la cui concatenazione di parole di codice possiede lunghezza complessiva:

$$
j = \sum_{r=1}^k l_{i_r}
$$

Sia $l_{\max} = \max_{1 \le i \le m} l_i$ la lunghezza massima tra le parole di codice di $C$. Poiché ogni parola di codice ha lunghezza minima pari ad almeno 1 bit ($l_i \ge 1$), la lunghezza complessiva $j$ di una sequenza di $k$ parole di codice è limitata inferiormente e superiormente:

$$
k \le j \le k l_{\max}
$$

Raggruppando i termini della sommatoria in base alla loro lunghezza totale $j$:

$$
S^k = \sum_{j=k}^{k l_{\max}} N_{k, j} D^{-j}
$$

dove $N_{k, j}$ indica il numero di distinte sequenze di $k$ simboli di sorgente la cui estensione di codice produce una parola di codice complessiva di lunghezza esattamente pari a $j$.

#### Il Ruolo Chiave dell'Univoca Decodificabilità

Per ipotesi fondamentale, il codice $C$ è __univocamente decodificabile__. Ciò implica che l'estensione di codice $C^*: \mathcal{X}^k \to \mathcal{D}^j$ è una funzione iniettiva: due sequenze distinte di $k$ simboli di sorgente non possono in alcun modo generare la medesima sequenza di simboli di codice.

Di conseguenza, ciascuna delle $N_{k, j}$ sequenze di codice di lunghezza $j$ deve essere una stringa differente scelta nell'insieme delle possibili parole di lunghezza $j$ costruibili sull'alfabeto $\mathcal{D}$. Poiché l'alfabeto ha cardinalità $D$, il numero totale di stringhe distinte di lunghezza $j$ è pari a $D^j$. Ne deriva la delimitazione superiore:

$$
N_{k, j} \le D^j
$$

#### Maggiorazione e Passaggio al Limite

Sostituendo la disuguaglianza $N_{k, j} \le D^j$ nell'espressione di $S^k$:

$$
S^k = \sum_{j=k}^{k l_{\max}} N_{k, j} D^{-j} \le \sum_{j=k}^{k l_{\max}} D^j D^{-j} = \sum_{j=k}^{k l_{\max}} 1
$$

Il numero di termini della sommatoria è pari a $k l_{\max} - k + 1$, che è strettamente maggiorato da $k l_{\max}$:

$$
S^k \le k l_{\max} - k + 1 \le k l_{\max}
$$

Estraendo la radice $k$-esima da entrambi i membri per qualsiasi $k \ge 1$:

$$
S = \sum_{i=1}^m D^{-l_i} \le (k l_{\max})^{1/k}
$$

Poiché tale disuguaglianza deve valere per qualsiasi intero positivo $k$, possiamo passare al limite per $k \to \infty$. Calcolando il limite:

$$
\lim_{k \to \infty} (k l_{\max})^{1/k} = \lim_{k \to \infty} \exp\left( \frac{\ln(k) + \ln(l_{\max})}{k} \right) = \exp(0) = 1
$$

Poiché $S$ è una costante reale indipendente da $k$ e $S \le (k l_{\max})^{1/k}$ per ogni $k$, ne consegue ineludibilmente che:

$$
S = \sum_{i=1}^m D^{-l_i} \le 1
$$

Il Teorema di McMillan è così integralmente dimostrato.

#### Conseguenza Fondamentale sulla Progettazione dei Codici

Poiché la classe dei codici istantanei soddisfa la disuguaglianza di Kraft e la classe dei codici univocamente decodificabili è soggetta al medesimo vincolo $\sum D^{-l_i} \le 1$, l'insieme delle lunghezze delle parole di codice ammissibili per un codice univocamente decodificabile coincide esattamente con l'insieme delle lunghezze ammissibili per un codice istantaneo.

Non esiste alcun codice univocamente decodificabile che possa raggiungere una lunghezza media di parola $\mathbb{E}[l(X)]$ strettamente inferiore a quella ottenibile dal miglior codice istantaneo (prefisso). I codici istantanei possiedono quindi efficienza di compressione pari a quella dei codici a ritardo di decodifica arbitrario, offrendo al contempo il vantaggio operativo di poter essere decodificati simbolo per simbolo in tempo reale senza memoria o lookahead.

## Dimostrazione Formale del Teorema di Ottimalità dei Codici di Huffman tramite Riduzione Canonica

L'algoritmo di Huffman (1952) costruisce un codice prefisso che minimizza la lunghezza media attesa $L = \sum_{i=1}^m p_i l_i$ tra tutti i possibili codici univocamente decodificabili su un assegnato insieme di probabilità di sorgente.

### Proprietà di un Codice Prefisso Ottimo (Forma Canonica)

Sia $\mathcal{X} = \{1, 2, \dots, m\}$ una sorgente discreta ordinata in senso decrescente di probabilità:

$$
p_1 \ge p_2 \ge \dots \ge p_m > 0
$$

Sia $C^*$ un codice prefisso ottimo con lunghezze $l_1, l_2, \dots, l_m$. Allora $C^*$ può essere ricondotto a una forma canonica che soddisfa le seguenti tre proprietà strutturali:

1. __Monotonia inversa delle lunghezze__: $p_j > p_k \implies l_j \le l_k$. Simboli a probabilità più elevata sono codificati con parole di codice di lunghezza minore o uguale.
   - _Dimostrazione_: Se per assurdo valesse $p_j > p_k$ ma $l_j > l_k$, scambiando le parole di codice assegnate a $j$ e $k$ la variazione della lunghezza media sarebbe:

$$
     \Delta L = (p_j l_k + p_k l_j) - (p_j l_j + p_k l_k) = (p_j - p_k)(l_k - l_j) < 0
$$

     La lunghezza media diminuirebbe strettamente, contraddicendo l'ottimalità di $C^*$.
2. __Eguaglianza di lunghezza massima per i due simboli meno probabili__: $l_{m-1} = l_m$.
   - _Dimostrazione_: Poiché le lunghezze sono ordinate in modo non decrescente ($l_1 \le l_2 \le \dots \le l_m$), la parola $l_m$ è la più lunga dell'albero. Se valesse $l_m > l_{m-1}$, allora nell'albero binario la foglia corrispondente al simbolo $m$ non potrebbe avere un fratello al livello $l_m$ assegnato a una parola di codice. Eliminando l'ultimo bit da $C(m)$, la nuova parola rimarrebbe prefissa (nessun altro nodo condivide tale prefisso) e la sua lunghezza si ridurrebbe a $l_m - 1$, riducendo la lunghezza media $\mathbb{E}[l(X)]$ e contraddicendo l'ottimalità.
3. __I due simboli meno probabili sono fratelli nell'albero__: I simboli $m-1$ ed $m$ differiscono unicamente nell'ultimo bit binario, condividendo un prefisso comune di lunghezza $l_m - 1$.
   - _Dimostrazione_: Se $C(m-1)$ e $C(m)$ non fossero fratelli, poiché $l_{m-1} = l_m$, la foglia sorella di $m$ apparterrebbe a un nodo di profondità massima $l_m$. Scambiando tale foglia con il simbolo $m-1$, la lunghezza media rimane invariata poiché $p_{m-1}$ e la probabilità del fratello hanno la stessa lunghezza $l_m$, posizionando $m-1$ ed $m$ come nodi fratelli.

### Procedura di Riduzione e Dimostrazione per Induzione

La dimostrazione di ottimalità procede per induzione sul numero di simboli dell'alfabeto $m$.

#### Base dell'Induzione ($m = 2$)
Per una sorgente binaria con $m = 2$, l'unico codice prefisso non degenere assegna un singolo bit a ciascun simbolo ($l_1 = l_2 = 1$). La lunghezza media è $L = 1$, che coincide con la costruzione di Huffman. La base dell'induzione è verificata.

#### Passo Induttivo (Metodo Algebrico Diretto di Baruffa, Lucidi 25–26)

Si assuma che l'algoritmo di Huffman generi un codice canonico ottimo per qualsiasi sorgente con $m-1$ simboli.

Sia $\mathbf{p} = [p_1, p_2, \dots, p_m]$ la distribuzione di probabilità ordinata della sorgente $\mathcal{X}$ a $m$ simboli, e sia $\mathbf{p}' = [p_1, \dots, p_{m-2}, p_{m-1} + p_m]$ la distribuzione della sorgente ridotta $\mathcal{X}'$ a $m-1$ simboli.

Indichiamo con $C_m^*(\mathbf{p})$ un codice canonico ottimo per $\mathbf{p}$ (con lunghezza minima $L^*(\mathbf{p})$) e con $C_{m-1}^*(\mathbf{p}')$ un codice canonico ottimo per $\mathbf{p}'$ (con lunghezza minima $L^*(\mathbf{p}')$).

1. __Espansione del codice ottimo ridotto__: A partire da $C_{m-1}^*(\mathbf{p}')$, si costruisce un codice $C_m(\mathbf{p})$ per la sorgente a $m$ simboli estendendo la parola associata a $p_{m-1} + p_m$ con i due bit '0' e '1'. La lunghezza media del codice esteso soddisfa:

$$
   L(C_m(\mathbf{p})) = L^*(C_{m-1}^*(\mathbf{p}')) + p_{m-1} + p_m
$$

2. __Riduzione del codice canonico ottimo originario__: A partire dal codice ottimo canonico $C_m^*(\mathbf{p})$ (in cui per la proprietà 3 i simboli $m-1$ ed $m$ sono fratelli di massima lunghezza), si fondono tali foglie eliminando l'ultimo bit, ottenendo un codice prefisso valido $C_{m-1}(\mathbf{p}')$ la cui lunghezza media vale:

$$
   L(C_{m-1}(\mathbf{p}')) = L^*(C_m^*(\mathbf{p})) - (p_{m-1} + p_m)
$$

3. __Somma delle due relazioni algebriche__: Sommando membro a membro le due equazioni:

$$
   L(C_m(\mathbf{p})) + L(C_{m-1}(\mathbf{p}')) = L^*(C_{m-1}^*(\mathbf{p}')) + p_{m-1} + p_m + L^*(C_m^*(\mathbf{p})) - p_{m-1} - p_m = L^*(C_{m-1}^*(\mathbf{p}')) + L^*(C_m^*(\mathbf{p}))
$$

   Riordinando i termini:

$$
   \left[ L(C_m(\mathbf{p})) - L^*(C_m^*(\mathbf{p})) \right] + \left[ L(C_{m-1}(\mathbf{p}')) - L^*(C_{m-1}^*(\mathbf{p}')) \right] = 0
$$

   Poiché per definizione di ottimalità nessun codice può avere una lunghezza media inferiore a quella del rispettivo codice ottimo:

$$
   L(C_m(\mathbf{p})) - L^*(C_m^*(\mathbf{p})) \ge 0 \quad \text{e} \quad L(C_{m-1}(\mathbf{p}')) - L^*(C_{m-1}^*(\mathbf{p}')) \ge 0
$$

   La somma di due quantità non negative è pari a zero se e solo se ciascun termine si annulla identicamente:

$$
   L(C_m(\mathbf{p})) - L^*(C_m^*(\mathbf{p})) = 0 \implies L(C_m(\mathbf{p})) = L^*(C_m^*(\mathbf{p}))
$$

Ciò dimostra direttamente che l'estensione del codice ottimo per la distribuzione ridotta $\mathbf{p}'$ è un codice globalmente ottimo per la sorgente a $m$ simboli $\mathbf{p}$.

Partendo dalla base ottima a 2 simboli e procedendo induttivamente:

$$
\mathbf{p}' = [p_1, p_2 + p_3] \to \mathbf{p} = [p_1, p_2, p_3] \to \dots \to \mathbf{p}' = [p_1, \dots, p_{m-1} + p_m] \to \mathbf{p} = [p_1, \dots, p_m]
$$

l'algoritmo di Huffman produce un codice rigorosamente ottimo per qualunque cardinalità $m$.

## Teorema sull'Ottimalità Competitiva della Codifica di Shannon e Huffman

Nella teoria classica della compressione, l'ottimalità dei codici viene generalmente formulata rispetto al valore atteso della lunghezza: $\min \mathbb{E}[l(X)]$. Tuttavia, in un'ottica decisionale o di teoria dei giochi competitiva, ci si potrebbe domandare: *è possibile che un codice alternativo $C'$ risulti migliore del codice ottimo nella maggioranza delle trasmissioni individuali, pur avendo una media leggermente peggiore a causa di parole molto lunghe assegnate a eventi rari?*

Il Teorema dell'Ottimalità Competitiva (Cover & Thomas, Sez. 5.10; Lucido 32–33) inquadra il confronto tra codici prefissi come un gioco a somma zero tra due giocatori, stabilendo la dominanza stocastica intrinseca della codifica di Shannon e di Huffman.

### Enunciato Formale (Cover & Thomas, Teorema 5.10.1)

Sia $l(x) = \lceil \log_2(1/p(x)) \rceil$ la lunghezza della parola assegnata dal codice di Shannon per una distribuzione $p(x)$ su $\mathcal{X}$. Sia $l'(x)$ la lunghezza delle parole di un qualsiasi altro codice univocamente decodificabile.

Per qualsiasi intero $c \ge 1$:

$$
\text{Pr}\{l(X) \ge l'(X) + c\} \le \frac{1}{2^{c-1}}
$$

Inoltre, nel gioco competitivo a payoff $W = \text{sign}(l'(X) - l(X)) \in \{-1, 0, 1\}$:

$$
\text{Pr}\{l(X) < l'(X)\} \ge \text{Pr}\{l(X) > l'(X)\}
$$

### Dimostrazione Analitica

Si consideri l'insieme degli eventi in cui il codice concorrente $l'$ batte il codice di Shannon $l$ di almeno $c$ bit:

$$
A_c = \{x \in \mathcal{X} : l(x) - l'(x) \ge c\} = \{x \in \mathcal{X} : l'(x) \le l(x) - c\}
$$

Dalla definizione della funzione soffitto nel codice di Shannon:

$$
l(x) = \left\lceil \log_2 \frac{1}{p(x)} \right\rceil < \log_2 \frac{1}{p(x)} + 1
$$

da cui discende:

$$
\log_2 \frac{1}{p(x)} > l(x) - 1 \implies p(x) < 2^{-(l(x) - 1)} = 2 \cdot 2^{-l(x)}
$$

Per ogni $x \in A_c$, vale $l'(x) \le l(x) - c$, ossia $l(x) \ge l'(x) + c$, da cui $2^{-l(x)} \le 2^{-(l'(x) + c)} = 2^{-c} 2^{-l'(x)}$. Sostituendo nella maggiorazione di $p(x)$:

$$
p(x) < 2 \cdot 2^{-c} 2^{-l'(x)} = 2^{-(c-1)} 2^{-l'(x)}
$$

Sommando le probabilità su tutti i simboli appartenenti all'insieme critico $A_c$:

$$
\text{Pr}\{l(X) \ge l'(X) + c\} = \sum_{x \in A_c} p(x) < 2^{-(c-1)} \sum_{x \in A_c} 2^{-l'(x)}
$$

Poiché $A_c \subseteq \mathcal{X}$ e i termini $2^{-l'(x)}$ sono strettamente positivi, estendendo la sommatoria a tutto l'alfabeto $\mathcal{X}$:

$$
\sum_{x \in A_c} 2^{-l'(x)} \le \sum_{x \in \mathcal{X}} 2^{-l'(x)}
$$

Essendo il codice concorrente $l'$ univocamente decodificabile, per il Teorema di McMillan (disuguaglianza di Kraft) vale $\sum_{x \in \mathcal{X}} 2^{-l'(x)} \le 1$. Ne consegue direttamente:

$$
\text{Pr}\{l(X) \ge l'(X) + c\} \le 2^{-(c-1)} \sum_{x \in \mathcal{X}} 2^{-l'(x)} \le \frac{1}{2^{c-1}}
$$

#### Conseguenze Notevoli

1. __Margine di 2 bit ($c = 2$)__:

$$
   \text{Pr}\{l(X) \ge l'(X) + 2\} \le \frac{1}{2^{2-1}} = \frac{1}{2}
$$

   Nessun codice concorrente può battere il codice di Shannon di $2$ o più bit con probabilità superiore al $50\%$.

2. __Decadimento Esponenziale per Margini Grandi__:
   La probabilità che un concorrente vinca di $c$ bit decresce geometricamente con la penalità $c$ (per $c=3$ è al più $1/4$, per $c=4$ è al più $1/8$, per $c=5$ è al più $1/16$).

3. __Dominanza nel Gioco Competitivo__:
   Definendo la variabile di payoff $W = \text{sign}(l'(X) - l(X)) \in \{-1, 0, 1\}$, si dimostra che $\mathbb{E}[W] = \text{Pr}\{l(X) < l'(X)\} - \text{Pr}\{l(X) > l'(X)\} \ge 0$, stabilendo che:

$$
   \text{Pr}\{l(X) < l'(X)\} \ge \text{Pr}\{l(X) > l'(X)\}
$$

   Il codice di Shannon (e di conseguenza il codice di Huffman che minimizza globalmente la lunghezza attesa) è stocasticamente dominante nel confronto a coppie.


## Dimostrazione del Teorema di Codifica di Canale (Diretta: Random Coding e Joint AEP)

Il Secondo Teorema Fondamentale di Shannon stabilisce che per qualsiasi canale discreto senza memoria (DMC) con capacità di informazione $C = \max_{p(x)} I(X; Y)$, e per qualsiasi tasso di trasmissione $R < C$, esiste una sequenza di codici di blocco $(2^{nR}, n)$ avente probabilità massima d'errore asintoticamente nulla per $n \to \infty$.

### Modello di Canale e Definizioni di Errore

Un codice di canale $(2^{nR}, n)$ è costituito da:
1. Un insieme di indici di messaggio $\mathcal{W} = \{1, 2, \dots, M\}$ con $M = \lceil 2^{nR} \rceil$.
2. Una funzione di codifica $X^n: \mathcal{W} \to \mathcal{X}^n$, che mappa ciascun messaggio $w$ in una parola di canale $X^n(w) = (X_1(w), X_2(w), \dots, X_n(w))$. L'insieme delle $M$ parole costituisce il __codebook__ $\mathcal{C}$.
3. Una funzione di decodifica deterministica $g: \mathcal{Y}^n \to \mathcal{W}$, che associa a ciascuna sequenza ricevuta $y^n$ una stima del messaggio $\hat{w} = g(y^n)$.

La probabilità condizionata d'errore dato che è stato trasmesso il messaggio $w$ è:

$$
\lambda_w = \text{Pr}\{g(Y^n) \neq w \mid W = w\} = \sum_{y^n : g(y^n) \neq w} p(y^n \mid X^n(w))
$$

La probabilità d'errore massima $\lambda^{(n)}$ e la probabilità d'errore media $P_e^{(n)}$ sono definite rispettivamente da:

$$
\lambda^{(n)} = \max_{w \in \mathcal{W}} \lambda_w, \qquad P_e^{(n)} = \frac{1}{M} \sum_{w=1}^M \lambda_w
$$

### Tecnica di Codifica Casuale di Shannon (Random Coding)

Poiché determinare il codebook ottimo deterministico è un problema NP-difficile a ricerca esaustiva, Shannon introdusse la tecnica di mediare la probabilità d'errore su un intero ensemble probabilistico di codebook generati casualmente.

1. Si fissa una distribuzione di probabilità d'ingresso $p(x)$ che massimizza la mutua informazione $I(X; Y)$.
2. Si generano indipendentemente le $M = 2^{nR}$ parole di codice $X^n(1), X^n(2), \dots, X^n(M)$ estraendo ciascuna componente $X_j(w)$ in modo i.i.d. secondo la PMF $p(x)$:

$$
   \text{Pr}\{X^n(w) = x^n\} = \prod_{j=1}^n p(x_j)
$$

3. Il codebook $\mathcal{C}$ così generato viene reso noto sia al trasmettitore sia al ricevitore.

### Regola di Decodifica tramite Insieme Congiuntamente Tipico

Il decodificatore riceve la sequenza $Y^n$ ed esamina se esiste un unico messaggio $w$ la cui parola di codice $X^n(w)$ risulti congiuntamente tipica con $Y^n$ rispetto alla distribuzione congiunta $p(x, y) = p(x)p(y \mid x)$.

Il ricevitore dichiara $\hat{w} = w$ se e solo se:
1. $(X^n(w), Y^n) \in A_\epsilon^{(n)}$;
2. Non esiste alcun altro indice $w' \neq w$ tale che $(X^n(w'), Y^n) \in A_\epsilon^{(n)}$.

Se non esiste alcun indice congiuntamente tipico, oppure se ve ne sono due o più (ambiguità), il decodificatore dichiara errore.

### Analisi della Probabilità d'Errore Media sull'Ensemble

Per la simmetria costruttiva della generazione casuale del codice, la probabilità d'errore media sull'ensemble $\mathbb{E}[P_e^{(n)}]$ è indipendente dal messaggio effettivamente inviato. Possiamo dunque assumere senza perdita di generalità che sia stato trasmesso il messaggio $W = 1$.

Definiamo gli eventi di errore associati alle parole del codebook:

$$
E_i = \left\{ (X^n(i), Y^n) \in A_\epsilon^{(n)} \right\}, \quad i = 1, 2, \dots, M
$$

L'errore globale si verifica se la parola corretta non è congiuntamente tipica ($E_1^c$), oppure se almeno una parola errata risulta accidentalmente congiuntamente tipica ($E_i$ per qualche $i \ge 2$). Applicando il limite dell'unione (__union bound__):

$$
\text{Pr}\{\mathcal{E} \mid W = 1\} = \text{Pr}\{E_1^c \cup E_2 \cup E_3 \cup \dots \cup E_M\} \le \text{Pr}\{E_1^c\} + \sum_{i=2}^M \text{Pr}\{E_i\}
$$

Analizziamo i singoli termini sfruttando le proprietà cardinali del Teorema AEP congiunto:

1. __Comportamento della parola trasmessa ($E_1^c$)__:
   Poiché $Y^n$ è generata dal canale alimentato con $X^n(1)$, la coppia $(X^n(1), Y^n)$ è distribuita secondo la vera legge congiunta $\prod_{j=1}^n p(x_j, y_j)$. Per il Teorema AEP congiunto, per qualsiasi $\epsilon > 0$ esiste $n_1$ tale che per ogni $n > n_1$:

$$
   \text{Pr}\{E_1^c\} = \text{Pr}\left\{ (X^n(1), Y^n) \notin A_\epsilon^{(n)} \right\} < \epsilon
$$

2. __Comportamento delle parole non trasmesse ($E_i$ per $i \ge 2$)__:
   Per costruzione dell'ensemble casuale, per $i \neq 1$ la parola di codice $X^n(i)$ è generata in modo statisticamente indipendente da $X^n(1)$, e quindi indipendente dall'uscita del canale $Y^n$. Di conseguenza, la coppia $(X^n(i), Y^n)$ è distribuita secondo il prodotto delle distribuzioni marginali:

$$
   \text{Pr}\{X^n(i) = x^n, Y^n = y^n\} = p(x^n) p(y^n)
$$

   Per la seconda proprietà dell'insieme congiuntamente tipico, la probabilità che due sequenze indipendenti cadano in $A_\epsilon^{(n)}$ è maggiorata da:

$$
   \text{Pr}\{E_i\} = \text{Pr}\left\{ (X^n(i), Y^n) \in A_\epsilon^{(n)} \right\} \le 2^{-n(I(X; Y) - 3\epsilon)}
$$

Sostituendo le due maggiorazioni nel limite dell'unione:

$$
\mathbb{E}[P_e^{(n)}] \le \epsilon + \sum_{i=2}^M 2^{-n(I(X; Y) - 3\epsilon)} = \epsilon + (M - 1) 2^{-n(I(X; Y) - 3\epsilon)} < \epsilon + 2^{nR} 2^{-n(I(X; Y) - 3\epsilon)}
$$

Raggruppando gli esponenti in base 2:

$$
\mathbb{E}[P_e^{(n)}] < \epsilon + 2^{-n(I(X; Y) - R - 3\epsilon)}
$$

Se il tasso di trasmissione soddisfa la condizione:

$$
R < I(X; Y) - 3\epsilon
$$

l'esponente è strettamente negativo. Facendo tendere la lunghezza del blocco $n \to \infty$, il secondo termine decade esponenzialmente a zero. Esiste pertanto un intero $n_2$ tale che per ogni $n > \max(n_1, n_2)$:

$$
\mathbb{E}[P_e^{(n)}] < 2\epsilon
$$

### Dalla Media d'Ensemble al Codice Deterministico e Diserbo (Expurgation)

1. Poiché la probabilità d'errore media mediata su tutti i codebook è strettamente inferiore a $2\epsilon$, deve esistere almeno un codebook deterministico specifico $\mathcal{C}^*$ la cui probabilità d'errore media soddisfa $P_e^{(n)}(\mathcal{C}^*) < 2\epsilon$.
2. Per passare dalla probabilità media $P_e^{(n)}$ alla probabilità d'errore massima $\lambda^{(n)}$, si applica la tecnica del __diserbo__ (__expurgation__): si eliminano dal codebook le $M/2$ parole di codice che presentano le probabilità d'errore condizionate $\lambda_w$ più elevate.
3. Sulla metà migliore di parole rimanenti (cardinalità $M' = M/2 = 2^{nR - 1}$), la probabilità d'errore di ciascuna parola deve soddisfare necessariamente $\lambda_w < 4\epsilon$, assicurando che $\lambda^{(n)} < 4\epsilon$.
4. Il rate effettivo del codice expurgato è $R' = \frac{1}{n}\log_2(M/2) = R - \frac{1}{n}$, che converge a $R$ per $n \to \infty$.

Poiché $\epsilon > 0$ è arbitrariamente piccolo e la scelta di $p(x)$ può essere effettuata massimizzando la mutua informazione, qualsiasi rate $R < C = \max_{p(x)} I(X; Y)$ è raggiungibile con probabilità massima d'errore arbitrariamente piccola.

## Dimostrazione della Parte Inversa del Teorema di Codifica di Canale (Converse via Fano)

La parte inversa (__converse__) del teorema stabilisce che è fisicamente impossibile trasmettere informazione con probabilità d'errore asintoticamente nulla a un tasso superiore alla capacità di canale: se $R > C$, la probabilità d'errore è strettamente separata da zero per qualsiasi sequenza di codici di blocco.

### Dimostrazione Analitica tramite la Disuguaglianza di Fano

Si consideri una sequenza di codici $(2^{nR}, n)$ avente probabilità media d'errore $P_e^{(n)} = \text{Pr}\{\hat{W} \neq W\}$.

Il messaggio $W$ è distribuito uniformemente sull'insieme $\{1, 2, \dots, 2^{nR}\}$. La sua entropia a priori è:

$$
H(W) = \log_2(2^{nR}) = nR
$$

Le variabili aleatorie del sistema formano la catena di Markov:

$$
W \to X^n(W) \to Y^n \to \hat{W} = g(Y^n)
$$

Applicando la Disuguaglianza di Fano alla stima del messaggio $W$ a partire dall'osservazione dell'uscita di canale $Y^n$:

$$
H(W \mid Y^n) \le H_B(P_e^{(n)}) + P_e^{(n)} \log_2(2^{nR} - 1) \le 1 + P_e^{(n)} n R
$$

Espandiamo l'entropia del messaggio $H(W)$ attraverso la regola della catena per l'informazione mutua:

$$
nR = H(W) = H(W \mid Y^n) + I(W; Y^n) \le 1 + P_e^{(n)} n R + I(W; Y^n)
$$

Per la Data Processing Inequality applicata alla catena $W \to X^n \to Y^n$:

$$
I(W; Y^n) \le I(X^n; Y^n)
$$

Valutiamo ora la mutua informazione tra le sequenze di canale per un canale privo di memoria:

$$
I(X^n; Y^n) = H(Y^n) - H(Y^n \mid X^n) = H(Y^n) - \sum_{i=1}^n H(Y_i \mid Y^{i-1}, X^n)
$$

Poiché il canale è discreto senza memoria, l'uscita $Y_i$ all'istante $i$ dipende unicamente dall'ingresso corrente $X_i$:

$$
H(Y_i \mid Y^{i-1}, X^n) = H(Y_i \mid X_i)
$$

Applicando la proprietà di indipendenza come limite superiore dell'entropia congiunta ($H(Y^n) \le \sum_{i=1}^n H(Y_i)$):

$$
I(X^n; Y^n) \le \sum_{i=1}^n H(Y_i) - \sum_{i=1}^n H(Y_i \mid X_i) = \sum_{i=1}^n I(X_i; Y_i)
$$

Poiché per ciascun singolo uso del canale vale $I(X_i; Y_i) \le \max_{p(x)} I(X; Y) = C$:

$$
I(X^n; Y^n) \le \sum_{i=1}^n C = n C
$$

Sostituendo tale limite superiore nella disuguaglianza precedente:

$$
nR \le 1 + P_e^{(n)} n R + n C
$$

Dividendo l'intera disuguaglianza per $n$:

$$
R \le \frac{1}{n} + P_e^{(n)} R + C
$$

Riorganizzando rispetto a $P_e^{(n)}$:

$$
P_e^{(n)} \ge 1 - \frac{C}{R} - \frac{1}{nR}
$$

Se si tenta di trasmettere a un tasso $R > C$, facendo tendere $n \to \infty$, il termine $1/(nR) \to 0$, per cui:

$$
\liminf_{n \to \infty} P_e^{(n)} \ge 1 - \frac{C}{R} > 0
$$

La probabilità d'errore è limitata inferiormente da una costante positiva invariabile. È impossibile rendere la trasmissione affidabile se il rate supera la capacità di canale $C$. La condizione $R \le C$ è pertanto necessaria oltre che sufficiente.

## Dimostrazione del Teorema di Separazione Sorgente-Canale di Shannon

Il Teorema di Separazione Sorgente-Canale (Shannon 1948; Cover & Thomas, Sez. 7.13) stabilisce che la progettazione di un sistema di telecomunicazioni può essere scissa in due blocchi indipendenti (compressione di sorgente e codifica di canale) senza alcuna perdita di ottimalità complessiva.

### Enunciato del Teorema di Separazione

Sia $\{V_i\}$ un processo stocastico discreto stazionario ed ergodico avente entropy rate $H(\mathcal{V})$, e sia assegnato un canale discreto senza memoria avente capacità $C$.

1. Se $H(\mathcal{V}) < C$, esiste un sistema di codifica di sorgente e di canale tale che la sorgente può essere trasmessa sul canale e ricostruita con probabilità d'errore asintoticamente nulla:

$$
   \lim_{n \to \infty} \text{Pr}\{\hat{V}^n \neq V^n\} = 0
$$

2. Se $H(\mathcal{V}) > C$, non esiste alcun sistema di comunicazione (nemmeno integrando congiuntamente codifica di sorgente e di canale) in grado di trasmettere la sorgente con probabilità d'errore arbitrariamente piccola; per qualsiasi codice, la probabilità d'errore è limitata inferiormente lontano da zero.

### Dimostrazione della Condizione Sufficiente (Architettura a Due Stadi)

Supponiamo che $H(\mathcal{V}) < C$. Fissiamo un tasso intermedio $R$ tale che:

$$
H(\mathcal{V}) < R < C
$$

1. __Stadio 1 (Codifica di Sorgente)__: Poiché $R > H(\mathcal{V})$, per il Teorema di Codifica di Sorgente di Shannon possiamo comprimere la sequenza di simboli $V^n$ in un indice binario $W \in \{1, 2, \dots, 2^{nR}\}$ con probabilità di errore di compressione $P_{e, \text{sorgente}} < \epsilon / 2$.
2. __Stadio 2 (Codifica di Canale)__: Poiché $R < C$, per il Teorema di Codifica di Canale possiamo trasmettere l'indice $W$ attraverso $n$ usi del canale rumoroso mediante un codice $(2^{nR}, n)$ garantendo una probabilità di errore di decodifica $P_{e, \text{canale}} < \epsilon / 2$.
3. __Ricostruzione Globale__: Per il limite dell'unione, la probabilità d'errore complessiva soddisfa:

$$
   P_{e, \text{totale}} \le P_{e, \text{sorgente}} + P_{e, \text{canale}} < \frac{\epsilon}{2} + \frac{\epsilon}{2} = \epsilon
$$

   L'architettura separata a due stadi raggiunge l'affidabilità perfetta.

### Dimostrazione della Condizione Necessaria (Converse Congiunto)

Supponiamo per assurdo che esista uno schema congiunto arbitrario (non necessariamente separato) che mappa $V^n$ direttamente in $X^n$, e decodifica $Y^n$ producendo la stima $\hat{V}^n$ con $\lim_{n \to \infty} P_e^{(n)} = 0$.

Le variabili soddisfano la catena di Markov:

$$
V^n \to X^n \to Y^n \to \hat{V}^n
$$

Applicando la disuguaglianza di Fano alla stima del vettore $\hat{V}^n$:

$$
H(V^n \mid Y^n) \le 1 + P_e^{(n)} n \log_2 |\mathcal{V}|
$$

Sviluppando l'entropia della sorgente:

$$
H(V^n) = H(V^n \mid Y^n) + I(V^n; Y^n) \le 1 + P_e^{(n)} n \log_2 |\mathcal{V}| + I(X^n; Y^n)
$$

Poiché per il canale privo di memoria $I(X^n; Y^n) \le n C$:

$$
H(V^n) \le 1 + P_e^{(n)} n \log_2 |\mathcal{V}| + n C
$$

Dividendo per $n$:

$$
\frac{H(V^n)}{n} \le \frac{1}{n} + P_e^{(n)} \log_2 |\mathcal{V}| + C
$$

Facendo tendere $n \to \infty$, poiché la sorgente ha entropy rate $\lim_{n \to \infty} \frac{H(V^n)}{n} = H(\mathcal{V})$ e per ipotesi $P_e^{(n)} \to 0$:

$$
H(\mathcal{V}) \le C
$$

Se valesse $H(\mathcal{V}) > C$, si avrebbe $P_e^{(n)} \ge \frac{H(\mathcal{V}) - C - 1/n}{\log_2 |\mathcal{V}|} > 0$, rendendo impossibile la trasmissione lossless.

Ciò dimostra l'universalità del principio di separazione: la progettazione separata della compressione dati e della codifica di canale è ottima in senso assoluto e non comporta alcun degrado prestazionale rispetto a schemi di codifica congiunta sorgente-canale.


## Dimostrazione Variazionale dell'Ottimalità della PDF Gaussiana come Massimizzatore di Entropia Differenziale

Il Teorema di Massima Entropia Differenziale (Shannon 1948; Cover & Thomas, Teorema 8.6.5) stabilisce che tra tutte le distribuzioni di probabilità continue multidimensionali aventi matrice di covarianza assegnata, la distribuzione Normale multivariata massimizza univocamente l'entropia differenziale.

### Enunciato del Teorema

Sia $\mathbf{X} \in \mathbb{R}^n$ un vettore aleatorio continuo a media nulla con matrice di covarianza assegnata e definita positiva:

$$
\mathbf{K} = \mathbb{E}[\mathbf{X}\mathbf{X}^T] > 0
$$

Sia $g(\mathbf{x})$ la sua effettiva funzione di densità di probabilità (PDF). Allora l'entropia differenziale $h(\mathbf{X}) = -\int_{\mathbb{R}^n} g(\mathbf{x}) \log_2 g(\mathbf{x}) \mathrm{d}\mathbf{x}$ soddisfa il limite superiore:

$$
h(\mathbf{X}) \le \frac{1}{2} \log_2 \left( (2\pi e)^n \det \mathbf{K} \right)
$$

con eguaglianza se e solo se $\mathbf{X}$ è distribuito secondo la densità Gaussiana multivariata $\mathbf{X} \sim \mathcal{N}_n(\mathbf{0}, \mathbf{K})$.

### Dimostrazione Analitica tramite la Divergenza di Kullback-Leibler

Sia $\phi(\mathbf{x})$ la funzione di densità di probabilità Gaussiana multivariata a media nulla avente la medesima matrice di covarianza $\mathbf{K}$:

$$
\phi(\mathbf{x}) = \frac{1}{(2\pi)^{n/2} (\det \mathbf{K})^{1/2}} \exp\left( -\frac{1}{2} \mathbf{x}^T \mathbf{K}^{-1} \mathbf{x} \right)
$$

Calcoliamo l'entropia differenziale naturale (espressa in nat) della densità Gaussiana $\phi(\mathbf{x})$:

$$
\ln \phi(\mathbf{x}) = -\frac{n}{2} \ln(2\pi) - \frac{1}{2} \ln(\det \mathbf{K}) - \frac{1}{2} \mathbf{x}^T \mathbf{K}^{-1} \mathbf{x}
$$

Integrando rispetto a $\phi(\mathbf{x})$:

$$
h_e(\phi) = -\int_{\mathbb{R}^n} \phi(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x} = \frac{n}{2} \ln(2\pi) + \frac{1}{2} \ln(\det \mathbf{K}) + \frac{1}{2} \mathbb{E}_\phi[\mathbf{X}^T \mathbf{K}^{-1} \mathbf{X}]
$$

Sfruttando la proprietà ciclica della traccia per forme quadratiche:

$$
\mathbb{E}_\phi[\mathbf{X}^T \mathbf{K}^{-1} \mathbf{X}] = \mathbb{E}_\phi[\text{Tr}(\mathbf{K}^{-1} \mathbf{X}\mathbf{X}^T)] = \text{Tr}\left( \mathbf{K}^{-1} \mathbb{E}_\phi[\mathbf{X}\mathbf{X}^T] \right) = \text{Tr}(\mathbf{K}^{-1} \mathbf{K}) = \text{Tr}(\mathbf{I}_n) = n
$$

Ne deriva:

$$
h_e(\phi) = \frac{1}{2} \ln(2\pi)^n + \frac{1}{2} \ln(\det \mathbf{K}) + \frac{n}{2} = \frac{1}{2} \ln\left( (2\pi e)^n \det \mathbf{K} \right) \quad \text{nat}
$$

Si consideri ora la divergenza di Kullback-Leibler (entropia relativa) tra la reale densità $g(\mathbf{x})$ e la densità Gaussiana di riferimento $\phi(\mathbf{x})$:

$$
D(g \parallel \phi) = \int_{\mathbb{R}^n} g(\mathbf{x}) \ln \frac{g(\mathbf{x})}{\phi(\mathbf{x})} \mathrm{d}\mathbf{x}
$$

Per il Teorema della Disuguaglianza dell'Informazione esteso a densità continue, la divergenza KL è non negativa:

$$
D(g \parallel \phi) \ge 0
$$

con eguaglianza se e solo se $g(\mathbf{x}) = \phi(\mathbf{x})$ quasi ovunque.

Sviluppiamo algebricamente la divergenza:

$$
D(g \parallel \phi) = \int_{\mathbb{R}^n} g(\mathbf{x}) \ln g(\mathbf{x}) \mathrm{d}\mathbf{x} - \int_{\mathbb{R}^n} g(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x} = -h_e(g) - \int_{\mathbb{R}^n} g(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x}
$$

Valutiamo il secondo integrale integrando la forma esplicita di $\ln \phi(\mathbf{x})$ rispetto alla misura $g(\mathbf{x})$:

$$
\int_{\mathbb{R}^n} g(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x} = -\frac{n}{2} \ln(2\pi) - \frac{1}{2} \ln(\det \mathbf{K}) - \frac{1}{2} \int_{\mathbb{R}^n} g(\mathbf{x}) (\mathbf{x}^T \mathbf{K}^{-1} \mathbf{x}) \mathrm{d}\mathbf{x}
$$

Sfruttando nuovamente la traccia e la definizione della matrice di covarianza di $g$:

$$
\int_{\mathbb{R}^n} g(\mathbf{x}) (\mathbf{x}^T \mathbf{K}^{-1} \mathbf{x}) \mathrm{d}\mathbf{x} = \mathbb{E}_g[\mathbf{X}^T \mathbf{K}^{-1} \mathbf{X}] = \text{Tr}\left( \mathbf{K}^{-1} \mathbb{E}_g[\mathbf{X}\mathbf{X}^T] \right) = \text{Tr}(\mathbf{K}^{-1} \mathbf{K}) = n
$$

Il secondo integrale dipende esclusivamente dai momenti del secondo ordine di $g(\mathbf{x})$, che per ipotesi coincidono con $\mathbf{K}$. Di conseguenza:

$$
\int_{\mathbb{R}^n} g(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x} = \int_{\mathbb{R}^n} \phi(\mathbf{x}) \ln \phi(\mathbf{x}) \mathrm{d}\mathbf{x} = -h_e(\phi)
$$

Sostituendo tale identità fondamentale nella divergenza di Kullback-Leibler:

$$
D(g \parallel \phi) = -h_e(g) - (-h_e(\phi)) = h_e(\phi) - h_e(g) \ge 0
$$

da cui discende:

$$
h_e(g) \le h_e(\phi) = \frac{1}{2} \ln\left( (2\pi e)^n \det \mathbf{K} \right) \quad \text{nat}
$$

Convertendo in base 2 (bit):

$$
h(g) \le \frac{1}{2} \log_2 \left( (2\pi e)^n \det \mathbf{K} \right) \quad \text{bit}
$$

L'uguaglianza stretta è verificata se e solo se $D(g \parallel \phi) = 0$, il che implica $g(\mathbf{x}) = \phi(\mathbf{x})$ quasi ovunque. La distribuzione Gaussiana multivariata è l'unico massimizzatore di entropia differenziale a covarianza fissata.

## Derivazione Rigorosa della Formula di Capacità di Shannon-Hartley

La formula di Shannon-Hartley descrive la capacità di trasmissione di un canale analogico a tempo continuo a banda limitata $B$ perturbato da rumore additivo bianco gaussiano (AWGN).

### Modello di Canale a Tempo Continuo

Si consideri il canale a tempo continuo:

$$
Y(t) = X(t) + Z(t)
$$

sotto le seguenti ipotesi operative:
1. Il segnale trasmesso $X(t)$ è rigorosamente limitato in frequenza alla banda $[-B, B]$ (Hz) e rispetta il vincolo di potenza media:

$$
   \lim_{T \to \infty} \frac{1}{T} \int_0^T X^2(t) \mathrm{d}t \le P
$$

2. Il rumore $Z(t)$ è un processo gaussiano stazionario, a media nulla, indipendente da $X(t)$, caratterizzato da densità spettrale di potenza (PSD) bilaterale piatta:

$$
   \mathcal{S}_Z(f) = \frac{N_0}{2} \quad \text{W/Hz}
$$

### Discretizzazione tramite il Teorema del Campionamento di Nyquist-Shannon

Per il Teorema del Campionamento, qualsiasi segnale a banda limitata $[-B, B]$ è univocamente e perfettamente rappresentato dalla sequenza dei suoi campioni discreti prelevati a frequenza di Nyquist $f_s = 2B$ campioni al secondo (intervallo di campionamento $T_s = \frac{1}{2B}$).

Su un orizzonte temporale finito di durata $T$, il segnale è completamente specificato da $n = 2BT$ campioni discreti:

$$
Y_i = X_i + Z_i, \quad i = 1, 2, \dots, n
$$

Calcoliamo i parametri probabilistici dei campioni discreti:

1. __Energia e Potenza del Segnale__:
   Il segnale a banda limitata $X(t)$ ammette lo sviluppo di campionamento $X(t) = \sum_{i} X_i \text{sinc}(2Bt - i)$, dove $X_i = X(i/(2B))$. Poiché le funzioni $\text{sinc}(2Bt - i)$ formano una base ortogonale con $\int_{-\infty}^{+\infty} \text{sinc}(2Bt - i)\text{sinc}(2Bt - j)\mathrm{d}t = \frac{1}{2B}\delta_{ij}$, l'energia del segnale su un intervallo di durata $T$ (contenente $n = 2BT$ campioni) vale:

$$
   E = \int_0^T X^2(t) \mathrm{d}t = \frac{1}{2B} \sum_{i=1}^{2BT} X_i^2 = P \cdot T
$$

   da cui la potenza media per singolo campione discreto (varianza di $X_i$) è data da:

$$
   \sigma_X^2 = \mathbb{E}[X_i^2] = \frac{1}{2BT} \sum_{i=1}^{2BT} X_i^2 = P
$$

2. __Varianza del Rumore Filtrato__:
   Il ricevitore è dotato di un filtro passa-basso ideale di banda $B$. La potenza di rumore che attraversa il filtro è pari all'integrale della PSD bilaterale sulla banda passante:

$$
   \sigma_Z^2 = \text{Var}(Z_i) = \int_{-B}^B \mathcal{S}_Z(f) \mathrm{d}f = \int_{-B}^B \frac{N_0}{2} \mathrm{d}f = \frac{N_0}{2} \cdot (2B) = N_0 B
$$

   Poiché la funzione di autocorrelazione del rumore filtrato è una sinc $\mathcal{R}_Z(\tau) = N_0 B \text{sinc}(2B\tau)$, agli istanti di campionamento $\tau = k T_s = k/(2B)$ con $k \neq 0$ la funzione si annulla identicamente. I campioni di rumore $Z_i$ sono dunque variabili aleatorie gaussiane incorrelate e, data la gaussianità, mutuamente indipendenti:

$$
   Z_i \sim \mathcal{N}(0, N_0 B) \quad \text{i.i.d.}
$$

### Calcolo della Capacità per Campione Discreto

Per ciascun campione discreto, l'informazione mutua tra ingresso e uscita è:

$$
I(X_i; Y_i) = h(Y_i) - h(Y_i \mid X_i) = h(Y_i) - h(X_i + Z_i \mid X_i) = h(Y_i) - h(Z_i)
$$

Poiché $Z_i \sim \mathcal{N}(0, N_0 B)$, la sua entropia differenziale è data da:

$$
h(Z_i) = \frac{1}{2} \log_2(2\pi e N_0 B)
$$

La potenza del segnale d'uscita soddisfa:

$$
\mathbb{E}[Y_i^2] = \mathbb{E}[(X_i + Z_i)^2] = \mathbb{E}[X_i^2] + \mathbb{E}[Z_i^2] = P + N_0 B
$$

Per il Teorema di Massima Entropia Differenziale, per una variabile con varianza fissata $\sigma_Y^2 = P + N_0 B$, l'entropia differenziale $h(Y_i)$ è massimizzata se e solo se $Y_i$ è gaussiana, il che avviene quando l'ingresso $X_i$ è gaussiano $X_i \sim \mathcal{N}(0, P)$:

$$
h(Y_i) \le \frac{1}{2} \log_2 \left( 2\pi e (P + N_0 B) \right)
$$

La capacità per singolo campione discreto vale pertanto direttamente:

$$
C_{\text{campione}} = \max I(X_i; Y_i) = \frac{1}{2} \log_2 \left( 2\pi e (P + N_0 B) \right) - \frac{1}{2} \log_2(2\pi e N_0 B) = \frac{1}{2} \log_2 \left( 1 + \frac{P}{N_0 B} \right) \quad \text{bit/campione}
$$

### Formula Finale di Shannon-Hartley

Poiché il canale mette a disposizione $2B$ campioni ortogonali al secondo, la capacità di canale complessiva espressa in bit al secondo (bit/s) è:

$$
C = 2B \cdot C_{\text{campione}} = 2B \cdot \frac{1}{2} \log_2 \left( 1 + \frac{P}{N_0 B} \right)
$$

Si ottiene la celebre __Formula di Shannon-Hartley__:

$$
C = B \log_2 \left( 1 + \frac{P}{N_0 B} \right) = B \log_2(1 + \text{SNR}) \quad \text{bit/s}
$$

dove $\text{SNR} = \frac{P}{N_0 B}$ è il rapporto segnale-rumore adimensionale sulla banda di ricezione $B$.

### Comportamento Asintotico a Banda Infinita ($B \to \infty$)

Se la larghezza di banda $B$ viene aumentata indefinitamente mantenendo costante la potenza totale trasmessa $P$ e la densità di rumore $N_0$:

$$
\lim_{B \to \infty} C = \lim_{B \to \infty} B \log_2 \left( 1 + \frac{P}{N_0 B} \right) = \lim_{B \to \infty} \frac{B}{\ln 2} \ln \left( 1 + \frac{P}{N_0 B} \right)
$$

Ponendo $x = \frac{P}{N_0 B} \to 0$ per $B \to \infty$, e sfruttando lo sviluppo di Taylor al primo ordine $\ln(1 + x) = x + O(x^2)$:

$$
C_\infty = \lim_{B \to \infty} \frac{B}{\ln 2} \left( \frac{P}{N_0 B} \right) = \frac{P}{N_0 \ln 2} \approx 1.4427 \frac{P}{N_0} \quad \text{bit/s}
$$

La capacità non diverge all'infinito, ma satura a un asintoto orizzontale finito. Aumentare la banda oltre una certa soglia incrementa proporzionalmente il rumore termico totale raccolto ($N_0 B$), bilanciando esattamente il guadagno dovuto al maggior numero di campioni per secondo.

### Il Limite Ultimo di Shannon ($E_b / N_0 \ge -1.59$ dB)

Sia $R$ il tasso di trasmissione espresso in bit/s. La potenza media del segnale può essere riscritta come il prodotto tra l'energia spesa per singolo bit di informazione $E_b$ e il rate $R$:

$$
P = R \cdot E_b
$$

Sostituendo nella formula di capacità e imponendo la condizione di trasmissibilità affidabile $R \le C$:

$$
R \le B \log_2 \left( 1 + \frac{R E_b}{N_0 B} \right)
$$

Definendo l'efficienza spettrale $\eta = \frac{R}{B}$ (espressa in bit/s/Hz):

$$
\eta \le \log_2 \left( 1 + \eta \frac{E_b}{N_0} \right) \iff 2^\eta - 1 \le \eta \frac{E_b}{N_0} \implies \frac{E_b}{N_0} \ge \frac{2^\eta - 1}{\eta}
$$

Nel limite di banda infinita (regime a massima efficienza di potenza, dove $\eta = R/B \to 0$):

$$
\lim_{\eta \to 0} \frac{2^\eta - 1}{\eta} = \left. \frac{\mathrm{d}}{\mathrm{d}\eta} 2^\eta \right|_{\eta = 0} = \ln 2
$$

Si ottiene il __Limite Ultimo di Shannon__:

$$
\frac{E_b}{N_0} \ge \ln 2 \approx 0.69315
$$

Convertendo il rapporto adimensionale in decibel (dB):

$$
\left( \frac{E_b}{N_0} \right)_{\text{dB}} \ge 10 \log_{10}(\ln 2) = 10 \log_{10}(0.69315) \approx -1.5917 \quad \text{dB}
$$

Nessun sistema di comunicazione wireless o cablato potrà mai operare con probabilità d'errore tendente a zero se l'energia ricevuta per bit rispetto alla densità spettrale di rumore scende al di sotto della soglia universale di $-1.59$ dB.

## Dimostrazione Informatica della Disuguaglianza di Hadamard

La Disuguaglianza di Hadamard (1893) è un risultato fondamentale dell'algebra lineare che stabilisce un limite superiore al determinante di matrici semidefinite positive.

### Enunciato

Sia $\mathbf{K} = [K_{ij}] \in \mathbb{R}^{n \times n}$ una matrice simmetrica definita positiva. Allora:

$$
\det \mathbf{K} \le \prod_{i=1}^n K_{ii}
$$

con eguaglianza se e solo se $\mathbf{K}$ è una matrice diagonale ($K_{ij} = 0$ per ogni $i \neq j$).

### Dimostrazione tramite Entropia Differenziale Multivariata

Si consideri un vettore aleatorio gaussiano multivariato $\mathbf{X} = (X_1, X_2, \dots, X_n)^T \sim \mathcal{N}_n(\mathbf{0}, \mathbf{K})$.

L'entropia differenziale congiunta del vettore $\mathbf{X}$ è data da:

$$
h(X_1, X_2, \dots, X_n) = \frac{1}{2} \log_2 \left( (2\pi e)^n \det \mathbf{K} \right)
$$

Applicando la regola della catena per l'entropia differenziale:

$$
h(X_1, X_2, \dots, X_n) = \sum_{i=1}^n h(X_i \mid X_1, \dots, X_{i-1})
$$

Poiché il condizionamento non può mai aumentare l'entropia differenziale ($h(A \mid B) \le h(A)$):

$$
h(X_1, X_2, \dots, X_n) \le \sum_{i=1}^n h(X_i)
$$

Ciascuna componente marginale $X_i$ è una variabile aleatoria gaussiana scalare con varianza $\sigma_i^2 = K_{ii}$. La sua entropia differenziale unidimensionale vale:

$$
h(X_i) = \frac{1}{2} \log_2(2\pi e K_{ii})
$$

Sommando su tutti gli indici $i = 1, \dots, n$:

$$
\sum_{i=1}^n h(X_i) = \frac{1}{2} \sum_{i=1}^n \log_2(2\pi e K_{ii}) = \frac{1}{2} \log_2 \left( (2\pi e)^n \prod_{i=1}^n K_{ii} \right)
$$

Confrontando il membro sinistro e il membro destro:

$$
\frac{1}{2} \log_2 \left( (2\pi e)^n \det \mathbf{K} \right) \le \frac{1}{2} \log_2 \left( (2\pi e)^n \prod_{i=1}^n K_{ii} \right)
$$

Essendo la funzione $\log_2(\cdot)$ strettamente monotona crescente:

$$
(2\pi e)^n \det \mathbf{K} \le (2\pi e)^n \prod_{i=1}^n K_{ii} \iff \det \mathbf{K} \le \prod_{i=1}^n K_{ii}
$$

L'uguaglianza si verifica se e solo se $h(X_i \mid X_1, \dots, X_{i-1}) = h(X_i)$ per ogni $i$, il che avviene se e solo se le variabili $X_1, \dots, X_n$ sono mutuamente indipendenti. Poiché per variabili congiuntamente gaussiane l'indipendenza equivale all'incorrelazione ($K_{ij} = 0$ per $i \neq j$), l'eguaglianza vale se e solo se la matrice $\mathbf{K}$ è puramente diagonale.




## Teorema di Rate-Distortion per la Sorgente Gaussiana con Distorsione Quadratica

Il Teorema di Rate-Distortion di Shannon (1959; Cover & Thomas, Teorema 10.3.2) caratterizza il limite teorico fondamentale alla compressione con perdita di una sorgente continua gaussiana unidimensionale sotto distorsione quadratica media (MSE).

### Enunciato del Teorema

Sia $X \sim \mathcal{N}(0, \sigma^2)$ una variabile aleatoria continua gaussiana a media nulla con varianza $\sigma^2 > 0$. Si adotti come misura di fedeltà l'errore quadratico:

$$
d(x, \hat{x}) = (x - \hat{x})^2
$$

Allora la funzione Rate-Distortion $R(D)$ della sorgente è data analiticamente da:

$$
R(D) = \begin{cases} \frac{1}{2} \log_2 \left( \frac{\sigma^2}{D} \right) & \text{se } 0 \le D \le \sigma^2 \\ 0 & \text{se } D > \sigma^2 \end{cases} \quad \text{bit/campione}
$$

e la corrispondente funzione Distortion-Rate $D(R)$ vale:

$$
D(R) = \sigma^2 2^{-2R}
$$

### Dimostrazione del Limite Inferiore (Parte Inversa / Converse)

Per qualsiasi distribuzione condizionata $p(\hat{x} \mid x)$ tale che $\mathbb{E}[(X - \hat{X})^2] \le D$, sviluppiamo l'informazione mutua tra la sorgente $X$ e la sua ricostruzione $\hat{X}$ tramite le entropie differenziali:

$$
I(X; \hat{X}) = h(X) - h(X \mid \hat{X})
$$

Poiché l'entropia differenziale è invariante per traslazioni deterministiche condizionate a $\hat{X}$:

$$
h(X \mid \hat{X}) = h(X - \hat{X} \mid \hat{X})
$$

Sfruttando la proprietà fondamentale secondo cui il condizionamento non può mai incrementare l'entropia differenziale ($h(A \mid B) \le h(A)$):

$$
h(X - \hat{X} \mid \hat{X}) \le h(X - \hat{X})
$$

da cui si ottiene la disuguaglianza:

$$
I(X; \hat{X}) \ge h(X) - h(X - \hat{X})
$$

Valutiamo i due termini di entropia differenziale:
1. La sorgente $X$ è gaussiana con varianza $\sigma^2$, pertanto la sua entropia differenziale è:

$$
   h(X) = \frac{1}{2} \log_2(2\pi e \sigma^2)
$$

2. La variabile d'errore di stima $E = X - \hat{X}$ ha media quadratica vincolata da:

$$
   \mathbb{E}[E^2] = \mathbb{E}[(X - \hat{X})^2] \le D
$$

   Poiché la varianza è limitata dal momento secondo $\text{Var}(E) \le \mathbb{E}[E^2] \le D$, e per il Teorema di Massima Entropia Differenziale la distribuzione gaussiana massimizza l'entropia per una varianza data:

$$
   h(X - \hat{X}) \le \frac{1}{2} \log_2(2\pi e \text{Var}(E)) \le \frac{1}{2} \log_2(2\pi e D)
$$

Sostituendo le due espressioni nella disequazione dell'informazione mutua:

$$
I(X; \hat{X}) \ge \frac{1}{2} \log_2(2\pi e \sigma^2) - \frac{1}{2} \log_2(2\pi e D) = \frac{1}{2} \log_2 \left( \frac{2\pi e \sigma^2}{2\pi e D} \right) = \frac{1}{2} \log_2 \left( \frac{\sigma^2}{D} \right)
$$

Poiché tale limite inferiore vale per qualsiasi canale di quantizzazione $p(\hat{x} \mid x)$ che rispetta il vincolo di distorsione $\mathbb{E}[(X - \hat{X})^2] \le D$, ne consegue che:

$$
R(D) = \min_{p(\hat{x} \mid x): \, \mathbb{E}[(X-\hat{X})^2] \le D} I(X; \hat{X}) \ge \frac{1}{2} \log_2 \left( \frac{\sigma^2}{D} \right)
$$

### Dimostrazione della Raggiungibilità (Canale Test Inverso)

Per dimostrare che il limite inferiore è stringente e coincidente con il minimo per ogni $0 < D \le \sigma^2$, si deve esibire una distribuzione congiunta $p(x, \hat{x})$ che soddisfi contemporaneamente:
1. La marginale su $X$ sia esattamente $\mathcal{N}(0, \sigma^2)$.
2. La distorsione media sia esattamente $\mathbb{E}[(X - \hat{X})^2] = D$.
3. L'informazione mutua raggiunga l'uguaglianza $I(X; \hat{X}) = \frac{1}{2}\log_2(\sigma^2 / D)$.

A differenza dei canali di comunicazione tradizionali in cui l'ingresso genera l'uscita in avanti, nella teoria Rate-Distortion risulta analiticamente vantaggioso parametrizzare il sistema definendo il __canale test inverso__ (Backward Test Channel):

$$
X = \hat{X} + Z
$$

dove:
- La variabile di ricostruzione $\hat{X}$ è gaussiana: $\hat{X} \sim \mathcal{N}(0, \sigma^2 - D)$.
- Il rumore di rappresentazione $Z$ è gaussiano, a media nulla, con varianza pari a $D$: $Z \sim \mathcal{N}(0, D)$.
- $\hat{X}$ e $Z$ sono statisticamente indipendenti.

Verifichiamo le tre proprietà:
1. __Marginale di $X$__:
   Essendo somma di due gaussiane indipendenti, $X$ è gaussiana a media nulla con varianza:

$$
   \mathbb{E}[X^2] = \mathbb{E}[\hat{X}^2] + \mathbb{E}[Z^2] = (\sigma^2 - D) + D = \sigma^2
$$

   La distribuzione marginale della sorgente è rispettata esattamente.

2. __Distorsione media__:
   L'errore di ricostruzione è $X - \hat{X} = Z$. Di conseguenza:

$$
   \mathbb{E}[(X - \hat{X})^2] = \mathbb{E}[Z^2] = D
$$

   Il vincolo di distorsione è soddisfatto con eguaglianza stretta.

3. __Informazione mutua__:
   Calcoliamo l'entropia condizionata:

$$
   h(X \mid \hat{X}) = h(\hat{X} + Z \mid \hat{X}) = h(Z \mid \hat{X}) = h(Z)
$$

   essendo $Z$ indipendente da $\hat{X}$. Poiché $Z \sim \mathcal{N}(0, D)$, la sua entropia è $h(Z) = \frac{1}{2}\log_2(2\pi e D)$. Sostituendo:

$$
   I(X; \hat{X}) = h(X) - h(X \mid \hat{X}) = \frac{1}{2}\log_2(2\pi e \sigma^2) - \frac{1}{2}\log_2(2\pi e D) = \frac{1}{2}\log_2\left( \frac{\sigma^2}{D} \right)
$$

Il canale test inverso raggiunge esattamente il limite inferiore. Se infine $D \ge \sigma^2$, è sufficiente scegliere la stima banale deterministica $\hat{X} = 0$, per la quale $\mathbb{E}[(X - 0)^2] = \sigma^2 \le D$, richiedendo $R(D) = I(X; 0) = 0$ bit. Il teorema è integralmente dimostrato.

## Derivazione Rigorosa della Soluzione di Reverse Water-Filling per Sorgenti Gaussiane Parallele

Si consideri un vettore di $m$ sorgenti continue gaussiane indipendenti $X_1, X_2, \dots, X_m$ aventi varianze decrescenti:

$$
X_i \sim \mathcal{N}(0, \sigma_i^2), \quad \sigma_1^2 \ge \sigma_2^2 \ge \dots \ge \sigma_m^2
$$

Si intenda comprimere l'intero vettore allocando un budget di distorsione quadratico complessivo pari a $D$, ripartito tra le singole componenti:

$$
\sum_{i=1}^m D_i = D
$$

### Formulazione del Problema Variazionale

Poiché le componenti sono indipendenti, l'informazione mutua totale è la somma delle informazioni mutue marginali. La funzione Rate-Distortion complessiva è il risultato della minimizzazione:

$$
R(D) = \min_{\{D_i\}} \sum_{i=1}^m R_i(D_i) = \min_{\{D_i\}} \sum_{i=1}^m \frac{1}{2} \log_2 \left( \frac{\sigma_i^2}{D_i} \right)
$$

sotto i vincoli:

$$
\sum_{i=1}^m D_i = D, \quad 0 < D_i \le \sigma_i^2 \quad \forall i = 1, \dots, m
$$

### Risoluzione tramite Moltiplicatori di Lagrange e Condizioni KKT

Convertendo i logaritmi in base naturale, la funzione Lagrangiana del problema di ottimizzazione convessa vincolata è data da:

$$
\mathcal{L}(D_1, \dots, D_m, \nu) = \sum_{i=1}^m \frac{1}{2} \ln \left( \frac{\sigma_i^2}{D_i} \right) + \nu \left( \sum_{i=1}^m D_i - D \right)
$$

Calcolando la derivata parziale rispetto a ciascuna distorsione $D_i$:

$$
\frac{\partial \mathcal{L}}{\partial D_i} = -\frac{1}{2 D_i} + \nu = 0 \implies D_i = \frac{1}{2\nu} \equiv \lambda
$$

dove $\lambda = \frac{1}{2\nu}$ è un parametro scalare costante indipendente dall'indice $i$ (livello dell'acqua o soglia di taglio).

Imponendo il vincolo di bordo $D_i \le \sigma_i^2$ (poiché per una componente con varianza $\sigma_i^2$ non ha senso allocare una distorsione superiore alla varianza stessa, in quanto con $D_i = \sigma_i^2$ il rate collassa a zero scegliendo $\hat{X}_i = 0$), le condizioni di Karush-Kuhn-Tucker (KKT) stabiliscono la regola ottima di allocazione della distorsione:

$$
D_i = \min(\lambda, \sigma_i^2) = \begin{cases} \lambda & \text{se } \lambda < \sigma_i^2 \\ \sigma_i^2 & \text{se } \lambda \ge \sigma_i^2 \end{cases}
$$

dove la costante $\lambda$ è univocamente determinata dall'equazione implicita di bilancio:

$$
\sum_{i=1}^m \min(\lambda, \sigma_i^2) = D
$$

### Espressione del Rate per Singola Componente e Rate Totale

Sostituendo la distorsione ottima $D_i$ nella funzione di rate di ciascuna componente:

$$
R_i(D_i) = \max\left( 0, \, \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) \right) = \begin{cases} \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) & \text{se } \sigma_i^2 > \lambda \\ 0 & \text{se } \sigma_i^2 \le \lambda \end{cases}
$$

Il tasso di codifica totale per il blocco di $m$ sorgenti vale:

$$
R(D) = \sum_{i=1}^m R_i(D_i) = \sum_{i=1}^m \max\left( 0, \, \frac{1}{2}\log_2\left( \frac{\sigma_i^2}{\lambda} \right) \right) \quad \text{bit/vettore}
$$

### Interpretazione Geometrica del Reverse Water-Filling

Il meccanismo è denominato __Reverse Water-Filling__ (riempimento d'acqua inverso) per contrasto con il water-filling standard impiegato per la capacità di canale:
1. Si visualizza un recipiente a canne verticali la cui base è posta alla quota zero e le cui altezze corrispondono alle varianze $\sigma_i^2$ delle sorgenti.
2. Si introduce "acqua" (la distorsione tollerata $D$) fino a raggiungere un livello costante $\lambda$.
3. __Componenti ad alta energia ($\sigma_i^2 > \lambda$)__: La distorsione allocata è plafonata al valore costante $\lambda$, mentre il rate $R_i = \frac{1}{2}\log_2(\sigma_i^2 / \lambda)$ è strettamente positivo. Più grande è la varianza, maggiore è il numero di bit investiti per codificarla con precisione.
4. __Componenti a bassa energia ($\sigma_i^2 \le \lambda$)__: Il livello dell'acqua supera l'altezza della colonna. La distorsione coincide interamente con la varianza ($D_i = \sigma_i^2$) e il rate assegnato è nullo ($R_i = 0$). Tali sorgenti vengono scartate (trascurate) dal codificatore, ponendo deterministicamente $\hat{X}_i = 0$.

Questo principio matematico costituisce il cardine della __codifica per trasformata__ (Transform Coding, Goyal 2001) alla base di standard di compressione multimediale quali JPEG, MP3, AAC e wavelet: si proietta il segnale su una base ortogonale di decorrelazione (Karhunen-Loève Transform o Discrete Cosine Transform) e si applica il reverse water-filling scartando i coefficienti spettrali a varianza trascurabile.

## Dimostrazione della Convessità della Funzione di Rate-Distortion $R(D)$

La convessità rispetto alla distorsione $D$ è una delle proprietà strutturali più importanti della funzione Rate-Distortion, garantendo l'assenza di minimi locali e la decrescenza monotona dell'efficienza marginale di compressione.

### Enunciato

Sia $R(D)$ la funzione Rate-Distortion di una sorgente stazionaria con misura di distorsione $d(x, \hat{x})$. Allora $R(D)$ è una funzione convessa di $D$:

$$
R(\alpha D_1 + (1 - \alpha) D_2) \le \alpha R(D_1) + (1 - \alpha) R(D_2), \quad \forall \alpha \in [0, 1]
$$

### Dimostrazione Analitica tramite Miscela di Canali di Transizione

Siano $D_1$ e $D_2$ due livelli di distorsione ammissibili con corrispondenti tassi ottimi $R(D_1)$ e $R(D_2)$.

Per la definizione di $R(D)$, per ogni $\epsilon > 0$ esistono due distribuzioni condizionate $q_1(\hat{x} \mid x)$ e $q_2(\hat{x} \mid x)$ tali che:

$$
\mathbb{E}_{q_1}[d(X, \hat{X})] \le D_1, \quad I_{q_1}(X; \hat{X}) \le R(D_1) + \epsilon
$$

$$
\mathbb{E}_{q_2}[d(X, \hat{X})] \le D_2, \quad I_{q_2}(X; \hat{X}) \le R(D_2) + \epsilon
$$

Fissato un coefficiente $\alpha \in [0, 1]$, si definisca la distribuzione condizionata di miscela (o combinazione convessa dei canali):

$$
q_\alpha(\hat{x} \mid x) = \alpha q_1(\hat{x} \mid x) + (1 - \alpha) q_2(\hat{x} \mid x)
$$

Valutiamo la distorsione media generata dal canale $q_\alpha$:

$$
\mathbb{E}_{q_\alpha}[d(X, \hat{X})] = \sum_{x} \sum_{\hat{x}} p(x) \left[ \alpha q_1(\hat{x} \mid x) + (1 - \alpha) q_2(\hat{x} \mid x) \right] d(x, \hat{x})
$$

Sfruttando la linearità rispetto ai pesi di miscela:

$$
\mathbb{E}_{q_\alpha}[d(X, \hat{X})] = \alpha \mathbb{E}_{q_1}[d(X, \hat{X})] + (1 - \alpha) \mathbb{E}_{q_2}[d(X, \hat{X})] \le \alpha D_1 + (1 - \alpha) D_2 \equiv D_\alpha
$$

Pertanto la distribuzione $q_\alpha$ è una scelta ammissibile per il calcolo di $R(D_\alpha)$.

Consideriamo ora l'informazione mutua $I(X; \hat{X})$ come funzionale della distribuzione di transizione $p(\hat{x} \mid x)$ per una data distribuzione di ingresso $p(x)$ fissata. È un teorema classico della teoria dell'informazione (Cover & Thomas, Teorema 2.7.4) che $I(X; \hat{X})$ è una funzione convessa di $p(\hat{x} \mid x)$ per $p(x)$ fisso:

$$
I_{q_\alpha}(X; \hat{X}) \le \alpha I_{q_1}(X; \hat{X}) + (1 - \alpha) I_{q_2}(X; \hat{X})
$$

Sostituendo le maggiorazioni iniziali:

$$
I_{q_\alpha}(X; \hat{X}) \le \alpha [R(D_1) + \epsilon] + (1 - \alpha) [R(D_2) + \epsilon] = \alpha R(D_1) + (1 - \alpha) R(D_2) + \epsilon
$$

Poiché $R(D_\alpha)$ è per definizione l'infimum dell'informazione mutua su tutti i canali con distorsione $\le D_\alpha$:

$$
R(D_\alpha) = R(\alpha D_1 + (1 - \alpha) D_2) \le I_{q_\alpha}(X; \hat{X}) \le \alpha R(D_1) + (1 - \alpha) R(D_2) + \epsilon
$$

Essendo la disuguaglianza valida per qualsiasi $\epsilon > 0$ arbitrariamente piccolo, passando al limite per $\epsilon \to 0$ si ottiene la disuguaglianza di convessità:

$$
R(\alpha D_1 + (1 - \alpha) D_2) \le \alpha R(D_1) + (1 - \alpha) R(D_2)
$$

### Corollari Fondamentali della Convessità

1. __Monotonia Decrescente e Pendenza Negativa__:
   Poiché consentire una distorsione maggiore allarga lo spazio di ottimizzazione, la funzione $R(D)$ è monotona non crescente. La convessità implica che la derivata prima (pendenza della curva) sia non positiva e monotona crescente verso lo zero:

$$
   s = \frac{\mathrm{d}R}{\mathrm{d}D} \le 0, \quad \frac{\mathrm{d}^2 R}{\mathrm{d}D^2} \ge 0
$$

2. __Rendimento Marginale Decrescente__:
   La spesa marginale di bit necessaria per abbattere la distorsione aumenta drasticamente al decrescere di $D$. Nelle vicinanze di $D \to 0$, la pendenza $|s| = -\frac{\mathrm{d}R}{\mathrm{d}D}$ tende a $+\infty$, riflettendo l'elevatissimo costo informativo richiesto per ricostruzioni ad alta fedeltà.

## Algoritmo di Blahut-Arimoto per il Calcolo Numerico della Funzione Rate-Distortion

Nelle applicazioni reali con alfabeti discreti o sorgenti arbitrarie, la funzione Rate-Distortion $R(D)$ non ammette quasi mai una forma analitica chiusa. L'__algoritmo di Blahut-Arimoto__ (Blahut 1972; Arimoto 1972) fornisce una procedura numerica iterativa ad alternanza di minimizzazione che converge globalmente al valore ottimo di $R(D)$.

### Riformulazione Lagrangiana

Il calcolo di $R(D)$ equivale a trovare la curva parametrizzata dal moltiplicatore di Lagrange $s \le 0$ (che rappresenta la pendenza locale della curva $R(D)$) minimizzando la funzione di costo:

$$
\min_{p(\hat{x} \mid x)} \left[ I(X; \hat{X}) - s \, \mathbb{E}[d(X, \hat{X})] \right]
$$

Si consideri la densità marginale sull'alfabeto di ricostruzione indotta dal canale:

$$
q(\hat{x}) = \sum_{x} p(x) p(\hat{x} \mid x)
$$

L'informazione mutua può essere espressa come:

$$
I(X; \hat{X}) = \sum_{x} \sum_{\hat{x}} p(x) p(\hat{x} \mid x) \ln \frac{p(\hat{x} \mid x)}{q(\hat{x})}
$$

Considerando $q(\hat{x})$ come una distribuzione ausiliaria libera, il problema si riformula come una doppia minimizzazione su due insiemi di distribuzioni:

$$
J(p(\hat{x} \mid x), q(\hat{x})) = \sum_{x} \sum_{\hat{x}} p(x) p(\hat{x} \mid x) \ln \frac{p(\hat{x} \mid x)}{q(\hat{x})} - s \sum_{x} \sum_{\hat{x}} p(x) p(\hat{x} \mid x) d(x, \hat{x})
$$

### Le Due Fasi dell'Alternating Minimization

Fissato il parametro di pendenza $s < 0$, l'algoritmo alterna ricorsivamente l'aggiornamento della distribuzione condizionata e della marginale:

1. __Passo 1: Ottimizzazione del Canale Condizionato $p(\hat{x} \mid x)$__:
   Tenendo fissa la distribuzione $q(\hat{x})$, la minimizzazione rispetto a $p(\hat{x} \mid x)$ sotto il vincolo $\sum_{\hat{x}} p(\hat{x} \mid x) = 1$ per ogni $x$ conduce alla soluzione in forma di Gibbs (distribuzione esponenziale di Boltzmann):

$$
   p^{(k+1)}(\hat{x} \mid x) = \frac{q^{(k)}(\hat{x}) e^{s \, d(x, \hat{x})}}{\sum_{\hat{x}'} q^{(k)}(\hat{x}') e^{s \, d(x, \hat{x}')}}
$$

2. __Passo 2: Aggiornamento della Marginale di Ricostruzione $q(\hat{x})$__:
   Tenendo fisso il nuovo canale condizionato $p^{(k+1)}(\hat{x} \mid x)$, la minimizzazione rispetto a $q(\hat{x})$ è soddisfatta esattamente ponendo $q(\hat{x})$ pari alla reale marginale indotta:

$$
   q^{(k+1)}(\hat{x}) = \sum_{x} p(x) p^{(k+1)}(\hat{x} \mid x)
$$

### Convergenza e Calcolo della Curva

Poiché il funzionale $J(p, q)$ è convesso rispetto a ciascun argomento ed è limitato inferiormente, la discesa coordinata alternata garantisce la convergenza monotona al minimo globale.

A convergenza dell'algoritmo per un dato parametro $s$, si valutano direttamente la distorsione media risultante $D(s)$ e il corrispondente rate $R(s)$:

$$
D(s) = \sum_{x} \sum_{\hat{x}} p(x) p^*(\hat{x} \mid x) d(x, \hat{x})
$$

$$
R(s) = \sum_{x} \sum_{\hat{x}} p(x) p^*(\hat{x} \mid x) \log_2 \frac{p^*(\hat{x} \mid x)}{q^*(\hat{x})}
$$

Facendo variare il parametro $s \in (-\infty, 0]$, la coppia $(D(s), R(s))$ traccia con precisione arbitraria l'intera frontiera ottima $R(D)$ della sorgente.

## Dimostrazione dell'Ottimalità dei Codici di Golomb per Distribuzioni Geometriche

La codifica di Golomb (1966; Gallager & Van Voorhis 1975) costituisce una famiglia universale di codici prefissi a lunghezza variabile progettata specificamente per sorgenti discrete supportate sull'alfabeto infinito numerabile dei numeri interi non negativi $\mathbb{N}_0 = \{0, 1, 2, \dots\}$, la cui distribuzione di probabilità decade esponenzialmente secondo una legge geometrica.

### Modello di Sorgente Geometrica

Si consideri una variabile aleatoria discreta $X \in \{0, 1, 2, \dots\}$ avente funzione di massa di probabilità (PMF) geometrica unificata di parametro $\theta \in (0, 1)$:

$$
p(x) = (1 - \theta) \theta^x, \quad x = 0, 1, 2, \dots
$$

Tale distribuzione modella tipicamente le lunghezze delle sequenze di zeri (run-length) tra due eventi rari successivi, i coefficienti quantizzati di trasformate spettrali (DCT, Wavelet) e gli errori di predizione nei codificatori lossless audio e video (FLAC, JPEG-LS, H.264).

### Decomposizione Euclidea e Struttura del Codice di Golomb

Fissato un intero positivo $M \ge 1$ (parametro di Golomb), qualsiasi numero intero $x \ge 0$ ammette un'unica scomposizione euclidea con quoziente $q$ e resto $r$:

$$
x = q M + r
$$

dove:

$$
q = \left\lfloor \frac{x}{M} \right\rfloor \in \{0, 1, 2, \dots\}, \quad r = x \bmod M \in \{0, 1, \dots, M-1\}
$$

La probabilità congiunta del quoziente e del resto si fattorizza nel modo seguente:

$$
p(x) = p(q M + r) = (1 - \theta) \theta^{q M + r} = (\theta^M)^q \cdot (1 - \theta) \theta^r
$$

Calcoliamo le distribuzioni marginali di $q$ ed $r$:
1. La probabilità marginale del quoziente $q$ è:

$$
   p_Q(q) = \sum_{r=0}^{M-1} p(q M + r) = (1 - \theta) \theta^{q M} \sum_{r=0}^{M-1} \theta^r = (1 - \theta) \theta^{q M} \frac{1 - \theta^M}{1 - \theta} = (1 - \theta^M) (\theta^M)^q
$$

   Il quoziente $q$ segue esattamente una distribuzione geometrica di parametro $\theta^M$.

2. La probabilità condizionata del resto $r$ dato il quoziente $q$ vale:

$$
   p_{R \mid Q}(r \mid q) = \frac{p(q M + r)}{p_Q(q)} = \frac{(1 - \theta) \theta^{q M + r}}{(1 - \theta^M) \theta^{q M}} = \frac{1 - \theta}{1 - \theta^M} \theta^r
$$

   Tale distribuzione è completamente indipendente dal valore del quoziente $q$.

Ne consegue che $Q$ ed $R$ sono variabili aleatorie mutuamente indipendenti. L'albero di codifica di Huffman per la variabile $X$ si scompone nel prodotto cartesiano di due alberi indipendenti:
- un albero per il quoziente $q$;
- un albero per il resto $r$.

### Teorema di Gallager-Van Voorhis sulla Scelta Ottima di $M$

Robert Gallager e David Van Voorhis (1975) hanno dimostrato che il codice di Huffman ottimo su un alfabeto infinito per la distribuzione geometrica $p(x) = (1-\theta)\theta^x$ coincide con il codice di Golomb se e solo se il parametro $M$ è scelto come l'unico intero che soddisfa la disequazione:

$$
\theta^M + \theta^{M+1} \le 1 < \theta^M + \theta^{M-1}
$$

la cui soluzione in forma chiusa è data dall'arrotondamento:

$$
M = \left\lceil -\frac{\log_2(1 + \theta)}{\log_2 \theta} \right\rceil \approx \left\lceil -\frac{1}{\log_2 \theta} \right\rceil
$$

Sotto tale condizione:
1. __Codifica del Quoziente $q$__:
   Poiché $\theta^M \approx \frac{1}{2}$, la distribuzione del quoziente è approssimativamente diadica $p_Q(q) \approx 2^{-(q+1)}$. Il codice di Huffman ottimo per una distribuzione geometrica con probabilità di successo $1/2$ è il __codice unario__:

$$
   C_{\text{unario}}(q) = \underbrace{11\dots1}_{q \text{ volte}} 0
$$

   avente lunghezza $l_Q(q) = q + 1$ bit.

2. __Codifica del Resto $r$__:
   Il resto assume $M$ valori possibili con probabilità debolmente decrescenti. La codifica ottima è un codice prefisso a troncamento binario (Truncated Binary Code):
   - Se $M = 2^k$ è una potenza di due (famiglia dei __codici di Rice__), il resto è rappresentato direttamente dalla sua espressione binaria naturale a $k = \log_2 M$ bit.
   - Se $M$ non è una potenza di due, siano $k = \lfloor \log_2 M \rfloor$ e $u = 2^{k+1} - M$. I primi $u$ valori di resto ($0 \le r < u$) sono codificati con $k$ bit, mentre i rimanenti $M - u$ valori ($u \le r < M$) sono codificati con $k+1$ bit aggiungendo l'offset $u$.

La lunghezza media attesa del codice risultante soddisfa:

$$
H(X) \le L_{\text{Golomb}} < H(X) + 1
$$

coincidendo esattamente con il limite di Shannon per l'alfabeto infinito.

## Dimostrazione del Teorema di Ziv-Lempel sull'Efficienza Asintotica di LZ78

L'algoritmo di compressione universale LZ78 (Jacob Ziv & Abraham Lempel, 1978) comprime qualsiasi sequenza stazionaria ed ergodica raggiungendo asintoticamente l'entropy rate della sorgente, senza alcuna conoscenza preliminare della funzione di massa di probabilità.

### Il Parsing Incrementale di LZ78

Sia $x^n = x_1 x_2 \dots x_n$ una stringa di lunghezza $n$ generata da un alfabeto finito $\mathcal{X}$ di cardinalità $|\mathcal{X}|$.

Il meccanismo di __parsing incrementale__ partiziona $x^n$ in $c(n)$ frasi distinte:

$$
x^n = w_1 w_2 \dots w_{c(n)}
$$

in modo tale che ogni frase $w_k$ sia la frase più corta non ancora incontrata nella sequenza passata. Ciascuna frase $w_k$ (eccetto al più l'ultima) è ottenuta concatenando una frase prefissa già censita $w_{j(k)}$ ($0 \le j(k) < k$, dove $w_0 = \epsilon$ è la stringa vuota) con un singolo carattere innovativo $a_k \in \mathcal{X}$:

$$
w_k = w_{j(k)} \cdot a_k
$$

### Lemma Combinatorio sul Limite Superiore del Numero di Frasi $c(n)$

Sia $c(n)$ il numero di frasi distinte in un parsing incrementale di una stringa di lunghezza $n$ su alfabeto $\mathcal{X}$. Vogliamo massimizzare $c(n)$ a parità di lunghezza $n$.

Il numero massimo di frasi distinte si ottiene quando la sequenza contiene tutte le stringhe corte prima di quelle lunghe:
- $|\mathcal{X}|$ frasi di lunghezza 1;
- $|\mathcal{X}|^2$ frasi di lunghezza 2;
- in generale, $|\mathcal{X}|^j$ frasi di lunghezza $j$.

Sia $k$ il massimo intero tale che la somma delle lunghezze di tutte le stringhe distinte fino a lunghezza $k$ non superi $n$:

$$
n_k = \sum_{j=1}^k j |\mathcal{X}|^j
$$

Valutiamo la sommatoria tramite la formula per serie arithmetico-geometriche:

$$
n_k = \frac{|\mathcal{X}|}{(|\mathcal{X}| - 1)^2} \left[ (k |\mathcal{X}| - k - 1)|\mathcal{X}|^k + 1 \right] = \frac{k |\mathcal{X}|^{k+1}}{|\mathcal{X}| - 1} \left( 1 - O\left(\frac{1}{k}\right) \right)
$$

Il numero totale di frasi corrispondente è:

$$
c_k = \sum_{j=1}^k |\mathcal{X}|^j = \frac{|\mathcal{X}|^{k+1} - |\mathcal{X}|}{|\mathcal{X}| - 1} \approx \frac{|\mathcal{X}|^{k+1}}{|\mathcal{X}| - 1}
$$

Confrontando $n_k$ e $c_k$:

$$
n_k \approx k \cdot c_k
$$

Prendendo il logaritmo di $c_k$:

$$
\log_{|\mathcal{X}|} c_k \approx k + 1 \implies k \approx \log_{|\mathcal{X}|} c_k
$$

da cui discende:

$$
n \approx c(n) \log_{|\mathcal{X}|} c(n)
$$

Invertendo la relazione asintotica, per qualsiasi stringa di lunghezza $n$ su alfabeto di cardinalità $|\mathcal{X}|$, il numero di frasi distinte soddisfa uniformemente il limite superiore:

$$
c(n) \le \frac{n}{(1 - \epsilon_n) \log_{|\mathcal{X}|} n}
$$

dove $\epsilon_n \to 0$ al tendere di $n \to \infty$.

### Calcolo della Lunghezza della Sequenza Codificata $l(x^n)$

Ciascuna frase $w_k$ per $k = 1, \dots, c(n)$ è identificata dalla coppia $(j(k), a_k)$, dove:
- $j(k) \in \{0, 1, \dots, k-1\}$ è il puntatore alla frase prefissa nel dizionario, rappresentabile con $\lceil \log_2 c(n) \rceil$ bit;
- $a_k \in \mathcal{X}$ è il carattere innovativo, rappresentabile con $\lceil \log_2 |\mathcal{X}| \rceil$ bit.

La lunghezza complessiva del codice binario generato da LZ78 è data da:

$$
l(x^n) = \sum_{k=1}^{c(n)} \left[ \lceil \log_2 c(n) \rceil + \lceil \log_2 |\mathcal{X}| \rceil \right] = c(n) \lceil \log_2 c(n) \rceil + c(n) \lceil \log_2 |\mathcal{X}| \rceil
$$

Sviluppando i limiti per $n$ grande:

$$
l(x^n) \le c(n) \log_2 c(n) + O(c(n))
$$

Sostituendo il limite superiore combinatorio su $c(n)$:

$$
l(x^n) \le \frac{n}{\log_{|\mathcal{X}|} n} \log_2 \left( \frac{n}{\log_{|\mathcal{X}|} n} \right) + O\left( \frac{n}{\log n} \right)
$$

Poiché $\log_2(n / \log_{|\mathcal{X}|} n) = \log_2 n - \log_2 \log_{|\mathcal{X}|} n$, e $\log_{|\mathcal{X}|} n = \frac{\log_2 n}{\log_2 |\mathcal{X}|}$:

$$
l(x^n) \le \frac{n \log_2 |\mathcal{X}|}{\log_2 n} \left( \log_2 n - \log_2 \log_{|\mathcal{X}|} n \right) = n \log_2 |\mathcal{X}| \left( 1 - \frac{\log_2 \log_{|\mathcal{X}|} n}{\log_2 n} \right)
$$

### Dimostrazione dell'Ottimalità Asintotica per Sorgenti Ergodiche

Sia $\{X_i\}_{i=-\infty}^{+\infty}$ un processo stocastico stazionario ed ergodico con tasso di entropia $H(\mathcal{X})$.

Per il Teorema di Asymptotic Equipartition Property (AEP) per processi con memoria (Shannon-McMillan-Breiman), la sequenza $X^n$ cade con probabilità tendente ad 1 all'interno dell'insieme tipico $A_\epsilon^{(n)}$, la cui densità congiunta soddisfa:

$$
p(X^n) \approx 2^{-n H(\mathcal{X})}
$$

Ziv e Lempel (1978, Teorema 2) hanno dimostrato che per qualsiasi partizione di una sequenza appartenente all'insieme tipico, la complessità di parsing combinatoria è inferiormente limitata dall'entropia empirica:

$$
\liminf_{n \to \infty} \frac{c(n) \log_2 c(n)}{n} \ge H(\mathcal{X})
$$

e simultaneamente, per la costruzione del codice LZ78, il rapporto di compressione asintotico soddisfa:

$$
\limsup_{n \to \infty} \frac{l(X^n)}{n} \le H(\mathcal{X}) \quad \text{quasi certamente (con probabilità 1)}
$$

Ne discende l'eguaglianza asintotica fondamentale:

$$
\lim_{n \to \infty} \frac{l(X^n)}{n} = H(\mathcal{X}) \quad \text{a.s.}
$$

L'algoritmo LZ78 è universale: converge al limite teorico assoluto di Shannon per qualsiasi sorgente stazionaria ed ergodica senza dover stimare preventivamente la distribuzione di probabilità né conoscere la memoria del processo.

## Teorema del Tempo di Ricorrenza di Kac e Ottimalità Asintotica di LZ77

L'algoritmo a finestra scorrevole LZ77 (Jacob Ziv & Abraham Lempel, 1977) adotta una strategia radicalmente diversa rispetto a LZ78: ricerca le occorrenze delle stringhe correnti all'interno di un buffer di memoria passato (finestra scorrevole di dimensione $W$).

La dimostrazione originaria di Ziv e Lempel garantiva l'ottimalità di LZ77 rispetto a compressori a stati finiti (Finite-State Compressors). L'ottimalità asintotica globale rispetto all'entropia di Shannon è stata dimostrata rigorosamente da Aaron Wyner, Jacob Ziv e Mark Kac tramite la teoria dei __tempi di ricorrenza__.

### Lemma di Ricorrenza di Mark Kac (1947)

Sia $\{X_i\}_{i=-\infty}^{+\infty}$ un processo stocastico stazionario ed ergodico a valori in un alfabeto discreto $\mathcal{X}$.

Sia $x_1^n = (x_1, \dots, x_n)$ un blocco prefissato di $n$ simboli avente probabilità stazionaria $p(x_1^n) > 0$. Si definisca il __tempo di prima ricorrenza__ (o tempo di ritorno) $R_n(x_1^n)$ come il numero di passi temporali necessari per osservare nuovamente lo stesso blocco $x_1^n$ procedendo all'indietro nella storia del processo:

$$
R_n(x_1^n) = \min \left\{ k \ge 1 : X_{-k+1}^{-k+n} = x_1^n \right\}
$$

Il __Lemma del Tempo di Ritorno di Kac__ stabilisce che per qualsiasi processo stazionario ed ergodico, il valore atteso condizionato del tempo di ricorrenza di una sequenza è esattamente pari al reciproco della sua probabilità:

$$
\mathbb{E}\left[ R_n(X^n) \mid X^n = x_1^n \right] = \frac{1}{p(x_1^n)}
$$

### Relazione tra Tempo di Ricorrenza ed Entropia

Prendendo il logaritmo in base 2 del tempo di ritorno ed applicando la disuguaglianza di Jensen:

$$
\mathbb{E}\left[ \log_2 R_n(X^n) \mid X^n = x_1^n \right] \le \log_2 \mathbb{E}\left[ R_n(X^n) \mid X^n = x_1^n \right] = \log_2 \frac{1}{p(x_1^n)} = -\log_2 p(x_1^n)
$$

Integrando rispetto alla distribuzione di tutte le sequenze $X^n$:

$$
\mathbb{E}\left[ \log_2 R_n(X^n) \right] \le \mathbb{E}[-\log_2 p(X^n)] = H(X^n)
$$

Dividendo per la lunghezza del blocco $n$:

$$
\frac{1}{n} \mathbb{E}\left[ \log_2 R_n(X^n) \right] \le \frac{H(X^n)}{n}
$$

Wyner e Ziv (1989) e Ornstein e Weiss (1993) hanno dimostrato il teorema di convergenza forte: per qualsiasi processo stazionario ed ergodico, la media temporale del logaritmo del tempo di ricorrenza converge quasi certamente all'entropy rate $H(\mathcal{X})$:

$$
\lim_{n \to \infty} \frac{1}{n} \log_2 R_n(X^n) = H(\mathcal{X}) \quad \text{con probabilità 1}
$$

### Connessione Fondamentale con la Dimensione della Finestra in LZ77

In LZ77, la ricerca del match più lungo avviene all'interno di una finestra di dimensione $W$.

Dal teorema di Kac discende che una sequenza tipica di lunghezza $n$ ricorre nel passato a una distanza media:

$$
R_n \approx 2^{n H(\mathcal{X})}
$$

Di conseguenza:
1. Se la dimensione della finestra di memoria soddisfa $W \ge 2^{n(H(\mathcal{X}) + \epsilon)}$, con probabilità tendente ad 1 la sequenza di lunghezza $n$ è già comparsa all'interno del buffer passato e può essere codificata mediante un puntatore.
2. Il puntatore richiede $\log_2 W \approx n(H(\mathcal{X}) + \epsilon)$ bit per specificare la posizione all'indietro nella finestra.
3. Il costo trasmissivo per singolo simbolo di sorgente vale quindi:

$$
\frac{\text{Costo del puntatore}}{n} \approx \frac{\log_2 W}{n} \approx \frac{n H(\mathcal{X})}{n} = H(\mathcal{X}) \quad \text{bit/simbolo}
$$

Le stringhe che non ricadono all'interno della finestra appartengono a code di probabilità atipiche infinitesime e, nel limite asintotico di finestra grande ($W \to \infty$), non degradano il tasso medio di compressione. La codifica a tempo di ricorrenza di LZ77 raggiunge asintoticamente l'entropy rate di Shannon.

