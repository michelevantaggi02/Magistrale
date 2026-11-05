# C. Entropia Differenziale e Canale Gaussiano

La teoria dell'informazione sviluppata nei capitoli precedenti ha trattato variabili aleatorie a valori in alfabeti discreti, dove l'entropia di Shannon misura in modo assoluto e non negativo il grado medio di incertezza della sorgente o il numero minimo di bit necessari per una codifica senza perdita.

Nel passaggio a sistemi fisici e canali di comunicazione continui (come le forme d'onda analogiche, i segnali radio e le tensioni campionate), le grandezze sono descritte da variabili aleatorie continue supportate su intervalli della retta reale o su regioni dello spazio euclideo $n$-dimensionale $\mathbb{R}^n$. L'estensione dell'entropia al dominio continuo, introdotta da Claude Shannon nel 1948 con la definizione di __entropia differenziale__, presenta proprietà geometriche e analitiche profondamente diverse rispetto al caso discreto:
1. L'entropia differenziale non è una misura assoluta del contenuto informativo intrinseco, ma una misura relativa alla densità di riferimento della coordinata scelta.
2. Può assumere valori negativi e diverge a $-\infty$ al restringersi del supporto a singoli punti atomici.
3. Non è invariante per trasformazioni di coordinate non lineari o riscalamenti.

Tuttavia, l'entropia differenziale preserva intatta l'interpretazione geometrica asintotica tramite il volume dell'insieme tipico e costituisce il fondamento matematico per derivare la capacità dei canali analogici ad onda continua, culminando nella celebre formula di Shannon-Hartley per il canale a rumore additivo bianco gaussiano (AWGN).

## Definizione di Entropia Differenziale e Limiti del Dominio Continuo

Sia $X$ una variabile aleatoria continua con funzione di distribuzione cumulativa (CDF) $F(x) = \text{Pr}\{X \le x\}$. Se $F(x)$ è assolutamente continua rispetto alla misura di Lebesgue, esiste la funzione di densità di probabilità (PDF) definita dalla derivata quasi ovunque:

$$
f(x) = \frac{\mathrm{d}F(x)}{\mathrm{d}x}
$$

tale che $\int_{-\infty}^{+\infty} f(x) \mathrm{d}x = 1$. Il supporto della variabile aleatoria è definito come l'insieme dei punti in cui la densità è strettamente positiva:

$$
\mathcal{S} = \{ x \in \mathbb{R} : f(x) > 0 \}
$$

L'__entropia differenziale__ $h(X)$ di una variabile aleatoria continua $X$ con densità di probabilità $f(x)$ è definita dall'integrale di Lebesgue:

$$
h(X) = -\int_{\mathcal{S}} f(x) \log_2 f(x) \mathrm{d}x = \mathbb{E}[-\log_2 f(X)]
$$

Analogamente al caso discreto, l'entropia differenziale dipende esclusivamente dalla funzione di densità di probabilità $f(x)$ e non dai particolari valori numerici assunti dalla variabile aleatoria; per tale ragione viene frequentemente denotata nella letteratura scientifica come $h(f)$.

La definizione presuppone formalmente che l'integrale esista finito. Qualora la variabile aleatoria presenti distribuzioni miste (ossia una componente continua con densità e una componente discreta concentrata su masse puntiformi o atomi), l'integrale classico non è definito in senso ordinario e l'entropia complessiva collassa, richiedendo l'uso congiunto della teoria delle misure o della quantizzazione finita.

### Differenze Fondamentali rispetto all'Entropia Discreta

L'analogia formale tra l'espressione $H(X) = -\sum p_i \log_2 p_i$ e $h(X) = -\int f(x) \log_2 f(x) \mathrm{d}x$ non deve indurre ad assimilare l'entropia differenziale a una semplice sommatoria al limite. Esistono differenze concettuali e matematiche tassative:

1. __Non negatività violata ($h(X)$ può essere negativa)__:
   Nell'entropia discreta, essendo $0 \le p_i \le 1$, il logaritmo $-\log_2 p_i$ è sempre non negativo, garantendo $H(X) \ge 0$. Per una variabile continua, la densità di probabilità $f(x)$ rappresenta una densità per unità di misura e può assumere valori locali arbitrariamente elevati ($f(x) > 1$). Quando la probabilità si concentra in un intervallo di ampiezza infinitesima, il termine $-\log_2 f(x)$ diviene strettamente negativo, determinando un valore complessivo $h(X) < 0$.

2. __Assenza di invarianza per riscalamento delle coordinate__:
   Mentre per una variabile discreta qualsiasi trasformazione biunivoca $Y = g(X)$ preserva identica l'entropia ($H(g(X)) = H(X)$), per l'entropia differenziale un riscalamento lineare $Y = aX$ introduce un fattore additivo pari a $\log_2 |a|$. L'entropia differenziale dipende criticamente dal sistema di unità di misura adottato (ad esempio, misurare una grandezza in metri o in millimetri varia l'entropia differenziale di un valore costante).

3. __Interpretazione Geometrica del Volume di Supporto__:
   Nonostante $h(X)$ possa essere negativa, la grandezza esponenziale $2^{h(X)}$ rappresenta il __volume effettivo__ (o lunghezza effettiva per $n=1$) occupato dalla distribuzione di probabilità nello spazio campionario:

$$
\text{Vol}_{\text{eff}}(X) = 2^{h(X)} \ge 0
$$

Tale volume effettivo è sempre rigorosamente non negativo e quantifica l'estensione del supporto equivalente che conterrebbe la medesima incertezza sotto una distribuzione uniforme.

## Calcolo Esplicito per Distribuzioni Notevoli

L'analisi comparativa di distribuzioni continue standard illustra concretamente la genesi di valori sia positivi che negativi dell'entropia differenziale.

### Distribuzione Uniforme

Si consideri una variabile aleatoria distribuita uniformemente nell'intervallo $[0, a]$ con $a > 0$. La sua densità di probabilità è:

$$
f(x) = \begin{cases} \frac{1}{a} & \text{se } 0 \le x \le a \\ 0 & \text{altrove} \end{cases}
$$

L'entropia differenziale si ottiene integrando sul supporto $[0, a]$:

$$
h(X) = -\int_0^a \frac{1}{a} \log_2 \left(\frac{1}{a}\right) \mathrm{d}x = \log_2 a \int_0^a \frac{1}{a} \mathrm{d}x = \log_2 a \quad \text{bit}
$$

L'analisi al variare del parametro geometrico $a$ evidenzia:
- Per $a = 1$: $h(X) = \log_2 1 = 0$ bit. Una variabile uniforme su intervallo unitario possiede entropia differenziale esattamente nulla.
- Per $a > 1$: $h(X) > 0$ bit (ad esempio, per $a = 4$, $h(X) = \log_2 4 = 2$ bit).
- Per $a < 1$: $h(X) < 0$ bit. Ad esempio, per $a = \frac{1}{8}$, si ottiene $h(X) = \log_2(2^{-3}) = -3$ bit.
- Il volume effettivo associato è $2^{h(X)} = 2^{\log_2 a} = a$, che coincide esattamente con l'ampiezza fisica dell'intervallo di supporto, confermando la perfetta coerenza geometrica.

### Distribuzione Normale (Gaussiana) Unidimensionale

Sia $X \sim \mathcal{N}(\mu, \sigma^2)$ una variabile aleatoria gaussiana scalare con media $\mu$ e varianza $\sigma^2 > 0$. La sua funzione di densità di probabilità è data da:

$$
\phi(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)
$$

Per semplificare l'integrazione, si calcola inizialmente l'entropia differenziale naturale espressa in nats ($h_e$):

$$
\ln \phi(x) = -\frac{1}{2} \ln(2\pi\sigma^2) - \frac{(x - \mu)^2}{2\sigma^2}
$$

Sostituendo nell'integrale di definizione:

$$
h_e(\phi) = -\int_{-\infty}^{+\infty} \phi(x) \ln \phi(x) \mathrm{d}x = \int_{-\infty}^{+\infty} \phi(x) \left[ \frac{1}{2}\ln(2\pi\sigma^2) + \frac{(x - \mu)^2}{2\sigma^2} \right] \mathrm{d}x
$$

Sfruttando la linearità dell'operatore valore atteso e sapendo che $\int_{-\infty}^{+\infty} \phi(x)\mathrm{d}x = 1$ e $\mathbb{E}[(X - \mu)^2] = \sigma^2$:

$$
h_e(\phi) = \frac{1}{2}\ln(2\pi\sigma^2) + \frac{\mathbb{E}[(X - \mu)^2]}{2\sigma^2} = \frac{1}{2}\ln(2\pi\sigma^2) + \frac{\sigma^2}{2\sigma^2} = \frac{1}{2}\ln(2\pi\sigma^2) + \frac{1}{2}
$$

Riconoscendo che $\frac{1}{2} = \frac{1}{2}\ln(e)$:

$$
h_e(\phi) = \frac{1}{2}\ln(2\pi\sigma^2) + \frac{1}{2}\ln(e) = \frac{1}{2}\ln(2\pi e \sigma^2) \quad \text{nat}
$$

Convertendo l'unità di misura in bit tramite la relazione $h(X) = \log_2(e) h_e(X) = \frac{h_e(X)}{\ln 2}$:

$$
h(X) = \frac{1}{2}\log_2(2\pi e \sigma^2) \quad \text{bit}
$$

Dalla formula discendono proprietà salienti:
1. __Indipendenza dal valore atteso__: L'entropia differenziale gaussiana dipende unicamente dalla dispersione $\sigma^2$ e non dalla traslazione $\mu$.
2. __Valore numerico per varianza unitaria__: Per $\sigma^2 = 1$, l'entropia differenziale è $h(X) = \frac{1}{2}\log_2(2\pi e) \approx \frac{1}{2}\log_2(17.0795) \approx 2.0471$ bit.
3. __Soglia di annullamento dell'entropia__: L'entropia differenziale si annulla ($h(X) = 0$) quando l'argomento del logaritmo è unitario:

$$
   2\pi e \sigma^2 = 1 \iff \sigma = \frac{1}{\sqrt{2\pi e}} \approx 0.2420
$$

   Per $\sigma < 0.2420$, l'entropia della gaussiana assume valori negativi ($h(X) < 0$), riflettendo un'estrema localizzazione della massa di probabilità attorno alla media.

## Proprietà di Equipartizione Asintotica (AEP) nel Continuo e Insieme Tipico

Il ruolo cardine dell'entropia differenziale nella teoria dell'informazione risiede nella sua capacità di caratterizzare il comportamento geometrico asintotico di vettori di campioni continui indipendenti e identicamente distribuiti (i.i.d.), in perfetta analogia con la [[8. Proprietà di Equipartizione Asintotica (AEP)]] discreta.

Sia $X_1, X_2, \dots, X_n$ una sequenza di variabili aleatorie continue i.i.d. distribuite secondo la densità $f(x)$. La densità congiunta della sequenza vettoriale $\mathbf{X} = (X_1, \dots, X_n)^T$ fattorizza nel prodotto delle marginali:

$$
f(x_1, x_2, \dots, x_n) = \prod_{i=1}^n f(x_i)
$$

### Teorema AEP Continuo

Sia $X_1, X_2, \dots, X_n$ una successione di variabili aleatorie i.i.d. aventi densità $f(x)$. Allora:

$$
-\frac{1}{n}\log_2 f(X_1, X_2, \dots, X_n) \xrightarrow{P} \mathbb{E}[-\log_2 f(X)] = h(X) \quad \text{in probabilità}
$$

__Dimostrazione__:
La variabile casuale $Y_i = -\log_2 f(X_i)$ è una funzione di $X_i$. Poiché le $X_i$ sono i.i.d., anche le $Y_i$ costituiscono una successione di variabili aleatorie scalari i.i.d., con valore atteso:

$$
\mathbb{E}[Y_i] = \mathbb{E}[-\log_2 f(X_i)] = h(X)
$$

Applicando direttamente la Legge Debole dei Grandi Numeri (WLLN) alla media campionaria $\frac{1}{n}\sum_{i=1}^n Y_i$:

$$
-\frac{1}{n}\log_2 f(X_1, \dots, X_n) = -\frac{1}{n}\sum_{i=1}^n \log_2 f(X_i) \xrightarrow{P} h(X)
$$

per ogni $\epsilon > 0$, la probabilità che la media campionaria si discosti da $h(X)$ di più di $\epsilon$ tende a zero al divergere di $n$.

### Definizione Geometrica dell'Insieme Tipico Continuo

Fissato un parametro $\epsilon > 0$ e una dimensione $n$, l'__insieme tipico continuo__ $A_\epsilon^{(n)}$ rispetto alla densità $f(x)$ è definito come:

$$
A_\epsilon^{(n)} = \left\{ (x_1, \dots, x_n) \in \mathcal{S}^n : \left| -\frac{1}{n}\log_2 f(x_1, \dots, x_n) - h(X) \right| \le \epsilon \right\}
$$

dove la densità congiunta di ciascuna sequenza appartenente all'insieme soddisfa la delimitazione esponenziale uniforme:

$$
2^{-n(h(X) + \epsilon)} \le f(x_1, \dots, x_n) \le 2^{-n(h(X) - \epsilon)}
$$

Nel dominio continuo, la nozione discreta di cardinalità $|A_\epsilon^{(n)}|$ è formalmente sostituita dalla misura euclidea di __volume__ $n$-dimensionale, calcolato tramite l'integrale multiplo di Lebesgue:

$$
\text{Vol}(A_\epsilon^{(n)}) = \int_{A_\epsilon^{(n)}} \mathrm{d}x_1 \mathrm{d}x_2 \dots \mathrm{d}x_n
$$

![[slide_07_typical_set_continuous_volume.png|center mid]]

### Le Proprietà Cardinali dell'Insieme Tipico Continuo

L'insieme tipico continuo gode di tre proprietà fondamentali:
1. $\text{Pr}\{A_\epsilon^{(n)}\} > 1 - \epsilon$ per $n$ sufficientemente grande.
2. $\text{Vol}(A_\epsilon^{(n)}) \le 2^{n(h(X) + \epsilon)}$ per ogni $n$.
3. $\text{Vol}(A_\epsilon^{(n)}) \ge (1 - \epsilon) 2^{n(h(X) - \epsilon)}$ per $n$ sufficientemente grande.

__Dimostrazione analitica__:
- La Proprietà 1 discende direttamente dalla convergenza in probabilità garantita dalla Legge dei Grandi Numeri:

$$
  \lim_{n \to \infty} \text{Pr}\left\{ \left| -\frac{1}{n}\log_2 f(X^n) - h(X) \right| \le \epsilon \right\} = 1 \implies \text{Pr}\{A_\epsilon^{(n)}\} > 1 - \epsilon
$$

- Per la Proprietà 2, integrando la densità di probabilità totale sull'intero spazio campionario:

$$
  1 = \int_{\mathcal{S}^n} f(\mathbf{x}) \mathrm{d}\mathbf{x} \ge \int_{A_\epsilon^{(n)}} f(\mathbf{x}) \mathrm{d}\mathbf{x} \ge \int_{A_\epsilon^{(n)}} 2^{-n(h(X) + \epsilon)} \mathrm{d}\mathbf{x} = 2^{-n(h(X) + \epsilon)} \text{Vol}(A_\epsilon^{(n)})
$$

  Moltiplicando ambo i membri per $2^{n(h(X) + \epsilon)}$ si ottiene:

$$
  \text{Vol}(A_\epsilon^{(n)}) \le 2^{n(h(X) + \epsilon)}
$$

- Per la Proprietà 3, per $n$ sufficientemente grande tale che $\text{Pr}\{A_\epsilon^{(n)}\} \ge 1 - \epsilon$:

$$
  1 - \epsilon \le \text{Pr}\{A_\epsilon^{(n)}\} = \int_{A_\epsilon^{(n)}} f(\mathbf{x}) \mathrm{d}\mathbf{x} \le \int_{A_\epsilon^{(n)}} 2^{-n(h(X) - \epsilon)} \mathrm{d}\mathbf{x} = 2^{-n(h(X) - \epsilon)} \text{Vol}(A_\epsilon^{(n)})
$$

  da cui:

$$
  \text{Vol}(A_\epsilon^{(n)}) \ge (1 - \epsilon) 2^{n(h(X) - \epsilon)}
$$

Combinando i limiti, per $n$ sufficientemente elevato vale la doppia disuguaglianza:

$$
(1 - \epsilon) 2^{n(h(X) - \epsilon)} \le \text{Vol}(A_\epsilon^{(n)}) \le 2^{n(h(X) + \epsilon)}
$$

### Teorema del Volume Minimo e Lunghezza Equivalente

In analogia con il teorema di minima cardinalità per sorgenti discrete, l'insieme tipico continuo $A_\epsilon^{(n)}$ rappresenta l'insieme di __volume minimo__ in grado di racchiudere quasi la totalità della probabilità (probabilità $\ge 1 - \epsilon$), al primo ordine dell'esponente.

Essendo il volume di tale regione approssimativamente pari a $2^{n h(X)}$, la lunghezza del lato di un ipercubo $n$-dimensionale avente lo stesso volume effettivo vale:

$$
L_{\text{lato}} = \left( \text{Vol}(A_\epsilon^{(n)}) \right)^{1/n} \approx \left( 2^{n h(X)} \right)^{1/n} = 2^{h(X)}
$$

Questa relazione fornisce il significato fisico profondo dell'entropia differenziale:
- $h(X)$ è il logaritmo della lunghezza del lato equivalente dell'insieme di volume minimo che concentra la quasi totalità della misura di probabilità.
- __Bassa entropia differenziale__: La variabile casuale è concentrata in un volume spaziale effettivo minuscolo (alta densità locale).
- __Alta entropia differenziale__: La variabile casuale è ampiamente dispersa su regioni voluminose dello spazio campionario.

## Relazione Rigorosa tra Entropia Differenziale ed Entropia Discreta: La Quantizzazione

Per comprendere il legame quantitativo tra l'entropia differenziale $h(X)$ di un segnale analogico e l'entropia discreta $H$ derivante dalla sua conversione analogico-digitale (ADC), si analizza il processo di __quantizzazione uniforme__.

Sia $X$ una variabile aleatoria continua avente densità di probabilità $f(x)$. Si suddivida l'asse reale in intervalli disgiunti (bin o quanti) di ampiezza uniforme pari a $\Delta > 0$:

$$
I_i = [i\Delta, (i+1)\Delta), \quad i \in \mathbb{Z}
$$

![[slide_13_quantized_continuous_rv.png|center mid]]

Assumendo che la densità $f(x)$ sia continua all'interno di ciascun intervallo, per il Teorema della Media Integrale esiste almeno un punto interno $x_i \in I_i$ tale che l'integrale della densità su $I_i$ sia pari all'area del rettangolo di base $\Delta$ e altezza $f(x_i)$:

$$
p_i = \text{Pr}\{X \in I_i\} = \int_{i\Delta}^{(i+1)\Delta} f(x) \mathrm{d}x = f(x_i)\Delta
$$

Si definisce la variabile aleatoria quantizzata $X^\Delta$ come la variabile discreta che associa a ciascun intervallo $I_i$ il valore rappresentativo $x_i$:

$$
X^\Delta = x_i \quad \text{se } X \in I_i
$$

La distribuzione di probabilità discreta di $X^\Delta$ è data dall'insieme di masse $\{p_i\}_{i=-\infty}^{+\infty}$. Calcoliamo l'entropia discreta di Shannon della variabile quantizzata:

$$
H(X^\Delta) = -\sum_{i=-\infty}^{+\infty} p_i \log_2 p_i = -\sum_{i=-\infty}^{+\infty} f(x_i)\Delta \log_2 \left( f(x_i)\Delta \right)
$$

Sviluppando il logaritmo del prodotto $\log_2(f(x_i)\Delta) = \log_2 f(x_i) + \log_2 \Delta$:

$$
H(X^\Delta) = -\sum_{i=-\infty}^{+\infty} f(x_i)\Delta \log_2 f(x_i) - \sum_{i=-\infty}^{+\infty} f(x_i)\Delta \log_2 \Delta
$$

Raccogliendo il fattore costante $\log_2 \Delta$ al di fuori della seconda sommatoria e osservando che per conservazione della probabilità totale $\sum_{i} f(x_i)\Delta = \sum_i p_i = 1$:

$$
H(X^\Delta) = -\sum_{i=-\infty}^{+\infty} \Delta f(x_i) \log_2 f(x_i) - \log_2 \Delta
$$

### Teorema del Limite di Quantizzazione

Se la funzione $f(x)\log_2 f(x)$ è integrabile secondo Riemann sull'asse reale, la sommatoria a primo membro costituisce la somma di Riemann che converge all'integrale di Lebesgue all'infittirsi della griglia di quantizzazione ($\Delta \to 0$):

$$
\lim_{\Delta \to 0} \left( -\sum_{i=-\infty}^{+\infty} \Delta f(x_i) \log_2 f(x_i) \right) = -\int_{-\infty}^{+\infty} f(x) \log_2 f(x) \mathrm{d}x = h(X)
$$

Ne discende il fondamentale __Teorema del Limite di Quantizzazione__:

$$
\lim_{\Delta \to 0} \left[ H(X^\Delta) + \log_2 \Delta \right] = h(X)
$$

### Interpretazione Operativa a Risoluzione di $n$ Bit

Se si adotta una quantizzazione binaria a passo uniforme con risoluzione pari a $n$ bit frazionari, il passo di campionamento vale:

$$
\Delta = 2^{-n} \implies \log_2 \Delta = -n
$$

Sostituendo tale risoluzione nell'equazione di quantizzazione:

$$
H(X^\Delta) \approx h(X) - \log_2(2^{-n}) = h(X) + n \quad \text{bit}
$$

Tale formula riveste un ruolo operativo basilare nei sistemi di elaborazione numerica dei segnali:
1. $h(X) + n$ rappresenta il __numero medio di bit di informazione__ necessari per descrivere la variabile continua $X$ con un'accuratezza o risoluzione pari a $n$ bit.
2. Per incrementare l'accuratezza della misura continua di 1 bit (dimezzando il passo di quantizzazione $\Delta$), l'entropia della sequenza binaria risultante deve aumentare esattamente di 1 bit.
3. L'entropia differenziale $h(X)$ funge da termine di calibrazione (offset costante) indipendente dalla risoluzione $n$: distribuzioni con entropia differenziale più bassa richiedono meno bit complessivi a parità di risoluzione imposta.

### Esempi Numerici di Quantizzazione

- __Variabile Uniforme su $[0, 1]$__:
  Per $X \sim \mathcal{U}[0, 1]$, si è ricavato $h(X) = \log_2 1 = 0$ bit. Quantizzando con risoluzione $n$ bit ($\Delta = 2^{-n}$):

$$
  H(X^\Delta) \approx h(X) + n = 0 + n = n \quad \text{bit}
$$

  Il risultato coincide esattamente con l'entropia di una variabile discreta uniforme su $2^n$ livelli ($H = \log_2(2^n) = n$).

- __Variabile Uniforme ristretta su $[0, 1/8]$__:
  In questo intervallo $h(X) = \log_2(1/8) = -3$ bit. Applicando la quantizzazione a $n$ bit:

$$
  H(X^\Delta) \approx n - 3 \quad \text{bit}
$$

  Il risparmio di 3 bit riflette la certezza deterministica che i primi 3 bit più significativi dopo la virgola ($2^{-1}, 2^{-2}, 2^{-3}$) sono costantemente nulli, dovendo codificare soltanto la porzione residua dell'informazione.

- __Variabile Gaussiana con Dispersione Elevata__:
  Sia $X \sim \mathcal{N}(0, 100)$, avente deviazione standard $\sigma = 10$. La sua entropia differenziale è:

$$
  h(X) = \frac{1}{2}\log_2(2\pi e \cdot 100) = \frac{1}{2}\log_2(1707.95) \approx 5.37 \quad \text{bit}
$$

  La quantizzazione con accuratezza $n$ bit produce un'entropia discreta pari a $H(X^\Delta) \approx n + 5.37$ bit.

- __Collasso per Variabili Discrete__:
  Se si tenta di applicare la formula a una variabile puramente discreta, la sua entropia discreta $H(X^\Delta)$ satura a un valore finito $H(X)$ per passi $\Delta$ sufficientemente piccoli da isolare ciascun punto atomico. In tale circostanza:

$$
  h(X) = \lim_{\Delta \to 0} [H(X) + \log_2 \Delta] = H(X) + (-\infty) = -\infty
$$

  con volume di supporto nullo $\text{Vol}(\mathcal{S}) = 2^{-\infty} = 0$, a testimonianza del fatto che un insieme discreto occupa misura di Lebesgue nulla nel continuo.

## Entropia Differenziale Congiunta, Condizionata e Regola della Catena

Estendendo il modello a vettori aleatori composti da più variabili continue, si definiscono gli analoghi multidimensionali delle quantità informative.

Siano $X_1, X_2, \dots, X_n$ variabili aleatorie continue caratterizzate dalla densità congiunta $f(x_1, x_2, \dots, x_n) = f(\mathbf{x})$. L'__entropia differenziale congiunta__ è definita da:

$$
h(X_1, X_2, \dots, X_n) = -\int_{\mathbb{R}^n} f(\mathbf{x}) \log_2 f(\mathbf{x}) \mathrm{d}\mathbf{x}
$$

Date due variabili congiunte $X$ e $Y$ con densità $f(x, y)$, l'__entropia differenziale condizionata__ $h(X \mid Y)$ quantifica l'incertezza residua su $X$ una volta nota la determinazione di $Y$:

$$
h(X \mid Y) = -\int_{-\infty}^{+\infty} \int_{-\infty}^{+\infty} f(x, y) \log_2 f(x \mid y) \mathrm{d}x \mathrm{d}y
$$

Poiché per definizione di densità condizionata vale $f(x \mid y) = \frac{f(x, y)}{f(y)}$, sviluppando il logaritmo del quoziente:

$$
h(X \mid Y) = -\int f(x, y) \log_2 f(x, y) \mathrm{d}x\mathrm{d}y + \int f(x, y) \log_2 f(y) \mathrm{d}x\mathrm{d}y = h(X, Y) - h(Y)
$$

### Regola della Catena per l'Entropia Differenziale

Iterando la scomposizione per un vettore continuo $n$-dimensionale, si ottiene la __regola della catena__:

$$
h(X_1, X_2, \dots, X_n) = \sum_{i=1}^n h(X_i \mid X_1, \dots, X_{i-1})
$$

Come nel discreto, l'introduzione di condizionamento non può mai incrementare l'entropia differenziale media:

$$
h(X \mid Y) \le h(X)
$$

con eguaglianza stretta se e solo se $X$ e $Y$ sono statisticamente indipendenti. Di conseguenza, combinando la regola della catena con la proprietà di riduzione dell'entropia per condizionamento, si perviene al __limite di indipendenza__:

$$
h(X_1, X_2, \dots, X_n) \le \sum_{i=1}^n h(X_i)
$$

con eguaglianza se e solo se le coordinate $X_1, \dots, X_n$ sono mutuamente indipendenti.

## Divergenza di Kullback-Leibler e Informazione Mutua Continua

La __divergenza di Kullback-Leibler__ (o entropia relativa) tra due densità di probabilità continue $f(x)$ e $g(x)$ definite sul medesimo supporto è espressa dall'integrale:

$$
D(f \parallel g) = \int_{\mathcal{S}_f} f(x) \log_2 \frac{f(x)}{g(x)} \mathrm{d}x
$$

La divergenza KL è finita unicamente se il supporto di $f(x)$ è contenuto nel supporto di $g(x)$ (ossia $g(x) > 0$ ovunque $f(x) > 0$). Per convenzione di continuità, nei punti in cui $f(x) = 0$ si pone $0 \log_2(0 / g(x)) = 0$.

### Teorema della Disuguaglianza dell'Informazione nel Continuo

Per qualsiasi coppia di funzioni di densità di probabilità $f(x)$ e $g(x)$:

$$
D(f \parallel g) \ge 0
$$

con eguaglianza stretta se e solo se $f(x) = g(x)$ quasi ovunque rispetto alla misura di Lebesgue.

__Dimostrazione__:
Applicando la disuguaglianza di Jensen alla funzione logaritmo concava $-\log_2(\cdot)$:

$$
-D(f \parallel g) = \int_{\mathcal{S}_f} f(x) \log_2 \frac{g(x)}{f(x)} \mathrm{d}x = \mathbb{E}_f\left[ \log_2 \frac{g(X)}{f(X)} \right] \le \log_2 \left( \mathbb{E}_f\left[ \frac{g(X)}{f(X)} \right] \right)
$$

Valutando il valore atteso all'interno del logaritmo:

$$
\mathbb{E}_f\left[ \frac{g(X)}{f(X)} \right] = \int_{\mathcal{S}_f} f(x) \frac{g(x)}{f(x)} \mathrm{d}x = \int_{\mathcal{S}_f} g(x) \mathrm{d}x \le \int_{\mathbb{R}} g(x) \mathrm{d}x = 1
$$

Pertanto:

$$
-D(f \parallel g) \le \log_2(1) = 0 \implies D(f \parallel g) \ge 0
$$

Poiché il logaritmo è strettamente concavo, l'eguaglianza nella disuguaglianza di Jensen impone che il rapporto $\frac{g(x)}{f(x)}$ sia costante quasi ovunque, e dovendo entrambi gli integrali normalizzare ad 1, tale costante deve essere identicamente pari ad 1 ($f(x) = g(x)$ quasi ovunque).

### Informazione Mutua Continua

L'__informazione mutua__ $I(X; Y)$ tra due variabili aleatorie continue congiuntamente distribuite secondo $f(x, y)$ è definita come la divergenza di Kullback-Leibler tra la densità congiunta e il prodotto delle densità marginali:

$$
I(X; Y) = D(f(x, y) \parallel f(x)f(y)) = \int_{-\infty}^{+\infty} \int_{-\infty}^{+\infty} f(x, y) \log_2 \frac{f(x, y)}{f(x)f(y)} \mathrm{d}x \mathrm{d}y
$$

Scomponendo il logaritmo del rapporto, l'informazione mutua si esprime tramite le entropie differenziali:

$$
I(X; Y) = h(X) - h(X \mid Y) = h(Y) - h(Y \mid X) = h(X) + h(Y) - h(X, Y)
$$

A differenza dell'entropia differenziale $h(X)$, che può risultare negativa, l'informazione mutua continua gode della proprietà cardinale di essere __strettamente non negativa__:

$$
I(X; Y) \ge 0
$$

con $I(X; Y) = 0$ se e solo se $X$ e $Y$ sono statisticamente indipendenti ($f(x, y) = f(x)f(y)$ quasi ovunque).

### Invarianza di Scala e Definizione Universale per Partizioni Finite

Un aspetto cruciale dell'informazione mutua nel continuo risiede nella sua invarianza rispetto alla quantizzazione uniforme. Considerando le versioni discretizzate $X^\Delta$ e $Y^\Delta$ con passo $\Delta$:

$$
I(X^\Delta; Y^\Delta) = H(X^\Delta) - H(X^\Delta \mid Y^\Delta) \approx [h(X) - \log_2 \Delta] - [h(X \mid Y) - \log_2 \Delta] = h(X) - h(X \mid Y) = I(X; Y)
$$

I termini di divergenza infinitesima $-\log_2 \Delta$ si elidono perfettamente per cancellazione algebrica. Di conseguenza:

$$
\lim_{\Delta \to 0} I(X^\Delta; Y^\Delta) = I(X; Y)
$$

Ciò consente di formulare la definizione fondamentale e rigorosa dell'informazione mutua dovuta a Kolmogorov e Gelfand-Yaglom, valida per qualunque spazio probabilistico (anche in presenza di singolarità o masse discrete):

$$
I(X; Y) = \sup_{\mathcal{P}, \mathcal{Q}} I([X]_\mathcal{P}; [Y]_\mathcal{Q})
$$

dove l'estremo superiore (supremum) è valutato su tutte le possibili partizioni finite $\mathcal{P} = \{P_i\}$ e $\mathcal{Q} = \{Q_j\}$ dei rispettivi spazi campionari. La successione delle informazioni mutue discretizzate converge monotonicamente da sinistra al valore continuo $I(X; Y)$.

### Esempio Analitico: Informazione Mutua tra Variabili Gaussiane Correlate

Si consideri un vettore gaussiano bivariato $(X, Y)^T \sim \mathcal{N}_2(\mathbf{0}, \mathbf{K})$ a media nulla con matrice di covarianza:

$$
\mathbf{K} = \begin{bmatrix} \sigma^2 & \rho\sigma^2 \\ \rho\sigma^2 & \sigma^2 \end{bmatrix}
$$

dove $\rho \in (-1, 1)$ rappresenta il coefficiente di correlazione lineare di Pearson.

Il determinante della matrice di covarianza vale:

$$
\det \mathbf{K} = \sigma^2 \cdot \sigma^2 - (\rho\sigma^2)^2 = \sigma^4(1 - \rho^2)
$$

Le entropie differenziali marginali sono date da:

$$
h(X) = h(Y) = \frac{1}{2}\log_2(2\pi e \sigma^2)
$$

L'entropia differenziale congiunta bivariata è:

$$
h(X, Y) = \frac{1}{2}\log_2\left( (2\pi e)^2 \det \mathbf{K} \right) = \frac{1}{2}\log_2\left( (2\pi e)^2 \sigma^4(1 - \rho^2) \right)
$$

Calcoliamo l'informazione mutua sommando le marginali e sottraendo la congiunta:

$$
I(X; Y) = h(X) + h(Y) - h(X, Y) = \frac{1}{2}\log_2(2\pi e \sigma^2) + \frac{1}{2}\log_2(2\pi e \sigma^2) - \frac{1}{2}\log_2\left( (2\pi e)^2 \sigma^4 (1 - \rho^2) \right)
$$

Raggruppando i logaritmi:

$$
I(X; Y) = \frac{1}{2}\log_2\left( \frac{(2\pi e \sigma^2)^2}{(2\pi e)^2 \sigma^4 (1 - \rho^2)} \right) = \frac{1}{2}\log_2\left( \frac{1}{1 - \rho^2} \right) = -\frac{1}{2}\log_2(1 - \rho^2) \quad \text{bit}
$$

Dall'espressione analitica emergono proprietà determinanti:
1. __Invarianza dalla varianza__: L'informazione mutua dipende esclusivamente dal parametro adimensionale di accoppiamento $\rho$ e non dalla varianza marginale $\sigma^2$ (invarianza per amplificazione lineare dei segnali).
2. __Indipendenza stocastica__: Se $\rho = 0$, $I(X; Y) = -\frac{1}{2}\log_2(1) = 0$ bit. Variabili incorrelate congiuntamente gaussiane sono indipendenti e condividono informazione nulla.
3. __Dipendenza deterministica al limite__: Quando $|\rho| \to 1$ (perfetta correlazione o anticorrelazione lineare), l'argomento del logaritmo diverge:

$$
   \lim_{|\rho| \to 1} I(X; Y) = \lim_{|\rho| \to 1} \left( -\frac{1}{2}\log_2(1 - \rho^2) \right) = +\infty
$$

   La conoscenza esatta di una variabile rimuove un'incertezza infinitamente densa sull'altra variabile continua.

## Comportamento dell'Entropia Differenziale sotto Trasformazioni Affini

Un'operazione standard nell'elaborazione dei segnali consiste nell'applicazione di trasformazioni lineari o affini ai vettori campionati.

### Teorema della Trasformazione Scalare

Sia $X$ una variabile aleatoria continua con densità $f_X(x)$ ed entropia differenziale $h(X)$. Sia $Y = aX + b$ con costanti $a, b \in \mathbb{R}$ e $a \neq 0$. Allora:

$$
h(aX + b) = h(X) + \log_2 |a|
$$

__Dimostrazione__:
La trasformazione $y = ax + b$ è biunivoca con inversa $x = \frac{y - b}{a}$ e derivata $\frac{\mathrm{d}x}{\mathrm{d}y} = \frac{1}{a}$. La densità di probabilità della variabile trasformata $Y$ è:

$$
f_Y(y) = \frac{1}{|a|} f_X\left( \frac{y - b}{a} \right)
$$

Calcoliamo l'entropia differenziale di $Y$:

$$
h(Y) = -\int_{-\infty}^{+\infty} f_Y(y) \log_2 f_Y(y) \mathrm{d}y = -\int_{-\infty}^{+\infty} \frac{1}{|a|} f_X\left( \frac{y - b}{a} \right) \log_2 \left[ \frac{1}{|a|} f_X\left( \frac{y - b}{a} \right) \right] \mathrm{d}y
$$

Operando il cambio di variabile nell'integrale $x = \frac{y - b}{a}$, da cui $\mathrm{d}y = |a|\mathrm{d}x$:

$$
h(Y) = -\int_{-\infty}^{+\infty} \frac{1}{|a|} f_X(x) \left[ \log_2 f_X(x) - \log_2 |a| \right] |a|\mathrm{d}x
$$

Semplificando il fattore $|a|$ ed espandendo la differenza di integrali:

$$
h(Y) = -\int_{-\infty}^{+\infty} f_X(x) \log_2 f_X(x) \mathrm{d}x + \log_2 |a| \int_{-\infty}^{+\infty} f_X(x) \mathrm{d}x = h(X) + \log_2 |a|
$$

Due corollari immediati ne derivano:
1. __Invarianza per traslazione__: Ponendo $a = 1$, per qualunque costante $c$:

$$
   h(X + c) = h(X)
$$

   Spostare rigidamente una distribuzione sull'asse reale non altera la conformazione della densità né il volume del supporto effettivo.
2. __Amplificazione del segnale__: Se $a = 2$, $h(2X) = h(X) + 1$ bit. Raddoppiare l'ampiezza di una grandezza fisica incrementa l'entropia differenziale esattamente di 1 bit, raddoppiando l'estensione del supporto.

### Teorema della Trasformazione Lineare Multivariata

Sia $\mathbf{X} \in \mathbb{R}^n$ un vettore aleatorio continuo con entropia differenziale $h(\mathbf{X})$ e sia $\mathbf{A} \in \mathbb{R}^{n \times n}$ una matrice quadrata deterministica invertibile a rango pieno ($\det \mathbf{A} \neq 0$). Sia $\mathbf{b} \in \mathbb{R}^n$ un vettore costante. Per il vettore trasformato $\mathbf{Y} = \mathbf{A}\mathbf{X} + \mathbf{b}$:

$$
h(\mathbf{A}\mathbf{X} + \mathbf{b}) = h(\mathbf{X}) + \log_2 |\det \mathbf{A}|
$$

__Interpretazione geometrica__:
Il determinante della matrice di trasformazione $\det \mathbf{A}$ rappresenta il fattore jacobiano di dilatazione o contrazione del volume nello spazio euclideo $n$-dimensionale:

$$
\mathrm{d}\mathbf{y} = |\det \mathbf{A}| \mathrm{d}\mathbf{x}
$$

Poiché l'entropia differenziale misura il logaritmo del volume equivalente della distribuzione, la moltiplicazione per $\mathbf{A}$ espande il volume del supporto di un fattore $|\det \mathbf{A}|$, traducendosi nell'incremento additivo esatto $\log_2 |\det \mathbf{A}|$. Nel caso speciale di matrici ortogonali (rotazioni spaziali, con $\mathbf{A}^T\mathbf{A} = \mathbf{I} \implies |\det \mathbf{A}| = 1$), l'entropia differenziale è rigorosamente invariante:

$$
h(\mathbf{Q}\mathbf{X}) = h(\mathbf{X}), \quad \forall \mathbf{Q} \text{ ortogonale}
$$

## Entropia della Gaussiana Multivariata e Teorema di Massima Entropia

Sia $\mathbf{X} = (X_1, X_2, \dots, X_n)^T \in \mathbb{R}^n$ un vettore aleatorio gaussiano multivariato avente vettore delle medie $\boldsymbol{\mu} = \mathbb{E}[\mathbf{X}]$ e matrice di covarianza definita positiva:

$$
\mathbf{K} = \mathbb{E}[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^T] > 0
$$

La funzione di densità di probabilità congiunta è data da:

$$
\phi_{\mathbf{K}}(\mathbf{x}) = \frac{1}{(2\pi)^{n/2} (\det \mathbf{K})^{1/2}} \exp\left( -\frac{1}{2} (\mathbf{x} - \boldsymbol{\mu})^T \mathbf{K}^{-1} (\mathbf{x} - \boldsymbol{\mu}) \right)
$$

### Entropia Differenziale Multivariata

L'entropia differenziale del vettore gaussiano multivariato $\mathbf{X} \sim \mathcal{N}_n(\boldsymbol{\mu}, \mathbf{K})$ espressa in bit è:

$$
h(\mathbf{X}) = \frac{1}{2}\log_2 \left( (2\pi e)^n \det \mathbf{K} \right) \quad \text{bit}
$$

### Teorema di Massima Entropia Differenziale

Il Teorema di Massima Entropia Differenziale (Cover & Thomas, Teorema 8.6.5) stabilisce che tra tutte le distribuzioni di probabilità continue multidimensionali definite su $\mathbb{R}^n$ aventi la medesima matrice di covarianza $\mathbf{K}$, la distribuzione Normale multivariata massimizza univocamente l'entropia differenziale:

$$
h(\mathbf{X}) \le \frac{1}{2}\log_2 \left( (2\pi e)^n \det \mathbf{K} \right)
$$

con eguaglianza se e solo se $\mathbf{X} \sim \mathcal{N}_n(\boldsymbol{\mu}, \mathbf{K})$.

La dimostrazione analitica rigorosa, basata sulla disuguaglianza di Kullback-Leibler $D(g \parallel \phi_{\mathbf{K}}) \ge 0$ e sulle proprietà della traccia di forme quadratiche $\mathbb{E}_g[\mathbf{X}^T \mathbf{K}^{-1} \mathbf{X}] = \text{Tr}(\mathbf{K}^{-1}\mathbf{K}) = n$, è esposta integralmente in [[zz. Argomenti extra#Dimostrazione Variazionale dell'Ottimalità della PDF Gaussiana come Massimizzatore di Entropia Differenziale]].

### Significato Teorico ed Ingegneristico

Il principio di massima entropia conferisce alla distribuzione gaussiana un ruolo basilare nella teoria dell'informazione:
1. __Rappresentazione del Caso Peggiore (Worst-Case Uncertainty)__: Fissata la potenza o l'energia dei segnali (il vincolo del secondo ordine imposto da $\mathbf{K}$), la distribuzione normale rappresenta la sorgente di massima incertezza e massimo disordine possibile.
2. __Ottimalità nei Canali di Trasmissione__: Nei canali affetti da rumore, il segnale di rumore più distruttivo a parità di varianza è quello gaussiano, poiché possiede la massima entropia differenziale e degrada massimamente la capacità informativa.
3. __Compressione Dati e Modellazione__: Qualsiasi distribuzione non gaussiana possiede un'entropia differenziale strettamente inferiore a quella della gaussiana equivalente ($h(g) < h(\phi)$). Questo scarto quantifica la presenza di strutture, correlazioni o code non gaussiane che possono essere sfruttate da algoritmi di compressione lossy e modelli predittivi.

## Dimostrazione Informatica della Disuguaglianza di Hadamard

La celebre Disuguaglianza di Hadamard (1893) dell'algebra lineare, la quale stabilisce che il determinante di una matrice simmetrica definita positiva $\mathbf{K} \in \mathbb{R}^{n \times n}$ è superiormente limitato dal prodotto degli elementi diagonali:

$$
\det \mathbf{K} \le \prod_{i=1}^n K_{ii}
$$

ammette una dimostrazione immediata e geometrica sfruttando le proprietà dell'entropia differenziale di un vettore gaussiano $\mathbf{X} \sim \mathcal{N}_n(\mathbf{0}, \mathbf{K})$.

Sfruttando la regola della catena e la proprietà che il condizionamento riduce l'entropia:

$$
h(X_1, \dots, X_n) \le \sum_{i=1}^n h(X_i)
$$

Poiché $h(\mathbf{X}) = \frac{1}{2}\log_2((2\pi e)^n \det \mathbf{K})$ e ciascuna marginale gaussiana scalare ha entropia $h(X_i) = \frac{1}{2}\log_2(2\pi e K_{ii})$, eguagliando gli esponenti si ottiene istantaneamente la disuguaglianza con condizione di eguaglianza valida se e solo se le variabili sono mutuamente indipendenti ($K_{ij} = 0$ per ogni $i \neq j$, ovvero matrice $\mathbf{K}$ puramente diagonale). La derivazione completa è disponibile in [[zz. Argomenti extra#Dimostrazione Informatica della Disuguaglianza di Hadamard]].

## Errore di Stima, Disuguaglianza di Fano Continua e Limite CRLB

Un risultato di profonda sintesi tra la teoria dell'informazione e la teoria della stima (trattata nella Parte I) è la relazione che lega l'entropia differenziale all'errore quadratico medio minimo (MSE) conseguibile nella stima o predizione di una variabile aleatoria continua.

### Teorema del Limite Inferiore sull'Errore di Stima (Fano Continuo)

Sia $X$ una variabile aleatoria continua con densità $f(x)$ ed entropia differenziale $h(X)$. Per qualunque stimatore scalare costante $\hat{X}$ di $X$:

$$
\mathbb{E}[(X - \hat{X})^2] \ge \frac{1}{2\pi e} 2^{2 h(X)}
$$

con eguaglianza se e solo se $X$ è distribuita gaussianamente ($X \sim \mathcal{N}$) e lo stimatore coincide con il valore atteso $\hat{X} = \mathbb{E}[X]$.

__Dimostrazione__:
L'errore quadratico medio per una stima costante è minimizzato scegliendo la media della distribuzione:

$$
\min_{\hat{X}} \mathbb{E}[(X - \hat{X})^2] = \mathbb{E}[(X - \mathbb{E}[X])^2] = \text{Var}(X) = \sigma_X^2
$$

Per il Teorema di Massima Entropia Differenziale a varianza fissata $\sigma_X^2$, l'entropia differenziale di $X$ soddisfa il bound:

$$
h(X) \le \frac{1}{2}\log_2(2\pi e \sigma_X^2)
$$

Applicando la funzione esponenziale in base 2 ad ambo i membri:

$$
2^{2 h(X)} \le 2\pi e \sigma_X^2 \implies \sigma_X^2 \ge \frac{1}{2\pi e} 2^{2 h(X)}
$$

Combinando le disuguaglianze:

$$
\mathbb{E}[(X - \hat{X})^2] \ge \text{Var}(X) \ge \frac{1}{2\pi e} 2^{2 h(X)}
$$

L'uguaglianza è raggiunta se e solo se lo stimatore è ottimo in senso MSE ($\hat{X} = \mathbb{E}[X]$) e la variabile aleatoria $X$ raggiunge il massimo dell'entropia differenziale a varianza data, ossia è una variabile gaussiana.

### Corollario con Informazione Collaterale (Side Information)

Se il ricevitore dispone di una variabile aleatoria osservabile $Y$ (informazione collaterale) e implementa uno stimatore $\hat{X}(Y)$, la disuguaglianza si estende all'entropia differenziale condizionata:

$$
\mathbb{E}[(X - \hat{X}(Y))^2] \ge \frac{1}{2\pi e} 2^{2 h(X \mid Y)}
$$

Il limite inferiore è raggiunto con uguaglianza se e solo se la coppia $(X, Y)$ è congiuntamente gaussiana e lo stimatore è il Minimum Mean Square Error (MMSE) bayesiano $\hat{X}_{\text{MMSE}}(Y) = \mathbb{E}[X \mid Y]$, confermando l'assoluta convergenza teorica con i risultati del capitolo [[2. Stima Bayesiana - MMSE e LMMSE]].

### Concetto di Entropy Power e Connessione con il Limite di Cramér-Rao

La grandezza:

$$
N(X) = \frac{1}{2\pi e} 2^{2 h(X)}
$$

è denominata __potenza di entropia__ (Entropy Power) di Shannon. Essa rappresenta la potenza (varianza) di una variabile casuale gaussiana equivalente che possiede la medesima entropia differenziale di $X$.

Nella stima classica non polarizzata di un parametro di posizione $\theta$ con osservazioni $X = \theta + W$ (come analizzato in [[0. Fondamenti di Stima Classica e Limite di Cramer-Rao]]), la potenza di entropia è legata all'Informazione di Fisher $J(X)$ dalla celebre __Disuguaglianza Isoperimetrica di Fisher-Shannon__ (Stam 1959, Dembo-Cover-Thomas 1991):

$$
J(X) \cdot N(X) \ge 1 \iff \frac{1}{J(X)} \le N(X) = \frac{1}{2\pi e} 2^{2 h(X)}
$$

Poiché per il Teorema di Massima Entropia vale $N(X) \le \text{Var}(X)$, mentre per il limite di Cramér-Rao la varianza di qualsiasi stimatore non polarizzato soddisfa $\text{Var}(\hat{\theta}) \ge \frac{1}{J(X)}$, considerando lo stimatore naturale $\hat{\theta} = X$ si ottiene la catena fondamentale:

$$
\text{Var}(X) \ge \frac{1}{2\pi e} 2^{2 h(X)} \ge \frac{1}{J(X)}
$$

con uguaglianze simultanee se e solo se $X$ è distribuita gaussianamente. Tale disequazione salda in un unico principio geometrico la teoria dell'informazione, la disuguaglianza isoperimetrica e il limite di Cramér-Rao.

## Il Canale Additivo Gaussiano (AWGN) e il Teorema di Shannon-Hartley

L'applicazione ingegneristica più celebre e fondamentale dell'entropia differenziale è l'analisi della capacità di trasmissione di un canale analogico perturbato da rumore additivo bianco gaussiano (AWGN), introdotta da Shannon nel suo lavoro pionieristico del 1948.

### Canale Gaussiano a Tempo Discreto

Si consideri inizialmente il modello di canale discreto nel tempo:

$$
Y_i = X_i + Z_i, \quad i = 1, 2, \dots
$$

dove:
- $X_i$ è il simbolo trasmesso all'istante $i$, soggetto a un vincolo di potenza media per simbolo pari a $\mathbb{E}[X_i^2] \le P$.
- $Z_i \sim \mathcal{N}(0, N)$ è un rumore additivo gaussiano i.i.d., indipendente da $X_i$, con potenza (varianza) pari a $N = \sigma_Z^2$.

L'informazione mutua tra ingresso e uscita su un singolo uso del canale è data da:

$$
I(X; Y) = h(Y) - h(Y \mid X) = h(Y) - h(X + Z \mid X) = h(Y) - h(Z)
$$

Poiché il rumore $Z$ è gaussiano, la sua entropia differenziale è nota e costante:

$$
h(Z) = \frac{1}{2}\log_2(2\pi e N)
$$

La potenza media del segnale ricevuto $Y$ è limitata dalla somma delle potenze di ingresso e rumore:

$$
\mathbb{E}[Y^2] = \mathbb{E}[(X + Z)^2] = \mathbb{E}[X^2] + \mathbb{E}[Z^2] + 2\mathbb{E}[X]\mathbb{E}[Z] = \mathbb{E}[X^2] + N \le P + N
$$

Per massimizzare l'informazione mutua $I(X; Y)$ occorre massimizzare $h(Y)$ sotto il vincolo $\mathbb{E}[Y^2] \le P + N$. Per il Teorema di Massima Entropia Differenziale, $h(Y)$ è massimizzata se e solo se $Y$ è una variabile aleatoria gaussiana a varianza massima $P + N$:

$$
h(Y) \le \frac{1}{2}\log_2(2\pi e (P + N))
$$

Tale condizione è realizzata se e solo se l'ingresso $X$ è anch'esso distribuito secondo una legge normale $X \sim \mathcal{N}(0, P)$.

Sostituendo le due entropie nell'espressione dell'informazione mutua, la __capacità del canale gaussiano a tempo discreto__ vale:

$$
C = \max_{p(x): \mathbb{E}[X^2] \le P} I(X; Y) = \frac{1}{2}\log_2(2\pi e (P + N)) - \frac{1}{2}\log_2(2\pi e N) = \frac{1}{2}\log_2\left( 1 + \frac{P}{N} \right) \quad \text{bit/uso}
$$

### Canale Continuo a Banda Limitata: La Formula di Shannon-Hartley

Nei canali fisici di comunicazione radio o su linea cablata, la trasmissione avviene mediante forme d'onda a tempo continuo $X(t)$ limitate rigorosamente a una banda passante di frequenze pari a $B$ Hertz (intervallo $[-B, B]$) e soggette a un vincolo di potenza media continua $P$ Watt:

$$
Y(t) = X(t) + Z(t)
$$

dove il rumore termico $Z(t)$ è bianco, gaussiano e stazionario con densità spettrale di potenza (PSD) bilaterale piatta pari a $\frac{N_0}{2}$ W/Hz.

Per il Teorema del Campionamento di Nyquist-Shannon, qualsiasi segnale a banda $B$ è univocamente descritto da $2B$ campioni ortogonali al secondo. Ciascun campione di rumore ha varianza pari alla potenza che attraversa il filtro di ricezione di banda $B$:

$$
\sigma_Z^2 = N = \int_{-B}^B \frac{N_0}{2}\mathrm{d}f = N_0 B
$$

Moltiplicando la capacità del singolo campione discreto per il numero di campioni indipendenti generati in un secondo ($2B$), si perviene alla celebre __Formula di Shannon-Hartley__:

$$
C = 2B \cdot \left[ \frac{1}{2}\log_2\left( 1 + \frac{P}{N_0 B} \right) \right] = B \log_2\left( 1 + \frac{P}{N_0 B} \right) = B \log_2(1 + \text{SNR}) \quad \text{bit/s}
$$

dove $\text{SNR} = \frac{P}{N_0 B}$ è il rapporto segnale-rumore adimensionale sulla banda $B$. La derivazione integrale completa è esposta in [[zz. Argomenti extra#Derivazione Rigorosa della Formula di Capacità di Shannon-Hartley]].

### Comportamento Asintotico a Banda Infinita ($B \to \infty$)

Se la banda $B$ viene incrementata indefinitamente mantenendo costante la potenza totale del trasmettitore $P$, la capacità di canale non diverge all'infinito, ma satura a un asintoto orizzontale finito.

Sviluppando il limite al tendere di $B \to \infty$:

$$
C_\infty = \lim_{B \to \infty} B \log_2\left( 1 + \frac{P}{N_0 B} \right) = \lim_{B \to \infty} \frac{B}{\ln 2} \ln\left( 1 + \frac{P}{N_0 B} \right)
$$

Ponendo $x = \frac{P}{N_0 B} \to 0$ e sfruttando l'asintotica $\ln(1 + x) = x + O(x^2)$:

$$
C_\infty = \lim_{B \to \infty} \frac{B}{\ln 2} \left( \frac{P}{N_0 B} \right) = \frac{P}{N_0 \ln 2} \approx 1.4427 \frac{P}{N_0} \quad \text{bit/s}
$$

La ragione fisica di questa saturazione risiede nel fatto che un allargamento della banda $B$ comporta una raccolta proporzionale di maggior potenza di rumore termico complessivo ($N_0 B$), che degrada l'SNR riducendo il contenuto informativo per singolo campione esattamente alla stessa velocità con cui cresce il numero di campioni al secondo.

### Il Limite Ultimo di Shannon ($E_b / N_0 \ge -1.59$ dB)

Esprimendo la potenza di trasmissione come il prodotto tra l'energia spesa per singolo bit di informazione $E_b$ e il rate operativo $R$ bit/s ($P = R \cdot E_b$), e imponendo la condizione di trasmissibilità affidabile senza errori $R \le C$:

$$
\frac{R}{B} \le \log_2\left( 1 + \frac{R}{B} \frac{E_b}{N_0} \right)
$$

Definendo l'efficienza spettrale $\eta = \frac{R}{B}$ (espressa in bit/s/Hz), nel regime a banda infinita e massima espansione dello spettro ($\eta \to 0$):

$$
\lim_{\eta \to 0} \frac{2^\eta - 1}{\eta} = \ln 2 \implies \frac{E_b}{N_0} \ge \ln 2 \approx 0.69315
$$

Convertendo il rapporto adimensionale in decibel:

$$
\left( \frac{E_b}{N_0} \right)_{\text{dB}} \ge 10 \log_{10}(\ln 2) \approx -1.5917 \quad \text{dB}
$$

Il valore $-1.59$ dB rappresenta il __Limite Ultimo di Shannon__: al di sotto di questa soglia termodinamica universale, nessuna modulazione numerica o codice di correzione d'errore (indipendentemente dalla complessità computazionale dell'algoritmo di decodifica) potrà mai garantire una trasmissione a probabilità d'errore tendente a zero su canale AWGN.

