# C. PCA e ICA

Nei capitoli precedenti abbiamo affrontato paradigmi di apprendimento supervisionato e non supervisionato operando nello spazio nativo delle feature $\mathbb{R}^D$. Tuttavia, nell'ingegneria dei dati moderna e nei sistemi robotici avanzati, i campioni sono frequentemente descritti da vettori ad altissima dimensionalità: pensiamo a immagini sensoriali, matrici di feature estratte da reti neurali profonde o scansioni dense di sensori di bordo. In tali scenari ci scontriamo con la cosiddetta __maledizione della dimensionalità__ (_Curse of Dimensionality_): lo spazio cresce esponenzialmente rispetto al numero di variabili, rendendo i dati estremamente sparsi, amplificando il rumore e moltiplicando a dismisura il costo computazionale e il rischio di overfitting.

In questo capitolo analizziamo due metodologie cardine di __riduzione non supervisionata della dimensionalità__: la __Principal Component Analysis__ (__PCA__) e la __Independent Component Analysis__ (__ICA__). Esploriamo la PCA formulandola sia come massimizzazione variazionale della varianza proiettata sia come minimizzazione dell'errore quadratico di ricostruzione, provando analiticamente la convergenza al problema agli autovalori della matrice di covarianza empirica ed evidenziandone il legame profondo con la decomposizione a valori singolari (SVD). Affrontiamo quindi l'ICA per la risoluzione della __separazione cieca delle sorgenti__ (_Blind Source Separation_), proviamo analiticamente le tre ambiguità strutturali (permutazione, scala e rotazione gaussiana), dimostriamo la necessità della non-gaussianità statistica e ne deriviamo la stima di massima verosimiglianza mediante ascesa del gradiente.

## Riduzione della Dimensionalità Non Supervisionata

L'obiettivo fondamentale della riduzione della dimensionalità risiede nel mappare un dataset originale $\mathcal{D} = \{\mathbf{x}^{(0)}, \dots, \mathbf{x}^{(N-1)}\} \subset \mathbb{R}^D$ in una rappresentazione a dimensionalità ridotta $\mathcal{Z} = \{\mathbf{z}^{(0)}, \dots, \mathbf{z}^{(N-1)}\} \subset \mathbb{R}^K$, con $K \ll D$.

Tale operazione risponde a esigenze metodologiche e operative imprescindibili nell'ingegneria informatica:
- __Abbattimento della ridondanza informativa__: eliminare la forte correlazione o multicollinearità strutturale tra feature interdipendenti, condensando l'informazione in un numero minimo di assi sintetici;
- __Filtraggio del rumore stocastico__: scartare le direzioni di varianza trascurabile tipicamente dominate dal rumore di misura del sensore;
- __Compressione e scalabilità computazionale__: accelerare l'addestramento e l'inferenza di modelli a valle (es. classificatori o filtri di stima) riducendo le dimensioni dei tensori manipolati;
- __Visualizzazione e interpretazione dei dati__: consentire l'esplorazione geometrica diretta proiettando distribuzioni complesse su spazi bidimensionali ($K = 2$) o tridimensionali ($K = 3$).

> [!NOTE] Tassonomia Metodologica: Supervisionato vs Non Supervisionato
> A differenza di metodologie supervisionate come la Linear Discriminant Analysis (LDA), che sfrutta le etichette di classe per massimizzare la separabilità dei target, PCA e ICA operano in modo puramente non supervisionato: estraggono struttura unicamente dalla geometria e dalle proprietà statistiche intrinseche della matrice dei dati $\mathbf{X} \in \mathbb{R}^{N \times D}$.

## Principal Component Analysis (PCA)

La __Principal Component Analysis__ (PCA) identifica un sottospazio lineare a dimensionalità inferiore che preserva la massima quota possibile di informazione (varianza) dei dati originari, scartando le componenti associate a variazioni marginali o rumore.

Per cogliere l'intuizione fisica dell'algoritmo, consideriamo un dataset $\mathcal{D} = \{\mathbf{x}^{(0)}, \dots, \mathbf{x}^{(N-1)}\}$ contenente i risultati di un'indagine condotta su piloti di elicotteri radiocomandati. Ciascun campione è descritto da due feature continue ($D = 2$): l'abilità tecnica di guida ($x_1$) e il grado di divertimento percepito ($x_2$).

![[fig_14_1_direzione_massima_variazione_pca.svg|center mid]]

Intuitivamente, le due variabili presentano una marcata correlazione positiva: chi si diverte di più tende a esercitarsi con maggiore costanza e a sviluppare un'abilità superiore. Se osserviamo la distribuzione geometrica dei punti, emerge con chiarezza che la direzione di massima variabilità dei dati non corre lungo l'asse $x_1$ né lungo l'asse $x_2$, bensì lungo una retta inclinata definita dal versore $\mathbf{u}_1$. Viceversa, la direzione ortogonale $\mathbf{u}_2$ cattura una frazione minima di dispersione.

Anziché limitarci a rimuovere banalmente una delle due feature dopo aver calcolato la matrice di correlazione, la PCA combina linearmente le coordinate native, individuando un nuovo sistema di riferimento ortonormale orientato secondo gli assi di dispersione dominante.

### Pre-Elaborazione: Centratura e Standardizzazione dei Dati

Prima di applicare la procedura proiettiva, dobbiamo normalizzare le feature del dataset. Definiamo il vettore della media campionaria:

$$
\bar{\mathbf{x}} = \frac{1}{N} \sum_{i=0}^{N-1} \mathbf{x}^{(i)} \in \mathbb{R}^D
$$

Trasliamo ciascun campione sottraendo la media:

$$
\mathbf{x}^{(i)} \leftarrow \mathbf{x}^{(i)} - \bar{\mathbf{x}}
$$

La centratura garantisce che la media campionaria nello spazio trasformato sia rigorosamente nulla: $\sum_{i=0}^{N-1} \mathbf{x}^{(i)} = \mathbf{0}$. Se le feature presentano scale o unità di misura eterogenee (es. metri, secondi, gradi Kelvin), dividiamo ciascuna feature anche per la propria deviazione standard empirica $s_j$:

$$
x_j^{(i)} \leftarrow \frac{x_j^{(i)} - \bar{x}_j}{s_j}, \qquad s_j = \sqrt{\frac{1}{N} \sum_{i=0}^{N-1} (x_j^{(i)} - \bar{x}_j)^2}
$$

> [!WARNING] Regola Operativa di Pre-Elaborazione
> La standardizzazione impedisce che le feature espresse con unità di misura numericamente più elevate dominino artificiosamente la varianza globale a discapito di variabili informative a scala ridotta.

### Massimizzazione della Varianza Proiettata

Assumendo dati centrati con media nulla, consideriamo la proiezione ortogonale di ciascun vettore $\mathbf{x}^{(i)}$ lungo un versore unidirezionale $\mathbf{u} \in \mathbb{R}^D$ avente norma euclidea unitaria:

$$
\|\mathbf{u}\|_2^2 = \mathbf{u}^T \mathbf{u} = 1
$$

![[fig_14_2_proiezione_campione_direzione_variazione.svg|center mid]]

La coordinata scalare della proiezione del generico campione $\mathbf{x}^{(i)}$ lungo il versore $\mathbf{u}$ coincide con il prodotto scalare:

$$
z^{(i)} = (\mathbf{x}^{(i)})^T \mathbf{u} = \mathbf{u}^T \mathbf{x}^{(i)} \in \mathbb{R}
$$

Poiché il dataset è centrato all'origine, la media delle coordinate scalari proiettate si annulla identicamente:

$$
\bar{z} = \frac{1}{N} \sum_{i=0}^{N-1} z^{(i)} = \frac{1}{N} \sum_{i=0}^{N-1} (\mathbf{x}^{(i)})^T \mathbf{u} = \left( \frac{1}{N} \sum_{i=0}^{N-1} \mathbf{x}^{(i)} \right)^T \mathbf{u} = \mathbf{0}^T \mathbf{u} = 0
$$

Calcoliamo la varianza campionaria delle proiezioni scalari lungo $\mathbf{u}$:

$$
\mathrm{Var}(z) = \frac{1}{N} \sum_{i=0}^{N-1} (z^{(i)} - \bar{z})^2 = \frac{1}{N} \sum_{i=0}^{N-1} \left( (\mathbf{x}^{(i)})^T \mathbf{u} \right)^2
$$

Riformuliamo il quadrato dello scalare sfruttando la simmetria del prodotto scalare:

$$
((\mathbf{x}^{(i)})^T \mathbf{u})^2 = (\mathbf{u}^T \mathbf{x}^{(i)}) ((\mathbf{x}^{(i)})^T \mathbf{u}) = \mathbf{u}^T \left( \mathbf{x}^{(i)} (\mathbf{x}^{(i)})^T \right) \mathbf{u}
$$

Sostituendo all'interno della sommatoria e portando i versori $\mathbf{u}$ all'esterno dei termini dipendenti dall'indice $i$:

$$
\mathrm{Var}(z) = \mathbf{u}^T \left( \frac{1}{N} \sum_{i=0}^{N-1} \mathbf{x}^{(i)} (\mathbf{x}^{(i)})^T \right) \mathbf{u}
$$

Riconosciamo tra parentesi tonde la __matrice di covarianza empirica__ $\boldsymbol{\Sigma} \in \mathbb{R}^{D \times D}$ dei campioni:

$$
\boldsymbol{\Sigma} \triangleq \frac{1}{N} \sum_{i=0}^{N-1} \mathbf{x}^{(i)} (\mathbf{x}^{(i)})^T = \frac{1}{N} \mathbf{X}^T \mathbf{X}
$$

La varianza proiettata assume pertanto la forma quadratica compatta:

$$
\mathrm{Var}(z) = \mathbf{u}^T \boldsymbol{\Sigma} \mathbf{u}
$$

Il problema di massimizzazione della varianza si configura come un'ottimizzazione vincolata quadratica:

$$
\max_{\mathbf{u}} \mathbf{u}^T \boldsymbol{\Sigma} \mathbf{u} \qquad \text{sotto il vincolo} \qquad \mathbf{u}^T \mathbf{u} = 1
$$

### Risoluzione Analitica tramite Moltiplicatori di Lagrange

Per risolvere il problema applichiamo il metodo dei moltiplicatori di Lagrange. Costruiamo la funzione Lagrangiana scalare associata al vincolo di uguaglianza:

$$
\mathcal{L}(\mathbf{u}, \lambda) = \mathbf{u}^T \boldsymbol{\Sigma} \mathbf{u} - \lambda (\mathbf{u}^T \mathbf{u} - 1)
$$

Deriviamo la Lagrangiana rispetto al vettore $\mathbf{u}$:

$$
\nabla_{\mathbf{u}} \mathcal{L}(\mathbf{u}, \lambda) = 2 \boldsymbol{\Sigma} \mathbf{u} - 2 \lambda \mathbf{u}
$$

Imponiamo la condizione di stazionarietà annullando il gradiente:

$$
2 \boldsymbol{\Sigma} \mathbf{u} - 2 \lambda \mathbf{u} = \mathbf{0} \implies \boldsymbol{\Sigma} \mathbf{u} = \lambda \mathbf{u}
$$

L'annullamento del gradiente conduce all'equazione secolare agli autovalori. Sostituendo la relazione $\boldsymbol{\Sigma} \mathbf{u} = \lambda \mathbf{u}$ nell'espressione della varianza massimizzata:

$$
\mathrm{Var}(z) = \mathbf{u}^T \boldsymbol{\Sigma} \mathbf{u} = \mathbf{u}^T (\lambda \mathbf{u}) = \lambda \mathbf{u}^T \mathbf{u} = \lambda
$$

La varianza dei campioni proiettati lungo il versore $\mathbf{u}$ coincide esattamente con l'autovalore $\lambda$. Ne consegue che, per ottenere la __massima varianza possibile__, dobbiamo selezionare l'autovettore associato al __massimo autovalore__ della matrice di covarianza:

$$
\lambda_1 = \max_{j} \lambda_j \implies \mathbf{u}_1 = \mathbf{v}_1
$$

Il vettore $\mathbf{u}_1$ prende il nome di __prima componente principale__ (_First Principal Component_).

Deriviamo ora la seconda componente principale $\mathbf{u}_2$. Dobbiamo massimizzare la varianza residua imponendo sia la norma unitaria sia l'ortogonalità rispetto a $\mathbf{u}_1$:

$$
\max_{\mathbf{u}_2} \mathbf{u}_2^T \boldsymbol{\Sigma} \mathbf{u}_2 \qquad \text{s.t.} \qquad \mathbf{u}_2^T \mathbf{u}_2 = 1, \quad \mathbf{u}_2^T \mathbf{u}_1 = 0
$$

Impostiamo la Lagrangiana con due moltiplicatori scalari $\lambda$ e $\phi$:

$$
\mathcal{L}(\mathbf{u}_2, \lambda, \phi) = \mathbf{u}_2^T \boldsymbol{\Sigma} \mathbf{u}_2 - \lambda (\mathbf{u}_2^T \mathbf{u}_2 - 1) - 2 \phi (\mathbf{u}_2^T \mathbf{u}_1)
$$

Annulliamo il gradiente rispetto a $\mathbf{u}_2$:

$$
\nabla_{\mathbf{u}_2} \mathcal{L} = 2 \boldsymbol{\Sigma} \mathbf{u}_2 - 2 \lambda \mathbf{u}_2 - 2 \phi \mathbf{u}_1 = \mathbf{0}
$$

Moltiplichiamo a sinistra l'equazione per $\mathbf{u}_1^T$:

$$
2 \mathbf{u}_1^T \boldsymbol{\Sigma} \mathbf{u}_2 - 2 \lambda \mathbf{u}_1^T \mathbf{u}_2 - 2 \phi \mathbf{u}_1^T \mathbf{u}_1 = 0
$$

Sfruttando la simmetria di $\boldsymbol{\Sigma}$ e il fatto che $\boldsymbol{\Sigma} \mathbf{u}_1 = \lambda_1 \mathbf{u}_1$:

$$
\mathbf{u}_1^T \boldsymbol{\Sigma} \mathbf{u}_2 = (\boldsymbol{\Sigma} \mathbf{u}_1)^T \mathbf{u}_2 = (\lambda_1 \mathbf{u}_1)^T \mathbf{u}_2 = \lambda_1 (\mathbf{u}_1^T \mathbf{u}_2) = 0
$$

Poiché $\mathbf{u}_1^T \mathbf{u}_2 = 0$ per vincolo e $\mathbf{u}_1^T \mathbf{u}_1 = 1$, l'equazione scalare collassa a:

$$
- 2 \phi = 0 \implies \phi = 0
$$

Il vincolo di ortogonalità non aggiunge forze spettrali esterne: la condizione di stazionarietà ritorna a essere $\boldsymbol{\Sigma} \mathbf{u}_2 = \lambda \mathbf{u}_2$. Per massimizzare la varianza residua selezioniamo l'autovettore associato al secondo autovalore in ordine decrescente $\lambda_2$. Per induzione, le $K$ componenti principali corrispondono ai $K$ autovettori associati ai $K$ massimi autovalori ordinati $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_K$.

> [!IMPORTANT] Teorema Spettrale e Componenti Principali
> Le componenti principali della PCA coincidono con gli autovettori ortonormali della matrice di covarianza $\boldsymbol{\Sigma}$. Ciascun autovalore $\lambda_j$ quantifica esattamente la quota di varianza catturata dalla rispettiva componente $\mathbf{u}_j$.

### Formulazione Duale: Minimizzazione dell'Errore di Ricostruzione

La PCA ammette un'interpretazione duale perfettamente equivalente: anziché massimizzare la dispersione dei dati proiettati, possiamo formulare l'algoritmo cercando il sottospazio lineare che minimizza la somma degli errori quadratici commessi ricostruendo il dato originario $\mathbf{x}^{(i)}$ a partire dalla sua proiezione ortogonale $\hat{\mathbf{x}}^{(i)}$.

![[fig_ex_C_pca_proiezione_ricostruzione_scree_plot.png|center big]]

Definendo la proiezione unidimensionale $\hat{\mathbf{x}}^{(i)} = z^{(i)} \mathbf{u}_1 = (\mathbf{u}_1^T \mathbf{x}^{(i)}) \mathbf{u}_1$, l'errore di ricostruzione euclideo si esprime come:

$$
J_{\text{ric}}(\mathbf{u}_1) = \frac{1}{N} \sum_{i=0}^{N-1} \|\mathbf{x}^{(i)} - \hat{\mathbf{x}}^{(i)}\|_2^2 = \frac{1}{N} \sum_{i=0}^{N-1} \|\mathbf{x}^{(i)} - (\mathbf{u}_1^T \mathbf{x}^{(i)}) \mathbf{u}_1\|_2^2
$$

Verifichiamo analiticamente l'ortogonalità tra la proiezione $\hat{\mathbf{x}}^{(i)}$ e il vettore errore $(\mathbf{x}^{(i)} - \hat{\mathbf{x}}^{(i)})$:

$$
(\hat{\mathbf{x}}^{(i)})^T (\mathbf{x}^{(i)} - \hat{\mathbf{x}}^{(i)}) = (\mathbf{u}_1^T \mathbf{x}^{(i)}) \mathbf{u}_1^T (\mathbf{x}^{(i)} - (\mathbf{u}_1^T \mathbf{x}^{(i)}) \mathbf{u}_1) = (\mathbf{u}_1^T \mathbf{x}^{(i)}) [ \mathbf{u}_1^T \mathbf{x}^{(i)} - (\mathbf{u}_1^T \mathbf{x}^{(i)})(\mathbf{u}_1^T \mathbf{u}_1) ] = 0
$$

Grazie all'ortogonalità, applichiamo il Teorema di Pitagora al triangolo rettangolo formato dal dato originario, dalla sua proiezione e dall'errore:

$$
\|\mathbf{x}^{(i)}\|_2^2 = \|\hat{\mathbf{x}}^{(i)}\|_2^2 + \|\mathbf{x}^{(i)} - \hat{\mathbf{x}}^{(i)}\|_2^2 = (\mathbf{u}_1^T \mathbf{x}^{(i)})^2 + \|\mathbf{x}^{(i)} - \hat{\mathbf{x}}^{(i)}\|_2^2
$$

Mediando su tutto il dataset composto dagli $N$ campioni:

$$
\frac{1}{N} \sum_{i=0}^{N-1} \|\mathbf{x}^{(i)}\|_2^2 = \mathbf{u}_1^T \boldsymbol{\Sigma} \mathbf{u}_1 + J_{\text{ric}}(\mathbf{u}_1)
$$

Poiché la quantità a primo membro rappresenta la varianza totale dei dati originari (pari alla traccia della matrice di covarianza $\mathrm{Tr}(\boldsymbol{\Sigma}) = \sum_{j=1}^D \lambda_j$, costante fissata a priori dal dataset):

$$
\min_{\mathbf{u}_1} J_{\text{ric}}(\mathbf{u}_1) \iff \max_{\mathbf{u}_1} \mathbf{u}_1^T \boldsymbol{\Sigma} \mathbf{u}_1
$$

Minimizzare l'errore quadratico di ricostruzione equivale tassativamente a massimizzare la varianza proiettata. Estendendo la proiezione a un sottospazio di dimensione $K$ tramite la matrice ortonormale $\mathbf{V}_K = [\mathbf{v}_1, \dots, \mathbf{v}_K]$, la ricostruzione ottimale è $\hat{\mathbf{x}}^{(i)} = \mathbf{V}_K \mathbf{V}_K^T \mathbf{x}^{(i)}$, e l'errore minimo di ricostruzione coincide con la somma degli autovalori scartati:

$$
J_{\text{ric}}(\mathbf{V}_K) = \sum_{j=K+1}^D \lambda_j
$$

> [!TIP] Intuizione Geometrica d'Esame: Pitagora e Dualità
> Massimizzare la varianza catturata e minimizzare l'errore di compressione sono due facce della stessa medaglia: l'energia totale del segnale si scompone ortogonalmente tra lo spazio proiettato e il residuo. L'errore residuo corrisponde esattamente alla varianza associata alle dimensioni scartate.

### Calcolo Numerico tramite Singular Value Decomposition (SVD)

Nel calcolo numerico reale, la determinazione esplicita della matrice di covarianza $\boldsymbol{\Sigma} = \frac{1}{N}\mathbf{X}^T\mathbf{X}$ raddoppia il numero di condizionamento: $\kappa(\mathbf{X}^T \mathbf{X}) = (\kappa(\mathbf{X}))^2$. Questo raddoppio può causare gravi perdite di precisione per cancellazione numerica.

Per preservare la stabilità dell'algoritmo, applichiamo la __Singular Value Decomposition__ (SVD) direttamente sulla matrice dei dati centrati $\mathbf{X} \in \mathbb{R}^{N \times D}$:

$$
\mathbf{X} = \mathbf{U} \mathbf{D} \mathbf{V}^T
$$

dove:
- $\mathbf{U} \in \mathbb{R}^{N \times N}$ è una matrice ortogonale ($\mathbf{U}^T \mathbf{U} = \mathbf{I}_N$) i cui vettori colonna rappresentano gli autovettori di $\mathbf{X}\mathbf{X}^T$;
- $\mathbf{D} \in \mathbb{R}^{N \times D}$ è una matrice diagonale rettangolare contenente i valori singolari non negativi ordinati: $d_1 \ge d_2 \ge \dots \ge d_{\min(N, D)} \ge 0$;
- $\mathbf{V} \in \mathbb{R}^{D \times D}$ è una matrice ortogonale ($\mathbf{V}^T \mathbf{V} = \mathbf{I}_D$) le cui colonne $\mathbf{v}_j$ costituiscono la base ortonormale degli autovettori di $\mathbf{X}^T\mathbf{X}$.

Esplicitiamo la covarianza inserendo la scomposizione SVD:

$$
\boldsymbol{\Sigma} = \frac{1}{N} \mathbf{X}^T \mathbf{X} = \frac{1}{N} (\mathbf{V} \mathbf{D}^T \mathbf{U}^T)(\mathbf{U} \mathbf{D} \mathbf{V}^T) = \frac{1}{N} \mathbf{V} \mathbf{D}^T \mathbf{D} \mathbf{V}^T = \mathbf{V} \left( \frac{1}{N} \mathbf{D}^2 \right) \mathbf{V}^T
$$

Gli autovalori della matrice di covarianza discendono direttamente dai valori singolari $d_j$:

$$
\lambda_j = \frac{d_j^2}{N}
$$

Le componenti principali ricercate coincidono con le colonne della matrice $\mathbf{V} = [\mathbf{v}_1, \dots, \mathbf{v}_D]$. Inoltre, le coordinate proiettate $\mathbf{Z} \in \mathbb{R}^{N \times K}$ si ricavano direttamente senza dover moltiplicare per $\mathbf{V}_K$:

$$
\mathbf{Z} = \mathbf{X} \mathbf{V}_K = (\mathbf{U} \mathbf{D} \mathbf{V}^T) \mathbf{V}_K = \mathbf{U}_K \mathbf{D}_K
$$

### Estensione a K Componenti Principali e Proiezione Matriciale

Quando desideriamo estrarre $K$ direzioni di massima variazione ($K < D$), selezioniamo i primi $K$ autovettori corrispondenti ai $K$ autovalori dominanti $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_K$.

Costruiamo la matrice di proiezione rettangolare:

$$
\mathbf{V}_K = [\mathbf{v}_1, \mathbf{v}_2, \dots, \mathbf{v}_K] \in \mathbb{R}^{D \times K}
$$

La proiezione dell'intero dataset $\mathbf{X} \in \mathbb{R}^{N \times D}$ nel nuovo spazio ridotto $\mathbf{Z} \in \mathbb{R}^{N \times K}$ si calcola con un unico prodotto matriciale:

$$
\mathbf{Z} = \mathbf{X} \mathbf{V}_K
$$

Esplicitando la struttura a blocchi di matrici e vettori riga:

$$
\begin{bmatrix}
z_1^{(0)} & z_2^{(0)} & \dots & z_K^{(0)} \\
z_1^{(1)} & z_2^{(1)} & \dots & z_K^{(1)} \\
\vdots & \vdots & \ddots & \vdots \\
z_1^{(N-1)} & z_2^{(N-1)} & \dots & z_K^{(N-1)}
\end{bmatrix}
=
\begin{bmatrix}
(\mathbf{x}^{(0)})^T \\
(\mathbf{x}^{(1)})^T \\
\vdots \\
(\mathbf{x}^{(N-1)})^T
\end{bmatrix}
\begin{bmatrix}
\mathbf{v}_1 & \mathbf{v}_2 & \dots & \mathbf{v}_K
\end{bmatrix}
$$

Le colonne di $\mathbf{Z}$ godono di una proprietà algebrica fondamentale: la loro covarianza incrociata è rigorosamente nulla. Calcoliamo la matrice di covarianza empirica nello spazio trasformato:

$$
\boldsymbol{\Sigma}_Z = \frac{1}{N} \mathbf{Z}^T \mathbf{Z} = \frac{1}{N} \mathbf{V}_K^T \mathbf{X}^T \mathbf{X} \mathbf{V}_K = \mathbf{V}_K^T \boldsymbol{\Sigma} \mathbf{V}_K = \mathrm{diag}(\lambda_1, \lambda_2, \dots, \lambda_K)
$$

Le componenti trasformate risultano pertanto mutuamente incorrelate: $\mathrm{Cov}(z_j, z_l) = 0$ per ogni coppia di indici $j \neq l$.

### Algoritmo Procedurale della PCA

Sintetizziamo la sequenza analitica dei passi operativi dell'algoritmo PCA:

```pseudo
\begin{algorithm}
\caption{Principal Component Analysis (PCA)}
\begin{algorithmic}
\REQUIRE Matrice dei dati osservati $\mathbf{X} \in \mathbb{R}^{N \times D}$, dimensione ridotta desiderata $K \le D$
\ENSURE Matrice dei campioni proiettati $\mathbf{Z} \in \mathbb{R}^{N \times K}$, matrice degli autovettori $\mathbf{V}_K \in \mathbb{R}^{D \times K}$
\STATE Calcolo del vettore medio campionario: $\bar{\mathbf{x}} \leftarrow \frac{1}{N} \sum_{i=0}^{N-1} \mathbf{x}^{(i)}$
\STATE Centratura della matrice dei dati: $\mathbf{X} \leftarrow \mathbf{X} - \mathbf{1}_N \bar{\mathbf{x}}^T$
\STATE Decomposizione a valori singolari (SVD): $\mathbf{X} = \mathbf{U} \mathbf{D} \mathbf{V}^T$
\STATE Estrazione dei primi $K$ vettori colonna: $\mathbf{V}_K \leftarrow [\mathbf{v}_1, \dots, \mathbf{v}_K] \in \mathbb{R}^{D \times K}$
\STATE Calcolo delle coordinate proiettate: $\mathbf{Z} \leftarrow \mathbf{X} \mathbf{V}_K = \mathbf{U}_K \mathbf{D}_K$
\RETURN $\mathbf{Z}, \mathbf{V}_K$
\end{algorithmic}
\end{algorithm}
```

### Selezione del Numero di Componenti e Limiti della PCA

Per selezionare il numero ottimale di componenti $K$ da trattenere senza disperdere informazione rilevante, valutiamo la __frazione di varianza spiegata cumulata__:

$$
\eta(K) = \frac{\sum_{j=1}^K \lambda_j}{\sum_{i=1}^D \lambda_i} = \frac{\sum_{j=1}^K d_j^2}{\sum_{i=1}^D d_i^2} \in [0, 1]
$$

Si fissa comunemente una soglia conservativa (es. $\eta \ge 0.90$ o $0.95$, trattenendo il 90-95% dell'energia informativa originaria) oppure si individua il flesso (_elbow point_) nello __Scree Plot__, scartando gli autovalori oltre il plateau di rendimento marginale.

Sebbene la PCA sia rapida, esatta e risolvibile in forma chiusa, presenta quattro limiti concettuali stringenti:
- __Perdita di interpretabilità delle feature__: ciascuna componente $z_k$ è una combinazione lineare densa di tutte le $D$ variabili originarie, rendendo complessa l'identificazione del significato fisico del singolo predittore;
- __Sensibilità al rumore ad alta varianza__: la PCA assume che l'informazione risieda esclusivamente nell'ampiezza della varianza. Se un sensore introduce rumore stocastico a forte ampiezza, l'algoritmo allocherà una componente principale sul rumore, trascurando segnali utili a bassa ampiezza;
- __Linearità del sottospazio proiettivo__: la PCA opera esclusivamente proiezioni lineari piatte. Se la varietà dei dati possiede topologia curvilinea (es. eliche o Swiss Roll), la proiezione lineare collassa regioni distanti distruggendo la struttura geometrica originaria;
- __Natura puramente non supervisionata__: massimizzare la varianza globale non implica massimizzare la separabilità tra categorie: due classi con medie distinte ma allineate ortogonalmente rispetto alla direzione di massima dispersione globale vengono proiettate sovrapponendosi completamente.

> [!WARNING] Limiti Strutturali della PCA nell'Ingegneria dei Dati
> Nelle applicazioni di classificazione o riconoscimento pattern, una compressione PCA aggressiva può degradare le prestazioni se la direzione discriminante non coincide con la direzione di massima varianza. In tali contesti si prediligono tecniche supervisionate (es. LDA) o non lineari (es. Autoencoder, t-SNE, UMAP).

## Independent Component Analysis (ICA)

Così come la PCA, la __Independent Component Analysis__ (ICA) persegue la scoperta di una nuova rappresentazione dello spazio dei dati. Tuttavia, la finalità teorica è radicalmente diversa: anziché cercare coordinate ortogonali incorrelate che massimizzino la varianza, l'ICA mira a individuare le __sorgenti fisiche indipendenti__ che hanno generato le osservazioni e a disaccoppiarle.

### Il Problema del Cocktail Party e Modello Generativo

Per inquadrare il problema, consideriamo la celebre metafora acustica del __Cocktail Party Problem__: in una stanza sono presenti $D$ persone che parlano contemporaneamente ($D$ sorgenti acustiche indipendenti) e nell'ambiente sono disposti $D$ microfoni in posizioni geometriche differenti.

Ciascun microfono registra una combinazione lineare istantanea delle onde sonore emesse da tutti gli interlocutori, ponderata dalle rispettive distanze e attenuazioni acustiche. L'obiettivo consiste nel separare le singole voci originali operando esclusivamente sui tracciati audio registrati dai microfoni, senza alcuna conoscenza a priori né delle posizioni fisiche né della dinamica temporale dei singoli parlanti. Tale classe di problemi è formalizzata sotto il nome di __Separazione Cieca delle Sorgenti__ (_Blind Source Separation_, BSS).

Formalizziamo il processo definendo i vettori di segnale:
- Indichiamo con $s_j^{(i)} \in \mathbb{R}$ il segnale acustico generato dal $j$-esimo oratore all'istante temporale $i \in \{0, \dots, N-1\}$;
- Organizziamo i segnali delle sorgenti nell'istante $i$ nel vettore colonna $\mathbf{s}^{(i)} = [s_0^{(i)}, \dots, s_{D-1}^{(i)}]^T \in \mathbb{R}^D$;
- Indichiamo con $x_j^{(i)} \in \mathbb{R}$ il segnale campionato dal $j$-esimo microfono all'istante $i$;
- Organizziamo le registrazioni nell'istante $i$ nel vettore colonna $\mathbf{x}^{(i)} = [x_0^{(i)}, \dots, x_{D-1}^{(i)}]^T \in \mathbb{R}^D$.

![[fig_ex_C_ica_cocktail_party_non_gaussianity.png|center big]]

A ogni istante di campionamento, il vettore delle osservazioni $\mathbf{x}^{(i)}$ risulta dalla combinazione lineare istantanea delle sorgenti:

$$
\mathbf{x}^{(i)} = \mathbf{A} \mathbf{s}^{(i)}
$$

dove $\mathbf{A} \in \mathbb{R}^{D \times D}$ è una matrice quadrata invertibile denominata __Mixing Matrix__ (matrice di miscelazione).

Raccogliendo gli $N$ campioni temporali nelle rispettive matrici di dati:

$$
\mathbf{X} = [\mathbf{x}^{(0)}, \dots, \mathbf{x}^{(N-1)}] \in \mathbb{R}^{D \times N}, \qquad \mathbf{S} = [\mathbf{s}^{(0)}, \dots, \mathbf{s}^{(N-1)}] \in \mathbb{R}^{D \times N}
$$

il modello generativo globale si esprime in forma compatta:

$$
\mathbf{X} = \mathbf{A} \mathbf{S}
$$

L'obiettivo dell'ICA consiste nello stimare una matrice $\mathbf{W} \in \mathbb{R}^{D \times D}$, denominata __Unmixing Matrix__ (matrice di demiscelazione), tale da invertire l'effetto della matrice $\mathbf{A}$:

$$
\mathbf{W} \approx \mathbf{A}^{-1}
$$

Determinato $\mathbf{W}$, ricostruiamo le sorgenti originali a partire dalle sole misurazioni microfoniche:

$$
\hat{\mathbf{s}}^{(i)} = \mathbf{W} \mathbf{x}^{(i)} = \mathbf{W} \mathbf{A} \mathbf{s}^{(i)} \approx \mathbf{s}^{(i)}
$$

Esplicitando le righe della matrice di demiscelazione $\mathbf{W} = [\mathbf{w}_0, \mathbf{w}_1, \dots, \mathbf{w}_{D-1}]^T$, ciascun vettore riga $\mathbf{w}_j^T \in \mathbb{R}^{1 \times D}$ isola la singola sorgente $j$-esima:

$$
\hat{s}_j^{(i)} = \mathbf{w}_j^T \mathbf{x}^{(i)}
$$

### Ambiguità Strutturali della Demiscelazione

La matrice $\mathbf{W} = \mathbf{A}^{-1}$ è univocamente determinabile? In assenza di informazioni esterne sulla fisica del mezzo o sulla natura dei segnali, emergono tre ambiguità strutturali ineliminabili.

#### Ambiguità di Permutazione

Consideriamo una matrice di permutazione quadrata $\mathbf{P} \in \{0, 1\}^{D \times D}$, avente un solo elemento unitario per ciascuna riga e colonna e zeri altrove. Moltiplicare una matrice a sinistra per $\mathbf{P}$ equivale a scambiarne l'ordine delle righe.

Se stimiamo una matrice $\mathbf{W}' = \mathbf{P} \mathbf{W}$, i segnali ricostruiti diventano:

$$
\hat{\mathbf{s}}' = \mathbf{W}' \mathbf{x} = \mathbf{P} \mathbf{W} \mathbf{A} \mathbf{s} = \mathbf{P} \mathbf{s}
$$

Le sorgenti estratte coincidono con quelle originali, ma risultano disposte in un ordine differente. Disponendo unicamente dei segnali aggregati $\mathbf{x}$, non esiste alcun criterio matematico per associare l'etichetta "oratore 1" piuttosto che "oratore 2". Nel problema del Cocktail Party tale indeterminazione è del tutto irrilevante: l'obiettivo è isolare ciascuna voce su una traccia audio pulita, indipendentemente dalla traccia su cui essa viene allocata.

#### Ambiguità di Scala e di Segno

Supponiamo di moltiplicare la $j$-esima colonna della matrice di miscelazione $\mathbf{A}$ per uno scalare non nullo $\alpha \in \mathbb{R} \setminus \{0\}$, e contemporaneamente di riscalare la sorgente $s_j$ per il fattore reciproco $\frac{1}{\alpha}$:

$$
\mathbf{x}^{(i)} = (\alpha \mathbf{a}_j) \left( \frac{1}{\alpha} s_j^{(i)} \right) = \mathbf{a}_j s_j^{(i)}
$$

Il segnale rilevato dai microfoni rimane identico. Non possiamo determinare l'ampiezza assoluta delle sorgenti (il loro volume originale) né la polarità della forma d'onda (se $\alpha = -1$). Anche questa limitazione non preclude l'efficacia pratica: in acustica o elaborazione dei segnali, riscalare una sorgente equivale ad applicare un guadagno di amplificazione o invertire la fase di $180^\circ$, preservando integre l'informazione semantica e la fedeltà del messaggio.

#### Ambiguità Rotazionale delle Sorgenti Gaussiane e Obbligo di Non-Gaussianità

La terza ambiguità introduce un limite teorico fondamentale che vincola il dominio di applicabilità dell'ICA.

Ipotizziamo che le $D$ sorgenti originali siano generate da distribuzioni Gaussiane standard indipendenti e identicamente distribuite a media nulla e varianza unitaria:

$$
\mathbf{s}^{(i)} \sim \mathcal{N}(\mathbf{0}, \mathbf{I}_D)
$$

Calcoliamo il valore atteso e la matrice di covarianza dei segnali osservati $\mathbf{x}^{(i)} = \mathbf{A} \mathbf{s}^{(i)}$:

$$
\mathbb{E}[\mathbf{x}^{(i)}] = \mathbb{E}[\mathbf{A} \mathbf{s}^{(i)}] = \mathbf{A} \mathbb{E}[\mathbf{s}^{(i)}] = \mathbf{0}
$$

$$
\mathrm{Cov}[\mathbf{x}^{(i)}] = \mathbb{E}[\mathbf{x}^{(i)} (\mathbf{x}^{(i)})^T] = \mathbb{E}[(\mathbf{A} \mathbf{s}^{(i)}) (\mathbf{A} \mathbf{s}^{(i)})^T] = \mathbf{A} \mathbb{E}[\mathbf{s}^{(i)} (\mathbf{s}^{(i)})^T] \mathbf{A}^T = \mathbf{A} \mathbf{I}_D \mathbf{A}^T = \mathbf{A} \mathbf{A}^T
$$

Essendo una combinazione lineare di variabili congiuntamente normali, la distribuzione delle osservazioni è una Gaussiana multivariata:

$$
\mathbf{x}^{(i)} \sim \mathcal{N}(\mathbf{0}, \mathbf{A} \mathbf{A}^T)
$$

La cui densità di probabilità congiunta è data da:

$$
p_X(\mathbf{x}) = \frac{1}{(2\pi)^{D/2} |\det \mathbf{A}|} \exp\left( -\frac{1}{2} \mathbf{x}^T (\mathbf{A} \mathbf{A}^T)^{-1} \mathbf{x} \right)
$$

Consideriamo ora una generica matrice di rotazione ortogonale $\mathbf{R} \in \mathbb{R}^{D \times D}$, tale che $\mathbf{R} \mathbf{R}^T = \mathbf{I}_D$. Definiamo una matrice di miscelazione ruotata $\mathbf{A}' = \mathbf{A} \mathbf{R}$. Se i dati fossero stati generati con $\mathbf{A}'$, la covarianza dei segnali osservati sarebbe:

$$
\mathrm{Cov}[(\mathbf{x}^{(i)})'] = \mathbf{A}' (\mathbf{A}')^T = (\mathbf{A} \mathbf{R}) (\mathbf{A} \mathbf{R})^T = \mathbf{A} (\mathbf{R} \mathbf{R}^T) \mathbf{A}^T = \mathbf{A} \mathbf{I}_D \mathbf{A}^T = \mathbf{A} \mathbf{A}^T
$$

Inoltre, $|\det \mathbf{A}'| = |\det (\mathbf{A} \mathbf{R})| = |\det \mathbf{A}| \cdot |\det \mathbf{R}| = |\det \mathbf{A}| \cdot 1 = |\det \mathbf{A}|$. La densità di probabilità risultante $(\mathbf{x}^{(i)})' \sim \mathcal{N}(\mathbf{0}, \mathbf{A} \mathbf{A}^T)$ è identica a quella generata da $\mathbf{A}$.

> [!WARNING] Limite Fondamentale di Identificabilità dell'ICA
> Le distribuzioni Gaussiane multivariate con componenti indipendenti sono a simmetria sferica (isotrope): qualsiasi rotazione $\mathbf{R}$ preserva la forma circolare degli isocontorni di probabilità. Di conseguenza, nel caso di sorgenti Gaussiane, risulta impossibile discriminare $\mathbf{A}$ da $\mathbf{A}\mathbf{R}$.
> 
> __Assunzione Tassativa di ICA__: affinché le sorgenti siano identificabili, le componenti indipendenti devono essere rigorosamente __NON GAUSSIANE__ (al più una singola componente può essere Gaussiana).

Il Teorema del Limite Centrale fornisce la giustificazione probabilistica duale: la combinazione lineare di variabili casuali indipendenti produce una distribuzione che tende a essere "più gaussiana" di ciascuna delle componenti singole. Dunque, per demiscelare i segnali dobbiamo percorrere la strada opposta: __cercare la matrice $\mathbf{W}$ che massimizza la non-gaussianità dei segnali estratti__.

### Derivazione Analitica di ICA via Maximum Likelihood Estimation (MLE)

Per determinare i parametri della matrice di demiscelazione $\mathbf{W}$, applichiamo la stima di massima verosimiglianza sfruttando la formula del cambio di variabile per vettori casuali continui.

Consideriamo la trasformazione biunivoca invertibile $\mathbf{x} = \mathbf{A} \mathbf{s}$, da cui $\mathbf{s} = \mathbf{A}^{-1} \mathbf{x} = \mathbf{W} \mathbf{x}$. La densità di probabilità congiunta delle osservazioni si ottiene riscalando la densità delle sorgenti per il modulo del determinante dello Jacobiano della trasformazione inversa $\mathbf{J} = \frac{\partial \mathbf{s}}{\partial \mathbf{x}} = \mathbf{W}$:

$$
p_X(\mathbf{x}) = p_S(\mathbf{W} \mathbf{x}) |\det \mathbf{W}|
$$

In virtù dell'ipotesi di mutua indipendenza statistica tra le $D$ sorgenti generatrici, la densità congiunta $p_S(\mathbf{s})$ fattorizza esattamente nel prodotto delle densità marginali univariate:

$$
p_S(\mathbf{s}) = \prod_{j=0}^{D-1} p_S(s_j)
$$

Sostituendo l'espressione di ciascuna coordinata estratta $s_j = \mathbf{w}_j^T \mathbf{x}$:

$$
p_X(\mathbf{x}) = \left( \prod_{j=0}^{D-1} p_S(\mathbf{w}_j^T \mathbf{x}) \right) |\det \mathbf{W}|
$$

Per modellare la distribuzione non gaussiana delle sorgenti scegliamo come funzione di ripartizione cumulativa (CDF) la funzione sigmoide standard, che cresce monotonicamente da 0 a 1:

$$
F(s) = \sigma(s) = \frac{1}{1 + e^{-s}}
$$

La densità di probabilità (PDF) corrisponde alla derivata prima della CDF:

$$
p_S(s) = F'(s) = \sigma'(s) = \sigma(s)(1 - \sigma(s))
$$

Considerando un dataset di $N$ istanti temporali indipendenti $\mathbf{X} = \{\mathbf{x}^{(0)}, \dots, \mathbf{x}^{(N-1)}\}$, la log-verosimiglianza rispetto alla matrice $\mathbf{W}$ assume l'espressione:

$$
\ell(\mathbf{W}) = \ln \prod_{i=0}^{N-1} p_X(\mathbf{x}^{(i)}) = \sum_{i=0}^{N-1} \left( \sum_{j=0}^{D-1} \ln \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)}) + \ln |\det \mathbf{W}| \right)
$$

### Calcolo Analitico del Gradiente Matriciale

Per massimizzare $\ell(\mathbf{W})$ calcoliamo il gradiente rispetto al vettore $\mathbf{w}_j$ (che definisce la $j$-esima riga trasposta $\mathbf{w}_j^T$ di $\mathbf{W}$). Consideriamo il primo termine della sommatoria interna applicando la regola della catena:

$$
\nabla_{\mathbf{w}_j} \ln \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)}) = \frac{1}{\sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)})} \nabla_{\mathbf{w}_j} \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)})
$$

Calcoliamo la derivata seconda della sigmoide $\sigma''(s)$:

$$
\sigma''(s) = \frac{\mathrm{d}}{\mathrm{d}s} [\sigma(s)(1 - \sigma(s))] = \sigma'(s)(1 - \sigma(s)) - \sigma(s)\sigma'(s) = \sigma'(s)(1 - 2\sigma(s))
$$

Applicando la regola della catena per il gradiente rispetto al vettore $\mathbf{w}_j$:

$$
\nabla_{\mathbf{w}_j} \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)}) = \sigma''(\mathbf{w}_j^T \mathbf{x}^{(i)}) \mathbf{x}^{(i)} = \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)})(1 - 2\sigma(\mathbf{w}_j^T \mathbf{x}^{(i)})) \mathbf{x}^{(i)}
$$

Sostituendo nell'espressione del gradiente, il fattore $\sigma'$ a numeratore e denominatore si elide in modo esatto:

$$
\nabla_{\mathbf{w}_j} \ln \sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)}) = \frac{\sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)})(1 - 2\sigma(\mathbf{w}_j^T \mathbf{x}^{(i)}))}{\sigma'(\mathbf{w}_j^T \mathbf{x}^{(i)})} \mathbf{x}^{(i)} = (1 - 2\sigma(\mathbf{w}_j^T \mathbf{x}^{(i)})) \mathbf{x}^{(i)}
$$

Consideriamo ora la derivata del termine di log-determinante rispetto all'intera matrice $\mathbf{W}$. Sfruttando la proprietà differenziale del determinante mediante la formula di Jacobi $\mathrm{d} \ln \det \mathbf{W} = \mathrm{Tr}(\mathbf{W}^{-1} \mathrm{d}\mathbf{W})$:

$$
\nabla_{\mathbf{W}} \ln |\det \mathbf{W}| = (\mathbf{W}^{-1})^T
$$

Riassemblando i due contributi e sommando su tutti gli $N$ campioni temporali e sulle $D$ righe, otteniamo il gradiente matriciale completo:

$$
\nabla_{\mathbf{W}} \ell(\mathbf{W}) = \sum_{i=0}^{N-1} \begin{bmatrix}
(1 - 2\sigma(\mathbf{w}_0^T \mathbf{x}^{(i)})) \\
(1 - 2\sigma(\mathbf{w}_1^T \mathbf{x}^{(i)})) \\
\vdots \\
(1 - 2\sigma(\mathbf{w}_{D-1}^T \mathbf{x}^{(i)}))
\end{bmatrix} (\mathbf{x}^{(i)})^T + N (\mathbf{W}^{-1})^T
$$

Scriviamo l'equazione in forma vettorizzata definendo $\mathbf{y}^{(i)} = \sigma(\mathbf{W} \mathbf{x}^{(i)}) \in \mathbb{R}^D$:

$$
\nabla_{\mathbf{W}} \ell(\mathbf{W}) = \sum_{i=0}^{N-1} (\mathbf{1}_D - 2\mathbf{y}^{(i)}) (\mathbf{x}^{(i)})^T + N (\mathbf{W}^{-1})^T
$$

Raccogliendo l'intero batch dei dati nella matrice $\mathbf{X} \in \mathbb{R}^{D \times N}$ e definendo la matrice delle attivazioni sigmoidee $\mathbf{Y} = \sigma(\mathbf{W} \mathbf{X}) \in \mathbb{R}^{D \times N}$, il gradiente globale assume la forma compatta:

$$
\nabla_{\mathbf{W}} \ell(\mathbf{W}) = (\mathbf{1}_{D \times N} - 2\mathbf{Y}) \mathbf{X}^T + N (\mathbf{W}^{-1})^T
$$

La matrice ottima di demiscelazione $\mathbf{W}$ si stima iterativamente applicando l'algoritmo di ascesa del gradiente (_Gradient Ascent_):

$$
\mathbf{W} \leftarrow \mathbf{W} + \alpha \nabla_{\mathbf{W}} \ell(\mathbf{W})
$$

dove $\alpha > 0$ rappresenta il learning rate.

```pseudo
\begin{algorithm}
\caption{Independent Component Analysis (ICA via Maximum Likelihood)}
\begin{algorithmic}
\REQUIRE Matrice delle osservazioni $\mathbf{X} \in \mathbb{R}^{D \times N}$, tasso di apprendimento $\alpha > 0$, tolleranza di convergenza $\epsilon$
\ENSURE Matrice di demiscelazione $\mathbf{W} \in \mathbb{R}^{D \times D}$, sorgenti ricostruite $\hat{\mathbf{S}} \in \mathbb{R}^{D \times N}$
\STATE Inizializzazione della matrice di demiscelazione $\mathbf{W} \leftarrow \mathbf{I}_D$
\REPEAT
    \STATE Calcolo delle attivazioni sigmoidee: $\mathbf{Y} \leftarrow \sigma(\mathbf{W} \mathbf{X})$
    \STATE Calcolo del gradiente matriciale: $\nabla_{\mathbf{W}} \ell(\mathbf{W}) \leftarrow (\mathbf{1}_{D \times N} - 2\mathbf{Y}) \mathbf{X}^T + N (\mathbf{W}^{-1})^T$
    \STATE Aggiornamento dei pesi: $\mathbf{W}^{\text{nuovo}} \leftarrow \mathbf{W} + \alpha \nabla_{\mathbf{W}} \ell(\mathbf{W})$
    \STATE Calcolo della variazione di Frobenius: $\Delta \leftarrow \|\mathbf{W}^{\text{nuovo}} - \mathbf{W}\|_F$
    \STATE Aggiornamento matrice corrente: $\mathbf{W} \leftarrow \mathbf{W}^{\text{nuovo}}$
\UNTIL{$\Delta < \epsilon$}
\STATE Ricostruzione delle sorgenti stimate: $\hat{\mathbf{S}} \leftarrow \mathbf{W} \mathbf{X}$
\RETURN $\mathbf{W}, \hat{\mathbf{S}}$
\end{algorithmic}
\end{algorithm}
```

## Quadro Sinottico Comparativo: PCA vs ICA

Sintetizziamo le differenze concettuali, algebriche e statistiche che distinguono la Principal Component Analysis dalla Independent Component Analysis attraverso 10 criteri metodologici:

| Criterio Metodologico | Principal Component Analysis (PCA) | Independent Component Analysis (ICA) |
| :--- | :--- | :--- |
| __Obiettivo Primario__ | Massimizzare la varianza proiettata e comprimere le feature | Separare e isolare le sorgenti fisiche indipendenti (BSS) |
| __Modello Generativo__ | Proiezione lineare ortogonale diretta: $\mathbf{z} = \mathbf{V}_K^T \mathbf{x}$ | Modello causale lineare inverso: $\mathbf{x} = \mathbf{A}\mathbf{s} \implies \mathbf{s} = \mathbf{W}\mathbf{x}$ |
| __Relazione Statistica__ | Componenti debolmente __incorrelate__ ($\mathrm{Cov}(z_i, z_j) = 0$) | Componenti strettamente __indipendenti__ ($p(\mathbf{s}) = \prod p(s_j)$) |
| __Momenti Statistici Sfruttati__ | Momenti del secondo ordine (matrice di covarianza $\boldsymbol{\Sigma}$) | Momenti di ordine superiore al secondo (curtosi, informazione mutua) |
| __Geometria delle Basi__ | Assi rigorosamente __ortogonali__ ($\mathbf{u}_i^T \mathbf{u}_j = 0$ per $i \neq j$) | Assi arbitrari __non necessariamente ortogonali__ (direzioni libere) |
| __Ruolo della Gaussianità__ | Ottimale e perfetta per dati congiuntamente gaussiani | __Fallisce totalmente__ su dati gaussiani (richiede non-gaussianità) |
| __Ambiguità della Soluzione__ | Solo segno del versore ($\pm \mathbf{u}$) e spazi degeneri per autovalori uguali | Ambiguità di permutazione delle sorgenti e ambiguità di scala/segno |
| __Metodo di Risoluzione__ | Forma chiusa esatta: autovalori di $\mathbf{X}^T\mathbf{X}$ o SVD di $\mathbf{X}$ | Procedura numerica iterativa (ascesa del gradiente di verosimiglianza) |
| __Dimensionalità Risultante__ | Tipicamente ridotta ($K \ll D$) per compressione | Tipicamente conservata ($D$ sorgenti per $D$ sensori) per separazione |
| __Campi Applicativi Tipici__ | Riduzione rumore, visualizzazione 2D/3D, pre-elaborazione | Separazione audio (Cocktail Party), elaborazione segnali EEG/fMRI |

La sinergia tra PCA e ICA rappresenta un pilastro dell'elaborazione avanzata dei dati: la PCA condensa l'energia informativa eliminando le correlazioni lineari del secondo ordine, mentre l'ICA sfrutta la ricchezza statistica dei momenti superiori per svelare i processi generativi latenti che governano il fenomeno fisico osservato.
