# Indice

- [[#0. Immagini, Filtri E Gradienti|0. Immagini, Filtri E Gradienti]]
	- [[#0. Immagini, Filtri E Gradienti#Operatori Di Punto E Operatori Locali|Operatori Di Punto E Operatori Locali]]
	- [[#0. Immagini, Filtri E Gradienti#Cross-correlation E Convoluzione|Cross-correlation E Convoluzione]]
	- [[#0. Immagini, Filtri E Gradienti#Filtri Lineari|Filtri Lineari]]
	- [[#0. Immagini, Filtri E Gradienti#Filtri Non Lineari|Filtri Non Lineari]]
	- [[#0. Immagini, Filtri E Gradienti#Edge Detection|Edge Detection]]
	- [[#0. Immagini, Filtri E Gradienti#Canny Edges|Canny Edges]]
	- [[#0. Immagini, Filtri E Gradienti#Dai Filtri Alle Convolutional Neural Network|Dai Filtri Alle Convolutional Neural Network]]
- [[#1. Local Features E Harris Corner Detector|1. Local Features E Harris Corner Detector]]
	- [[#1. Local Features E Harris Corner Detector#Perché Le Local Features?|Perché Le Local Features?]]
	- [[#1. Local Features E Harris Corner Detector#Detector Vs Descriptor|Detector Vs Descriptor]]
	- [[#1. Local Features E Harris Corner Detector#Criterio Locale: Flat, Edge E Corner|Criterio Locale: Flat, Edge E Corner]]
	- [[#1. Local Features E Harris Corner Detector#Derivazione Matematica dell'Harris Detector|Derivazione Matematica dell'Harris Detector]]
	- [[#1. Local Features E Harris Corner Detector#La Pipeline Di Harris Nella Pratica|La Pipeline Di Harris Nella Pratica]]
	- [[#1. Local Features E Harris Corner Detector#Invarianze E Limiti Di Harris|Invarianze E Limiti Di Harris]]
- [[#2. Scale-Space, Descrittori SIFT E Feature Matching|2. Scale-Space, Descrittori SIFT E Feature Matching]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Dal Punto Di Interesse Al Feature Matching|Dal Punto Di Interesse Al Feature Matching]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Il Problema Della Scala E Della Rotazione|Il Problema Della Scala E Della Rotazione]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Selezione Di Scala E Scale-Space (LoG E DoG)|Selezione Di Scala E Scale-Space (LoG E DoG)]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Invarianza Alla Rotazione: Orientamento Canonico|Invarianza Alla Rotazione: Orientamento Canonico]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Descrittore SIFT: Architettura A 128 Dimensioni|Descrittore SIFT: Architettura A 128 Dimensioni]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Feature Matching E Lowe's Ratio Test|Feature Matching E Lowe's Ratio Test]]
	- [[#2. Scale-Space, Descrittori SIFT E Feature Matching#Approfondimento: Harris-Laplace|Approfondimento: Harris-Laplace]]
- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini|3. Trasformazioni Geometriche E Allineamento Di Immagini]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Differenza Tra Filtering E Warping|Differenza Tra Filtering E Warping]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Trasformazioni Lineari Nel Piano 2D|Trasformazioni Lineari Nel Piano 2D]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Coordinate Omogenee E Trasformazioni Affini|Coordinate Omogenee E Trasformazioni Affini]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Omografie E Spazio Proiettivo|Omografie E Spazio Proiettivo]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Stima Dei Parametri Dalle Corrispondenze|Stima Dei Parametri Dalle Corrispondenze]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Stima Dell'Omografia: Metodo DLT (Direct Linear Transform)|Stima Dell'Omografia: Metodo DLT (Direct Linear Transform)]]
	- [[#3. Trasformazioni Geometriche E Allineamento Di Immagini#Pipeline Completa Di Allineamento E Composizione|Pipeline Completa Di Allineamento E Composizione]]

# 0. Immagini, Filtri E Gradienti

Da un punto di vista matematico un'immagine _in bianco e nero_ è una mappa tra un dominio 2D ad un dominio scalare (intensità della luce), è quindi una __funzione__:

$$f: R^2\to \mathrm R$$

![[2.5_immagine_funzione.png]]

L'unica differenza tra un'immagine in bianco e nero e una _a colori_ (RGB) è che ho 3 matrici, si tratta quindi di un __tensore__ di profondità 3, dove ogni canale è un'immagine che rappresenta il livello di intensità dei canali Rosso, Verde e Blu.

>[!NOTE]
>In PyTorch le immagini vengono salvate nella configurazione:
>
>$$C \times H\times W $$
>
>Il primo indice sarà quindi il canale, poi l'altezza e infine la larghezza

## Operatori Di Punto E Operatori Locali

Un operatore è una funzione che riceve in input una o più immagini producendo un'altra immagine di output.

![[2.7_operatori.png]]

### Operatori Di Punto

Un operatore di punto trasforma un singolo pixel basandosi __solo sul valore di quel pixel__:

$$g(i, j) = h(f(i,j))$$

Vengono utilizzati per gestire il contrasto, la luminosità e tutte le operazioni che consistono nel manipolare la luminosità di ogni singolo pixel indipendentemente.

Nel deep learning si possono utilizzare anche per Thresholding, histogram equalization, input normalization.

#### Gain (Contrasto) E Bias (Luminosità)

L'aumento del contrasto si ottiene moltiplicando la funzione dell'immagine, è quindi un operatore di punto perché ogni pixel viene moltiplicato per uno scalare.
La stessa cosa vale per la luminosità, che si ottiene sommando lo stesso valore ad ogni pixel.

![[2.9_gain_bias.png]]

#### Histogram Equalization

Se prendiamo un'immagine e analizziamo la distribuzione dei valori possiamo costruire un istogramma che rappresenti la p.d.f. dell'immagine:
![[2.10_istogramma.png]]

Da questo istogramma possiamo ricavare alcuni dati statistici neccessari per analizzare l'immagine, come valore minimo, massimo, media e mediana.

Una volta ottenuto l'istogramma e visualizzata la sua c.d.f. (cumulative distribution function), possiamo schiarire alcuni dei pixel più scuri e scurire alcuni dei pixel più chiari, così da poter utilizzare l'intera gamma dinamica dell'immagine.

Per farlo si crea una funzione $T$ monotona che abbia come p.d.f. uniforme $p_s(s)=1$, questa funzione mappa i pixel nell'intervallo $[r, r+\mathrm dr]$ in $[s, s+\mathrm ds]$ :

$$p_s(s)\mathrm ds = p_r(r)\mathrm dr$$

dato che abbiamo $p_s(s) = 1$, possiamo trovare:

$$\frac {\mathrm ds}{\mathrm dr} = p_r(r) \to s = T(r) = \int_0^rp_r(u)\mathrm du = P_r(r)$$

Ovvero la c.d.f dell'immmagine.

![[2.12_hist_equal.png]]

>[!NOTE]
>Questa funzione è valida solo nel dominio analogico, in ambiente digitale il risultato non è perfettamente piatto.
>
> #### Versione discreta
> ![[2.13_equal_discre.png]]
> ![[2.13_risultato.png]]
> Nella versione discreta si avranno pixel con lo stesso valore iniziale, questi avranno sempre lo stesso valore in uscita dalla trasformazione.
> Inoltre il valore minimo non sarà 0, ma sarà la versione normalizzata del valore minimo rappresentato nell'immagine: $c(I_{min}) = h(I_{min}) / N$

#### Utilizzo Nel Deep Learning

![[2.14_usi.png]]

### Operatori Locali (Neighborhood)

Negli operatori locali la trasfomazione di un singolo pixel dipende anche dal __valore__ di un certo numero di __pixel vicini__:

$$g(i,j) = h(f(k,l), \quad(k,l) \in N(i,j))$$

Dove $N(i,j)$ indica i pixel vicini al pixel che stiamo trasformando.
La dimensione del vicinato dipende da quanto vogliamo far influenzare il pixel dai suoi vicini.

Questi operatori vengono utilizzati principalmente per filtri come il Gaussian Blur, Mean Filter, Sobel.

Nel deep learning li utilizzeremo inoltre come Median filter; convolutional layers nelle CNN.

#### Riduzione Del Rumore

![[2.15_noise.png]]

Aumentando il numero di immagini scattate diminuisce il rumore, ma spesso abbiamo una sola immagine.
Per risolvere questo problema si applicano dei filtri per ridurre il rumore bianco associato all'immagine.

Possiamo infatti modellare l'immagine come un segnale con aggiunta una componente di rumore bianco gaussiano avente come media $\mu =0$ e varianza $\sigma^2$:

$$f(i,j) = s(i,j) + n(i,j)$$

Per rimuovere il rumore bianco si può fare una media pesata tra il pixel e i suoi vicini, i pesi $h(u,v)$ vengono disposti su una griglia intorno al pixel di dimensione $k\times k$, ed ogni peso avrà valore $h = \frac 1{k^2}$:

$$g(i,j) = \sum_{u,v}f(i+u,j+v)h(u,v)$$

Possiamo poi quindi scomporre l'immagine nelle componenti di segnale e rumore:

$$g(i,j) = \sum_{u,v}{s(i+u,j+v)h(u,v)} + \sum_{u,v}{n(i+u,j+v)h(u,v)}$$

Il nostro obiettivo è quello di ridurre la componente di rumore il più possibile, e infatti se andiamo ad analizzare il funzionamento della griglia avremo:

$$Var\left [\sum_{u,v}n(i+u,j+v)h(u,v) \right ] = \sigma^2\sum_{u,v}h(u,v)^2 = \frac{\sigma^2}{k^2}$$

La varianza si divide per $k^2$, quindi la deviazione standard $\sigma$ si riduce di un fattore __$k$__.

>[!IMPORTANT]
>Anche nella parte di segnale avvengono dei cambiamenti, infatti se all'interno della griglia filtro il segnale non è tutto uguale (sono quindi presenti dei __bordi__ o dei dettagli), questi andranno a finire nella media pesata, generando un __blur__.
>
>![[2.17_blur.png]]
>
>Aumentando la dimensione della finestra diminuisce ulteriormente il rumore, ma aumenta il blur.

#### Filtri Lineari

Un filtro lineare sostituisce ogni pixel con una combinazione lineare dei suoi vicini.

![[2.18_linear.png]]

In questo esempio abbiamo definito noi i pesi, ma nelle CNN questi vengono __individuati con l'addestramento__.

## Cross-correlation E Convoluzione

La cross-correlation e la convoluzione sono due operazioni molto simili, la differenza principale è che il kernel usato in una è capovolto sia orizzontalmente che verticalmente rispetto all'altra.

![[2.19_cross_corr_conv.png]]

Spesso abbiamo dei kernel simmetrici (es: Gaussian o box), in questo caso sono identici, ma in alcuni casi non lo sono e bisogna flippare la matrice.

A livello matematico si preferisce la __convoluzione__, perché rispetta numerose proprietà matematiche che la cross-correlation non ha:

![[2.21_proprieta_conv.png]]

>[!NOTE]
>Nel deep learning non andiamo a fare distinzioni tra convoluzione e cross-correlation, perché come detto prima i kernel vengono trovati tramite addestramento e avremo quindi la disposizione corretta degli elementi.

### Sistema Lineare Shift-invariante

Un sistema lineare invariante allo shift può essere descritto come la convoluzione di un input con la risposta impulsiva del sistema, possiede inoltre le seguenti proprietà:

$$g = f *h$$

![[2.20_lsi.png]]

Queste proprietà ci torneranno molto utili per risparmiare calcoli complessi in seguito.

### Convoluzione Ai Bordi

Se provo a eseguire la convoluzione su un pixel lungo il bordo di un'immagine avrò come problema che la matrice del kernel andrà fuori dai limiti dell'immagine:

![[kernel_out_of_bounds.svg]]
Inoltre più grande sarà il kernel, più presente sarà questo problema (es: con un kernel 3x3 perdiamo 1px di bordo, con 5x5 2px e così via).

Come risultato avrò che la convoluzione sarà possibile solo lontano dai bordi, generando una matrice di dimensione inferiore rispetto a quella originale:

![[matrice_piccola.svg]]

### Metodi per Calcolare la Convoluzione Ai Bordi

Per raggirare il problema e riuscire a svolgere la convoluzione sui bordi è sufficiente aggiungere una quantità di bordo extra tanti quanti sono i pixel che andrebbero persi.

Ci sono però diverse scelte che si possono fare quando si aggiungono nuovi bordi:

![[2.22_bordi.png]]

- __Zero padding__: il più usato, aggiunge semplicemente un bordo nero
- __Replicate__: ripete lo stesso valore presente sul bordo
- __Reflect__: specchia i valori
- __Wrap__: ripete i valori nello stesso verso

### Stride

Lo stride indica ogni quanti pixel effettuare la convoluzione:

![[stride.svg]]

Con uno stride maggiore di 1 abbiamo un effetto di downsampling.

>[!EXAMPLE] Calcolare la dimensione della matrice di uscita
>
>$$N_{out} = \left \lfloor \frac {N_{in} + 2p - k}s \right \rfloor + 1$$
>
>Dove $N$ indica una delle due dimensioni della matrice ($H , W$), $p$ indica la larghezza del padding, $k$ la dimensione del kernel e $s$ lo stride.

## Filtri Lineari

Non tutti i kernel servono a sfocare l'immagine, alcuni effettuano altri tipi di trasformazioni.

![[2.26_filtri_lineari.png]]

### Moving Average (o Mean Filter, O Box blur)

Il pixel in output è la media dei pixel vicini:

$$g(i,j) = \frac 1{k^2} \sum_{u,v}f(i + u, j+v)$$

![[2.24_moving_average.png]]

è utile per rimuovere il rumore, ma sfoca tutta l'immagine.

### Filtro Gaussiano

Il filtro gaussiano effettua anch'esso una sfocatura, ma è preferito rispetto al box perché Gauss ha una risposta in frequenza più liscia, il box filter potrebbe inserire degli artefatti nell'immagine rendendola meno pulita.
![[2.27_gauss_vs_box.png]]

>[!NOTE]
> La risposta in frequenza del box è un sinc, l'attenuazione tende quindi ad oscillare portando alla cancellazione di alcune frequenze e all'esaltazione di altre a causa dei sidelobes (nell'immagine ad un certo punto le bande vengono sfocate, per poi ricomparire con colori invertiti).

![[2.28_gauss.png]]

Nel filtro gaussiano, la deviazione standard $\sigma$ indica quanto lontano arriva l'influenza di un pixel.

Con una gaussiana a una dimensione il kernel viene tagliato dopo $\pm 3\sigma$ (o quanto è grande il kernel).

Si campiona poi ad ogni passo e si normalizza la funzione facendo la somma di tutti i valori campionati e dividendoli poi per quella somma, così da avere come risultato 1.

>[!NOTE]
>Nella versione a 2 dimensioni la gaussiana è separabile, posso quindi calcolare prima solo l'asse x e poi l'asse y.
>
>$$G_\sigma(x,y) = g_\sigma(x)g_\sigma(y) \implies f * G_\sigma = (f * g_\sigma(x)) * g_\sigma(y)$$
>
>Il costo computazionale diminuisce da $k^2$ MACs (Multiply and accumulate) a $2k$ MACs, è quindi estremamente vantaggioso.

Applicare la convoluzione tra 2 gaussiane equivale a generare una gaussiana con varianza la somma delle varianze delle due gaussiane.

![[2.29_gauss_sigma.png]]

### Sharpening

Se vuoi rendere l'immagine più nitida e definita puoi seguire questi passaggi:

- Blur dell'immagine
- Sottrai all'immagine originale quella sfocata
- aggiungi il risultato all'immagine originale

$$g = f + \alpha(f - f * G_\sigma)$$

![[2.31_sharpening.png]]

## Filtri Non Lineari

I filtri non lineari non vengono calcolati tramite convoluzione, ma usano formule diverse per ottenere risultati diversi.

Non essendo lineari non supportano nemmeno le proprietà della convoluzione, ma alcuni di loro possono essere shift-invarianti.

### Median Filter

Utile per eliminare gli outlier se sono presenti all'interno del vicinato.

![[2.32_median_outlier.png]]

Può aiutare ad eliminare il salt and pepper noise spesso presente nelle immagini.
A differenza del gaussian blur infatti riesce ad eliminare questo tipo di rumore mantenendo l'immagine più nitida.

![[2.33_salt_pepper.png]]

Non è però molto utile quando incontra più rumore raggruppato vicino, inoltre si perdono le linee e i dettagli sottili che possono rappresentare degli outlier nella griglia.

## Edge Detection

Il nostro obiettivo è capire cosa si nasconde dietro i numeri che rappresentano le immagini, l'elemento più semplice da estrarre è l'edge (il bordo), ovvero il confine tra 2 oggetti diversi all'interno dell'immagine.

![[2.35_edge_cause.png]]

Per calcolare i bordi possiamo utilizzare la derivata prima, dato che un bordo è un rapido cambiamento nell'immagine.

![[2.36_derivata.png]]

Trovare i bordi ci aiuta perché sono meno sensibili alle variazioni luminose, calcolando il gradiente infatti troviamo che per gain $a$ e bias $b$:

$$\nabla (a f + b) = a \nabla f$$

Perdiamo il bias, mentre il gain scala la norma del gradiente, mantenendo l'orientamento (che è quello che ci interessa).

### Step per Il Riconoscimento Dei Bordi

Non sempre i bordi sono ben definiti, per questo dobbiamo sviluppare delle pipeline con dei filtri per poterli accentuare:

1. __Filtrare l'immagine__: il calcolo del gradiente è molto sensibile al rumore, quindi dobbiamo ridurre i suoi effetti filtrando l'immagine.
2. __Miglioramento__: Calcolare i cambiamenti locali dell'intensità (la magnitudine del gradiente), così che i bordi siano più visibili.
3. __Riconoscimento__: Mantieni soltanto i punti dove il gradiente è più forte. Spesso usando un valore di soglia (Canny aggiunge la soppressione dei non massimi e l'isteresi
4. __Localizzazione__: In alcune applicazioni localizza il bordo con accuratezza sub-pixel e stima il suo orientamento.

### Calcolo Del Gradiente

Il gradiente di un'immagine contiene tutte le derivate parziali per ogni dimensione dell'immagine:

$$\nabla f = \left [ \frac {\partial f }{\partial x}, \frac {\partial f}{\partial y}\right]$$

L'intensità (magnitudine) del bordo e la direzione del gradiente sono date dalle formule:

![[2.38_angolo_magnitudine.png]]

Il gradiente è rivolto verso il punto dove avviene il cambiamento di intensità maggiore, è collegato con la direzione del bordo dato che sono perpendicolari tra loro: il bordo è una curva lungo la quale l'__intensità è costante__.

![[gradient_direction.svg]]
![[2.45_gradient_orient.png]]

#### Dominio Digitale

Per calcolare il gradiente nel dominio digitale si può utilizzare una versione discreta della __definizione di derivata__:

$$\lim_{h\to0}\frac{f(x+h) - f(x)}{h}\quad \xrightarrow[\text{pixel consecutivi}]{h=1} \quad f(x+1) - f(x)$$

Possiamo calcolare il gradiente come se fosse una convoluzione avente un kernel $1\times2$, ma dato che utilizzare un kernel di dimensione pari può causare confusione su quale pixel si sta controllando, si utillizza un kernel di dimensione $1\times 3$:

![[2.39_gradient_conv.png]]

La nuova formula utilizzata sarà quindi una media tra il pixel precedente e il pixel successivo a quello analizzato:

$$\frac{\partial f}{\partial x} \approx \frac{f(i, j+1) - f(i, j-1)}2$$

Ovviamente il gradiente va calcolato sia per l'asse x che per l'asse y.
![[2.40_gradient_result.png]]

### Filtrare Il Rumore

Come detto in precedenza, calcolare il gradiente su un'immagine affetta da rumore rischia di identificare bordi che non devono essere presenti. Usando un filtro rendiamo meno evidente il bordo, ma rimuove il rumore così da rendere il bordo più riconoscibile.

![[2.41_filter_border.png]]

Stiamo quindi cercando di calcolare una convoluzione (il filtro gaussiano) per poi calcolare una seconda convoluzione (il gradiente), questo risulta computazionalmente complesso. Esiste però un modo per risparmiare una grossa quantità di calcoli sfruttando le [[#Cross-correlation E Convoluzione|Proprietà della convoluzione]]:

$$\frac d{dx}(f*G_\sigma) = f * \frac{dG_\sigma}{dx}$$

Questa proprietà è valida perché se scriviamo la formula estesa della convoluzione troviamo che soltanto il filtro $h$ dipende da $x$, ottenendo quindi la seguente formula:

![[2.42_formula_derivata.png]]

Possiamo quindi avere lo stesso risultato effettuando una singola convoluzione della derivata del filtro gaussiano, che non dobbiamo calcolare durante l'esecuzione perché può essere fatto in anticipo.

![[2.42_deriv_gauss.png]]

Ovviamente la derivata deve essere calcolata sia sull'asse x, che sull'asse y, portando alla creazione dei seguenti kernel:

![[2.43_derivate_gauss.png]]

La formula finale della derivata sarà quindi:

![[2.43_formula_derivate.png]]

### Operatori Prewitt E Sobel

Nella pratica, al posto di calcolare un filtro gaussiano e il gradiente, per trovare i bordi sono stati progettati 2 tipi di kernel, Prewitt e Sobel, che riescono a fornire risultati migliori:

![[2.44_sobel_esempio.png]]

![[2.44_prewitt_sobel_formule.png]]

L'operatore di Sobel è un'approssimazione su piccola scala della derivata di una Gaussiana.

Ad esempio, il kernel $S_x$ è ottenuto dal prodotto esterno di due filtri 1D:

$$S_x = \begin{bmatrix} 1 \\ 2 \\ 1 \end{bmatrix} \begin{bmatrix} -1 & 0 & 1 \end{bmatrix} = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}$$

- __Deriva lungo l'asse x__: attraversa i bordi verticali calcolandone la pendenza tramite la differenza centrale $[-1, 0, 1]$.
- __Applica uno smoothing lungo l'asse y__: agisce parallelamente al bordo con il filtro binomiale $[1, 2, 1]^T$ (approssimazione di una Gaussiana) per ridurre il rumore.

Il __kernel di Prewitt__ funziona allo stesso modo, ma usa pesi uniformi $[1, 1, 1]^T$ al posto del filtro binomiale per lo smoothing.

### Derivate Seconde (Laplaciane)

![[2.46_laplaciane.png]]

Per individuare i bordi si possono utilizzare anche le derivate seconde: nel punto dove con la derivata prima troviamo il massimo locale, con la derivata seconda troviamo un cambio di segno.

Con le derivate seconde si possono ottenere risultati più puliti, ma hanno un costo computazionale maggiore.

![[2.46_laplaciano_risultato.png]]

![[2.46_laplace_matrici.png]]

In generale quindi, si cercano i bordi dove è presente una forte risposta del gradiente.

#### Laplaciano Del Gaussiano (LoG)

![[2.47_LoG.png]]

Ovviamente possiamo calcolare direttamente la formula della derivata di secondo ordine della distribuzione normale, dato che rispetta sempre la [[#Filtrare Il Rumore|Proprietà della convoluzione]] che abbiamo visto anche con la derivata prima.

## Canny Edges

L'algoritmo di Canny è il metodo classico di riferimento per l'edge detection, progettato per individuare i contorni in modo ottimale riducendo il rumore, localizzando i bordi con precisione di un singolo pixel ed evitando falsi rilevamenti.

### Step per Il Calcolo Dei Canny Edges

1. __Filtra l'immagine__ con la derivata della Gaussiana: effettua la convoluzione sia sull'asse x che y, questo ci dà sia la pulizia dell'immagine che la differenziazione.
2. __Magnitudine e orientamento__: Calcola la magnitudine del gradiente e l'orientamento dei bordi. Inserire una soglia sulla magnitudine genera bordi troppo spessi.
3. __Soppressione dei non massimi__: Mantieni solo i massimi locali lungo la direzione del gradiente, impostando i restanti a 0, questo assottiglierà i bordi a 1px.
4. __Doppia soglia e isteresi__: usa una doppia soglia per individuare e ricostruire la continuità dei bordi.

### Filtrare L'immagine

![[2.50_smooth_canny.png]]

>[!NOTE]
>Da notare che in questo esempio usa la derivata prima

>[!IMPORTANT]
> è essenziale impostare adeguatamente la deviazione standard della gaussiana, in quanto da questa dipende il livello di dettaglio dei bordi individuati:
> ![[2.59_canny_sigma.png]]
> Gli __iperparametri__ di Canny sono $\sigma, t\_high, t\_low$

### Magnitudine E Orientamento

Calcolare la magnitudine del gradiente ci aiuta a individuare dei cambiamenti nell'immagine, ma non riusciamo subito ad individuare il bordo preciso al pixel.

![[2.51_magnitude_orient_canny.png]]

### Soppressione Dei Non Massimi

Per scegliere 1 solo pixel di bordo ci basiamo sulla __direzione__ del gradiente, compariamo ogni pixel con quelli lungo la stessa direzione e scegliamo quello con la magnitudine più alta.

![[2.52_canny_max.png]]

Il modo migliore per scegliere la direzione giusta del bordo è quello di prendere la direzione e quantizzarla in 4:
![[2.53_direzione_quant.png]]

In questo modo posso controllare solo le caselle necessarie della griglia, e scegliere quella con il valore massimo:
![[2.54_canny.png]]

Come risultato avremo quindi dei bordi tutti di larghezza 1, che avranno più o meno intensità sul pixel:
![[2.55_canny.png]]

### Doppia Soglia E Isteresi

Dato che i bordi individuati hanno tutti intensità variabile, si analizzano per individuare quelli che potrebbero avere un'intensità troppo bassa, e che quindi potrebbero essere rumore.

Si adottano quindi 2 soglie:
- __t_high__: _sopra_ questa soglia tutti i punti vengono accettati automaticamente come bordi
- __t_low__: _sotto_ questa soglia tutti i punti vengono automaticamente scartati

![[5.56_double_thres.png]]

I punti che invece si trovano nella parte intermedia tra le due soglie vengono definiti __deboli__, e devono seguire il processo di isteresi.

#### Isteresi

Prendendo l'insieme dei punti deboli, se tra questi punti è presente un percorso che li collega ad un punto __forte__ allora vengono __accettati__ come bordo, altrimenti vengono scartati.
![[5.57_isteresi.png]]

Ogni pixel ha 8 vicini (i pixel intorno) incluse le diagonali, il percorso è valido in qualsiasi direzione così che possa seguire le curve del bordo.

### Usabilità E Limiti

Nonostante si tratti di una tecnologia risalente agli anni '80, i canny edges vengono attualmente utilizzati per molti scopi come ad esempio il lane detection delle strade, la scansione dei documenti o altro.

La limitazione principale risiede nel fatto che i canny rilevano soltanto dei cambi di intensità, che possono essere dati anche da cambi di texture, ombre o specularità sullo stesso oggetto. Allo stesso modo dei cambi poco intensi possono non essere rilevati correttamente.

Nel caso in cui sorgano questi problemi si dovrà ricorrere ad altri tipi di boundary detectors come HED, oppure segmentation models come Mask R-CNN o SAM, che individuano i confini degli oggetti tramite addestramento.

Imparare i Canny Edges è comunque importante in quanto anche questi altri modelli utilizzano internamente il calcolo dei gradienti orientati.

## Dai Filtri Alle Convolutional Neural Network

Un layer convoluzionale filtra l'immagine ed applica la convoluzione, con la differenza che i parametri del filtro vengono ottenuti tramite l'addestramento.

Un layer convoluzionale quindi impara ad estrarre da solo le features.
![[2.62_conv.png]]

![[63.png]]

# 1. Local Features E Harris Corner Detector

Nel deep learning lavoriamo direttamente sui dati grezzi del segnale (i pixel dell'immagine), a differenza del machine learning classico dove le features venivano estratte a mano prima dell'apprendimento.

Anche se nelle reti neurali il compito di estrarre le features viene svolto dai layer convoluzionali in modo end-to-end, capire a fondo la teoria della _feature detection_ classica è fondamentale: costituisce la base geometrica della visione artificiale, ed è essenziale per la robotica autonoma, la stima della posa, l'odometria e la ricostruzione 3D.

## Perché Le Local Features?

Quando abbiamo due o più immagini della stessa scena scattate da angolazioni diverse, nessuno ci dice a priori come le immagini siano traslate, ruotate o scalate tra loro.

Dobbiamo quindi trovare degli elementi visivi in comune (__features__) che possano essere individuati in modo indipendente e preciso in entrambe le viste. Trovando queste corrispondenze possiamo calcolare lo spostamento o la trasformazione geometrica che le lega.

![[casetta_traslata_corrispondenza.svg]]

>[!NOTE] Obiettivo Geometrico
>Riconoscere lo stesso punto fisico della scena $p_1 = (x_1, y_1)$ e $p_2 = (x_2, y_2)$ in due immagini diverse permette di stimare il vettore di spostamento $(\Delta x, \Delta y)$, la rotazione o la matrice di trasformazione tra le due viste.

### Esempio: Panorama Stitching

Nel panorama stitching scattiamo foto parzialmente sovrapposte ruotando la fotocamera:

![[slide_03_panorama_stitching.png]]

Per unire gli scatti in un'unica immagine senza discontinuità si segue una pipeline in tre stadi:
1. __Feature Extraction__: estraiamo i punti salienti in modo indipendente su ogni immagine.
2. __Feature Matching__: colleghiamo i punti corrispondenti tra le viste.
3. __Alignment & Blending__: calcoliamo la trasformazione geometrica e fondiamo le immagini.

![[slide_04_panorama_extract_match.png]]

### Odometria Visuale Ed Errore Di Drift

In robotica usiamo le feature per la __Visual Odometry__ e lo __SLAM__: analizzando i frame consecutivi della telecamera stimiamo la traiettoria del robot nello spazio.

![[slide_06_visual_odometry_drift.png]]

>[!WARNING] Accumulo dell'Errore (Drift)
>Ogni spostamento è stimato rispetto al frame precedente. Piccole imprecisioni sui punti si sommano nel tempo generando una deriva progressiva (__drift__, ad esempio $3.4\text{ px}$ dopo soli 36 frame). Punti stabili e localizzati con precisione sub-pixel riducono drasticamente questo errore.

## Detector Vs Descriptor

Il problema di trovare corrispondenze si divide in due passaggi distinti:

![[casetta_descriptor_vettori.svg]]

### Detector: "Dove Si Trova Il Punto?"

Il __detector__ individua le coordinate $(x, y)$ dei punti notevoli sulla singola immagine, in modo completamente indipendente dall'altra vista:
- Deve essere __ripetibile__: lo stesso punto fisico nello spazio 3D deve essere individuato nella stessa posizione su immagini diverse, nonostante cambi di luce, posa o sfocatura.
- Deve essere __ben localizzato__: l'errore sulla posizione deve essere minimo (accuratezza sub-pixel).
- Deve garantire una __buona distribuzione__: i punti devono essere sparsi su tutta l'immagine, evitando che si concentrino tutti nella stessa zona.

### Descriptor: "Cosa C'è Attorno Al Punto?"

Il __descriptor__ prende la regione attorno al punto (la _patch_) e calcola un vettore numerico $\mathbf{f} \in \mathbb{R}^D$ che ne descrive l'aspetto:
- Deve essere __distintivo__: punti diversi devono avere descrittori molto distanti nello spazio dei vettori.
- Deve essere __invariante__: il vettore deve rimanere il più possibile uguale a fronte di rotazioni, cambi di scala, illuminazione o rumore.
- Deve essere __facile da comparare__: confrontando i vettori con la distanza euclidea possiamo trovare rapidamente il punto più simile tra le due immagini.

>[!IMPORTANT]
>L'algoritmo di __Harris & Stephens__ che vediamo in questa lezione è __esclusivamente un detector__: fornisce coordinate $(x, y)$ di angoli, ma non genera alcun vettore descrittore. I descrittori e il matching saranno affrontati nella lezione successiva.

## Criterio Locale: Flat, Edge E Corner

Non possiamo usare singoli pixel isolati per l'allineamento: in zone con colori uniformi ci sono troppi pixel identici, rendendo impossibile capire quale sia quello giusto.

Dobbiamo quindi cercare pixel con caratteristiche inusuali. Per farlo analizziamo come varia l'intensità luminosa quando muoviamo una piccola finestra d'osservazione $W$ attorno al punto:

![[casetta_flat_edge_corner.svg]]

Prendendo come esempio reale l'immagine della moto:

![[slide_14_moto_flat_edge_corner.png]]

Possiamo distinguere tre situazioni:

1. __Regione Piatta (Flat)__:
   - Spostando la finestra in qualsiasi direzione l'intensità non cambia ($E(u, v) \approx 0$).
   - È impossibile da usare: ogni pixel vicino è identico e ambiguo.

2. __Bordo (Edge)__:
   - Se muoviamo la finestra __lungo il bordo__ l'intensità non cambia ($E \approx 0$).
   - Se la muoviamo __perpendicolarmente al bordo__ c'è un brusco cambiamento ($E \gg 0$).
   - Questo genera il __problema dell'apertura (Aperture Problem)__: la posizione è vincolata solo in 1D, mentre lungo la linea del bordo può scivolare liberamente. Non va bene per una localizzazione 2D.

3. __Angolo (Corner)__:
   - Qualsiasi spostamento in __qualunque direzione 2D__ provoca una variazione netta d'intensità.
   - L'errore cresce rapidamente in ogni direzione assumendo la forma di una "ciotola" (_bowl_).
   - È il punto ideale: la posizione è vincolata univocamente in tutte le direzioni.

![[slide_16_three_moments_shift.png]]

>[!NOTE] Localizzazione Locale vs Unicità Globale
>Harris misura la stabilità locale della posizione, __non l'unicità globale__.
>Su texture ripetitive (come una scacchiera o le finestre di un palazzo), ogni vertice è un ottimo corner a livello locale, ma nell'immagine ce ne sono decine identici:
>
>![[slide_18_checkerboard_local_vs_global.png]]
>
>Un detector locale non può risolvere questa ambiguità: andrà filtrata dopo durante il matching o con vincoli geometrici globali (RANSAC).

## Derivazione Matematica dell'Harris Detector

L'idea è calcolare l'errore generato muovendo la finestra all'interno dell'area circostante.

### Funzione Di Errore $E(u, v)$

Definiamo l'errore di corrispondenza quando la finestra $W$ viene spostata di un vettore $\Delta \mathbf{x} = [u, v]^T$:

$$
E(u, v) = \sum_{(x, y) \in W} w(x, y) \left[ I(x+u, y+v) - I(x, y) \right]^2
$$

Dove:
- $I(x, y)$ è l'intensità dell'immagine in scala di grigi.
- $w(x, y)$ è una finestra di pesi: può essere una finestra rettangolare unitaria, oppure una __gaussiana__ circolare con deviazione standard $\sigma_i$, che dà più peso ai pixel centrali ed evita discontinuità sui bordi della finestra.

![[slide_20_harris_bowl_shift.png]]

In un corner $E(u, v)$ cresce rapidamente in tutte le direzioni, formando una ciotola ripida.

### Approssimazione Di Taylor Al Primo Ordine

Calcolare $E(u, v)$ spostando fisicamente la finestra in tutte le direzioni richiederebbe troppi calcoli.

Per piccoli spostamenti $(u, v)$ possiamo approssimare l'intensità traslata con lo sviluppo in serie di Taylor al primo ordine:

$$
I(x+u, y+v) \approx I(x, y) + \frac{\partial I}{\partial x} u + \frac{\partial I}{\partial y} v = I(x, y) + \nabla I^T \Delta \mathbf{x}
$$

Dove $\nabla I = [I_x, I_y]^T$ è il gradiente dell'immagine calcolato sul punto $(x, y)$.

La variazione di intensità diventa quindi lineare rispetto allo spostamento:

$$
I(x+u, y+v) - I(x, y) \approx I_x u + I_y v = \nabla I^T \Delta \mathbf{x}
$$

![[slide_23_taylor_1d_error.png]]

>[!NOTE]
>Fino a circa un pixel di spostamento l'approssimazione lineare è molto accurata. Poiché un corner registra un salto di intensità netto già per frazioni di pixel, il primo ordine di Taylor è più che sufficiente.

### Matrice Dei Secondi Momenti $C$

Sostituendo l'approssimazione lineare nella formula dell'errore quadratico:

$$
E(u, v) \approx \sum_{(x, y) \in W} w(x, y) \left( \nabla I^T \Delta \mathbf{x} \right)^2 = \Delta \mathbf{x}^T \left[ \sum_{(x, y) \in W} w(x, y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix} \right] \Delta \mathbf{x}
$$

Possiamo riscriverlo in forma compatta:

$$
E(u, v) \approx \Delta \mathbf{x}^T C \, \Delta \mathbf{x}
$$

La matrice simmetrica $2 \times 2$ prende il nome di __matrice di struttura__ o __matrice dei secondi momenti__ $C$:

$$
C = \begin{bmatrix} \sum_W w \, I_x^2 & \sum_W w \, I_x I_y \\ \sum_W w \, I_x I_y & \sum_W w \, I_y^2 \end{bmatrix} = \begin{bmatrix} \langle I_x^2 \rangle & \langle I_x I_y \rangle \\ \langle I_x I_y \rangle & \langle I_y^2 \rangle \end{bmatrix}
$$

#### Calcolo Pratico Tramite Convoluzione 2D

Come abbiamo visto per i [[0. Immagini, filtri e gradienti#Filtri Lineari|Filtri Lineari nella Lezione 0]], nella pratica non si usa un ciclo for sui pixel: fare una media pesata con una finestra gaussiana equivale esattamente a calcolare una __convoluzione 2D__ con un kernel gaussiano $G_{\sigma_i}$.

Il calcolo della matrice $C$ su tutta l'immagine si articola quindi in quattro passaggi:
1. __Calcolo dei gradienti__: calcoliamo $I_x$ e $I_y$ con Sobel o con la convoluzione della derivata di una gaussiana a scala $\sigma_d$ (vedi [[0. Immagini, filtri e gradienti#Operatori Prewitt E Sobel|Lezione 0]]).
2. __Prodotti puntuali__: calcoliamo pixel per pixel tre immagini: $I_x^2$, $I_y^2$ e $I_x I_y$.
3. __Smoothing gaussiano__: applichiamo la convoluzione 2D con filtro gaussiano $G_{\sigma_i}$ su ciascuna delle tre immagini dei prodotti:

   $$\langle I_x^2 \rangle = G_{\sigma_i} * (I_x^2), \quad \langle I_y^2 \rangle = G_{\sigma_i} * (I_y^2), \quad \langle I_x I_y \rangle = G_{\sigma_i} * (I_x I_y)$$

4. __Mappe di $C$__: per ogni pixel $(x, y)$, i valori delle tre immagini filtrate corrispondono direttamente agli elementi della matrice $C(x, y)$.

>[!IMPORTANT] Perché un Singolo Pixel Non Basta (Rango 1)
>Per un singolo pixel isolato, la matrice $\nabla I \nabla I^T = \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$ ha determinante nullo:
>
>$$\det(\nabla I \nabla I^T) = I_x^2 I_y^2 - (I_x I_y)^2 = 0$$
>
>Ha quindi rango 1: esiste sempre una direzione perpendicolare al gradiente in cui la variazione è nulla. Anche su un angolo, un singolo pixel dà una sola direzione di variazione.
>
>![[slide_26_shift_synthetic_gradients.png]]
>
>Per avere __rango 2__ (variazione in tutte le direzioni) dobbiamo per forza integrare su una finestra $W$ che contenga gradienti orientati in direzioni diverse.

![[slide_27_sum_products_not_gradients.png]]

>[!NOTE] Sommare i Prodotti e Non i Gradienti
>- Se sommassimo direttamente i gradienti $(\sum \nabla I)$, su una linea sottile i gradienti con versi opposti sui due lati si cancellerebbero a vicenda ($\sum \nabla I \approx 0$).
>- Sommando invece i prodotti $\sum w \nabla I \nabla I^T$, i segni opposti vengono elevati al quadrato e non si elidono.

### Analisi Degli Autovalori Di $C$

La matrice $C$ ci fornisce direttamente l'andamento dell'errore $E(u, v)$ per qualsiasi direzione di spostamento:

![[slide_30_maps_E_from_C.png]]

Essendo reale e simmetrica, $C$ ha due autovalori reali non negativi $\lambda_1, \lambda_2 \ge 0$ (con $\lambda_{\max} \ge \lambda_{\min} \ge 0$):
- $\lambda_{\max}$: la variazione nella direzione lungo cui l'immagine cambia più bruscamente.
- $\lambda_{\min}$: la variazione nella direzione perpendicolare, lungo cui l'immagine cambia meno.

![[slide_31_strongest_weakest_change.png]]

![[slide_34_harris_autovalori.png]]

Analizzando i due autovalori sul piano $(\lambda_{\max}, \lambda_{\min})$ possiamo classificare la regione:
- __Flat__: entrambi vicini a zero ($\lambda_{\max} \approx 0$, $\lambda_{\min} \approx 0$).
- __Edge__: $\lambda_{\max} \gg \lambda_{\min} \approx 0$. Spostandosi lungo il bordo l'errore è nullo.
- __Corner__: entrambi nettamente maggiori di zero ($\lambda_{\min} > \tau$).

![[slide_33_score_weakest_change_curves.png]]

>[!NOTE] Criterio di Shi-Tomasi (1994)
>Shi e Tomasi proposero di usare direttamente il valore del minimo autovalore come punteggio:
>
>$$\text{Score} = \lambda_{\min}$$
>
>Se $\lambda_{\min} > \tau$, il punto è un corner. È il criterio usato in OpenCV in `cv2.goodFeaturesToTrack` (con `useHarrisDetector=False`).

### Risposta Di Harris & Stephens ($R$) Senza Calcolare Autovalori

Calcolare esplicitamente gli autovalori per ogni pixel richiede radici quadrate, un'operazione costosa.

Harris e Stephens notarono che possiamo stimare l'entità dei due autovalori usando il determinante e la traccia della matrice $C$, che si calcolano direttamente con semplici moltiplicazioni e somme:
1. __Determinante__: $\det(C) = \lambda_1 \lambda_2 = \langle I_x^2 \rangle \langle I_y^2 \rangle - \langle I_x I_y \rangle^2$
2. __Traccia__: $\operatorname{tr}(C) = \lambda_1 + \lambda_2 = \langle I_x^2 \rangle + \langle I_y^2 \rangle$

Definirono quindi la funzione di risposta del corner $R$:

$$
R = \det(C) - k \left( \operatorname{tr}(C) \right)^2
$$

Dove $k$ è una costante empirica, tipicamente compresa tra $0.04$ e $0.06$.

![[slide_37_harris_stephens_values.png]]

Il comportamento di $R$ rispecchia perfettamente le tre tipologie di regioni:
- __Corner__: $\lambda_1$ e $\lambda_2$ sono entrambi grandi $\implies \det(C)$ domina sul termine quadratico $\implies \mathbf{R > 0}$ (valore positivo alto).
- __Edge__: un autovalore è grande e l'altro è quasi nullo ($\lambda_1 \gg 0, \lambda_2 \approx 0$) $\implies \det(C) \approx 0$, mentre la traccia al quadrato è grande $\implies \mathbf{R < 0}$ (valore marcatamente negativo).
- __Flat__: entrambi gli autovalori sono quasi nulli $\implies \mathbf{R \approx 0}$.

![[slide_39_same_image_two_responses.png]]

### Soglia E Soppressione Dei Non-Massimi (NMS)

La mappa di risposta $R(x, y)$ produce valori positivi alti per un intero gruppo di pixel attorno a ogni vertice. Per isolare i singoli punti discreti si applicano due filtri:

1. __Soglia Relativa (Thresholding)__: scartiamo i pixel sotto una percentuale del massimo globale: $R(x, y) > \tau \cdot \max R$ (tipicamente $\tau = 0.01 - 0.02$, ovvero l'$1-2\%$).
2. __Soppressione dei Non-Massimi (NMS)__: per evitare di avere risposte multiple sullo stesso angolo, manteniamo un pixel solo se il suo punteggio $R$ è strettamente maggiore di tutti i pixel nel suo vicinato locale (es. finestra $7 \times 7$ o $9 \times 9$), azzerando gli altri.

![[slide_43_nms_checkerboard.png]]

Su immagini reali il blob continuo di risposte viene ridotto dall'NMS al singolo picco geometrico:

![[slide_44_nms_real_corner_3d.png]]

## La Pipeline Di Harris Nella Pratica

L'intero algoritmo viene eseguito sull'immagine combinando operazioni di convoluzione 2D e prodotti puntuali:

![[slide_42_harris_step_by_step.png]]

![[harris_pipeline_step.svg]]

### Ruolo Delle Due Scale Gaussiane: $\sigma_d$ E $\sigma_i$

Nell'algoritmo intervengono due gaussiane distinte:

1. __Scala di Derivazione $\sigma_d$__:
   - È la scala del filtro gradiente usato per calcolare $I_x$ e $I_y$.
   - Determina a quali dettagli spaziali risponde il gradiente (rimuove rumore ad alta frequenza).
2. __Scala di Integrazione $\sigma_i$__:
   - È l'ampiezza della finestra gaussiana $w$ che calcola la media pesata dei prodotti nella matrice $C$.
   - Definisce quanto deve essere grande l'intorno per considerare la struttura un angolo.

Aumentando entrambe le scale (regola empirica: $\sigma_i \approx 1.5 - 2 \sigma_d$) avremo meno corner, ma più robusti ed eliminando le micro-oscillazioni:

![[slide_46_effect_sigma_d_sigma_i.png]]

Il risultato finale sull'immagine della motocicletta con $\sigma_d = 1$, $\sigma_i = 2$, $k = 0.04$, soglia $2\%$ e NMS $9 \times 9$:

![[slide_51_harris_corners_moto.png]]

## Invarianze E Limiti Di Harris

Analizziamo come si comporta il detector di fronte alle trasformazioni dell'immagine:

| Trasformazione | Comportamento di Harris | Perché |
| :--- | :---: | :--- |
| __Traslazione__ | __Covariante__ $\checkmark$ | Se l'immagine si sposta di $\mathbf{t}$, le coordinate dei corner si spostano esattamente di $\mathbf{t}$. |
| __Rotazione__ | __Covariante__ $\checkmark$ | Ruotando l'immagine, la forma quadratica ruota insieme ad essa: gli autovalori $\lambda_1, \lambda_2$ non cambiano, quindi la risposta $R$ rimane identica. |
| __Offset di Luminosità ($I + b$)__ | __Invariante__ $\checkmark$ | Come visto nell'[[0. Immagini, filtri e gradienti#Edge Detection|Edge Detection della Lezione 0]], il calcolo del gradiente elimina le costanti: $\nabla(I + b) = \nabla I$. |
| __Contrasto ($a \cdot I$)__ | __Parzialmente invariante__ $\sim$ | Moltiplicando per $a$ si ha $R' = a^4 R$. Usando una soglia relativa al massimo si compensa in teoria il fattore, ma in pratica si hanno problemi di saturazione (clipping a 255) o perdita di contrasto sotto 1 LSB. |
| __Cambiamento di Scala (Zoom)__ | <mark>__NON Invariante alla scala__</mark> $\times$ | __Limite fondamentale di Harris__: la finestra $\sigma_i$ ha dimensione fissa in pixel. Modificando lo zoom o la distanza, un angolo può sembrare un bordo piatto o fondersi con dettagli vicini. |

### Il Limite Della Scala: Verso Lo Scale-Space

Se ingrandiamo o rimpiccioliamo un'immagine, la finestra d'integrazione copre una porzione fisica diversa della scena:

![[slide_53_scale_change_rounded_corner.png]]

- Guardando uno spigolo arrotondato da vicino (zoom-in), la finestra vede solo un bordo quasi rettilineo ($R < 0$).
- Allontanandoci (zoom-out), la stessa curvatura viene compressa in pochi pixel e comincia a comportarsi come un angolo vivo ($R > 0$).

Misurando sperimentalmente la percentuale di corner ritrovati nella stessa posizione:

![[slide_54_repeatability_rotation_scale.png]]

- Con una rotazione di 45°, la ripetibilità è del __91%__ (la minima perdita è dovuta solo al campionamento discreto dei pixel).
- Con un cambio di scala ($0.48\times$), la ripetibilità crolla al __26%__ (e al __13%__ a $0.3\times$).

>[!IMPORTANT]
>Dato che Harris fissa i parametri $\sigma_d$ e $\sigma_i$ in pixel e non ha un modo per adattare la dimensione della finestra alla scala del dettaglio, __non è invariante al cambio di scala__.
>Per superare questo limite vedremo nella prossima lezione lo __Scale-Space__, il Laplaciano del Gaussiano (LoG / DoG) e l'algoritmo __SIFT__.

# 2. Scale-Space, Descrittori SIFT E Feature Matching

Nella lezione precedente abbiamo visto il detector di [[1. Local Features e Harris Corner Detector#Derivazione Matematica dell'Harris Detector|Harris]], che individua con precisione la posizione $(x, y)$ degli angoli. Abbiamo però scoperto il suo limite principale: la finestra ha una dimensione fissa in pixel e non è in grado di adattarsi se l'immagine subisce variazioni di scala (zoom).

Inoltre Harris è solo un detector: risponde alla domanda _"Dove si trova il punto?"_, ma non ci dice _"Cosa c'è attorno al punto?"_. Per accoppiare due fotografie della stessa scena dobbiamo associare univocamente ogni punto della prima al suo partner nella seconda.

In questa lezione affrontiamo i due passaggi chiave per risolvere il problema:
1. __Invarianza di Scala__: introducendo lo __Scale-Space__ per stimare la dimensione caratteristica di ciascun dettaglio a partire da una singola immagine.
2. __Descrittori Robusti (SIFT) e Matching__: costruire vettori numerici discriminativi invarianti a scala e rotazione, e associarli con il __Lowe's Ratio Test__.

## Dal Punto Di Interesse Al Feature Matching

L'obiettivo fondamentale è trovare punti di interesse unici che possano essere descritti facilmente e associati in modo non ambiguo tra viste differenti.

![[slide_04_p03_matching_goal_moto.png]]

### Separazione Concettuale: Detector Indipendente Vs Matching

Nelle due immagini il detector lavora in modo completamente indipendente:
- Su ciascuna immagine cerchiamo i punti candidati senza sapere a priori come la seconda vista sia traslata, ruotata o scalata rispetto alla prima.
- Solo dopo aver estratto ed etichettato ciascun punto con un proprio descrittore interveniamo con il confronto (__matching__).

![[slide_04_p05_detector_independent_candidates.png]]

### La Patch Come "Carta d'Identità" Del Punto

La prima idea per descrivere un punto $p = (x, y)$ consiste nel ritagliare una piccola finestra di pixel centrata su di esso (ad esempio $15 \times 15$ pixel), detta __patch__.

Srotolando i pixel riga per riga otteniamo un vettore numerico reale:

$$
\mathbf{f} \in \mathbb{R}^{225} \quad (15 \times 15 = 225 \text{ valori})
$$

![[slide_04_p06_patch_descriptor_vector.png]]

### Confronto Tramite Cross-Correlazione Normalizzata (NCC)

Per confrontare due patch $P_1$ e $P_2$ non possiamo usare la semplice differenza di intensità, perché cambierebbe con variazioni di luce. Usiamo la __Cross-Correlazione Normalizzata__ (NCC):

$$
\mathrm{NCC}(P_1, P_2) = \frac{\sum_i (P_1(i) - \bar{P}_1)(P_2(i) - \bar{P}_2)}{\sqrt{\sum_i (P_1(i) - \bar{P}_1)^2 \sum_i (P_2(i) - \bar{P}_2)^2}}
$$

Dove $\bar{P}_1$ e $\bar{P}_2$ sono le medie di intensità nelle due patch. La metrica vale $+1$ per perfetta coincidenza, $0$ per assenza di correlazione e $-1$ per contrasto opposto.

![[slide_04_p07_ncc_patches_comparison.png]]

Confrontando la patch di riferimento con varie zone dell'altra immagine, dettagli simili ottengono punteggi alti ($\mathrm{NCC} \approx 0.94$), mentre zone diverse danno valori vicini allo zero:

![[slide_04_p08_matching_ncc_candidates.png]]

## Il Problema Della Scala E Della Rotazione

Il confronto diretto tra patch di pixel grezzi con NCC funziona __solo per pure traslazioni__. Quando la fotocamera si sposta nello spazio compaiono due trasformazioni inevitabili:
1. __Zoom (Scala $s$)__: la fotocamera si avvicina o si allontana, modificando la dimensione apparente in pixel degli oggetti.
2. __Rotazione ($\alpha$)__: la fotocamera ruota attorno all'asse ottico, inducendo una rotazione sul piano dell'immagine.

![[slide_04_p09_zoom_rotation_effects.png]]

### Il Fallimento Del Patch Raw

Se usiamo finestre fisse a $15 \times 15$ pixel con rotazione o zoom, il confronto fallisce completamente:
- Con una rotazione di $30^\circ$, la correlazione tra patch identiche scende a $0.40$.
- Con uno zoom di fattore $s = 0.5$, l'NCC crolla a $-0.01$.

![[slide_04_p10_patch_failure_zoom_rotation.png]]

Il motivo è intuitivo: applicando una finestra fissa $15 \times 15$ sull'immagine rimpicciolita, la finestra copre un'area quattro volte più grande della scena reale, includendo sfondo e dettagli estranei.

![[slide_04_p11_zoom_scale_coverage_comparison.png]]

### Finestra Adattiva E Ricampionamento

Se conoscessimo il fattore di zoom $s$, potremmo restringere la finestra sull'immagine rimpicciolita esattamente dello stesso fattore ($r_2 = s \cdot r_1$), inquadrando la stessa porzione fisica di scena:

![[slide_04_p12_shrink_window_concept.png]]

Per confrontare le patch dobbiamo però produrre vettori della stessa lunghezza. La soluzione è __ricampionare la finestra adattiva su una griglia fissa__ di $15 \times 15$ campioni usando l'__interpolazione bilineare__ per valutare i valori nei punti intermedi:

![[slide_04_p13_resampling_patches_grid.png]]

In questo modo l'NCC si mantiene quasi costante sopra $0.93$ lungo tutto l'intervallo di zoom:

![[slide_04_p14_fixed_vs_shrunk_window_curve.png]]

![[slide_04_p15_repeatability_200points_zoom.png]]

### Il Problema Pratico: La Scala Varia Punto per Punto

Nelle scene reali non abbiamo un fattore di zoom globale $s$ noto a priori:
- Per la prospettiva della camera, l'ingrandimento dipende dalla profondità $Z$ di ciascun punto:

  $$x = f \frac{X}{Z}, \quad y = f \frac{Y}{Z}$$

- Oggetti a distanze diverse hanno scale locali $s_i$ diverse.
- __Dobbiamo quindi misurare la scala in modo autonomo per ogni singolo punto su ciascuna immagine__, prima di qualsiasi confronto.

![[slide_04_p16_depth_independent_scale_schematic.png]]

>[!WARNING] Il Doppio Problema di Scala (Detector vs Descriptor)
>Il problema di scala è presente sia dal lato detector che dal lato descriptor:
>1. __Lato Detector__: se il detector lavora a scala fissa (come Sobel o Harris classico), un angolo che nello zoom diventa troppo piccolo o troppo smussato __non viene nemmeno rilevato__. Se il detector perde il punto, nessun descrittore potrà mai accoppiarlo.
>2. __Lato Descriptor__: anche rilevando il punto, se la finestra non si adatta alla scala locale confronterà regioni di dimensione diversa generando descrittori scorrelati.

![[slide_04_p17_detector_misses_zoomed_corner.png]]

### Il Canonical Frame Del Keypoint

Per superare questo limite associamo a ciascun punto notevole (__keypoint__) un sistema di riferimento intrinseco detto __Canonical Frame__, definito da quattro parametri:

$$
\mathbf{p} = (x, y, \sigma, \theta)
$$

Dove:
- $(x, y)$ è la __posizione__ nell'immagine.
- $\sigma$ è la __scala caratteristica__ (dimensione del dettaglio).
- $\theta$ è l'__orientamento dominante__ del dettaglio.

![[slide_04_p19_canonical_frame_keypoint.png]]

La pipeline __SIFT (Scale-Invariant Feature Transform)__ sviluppata da David Lowe risolve il problema in quattro fasi:
1. __Scale-Space Extrema Detection__: ricerca di punti cospicui nello spazio delle scale (detector scale-invariant).
2. __Keypoint Localization__: raffinamento della posizione ed eliminazione di bordi instabili con l'Hessiano.
3. __Orientation Assignment__: stima dell'orientamento dominante $\theta$ per l'invarianza a rotazione.
4. __Keypoint Descriptor__: costruzione del vettore a 128 dimensioni basato su istogrammi di gradienti.

![[slide_04_p20_sift_pipeline_overview.png]]

## Selezione Di Scala E Scale-Space (LoG E DoG)

Come facciamo a determinare la dimensione $\sigma$ di un dettaglio lavorando su una sola immagine?

![[slide_04_p22_try_every_size_peak_curve.png]]

### Il Blur Gaussiano Come Manopola Di Scala

Come visto nei [[0. Immagini, filtri e gradienti#Filtro Gaussiano|Filtri Gaussiani della Lezione 0]], la deviazione standard $\sigma$ agisce da __manopola di scala__:
- Strutture più piccole di $\sigma$ vengono sfocate e rimosse.
- Strutture più grandi di $\sigma$ sopravvivono.
- Un filtro a scala $\sigma$ risponde in modo privilegiato a strutture con dimensione paragonabile a $\sigma$.

![[slide_04_p23_gaussian_blur_scales.png]]

### Il Principio Della Scala Caratteristica

Se applichiamo una funzione differenziale $f(\sigma)$ all'immagine sfocata a scale crescenti, la funzione risponderà diversamente ad ogni livello: __la scala caratteristica del dettaglio è identificata dal picco massimo della risposta__.

$$
\sigma_{\text{char}} = \arg\max_\sigma |f(\sigma)|
$$

![[slide_04_p24_characteristic_scale_peak_curve.png]]

Se un'immagine subisce uno zoom $s = 0.5$, rappresentando le risposte su un __asse logaritmico__ ($\log \sigma$), la curva dell'immagine rimpicciolita è identica alla prima ma traslata di $\log(s)$:
- Il picco della risposta si sposta esattamente del rapporto di zoom:

  $$\sigma_2 = s \cdot \sigma_1$$

![[slide_04_p25_characteristic_scale_zoom_shift.png]]

![[slide_04_p26_measured_peak_engine_cover.png]]

Una volta trovata la scala caratteristica $\sigma$, impostiamo il raggio della finestra proporzionalmente ad essa: $r = c \cdot \sigma$ (con $c \approx 3-6$).

![[slide_04_p27_scale_to_window_radius.png]]

### Il Laplaciano Di Gaussiana (LoG)

La funzione $f(\sigma)$ deve avere un __unico massimo ben definito__:
- Fare la media dell'intensità su un cerchio varia troppo lentamente e non dà picchi chiari.
- Serve un __filtro a blob__, sensibile a concentrazioni circolari di luce o buio rispetto allo sfondo.

![[slide_04_p28_blob_filter_peak_comparison.png]]

Come visto nelle [[0. Immagini, filtri e gradienti#Laplaciano Del Gaussiano (LoG)|Derivate Seconde della Lezione 0]], calcoliamo il Laplaciano dell'immagine sfocata:

$$
\nabla^2 L = L_{xx} + L_{yy} = I * \nabla^2 G_\sigma
$$

Il kernel analitico è il __Laplacian of Gaussian (LoG)__:

$$
\nabla^2 G_\sigma(x, y) = \left(\frac{x^2 + y^2 - 2\sigma^2}{\sigma^4}\right) G_\sigma(x, y)
$$

Cambiando segno ($-\nabla^2 G_\sigma$), il profilo assume la forma a __cappello messicano__ (_Mexican hat_): un centro positivo circondato da un anello negativo a somma nulla.

![[slide_04_p29_laplacian_of_gaussian_profile.png]]

### Il Problema Del Decadimento $1/\sigma^2$ E La Normalizzazione

Se applichiamo il LoG $\nabla^2 L$ a dischi di raggio crescente ($\rho = 4, 8, 16\text{ px}$), la posizione del picco è corretta ($\sigma \propto \rho$), ma __l'altezza del picco decade proporzionalmente a $1/\sigma^2$__:

![[slide_04_p30_log_response_unnormalized_decay.png]]

Questo accade perché lo smoothing distribuisce le pendenze su un intervallo più largo: le derivate seconde si riducono di un fattore $\sigma^2$. Un blob grande avrebbe quindi un picco piccolissimo rispetto al rumore ad alta frequenza.

Per risolvere introduciamo il __Laplaciano Normalizzato di Scala__, moltiplicando la risposta per $\sigma^2$:

$$
\sigma^2 \nabla^2 L = \sigma^2 (L_{xx} + L_{yy})
$$

Grazie al fattore $\sigma^2$, ogni cerchio produce un picco con la __stessa altezza invariante__, collocato a $\sigma_{\text{char}} = \rho / \sqrt{2}$.

![[slide_04_p31_normalized_log_scale_invariance.png]]

### Scale-Space 3D E Ricerca Degli Estremi (26 Vicini)

Costruiamo lo __Scale-Space__ discreto come uno stack tridimensionale di immagini, calcolando la risposta del Laplaciano normalizzato a scale a progressione geometrica: $\sigma_n = \sigma_0 \cdot k^n$.

![[slide_04_p32_scale_space_hubble_galaxies.png]]

Per estrarre i keypoint cerchiamo i punti che sono massimi o minimi locali rispetto all'intorno spaziale e di scala:

![[slide_04_p33_scale_space_3d_extrema_26neighbors.png]]

Ogni punto viene confrontato con i suoi __26 vicini__:
- 8 vicini sullo stesso piano di scala $\sigma$.
- 9 vicini sul livello di scala inferiore ($\sigma / k$).
- 9 vicini sul livello di scala superiore ($k\sigma$).

Se il punto ha valore strettamente superiore (o inferiore) a tutti i 26 vicini e supera una soglia minima di contrasto ($|\sigma^2 \nabla^2 L| > \tau$), viene accettato come keypoint con coordinate $(x, y, \sigma)$.

![[slide_04_p34_blob_detector_hubble_results.png]]

### Difference Of Gaussians (DoG): L'Approssimazione Veloce Di SIFT

Calcolare il LoG con le derivate seconde su ogni livello di scala richiede molti calcoli.

David Lowe nota che la derivata rispetto a $\sigma$ equivale alla diffusione del calore: $\frac{\partial L}{\partial \sigma} = \sigma \nabla^2 L$. Approssimando con differenze finite tra due livelli adiacenti sfocati a scala $\sigma$ e $k\sigma$:

$$
\frac{L(x, y, k\sigma) - L(x, y, \sigma)}{k\sigma - \sigma} \approx \sigma \nabla^2 L
$$

Moltiplicando per $(k - 1)\sigma$ otteniamo la __Difference of Gaussians (DoG)__:

$$
D(x, y, \sigma) = L(x, y, k\sigma) - L(x, y, \sigma) \approx (k - 1) \sigma^2 \nabla^2 L
$$

Dato che le immagini sfocate $L$ servono già per la piramide delle scale, la DoG elimina del tutto le derivate seconde: ogni livello DoG costa __una sola sottrazione per pixel__.

![[slide_04_p35_difference_of_gaussians_dog_approximation.png]]

### Eliminazione Dei Bordi Con La Matrice Hessiana

Il DoG risponde non solo sui blob, ma anche lungo i __bordi__.

Lungo un bordo la risposta del DoG forma un crinale (_ridge_). A causa del rumore, il massimo locale nello scale-space cade in punti casuali lungo la linea, rendendo il matching instabile:

![[slide_04_p36_edge_instability_noise.png]]

Per eliminare i punti di bordo, SIFT calcola la __matrice Hessiana 2D__ sulle derivate seconde della DoG:

$$
H = \begin{bmatrix} D_{xx} & D_{xy} \\ D_{xy} & D_{yy} \end{bmatrix}
$$

I due autovalori $\alpha, \beta$ quantificano le curvature:
- In un __blob__, la superficie curva fortemente in entrambe le direzioni ($\alpha, \beta$ dello stesso ordine di grandezza).
- Lungo un __bordo__, la superficie curva perpendicolarmente al bordo ($|\alpha| \gg 0$) ma è piatta lungo il bordo ($|\beta| \approx 0$).

Come fatto per Harris, usiamo traccia e determinante per evitare radici quadrate:

$$\mathrm{Tr}(H) = D_{xx} + D_{yy} = \alpha + \beta, \quad \det(H) = D_{xx} D_{yy} - D_{xy}^2 = \alpha \beta$$

Definendo il rapporto tra le curvature $r = \alpha / \beta$:

$$
\frac{\mathrm{Tr}(H)^2}{\det(H)} = \frac{(r + 1)^2}{r}
$$

SIFT impone una soglia massima sul rapporto di curvatura con $r = 10$:

$$
\frac{\mathrm{Tr}(H)^2}{\det(H)} < \frac{(10 + 1)^2}{10} = 12.1
$$

Se $\det(H) \le 0$ (punto di sella) o se il rapporto supera $12.1$, il punto viene scartato come bordo.

![[slide_04_p37_sift_hessian_curvature_edge_test.png]]

Con la scala misurata $\sigma$, la finestra si adatta automaticamente: su dati reali l'accuratezza di matching passa dal $14\%$ (finestra fissa) all'__$86\%$__.

![[slide_04_p38_window_follows_measured_sigma.png]]

![[slide_04_p39_repeatability_measured_sigma_174points.png]]

## Invarianza Alla Rotazione: Orientamento Canonico

Risolta la scala, dobbiamo gestire la rotazione $\alpha$. Ruotando la finestra sull'angolo corretto, l'NCC torna a $0.98$:

![[slide_04_p41_rotation_canonical_window_alignment.png]]

Poiché non conosciamo la rotazione a priori, stimiamo un __orientamento canonico $\theta$__ per ciascun keypoint analizzando i gradienti locali:
- Modulo: $m(x, y) = \sqrt{L_x^2 + L_y^2}$
- Direzione: $\phi(x, y) = \mathrm{atan2}(L_y, L_x)$

Ruotando l'immagine, ogni gradiente locale ruota della stessa quantità $\alpha$ mantenendo la propria magnitudine:

![[slide_04_p42_gradient_direction_magnitude_rotation.png]]

### Istogramma Delle Orientazioni A 36 Bin

1. Calcoliamo i gradienti nell'intorno circolare del keypoint (raggio $\propto \sigma$), pesandoli con una gaussiana di deviazione standard $1.5\sigma$.
2. Costruiamo un istogramma a __36 bin da $10^\circ$__ ciascuno: ogni gradiente vota nel bin della propria direzione con peso pari alla sua magnitudine pesata.
3. Il picco massimo dell'istogramma individua l'__orientamento canonico $\theta$__. Se sono presenti picchi secondari sopra l'__$80\%$ del massimo__, creiamo un keypoint duplicato con il secondo angolo per gestire ambiguità e simmetrie.

![[slide_04_p43_orientation_histogram_36bins.png]]

Ruotando il sistema di coordinate dell'angolo $\theta$, le direzioni relative diventano invarianti:

$$
\phi_{\text{rel}} = \phi - \theta \implies (\phi_1 + \alpha) - (\theta_1 + \alpha) = \phi_1 - \theta_1
$$

![[slide_04_p44_relative_gradient_angle_invariance.png]]

![[slide_04_p45_orientation_histogram_alignment_test.png]]

Ora ogni keypoint dispone del suo Canonical Frame completo $\mathbf{p} = (x, y, \sigma, \theta)$:

![[slide_04_p47_full_frame_scale_orientation.png]]

## Descrittore SIFT: Architettura A 128 Dimensioni

Perché non possiamo confrontare direttamente i pixel grezzi della finestra orientata?

La posizione, la scala e l'angolo stimati non sono mai perfetti. Se la finestra si sposta di appena $0.5\sigma$, l'NCC tra pixel grezzi crolla a $0.70$:

![[slide_04_p49_frame_estimation_error_fragility.png]]

### Istogrammi Di Gradienti Per Cella

L'idea di Lowe è aggregare statistiche locali:
- Dividiamo la regione in celle e creiamo un istogramma delle direzioni a __8 bin da $45^\circ$__ per ogni cella.
- Se la finestra subisce un piccolo errore di posizionamento, i bordi traslano leggermente dentro la cella ma i gradienti puntano nelle stesse direzioni: l'istogramma della cella rimane quasi identico (similarità $0.999$).

![[slide_04_p50_sift_one_cell_8bin_histogram.png]]

Usiamo una __griglia di $4 \times 4$ celle__: un singolo istogramma globale perderebbe del tutto la disposizione geometrica delle parti.

![[slide_04_p51_grid_vs_single_histogram_spatial_layout.png]]

Per evitare salti discontinui quando un gradiente si trova sul bordo tra due celle o tra due bin angolari, SIFT usa l'__interpolazione trilineare__ ripartendo il voto proporzionalmente tra le celle e i bin vicini.

![[slide_04_p52_trilinear_interpolation_shared_votes.png]]

### Costruzione Del Vettore Descrittore

![[slide_04_p53_building_descriptor_gradient_grid.png]]

![[slide_04_p54_sift_descriptor_architecture_128d.png]]

1. Campioniamo una griglia $16 \times 16$ di gradienti relativi attorno al punto, pesandoli con una gaussiana decrescente.
2. Dividiamo in $4 \times 4 = 16$ celle, calcolando un istogramma a 8 bin per cella.
3. Concateniamo i 16 istogrammi ottenendo il vettore descrittore finale:

   $$\mathbf{f} \in \mathbb{R}^{128} \quad (16 \text{ celle} \times 8 \text{ bin} = 128 \text{ valori})$$

4. __Normalizzazione e Clamping__:
   - Normalizziamo a norma euclidea unitaria: $\mathbf{f} \leftarrow \mathbf{f} / \|\mathbf{f}\|_2$.
   - Limitiamo ogni componente a un massimo di __$0.2$__ ($\min(f_i, 0.2)$) per tagliare gradienti anomali dovuti a riflessi speculari.
   - Rinormalizziamo a norma unitaria.

![[slide_04_p56_pixels_vs_sift_drift_curve.png]]

![[slide_04_p58_sift_complete_pipeline_one_slide.png]]

## Feature Matching E Lowe's Ratio Test

Estraendo i vettori $\mathbf{f}_i, \mathbf{g}_j \in \mathbb{R}^{128}$ dalle due immagini, misuriamo la loro similarità con la __distanza euclidea $L_2$__:

$$
d(\mathbf{f}, \mathbf{g}) = \|\mathbf{f} - \mathbf{g}\|_2 = \sqrt{\sum_{k=1}^{128} (f_k - g_k)^2}
$$

![[slide_04_p60_nearest_neighbor_ambiguity_space.png]]

### Il Limite Del Nearest Neighbor Puro

Prendere semplicemente il vicino più prossimo ($d_1 = \min \|\mathbf{f} - \mathbf{g}_j\|$) ha un grosso difetto: fornisce sempre un match, anche quando il punto è uscito dall'inquadratura o è coperto. Su dati reali, l'80% dei match del NN puro sono sbagliati e una soglia fissa su $d_1$ non riesce a separarli:

![[slide_04_p61_distance_vs_ratio_distribution.png]]

### Lowe's Ratio Test

Lowe confronta la distanza del primo vicino $d_1$ con quella del __secondo vicino più prossimo__ $d_2$:

$$
\text{Ratio} = \frac{d_1}{d_2}
$$

![[slide_04_p62_lowe_ratio_test_comparison.png]]

L'idea è semplice:
- __Match corretto__: se il punto ha trovato il suo vero partner, $d_1$ è piccolo e qualsiasi altro punto nella scena $d_2$ sarà molto più distante $\implies d_1 / d_2 \ll 1$.
- __Match errato o ambiguo__: se il punto non è presente o si trova su una texture ripetitiva, $d_1$ e $d_2$ sono candidati casuali con distanze simili $\implies d_1 / d_2 \approx 1$.

>[!IMPORTANT] Criterio di Lowe
>Accettiamo il match se e solo se:
>
>$$\frac{d_1}{d_2} < \tau \quad \text{con } \tau = 0.8$$

Abbassare la soglia da 1 a 0.8 elimina quasi tutti i match sbagliati perdendo pochissimi match corretti:
- Con $\tau = 1.0$: 419 corretti, 882 errati.
- Con $\tau = 0.8$: __361 corretti, solo 36 errati__.

![[slide_04_p63_ratio_test_motorcycle_results.png]]

I pochi outlier rimasti vengono infine eliminati applicando un vincolo geometrico globale tramite l'algoritmo __RANSAC__, che vedremo nella prossima lezione.

![[slide_04_p64_geometric_consistency_ransac_filter.png]]

![[slide_04_p65_ransac_hubble_matching_success.png]]

## Approfondimento: Harris-Laplace

SIFT si basa sugli estremi della DoG, che individuano principalmente __blob__. Se invece vogliamo rilevare veri __angoli__ associandoli comunque a una scala caratteristica, possiamo usare __Harris-Laplace__:
1. Usiamo __Harris__ a varie scale $\sigma_n$ per trovare la posizione precisa $(x, y)$ dei vertici.
2. Usiamo il __LoG normalizzato__ lungo la coordinata di scala per trovare il picco $\sigma$.

![[slide_04_p72_harris_laplace_vs_sift_blobs_corners.png]]

![[slide_04_p73_harris_laplace_steps_diagram.png]]

Su strutture rettilinee con rumore, il blob detector genera punti sparsi lungo i bordi (ripetibilità del 36%), mentre Harris-Laplace concentra i punti esattamente sui vertici geometrici (ripetibilità dell'83%):

![[slide_04_p74_edge_instability_blobs_vs_harris_laplace.png]]

# 3. Trasformazioni Geometriche E Allineamento Di Immagini

Nelle lezioni precedenti abbiamo visto come manipolare le intensità luminose dei pixel con i filtri e come estrarre punti di interesse invarianti con Harris e [[2. Scale-Space, Descrittori SIFT e Feature Matching#Descrittore SIFT: Architettura A 128 Dimensioni|SIFT]].

Nell'image processing tradizionale la griglia dei pixel rimane fissa: un filtro calcola un nuovo valore di luminosità per il pixel $(x, y)$, lasciando la sua posizione geometrica inalterata:

$$
I'(x, y) = g(I(x, y))
$$

Al contrario, in computer vision (per compiti come la ricostruzione 3D, l'odometria visiva o il panorama stitching) vogliamo compiere il percorso inverso: determinare la __trasformazione geometrica__ $T$ che descrive come si sono spostati i punti tra due immagini diverse:

$$
p' = T(p)
$$

Dove $p = [x, y]^T$ è la coordinata del punto nell'immagine di partenza e $p' = [x', y']^T$ è la sua posizione nell'immagine trasformata.

![[slide_05_p03_mosaics_odometry_applications.png]]

## Differenza Tra Filtering E Warping

È importante distinguere chiaramente i due approcci:
1. __Filtraggio (Filtering)__: modifica i valori numerici di intensità o colore dei pixel (il _range_), lasciando invariata la loro posizione sulla griglia.
2. __Deformazione (Warping)__: modifica la posizione spaziale dei pixel (il _dominio_), lasciando idealmente invariati i loro valori di luminosità.

![[slide_05_p07_filtering_vs_warping_backward.png]]

### Trasformazioni Globali Vs Locali

In questa lezione assumiamo che le trasformazioni siano __globali__: un'unica regola matematica $T$, governata da un piccolo numero di parametri, descrive lo spostamento di tutti i pixel dell'immagine.

>[!WARNING] Quando la Trasformazione Non è Globale
>Una trasformazione globale non è valida in due casi tipici:
>1. __Oggetti in movimento indipendente__: se un'auto si muove verso destra mentre noi ci spostiamo a sinistra, lo sfondo e l'auto seguiranno due trasformazioni diverse.
>2. __Parallasse 3D__: se la scena ha profondità e la camera trasla, gli oggetti vicini si spostano molto più velocemente rispetto allo sfondo lontano.
>In questi casi servono trasformazioni locali (Optical Flow o geometria epipolare).

![[slide_05_p08_global_transformation_rules.png]]

### Forward Warping Vs Backward Warping (Il Problema Dei Buchi)

Se proviamo ad applicare la trasformazione direttamente mappando ogni pixel dalla sorgente alla destinazione ($p' = T(p)$), usiamo il cosiddetto __Forward Warping__.

Questo metodo ha due gravi difetti:
- __Formazione di buchi (Holes)__: se ingrandiamo l'immagine (ad esempio raddoppiandola da $3 \times 3$ a $6 \times 6$), i pixel di partenza si allontanano tra loro lasciando molte celle di arrivo vuote.
- __Sovrascritture (Aliasing)__: se comprimiamo l'immagine, più pixel sorgente finiscono nello stesso pixel di destinazione.

![[interpolazione_forward_warping_buchi.svg]]

Per evitare questi problemi si adotta sempre il __Backward Warping__ (mappatura all'indietro):
1. Scandiamo ogni pixel intero $p' = [x', y']^T$ della griglia di destinazione.
2. Calcoliamo la coordinata di provenienza nell'immagine sorgente tramite la trasformazione inversa:

   $$p = T^{-1}(p')$$

3. Dato che la coordinata $p$ trovata non sarà quasi mai intera, stimiamo il valore di luminosità tramite __interpolazione spaziale__ tra i pixel vicini:
   - __Nearest Neighbor__: prende il pixel intero più vicino (veloce ma produce scalettature ed aliasing).
   - __Interpolazione Bilineare__: media pesata dei 4 pixel vicini in base alla distanza frazionaria (ottimo compromesso qualità/costo).
   - __Interpolazione Bicubica__: usa una finestra $4 \times 4$ pesata con polinomi cubici (più liscia ma più costosa).
4. Se il punto calcolato cade fuori dai bordi dell'immagine sorgente, impostiamo il pixel a nero (valore 0).

## Trasformazioni Lineari Nel Piano 2D

Una trasformazione $T: \mathbb{R}^2 \to \mathbb{R}^2$ è lineare se rispetta il principio di sovrapposizione ($T(\alpha p_1 + \beta p_2) = \alpha T(p_1) + \beta T(p_2)$). Possiamo esprimerla con una matrice $2 \times 2$:

$$
\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} m_{11} & m_{12} \\ m_{21} & m_{22} \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}
$$

![[slide_05_p10_linear_transformation_2x2_grid.png]]

Le colonne della matrice rappresentano esattamente le __nuove posizioni assunte dai versori della base canonica__ $[1, 0]^T$ e $[0, 1]^T$ dopo la trasformazione.

### Tipi Fondamentali Di Trasformazioni 2D

1. __Scalatura (Scaling)__:

   $$M_{\text{scale}} = \begin{bmatrix} s_x & 0 \\ 0 & s_y \end{bmatrix} \implies \begin{cases} x' = s_x x \\ y' = s_y y \end{cases}$$

   Se $s_x = s_y$ lo scaling è isotropo (mantiene le proporzioni); se $s_x \ne s_y$ è anisotropo e cambia l'aspect ratio.
   ![[slide_05_p11_scaling_aspect_ratio_matrix.png]]

2. __Rotazione Pura Attorno all'Origine__:

   $$R(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$$

   Matrice ortogonale ($R^T R = I$), determinante $\det(R) = +1$, preserva distanze e angoli.
   ![[slide_05_p12_rotation_matrix_columns.png]]

3. __Riflessione (Mirroring)__: inverte il segno di un asse (determinante $-1$).

4. __Scorrimento (Shear)__:
   Sposta una coordinata in proporzione all'altra, inclinando i rettangoli in parallelogrammi:

   $$M_{\text{shear}, x} = \begin{bmatrix} 1 & s_h \\ 0 & 1 \end{bmatrix} \implies \begin{cases} x' = x + s_h y \\ y' = y \end{cases}$$

   ![[slide_05_p13_mirror_and_shear_matrices.png]]

>[!IMPORTANT] Ruolo dello Shear nei Sensori Reali
>Lo shear serve a modellare non-idealità fisiche della cattura:
>- __Rolling Shutter__: nei sensori CMOS le righe dell'immagine non vengono lette simultaneamente ma sequenzialmente dall'alto verso il basso. Se la telecamera o un oggetto si muove rapidamente, ogni riga subisce uno scostamento proporzionale a $y$, generando uno shear evidente.
>- __Skew del sensore__: modella imperfezioni costruttive in cui i pixel non formano angoli retti perfetti di $90^\circ$.

![[slide_05_p14_entries_of_M_deformation.png]]

### Proprietà Delle Trasformazioni Lineari $2 \times 2$

- __L'origine non si sposta mai__: $M \begin{bmatrix} 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}$.
- __Conservano rette e parallelismo__: rette parallele restano parallele dopo la trasformazione.
- __Non sono commutative__: moltiplicare matrici in ordine diverso dà risultati diversi ($M_1 M_2 \ne M_2 M_1$). Applicare prima una rotazione e poi uno shear è diverso dal fare prima lo shear e poi la rotazione!
  ![[slide_05_p16_composition_order_matters.png]]

## Coordinate Omogenee E Trasformazioni Affini

La trasformazione più semplice è la __traslazione__: spostare tutti i punti di un vettore $t = [t_x, t_y]^T$:

$$
\begin{cases} x' = x + t_x \\ y' = y + t_y \end{cases}
$$

Tuttavia la traslazione __sposta l'origine__ ($\begin{bmatrix} 0 \\ 0 \end{bmatrix} + t = t \ne 0$). Dato che una matrice lineare $2 \times 2$ mappa sempre l'origine in se stessa, __è impossibile rappresentare una traslazione con una matrice $2 \times 2$__.

![[slide_05_p17_translation_moves_origin.png]]

### Definizione Di Coordinate Omogenee

Per unificare rotazioni, scalature e traslazioni in una sola moltiplicazione matriciale usiamo le __coordinate omogenee__, aggiungendo una terza componente unitaria al punto:

$$
\tilde{p} = \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}
$$

In questo modo possiamo scrivere la trasformazione con una matrice $3 \times 3$:

$$
\begin{bmatrix} x' \\ y' \\ 1 \end{bmatrix} = \begin{bmatrix} m_{11} & m_{12} & t_x \\ m_{21} & m_{22} & t_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}
$$

![[slide_05_p18_homogeneous_coordinates_3x3.png]]

### La Trasformazione Affine (6 Gradi Di Libertà)

Una matrice con l'ultima riga fissata a $\begin{bmatrix} 0 & 0 & 1 \end{bmatrix}$:

$$
T_{\text{affine}} = \begin{bmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{bmatrix}
$$

prende il nome di __trasformazione affine__. Ha esattamente __6 parametri indipendenti (6 DoF)__: 4 per la parte lineare (rotazione, scala, shear) e 2 per la traslazione.

![[slide_05_p19_affine_transformation_matrix.png]]

Con le coordinate omogenee possiamo anche ruotare attorno a un centro arbitrario $c$:
1. Trasliamo il centro all'origine: $T(-c)$
2. Ruotiamo: $R(\theta)$
3. Riportiamo indietro il centro: $T(c)$

$$M = T(c) R(\theta) T(-c)$$

![[slide_05_p20_rotation_about_arbitrary_center.png]]

Le trasformazioni affini mantengono il parallelismo tra le rette, ma __non possono modellare la prospettiva__: in una fotografia reale le rette parallele convergono verso un punto di fuga.

![[slide_05_p22_perspective_ruled_paper_convergence.png]]

## Omografie E Spazio Proiettivo

Quando permettiamo anche all'ultima riga della matrice $3 \times 3$ di assumere valori generici, otteniamo la classe di trasformazioni più generale del piano 2D: l'__Omografia__ (o trasformazione proiettiva):

$$
H = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix}
$$

Moltiplicando per il punto omogeneo $[x, y, 1]^T$ otteniamo un vettore $[X', Y', W']^T$:

$$
\begin{bmatrix} X' \\ Y' \\ W' \end{bmatrix} = H \begin{bmatrix} x \\ y \\ 1 \end{bmatrix} \implies W' = h_{31} x + h_{32} y + h_{33}
$$

### Divisione Proiettiva

Nelle trasformazioni affini $W' = 1$ sempre. Nell'omografia $W'$ __varia da punto a punto__ a seconda della posizione $(x, y)$.

Per tornare alle coordinate cartesiane dobbiamo fare la __divisione proiettiva__ (dividendo per $W'$):

$$
\begin{cases}
x' = \dfrac{X'}{W'} = \dfrac{h_{11} x + h_{12} y + h_{13}}{h_{31} x + h_{32} y + h_{33}} \\[10pt]
y' = \dfrac{Y'}{W'} = \dfrac{h_{21} x + h_{22} y + h_{23}}{h_{31} x + h_{32} y + h_{33}}
\end{cases}
$$

![[slide_05_p24_homography_division_by_W.png]]

Nei punti in cui $W'$ è grande le coordinate vengono divise per un valore maggiore, provocando un rimpicciolimento: questo emula esattamente l'effetto della prospettiva, dove gli oggetti lontani appaiono più piccoli.

### Ambiguità Di Scala Proiettiva (8 Gradi Di Libertà)

Moltiplicando l'intera matrice $H$ per una costante scalare $\lambda \ne 0$, la divisione proiettiva elimina $\lambda$:

$$
\frac{\lambda X'}{\lambda W'} = \frac{X'}{W'} = x'
$$

Di conseguenza $H \sim \lambda H$: ci sono infinite matrici che producono la stessa identica trasformazione sul piano. La matrice ha 9 elementi ma solo __8 gradi di libertà (8 DoF)__.

Per fissare la scala negli algoritmi si impone una condizione:
- Fissare l'ultimo elemento a 1 ($h_{33} = 1$).
- Oppure imporre norma unitaria sul vettore dei parametri: $\|h\|_2 = 1$ (approccio più robusto usato con la SVD).

![[slide_05_p26_changing_h31_h32_effects.png]]

### Quando l'Omografia È Esatta

L'omografia 2D tra due immagini rappresenta una relazione geometrica fisicamente esatta se si verifica una di queste tre condizioni:
1. __La scena è planare__: tutti i punti giacciono su un piano, quindi non c'è parallasse.
2. __La telecamera ruota sul proprio centro ottico__: non c'è traslazione ($\Delta C = 0$), solo rotazione pura (è il principio che permette di creare i panorami).
3. __La scena è molto lontana__: le variazioni di profondità sono trascurabili rispetto alla distanza (es. foto aeree o satellitari).

![[slide_05_p28_when_homography_exact_conditions.png]]

Sotto un'omografia angoli, distanze e parallelismo vengono persi; si conservano però la __collinearità__ (le rette restano rette) e il __Cross-Ratio__ (rapporto d'incrocio) di quattro punti allineati.

### Tabella Riassuntiva Delle Trasformazioni 2D

| Trasformazione | Matrice $3 \times 3$ | DoF | Proprietà Conservate | Punti Minimi |
| :--- | :---: | :---: | :--- | :---: |
| __Traslazione__ | $\begin{bmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{bmatrix}$ | 2 | Orientazione, distanze, angoli, parallelismo | 1 punto |
| __Euclidea (Rigida)__ | $\begin{bmatrix} \cos\theta & -\sin\theta & t_x \\ \sin\theta & \cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix}$ | 3 | Distanze, angoli, aree, parallelismo | 2 punti |
| __Similarità__ | $\begin{bmatrix} s\cos\theta & -s\sin\theta & t_x \\ s\sin\theta & s\cos\theta & t_y \\ 0 & 0 & 1 \end{bmatrix}$ | 4 | Angoli, rapporti di distanze, parallelismo | 2 punti |
| __Affine__ | $\begin{bmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{bmatrix}$ | 6 | Parallelismo, rapporti di aree | 3 punti |
| __Omografia__ | $\begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix}$ | 8 | Collinearità, Cross-Ratio | 4 punti |

![[slide_05_p30_hierarchy_2d_transformations_table.png]]

## Stima Dei Parametri Dalle Corrispondenze

Supponiamo di avere estratto le corrispondenze tra due immagini: $\{(p_i, p_i')\}_{i=1}^n$. Dobbiamo trovare i parametri della trasformazione $T$ che spiegano al meglio lo spostamento di questi punti.

### Traslazione: Perché la Media È la Soluzione Ottima

Se abbiamo un solo match $(p_1, p_1')$:

$$x_1' = x_1 + t_x \implies t_x = x_1' - x_1$$

$$y_1' = y_1 + t_y \implies t_y = y_1' - y_1$$

Con un solo punto la soluzione è immediata, ma le posizioni dei keypoint hanno sempre un piccolo errore di misura ($\pm 1$ px). Usando un solo punto, quell'errore si trasferirebbe a tutta l'immagine.

![[slide_05_p33_one_match_translation_exact_error.png]]

Se abbiamo $n$ corrispondenze, ogni match fornisce una stima leggermente diversa dello spostamento. Vogliamo risolvere un problema di ottimizzazione ai minimi quadrati, minimizzando la somma dei residui quadratici:

$$
E(t_x) = \sum_{i=1}^n \left( x_i' - x_i - t_x \right)^2
$$

![[slide_05_p36_squared_residuals_cost_function.png]]

La funzione di costo è una parabola convessa. Per trovare il minimo calcoliamo la derivata prima e la poniamo uguale a zero:

$$
\frac{\mathrm{d}E}{\mathrm{d}t_x} = -2 \sum_{i=1}^n (x_i' - x_i - t_x) = 0 \implies \sum_{i=1}^n (x_i' - x_i) - n \, t_x = 0
$$

Risolvendo per $t_x$:

$$
t_x^* = \frac{1}{n} \sum_{i=1}^n (x_i' - x_i), \quad t_y^* = \frac{1}{n} \sum_{i=1}^n (y_i' - y_i)
$$

Come si nota, dopo tutti i calcoli matematici __il parametro ottimo ai minimi quadrati è esattamente la media degli spostamenti__. Gli errori indipendenti si compensano a vicenda.

![[slide_05_p38_least_squares_calculus_solution.png]]

### Formulazione Matriciale Ed Equazioni Normali

In forma matriciale il sistema di residui per tutte le corrispondenze è $A t \approx b$.

Minimizzando il costo $\|A t - b\|^2$ troviamo le cosiddette __Equazioni Normali__:

$$
(A^T A) t = A^T b \implies t^* = (A^T A)^{-1} A^T b
$$

Dove $(A^T A)^{-1} A^T$ è la __pseudoinversa di Moore-Penrose__.

### Stima Della Trasformazione Affine (6 Parametri)

Per la trasformazione affine abbiamo 6 incognite $m = [a_{11}, a_{12}, t_x, a_{21}, a_{22}, t_y]^T$. Ciascun match fornisce 2 equazioni:

$$
\begin{bmatrix}
x_i & y_i & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & x_i & y_i & 1
\end{bmatrix} m \approx \begin{bmatrix} x_i' \\ y_i' \end{bmatrix}
$$

Servono __almeno 3 corrispondenze non collineari__ (ogni punto dà 2 equazioni, $3 \times 2 = 6$). Con più di 3 punti risolviamo il sistema sovradeterminato con le equazioni normali $m^* = (A^T A)^{-1} A^T b$.

![[slide_05_p42_affine_estimation_6parameters.png]]

Se i punti sono collineari (sulla stessa retta), il sistema perde un grado di libertà e la matrice $A^T A$ diventa singolare ($\det = 0$), non potendo essere invertita.

## Stima Dell'Omografia: Metodo DLT (Direct Linear Transform)

Nel caso dell'omografia le equazioni contengono la divisione proiettiva:

$$
x_i' = \frac{h_{11} x_i + h_{12} y_i + h_{13}}{h_{31} x_i + h_{32} y_i + h_{33}}, \quad y_i' = \frac{h_{21} x_i + h_{22} y_i + h_{23}}{h_{31} x_i + h_{32} y_i + h_{33}}
$$

Queste equazioni non sono lineari nella forma standard. Possiamo però linearizzarle notando che il punto trasformato $H \tilde{p}_i$ e il punto misurato $\tilde{p}_i'$ hanno la stessa direzione nello spazio proiettivo: il loro __prodotto vettoriale deve essere nullo__:

$$
\tilde{p}_i' \times (H \tilde{p}_i) = \mathbf{0}
$$

Sviluppando il prodotto vettoriale otteniamo 2 equazioni lineari indipendenti per ciascun punto:

$$
\begin{bmatrix}
0 & 0 & 0 & -x_i & -y_i & -1 & y_i' x_i & y_i' y_i & y_i' \\
x_i & y_i & 1 & 0 & 0 & 0 & -x_i' x_i & -x_i' y_i & -x_i'
\end{bmatrix} h = \begin{bmatrix} 0 \\ 0 \end{bmatrix}
$$

Impilando $n$ match otteniamo il sistema lineare omogeneo:

$$
A h \approx \mathbf{0}
$$

Poiché $H$ ha 8 DoF e ogni match dà 2 equazioni, servono __almeno 4 corrispondenze a tre a tre non collineari__ (matrice $8 \times 9$).

![[slide_05_p44_homography_cross_product_Ah_zero.png]]

### Risoluzione Tramite Moltiplicatori Di Lagrange E SVD

Il sistema ammette la soluzione banale $h = \mathbf{0}$. Per evitarla imponiamo il vincolo di norma unitaria $\|h\|_2 = 1$ e minimizziamo il residuo $\|A h\|^2 = h^T (A^T A) h$.

Usando i moltiplicatori di Lagrange:

$$
\mathcal{L}(h, \lambda) = h^T (A^T A) h - \lambda (h^T h - 1)
$$

Derivando rispetto a $h$:

$$
(A^T A) h = \lambda h
$$

Il costo minimo residuo coincide con l'autovalore $\lambda$. La soluzione ottima corrisponde quindi all'__autovettore associato al minimo autovalore di $A^T A$__.

Invece di calcolare $A^T A$ (che amplifica gli errori numerici), calcoliamo la decomposizione a valori singolari (__SVD__) della matrice $A$:

$$
A = U \Sigma V^T
$$

La soluzione cercata è semplicemente l'__ultima colonna di $V$__ (corrispondente al valore singolare più piccolo).

![[slide_05_p45_dlt_svd_smallest_singular_value.png]]

### La Normalizzazione Di Hartley

Se applichiamo il DLT direttamente alle coordinate dei pixel (es. $1000 \times 1000$), le coordinate $x, y$ sono dell'ordine di $10^3$, mentre i termini misti $x_i x_i'$ sono dell'ordine di $10^6$. Nel prodotto $A^T A$ i coefficienti spaziano da $1$ a $10^{12}$, rendendo la matrice instabile dal punto di vista numerico.

La soluzione (proposta da Hartley) consiste nel __normalizzare le coordinate__ prima del DLT:
1. Trasliamo i punti in modo che il baricentro sia nell'origine $(0, 0)$.
2. Scaliamo i punti affinché la distanza media dall'origine sia $\sqrt{2}$.
3. Risolviamo il DLT sui punti normalizzati ottenendo $\tilde{H}$.
4. Riportiamo l'omografia nelle coordinate originali denormalizzando:

   $$H = T_2^{-1} \tilde{H} T_1$$

![[slide_05_p46_hartley_normalization_coordinates.png]]

Con 4 punti l'errore di misura si propaga provocando distorsioni evidenti sui bordi; con molte corrispondenze (es. 40) il sistema ai minimi quadrati compensa il rumore e l'errore di riproiezione scende sotto 1 pixel:

![[slide_05_p47_4matches_vs_40matches_error.png]]

## Pipeline Completa Di Allineamento E Composizione

La pipeline completa per comporre un panorama si articola in quattro fasi:

![[slide_05_p50_image_alignment_pipeline_overview.png]]

1. __Estrazione e Matching__: estraiamo keypoint e descrittori SIFT da entrambe le immagini, poi applichiamo il [[2. Scale-Space, Descrittori SIFT e Feature Matching#Lowe's Ratio Test|Ratio Test di Lowe]] ($d_1 / d_2 < 0.8$).
2. __Stima dell'Omografia__: stimiamo $H$ usando il DLT normalizzato sui punti corrispondenti.
3. __Backward Warping sul Canvas Comune__:
   - Calcoliamo le dimensioni del canvas comune proiettando i quattro angoli di $I_1$ tramite $H$.
   - Scandiamo i pixel del canvas e interpoliamo bilinearmente da $I_1$ usando $H^{-1}$.
4. __Blending__: nelle zone sovrapposte applichiamo una dissolvenza morbida (_alpha blending_) per nascondere i tagli tra le immagini.

![[slide_05_p53_canvas_inverse_warping_blending.png]]

### Il Limite Dei Minimi Quadrati: La Sensibilità Agli Outlier

I minimi quadrati funzionano bene solo se gli errori seguono una distribuzione normale attorno allo zero.

Se tra i match c'è __anche un solo outlier__ (un match completamente sbagliato, ad esempio causato da una simmetria o da un falso rilevamento):
- L'errore di quel punto può essere di centinaia di pixel ($r_i \approx 500$).
- Elevando al quadrato ($500^2 = 250.000$), questo singolo punto sposta da solo l'intera soluzione, rovinando completamente l'allineamento.

![[slide_05_p54_outlier_catastrophic_failure.png]]

>[!IMPORTANT]
>I minimi quadrati hanno un punto di rottura dello $0\%$: basta una sola corrispondenza errata per fallire.
>Nelle applicazioni reali si usa l'algoritmo __RANSAC (Random Sample Consensus)__, che seleziona casualmente campioni minimi di punti per isolare gli inlier ed eliminare tutti gli outlier prima della stima finale.
