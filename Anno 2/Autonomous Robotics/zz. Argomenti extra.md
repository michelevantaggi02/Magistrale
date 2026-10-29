# Zz. Argomenti Extra

Questo documento raccoglie dimostrazioni, approfondimenti matematici e argomenti collaterali utili alla comprensione completa degli argomenti del corso di _Autonomous Robotics_, ma non strettamente richiesti come parte teorica principale d'esame.

## Metodi Di Integrazione ODE (Eulero, RK2, RK4)

Tutti i modelli cinematici continui dei robot mobili sono descritti da sistemi di equazioni differenziali ordinarie (ODE) del primo ordine:

$$
\dot{\mathbf{x}} = f(\mathbf{x}(t), \mathbf{u}(t), t), \quad \mathbf{x}(t_0) = \mathbf{x}_0
$$

Per simulare il comportamento del robot o calcolarne la posa su un controllore digitale dobbiamo integrare numericamente queste equazioni su una griglia temporale discreta con passo $T$ costante ($t = k T$).

### Metodo Di Eulero Esplicito (Ordine 1)

Il metodo più semplice consiste nell'approssimare la derivata temporale $\dot{\mathbf{x}}$ con il rapporto incrementale in avanti del primo ordine:

$$
\dot{\mathbf{x}} \approx \frac{\mathbf{x}((k + 1)T) - \mathbf{x}(kT)}{T}
$$

Uguagliando al campo vettoriale calcolato all'inizio dell'intervallo:

$$
\frac{\mathbf{x}((k + 1)T) - \mathbf{x}(kT)}{T} \approx f(\mathbf{x}(kT), \mathbf{u}(kT), kT)
$$

Otteniamo la formula ricorsiva di aggiornamento:

$$
\mathbf{x}(k + 1) = \mathbf{x}(k) + \Delta \mathbf{x}_E(k)
$$

Dove l'incremento di Eulero è:

$$
\Delta \mathbf{x}_E(k) = T \, f(\mathbf{x}(kT), \mathbf{u}(kT), kT)
$$

- __Vantaggio__: richiede una sola valutazione della funzione $f$ per passo (computazionalmente immediato).
- __Limite__: ha un errore locale di troncamento $O(T^2)$ e un errore globale $O(T)$. Se il passo $T$ non è piccolissimo, la traiettoria accumula rapidamente errori visibili.

### Metodo Di Runge-Kutta Al Secondo Ordine (RK2 / Midpoint)

Per aumentare l'accuratezza senza calcolare derivate analitiche superiori, i metodi Runge-Kutta valutano la funzione $f$ in punti intermedi del passo temporale.

Il metodo RK2 (noto anche come metodo del punto medio) calcola due stadi:
1. Una prima stima di prova della pendenza all'inizio del passo:

   $$k_1 = T \, f(\mathbf{x}(kT), \mathbf{u}(kT), kT)$$

2. Una seconda valutazione della pendenza nel punto medio dell'intervallo ($t + T/2$), usando lo stato stimato con metà incremento $k_1$:

   $$k_2 = T \, f\left(\mathbf{x}(kT) + \frac{1}{2} k_1, \; \mathbf{u}\left(kT + \frac{T}{2}\right), \; kT + \frac{T}{2}\right)$$

La posa finale al passo successivo è:

$$
\mathbf{x}(k + 1) = \mathbf{x}(k) + k_2
$$

Nel caso del robot a guida differenziale stazionario con ingressi tenuti costanti nel passo (_sample and hold_, $\mathbf{u}(t) = \mathbf{u}(k)$):

$$
\mathbf{x}(k + 1) = \mathbf{x}(k) + T \, f\left(\mathbf{x}(k) + \frac{1}{2} k_1, \; \mathbf{u}(k)\right)
$$

Questo porta direttamente alle equazioni viste nel capitolo [[0. Modelli Cinematici e di Movimento#Metodo Di Runge-Kutta Al Secondo Ordine (RK-2)|0. Modelli Cinematici e di Movimento]], dove la direzione viene ruotata di metà dell'angolo incrementale ($\theta_t + \frac{\omega_t T}{2}$).
- Ha un errore locale $O(T^3)$ e un errore globale $O(T^2)$.

### Metodo Di Runge-Kutta Al Quarto Ordine (RK4)

Il metodo Runge-Kutta classico di quarto ordine rappresenta il punto di riferimento nell'integrazione numerica scientifica (è la base usata anche da risolutori come `scipy.integrate.odeint` o `ode45`).

Esegue quattro valutazioni intermedie del campo vettoriale:

$$
\begin{cases}
k_1 = T \, f(\mathbf{x}(kT), \mathbf{u}(kT), kT) \\[6pt]
k_2 = T \, f\left(\mathbf{x}(kT) + \frac{1}{2} k_1, \; \mathbf{u}\left(kT + \frac{T}{2}\right), \; kT + \frac{T}{2}\right) \\[6pt]
k_3 = T \, f\left(\mathbf{x}(kT) + \frac{1}{2} k_2, \; \mathbf{u}\left(kT + \frac{T}{2}\right), \; kT + \frac{T}{2}\right) \\[6pt]
k_4 = T \, f\left(\mathbf{x}(kT) + k_3, \; \mathbf{u}(kT + T), \; kT + T\right)
\end{cases}
$$

Lo stato al passo successivo si ottiene combinando le quattro pendenze con una media pesata (regola di Simpson):

$$
\mathbf{x}(k + 1) = \mathbf{x}(k) + \frac{1}{6} k_1 + \frac{1}{3} k_2 + \frac{1}{3} k_3 + \frac{1}{6} k_4
$$

- __Vantaggi__: garantisce un'accuratezza elevatissima con errore globale $O(T^4)$.
- __Costo__: richiede 4 valutazioni di $f$ per ciascun passo di campionamento.

### Tabella Comparativa Dei Metodi Di Integrazione

La formula generale di aggiornamento a un passo è:

$$
\mathbf{x}(k + 1) = \mathbf{x}(k) + \Delta f
$$

| Metodo | Incremento $\Delta f$ | Valutazioni di $f$ | Ordine Globale | Proprietà Geometrica |
| :--- | :--- | :---: | :---: | :--- |
| __Eulero__ | $\Delta f_E = k_1$ | 1 | $O(T)$ | Avanzamento lungo la retta tangente iniziale |
| __Runge-Kutta 2 (Midpoint)__ | $\Delta f_{RK2} = k_2$ | 2 | $O(T^2)$ | Valutazione della pendenza nel punto medio temporale |
| __Runge-Kutta 4__ | $\Delta f_{RK4} = \frac{1}{6} k_1 + \frac{1}{3} k_2 + \frac{1}{3} k_3 + \frac{1}{6} k_4$ | 4 | $O(T^4)$ | Media pesata con integrazione di Simpson a 4 stadi |

## Derivazione Analitica Del Drift Quadratico Nelle IMU

Nelle Unità di Misura Inerziali (trattate in [[2. Sensori per la Robotica Mobile#Unità Di Misura Inerziale (IMU)|2. Sensori per la Robotica Mobile]]), la stima della posizione mediante navigazione inerziale pura (_dead reckoning_) richiede la doppia integrazione delle accelerazioni lineari depurate dalla gravità:

$$
\mathbf{p}(t) = \mathbf{p}(0) + \mathbf{v}(0)t + \int_{0}^{t} \left( \int_{0}^{\tau} \mathbf{a}_{\text{moto}}(s) \, ds \right) d\tau
$$

L'accelerazione di moto $\mathbf{a}_{\text{moto}}^b$ nel frame corpo $\{b\}$ viene ricavata sottraendo la gravità $\mathbf{g}^w = [0, 0, -g]^T$:

$$
\mathbf{a}_{\text{moto}}^b = \mathbf{a}_{\text{misurata}}^b - R_w^b(t) \, \mathbf{g}^w
$$

### Propagazione Dell'Errore Angolare Del Giroscopio

Supponiamo che i giroscopi siano affetti da un bias angolare costante residuo $\delta\boldsymbol{\omega}$. L'orientamento stimato $\hat{R}_w^b(t)$ differisce dalla rotazione reale $R_w^b(t)$ per un errore angolare che cresce linearmente nel tempo:

$$
\delta\theta(t) \approx \delta\omega \cdot t
$$

Nella compensazione della gravità, un errore angolare $\delta\theta$ attorno a un asse orizzontale proietta una componente spuria del vettore di gravità $g \approx 9.81\text{ m/s}^2$ sugli assi orizzontali del robot:

$$
\Delta a_x(t) \approx g \cdot \sin(\delta\theta(t)) \approx g \cdot \delta\omega \cdot t
$$

Integrando doppiamente questa accelerazione spuria per ottenere la posizione orizzontale:

$$
\Delta p_x(t) = \int_{0}^{t} \int_{0}^{\tau} (g \cdot \delta\omega \cdot s) \, ds \, d\tau = \frac{1}{6} g \cdot \delta\omega \cdot t^3
$$

L'errore angolare nel giroscopio provoca quindi una deriva di posizione che cresce addirittura come __$O(t^3)$__ a causa dell'accoppiamento con la gravità.

### Bias Costante Dell'Accelerometro E Deriva Quadratica $O(t^2)$

Se consideriamo invece un bias residuo costante proprio dell'accelerometro $\Delta a_{\text{bias}}$ (anche assumendo l'orientamento perfettamente noto):

$$
\Delta p(t) = \int_{0}^{t} \int_{0}^{\tau} \Delta a_{\text{bias}} \, ds \, d\tau = \frac{1}{2} \Delta a_{\text{bias}} \, t^2
$$

L'errore di posizione cresce in modo rigorosamente __quadratico $O(t^2)$__.

#### Esempio Numerico Quantitativo

Consideriamo un accelerometro MEMS di fascia commerciale con un bias residuo di appena:

$$
\Delta a_{\text{bias}} = 0.01\text{ m/s}^2 \quad (\approx 1\text{ mg})
$$

Dopo un intervallo di navigazione libera di $t = 60\text{ secondi}$ (un minuto), l'errore di posizionamento accumulato vale:

$$
\Delta p(60) = \frac{1}{2} (0.01) (60)^2 = \frac{1}{2} (0.01) (3600) = 18\text{ metri}
$$

Dopo 5 minuti ($300\text{ s}$), l'errore raggiunge:

$$
\Delta p(300) = \frac{1}{2} (0.01) (90000) = 450\text{ metri}
$$

Questo risultato dimostra analiticamente l'impossibilità fisica di utilizzare una IMU come sensore di posizionamento stand-alone senza frequenti correzioni esterne assolute (GPS, LiDAR o telecamere).

### Giroscopi Ottici FOG Ed Effetto Sagnac

Nelle applicazioni aerospaziali e nei veicoli autonomi ad alta affidabilità si impiegano i giroscopi a fibra ottica (__FOG__, _Fiber Optic Gyro_, come il sensore KVH 1750 citato nel capitolo principale).

Il FOG sfrutta l'__Effetto Sagnac__: due fasci di luce laser a stato solido vengono iniettati in versi opposti (orario e antiorario) all'interno di una bobina di fibra ottica avvolta per centinaia di metri o chilometri di lunghezza.

Se la bobina ruota con velocità angolare $\Omega$ attorno al proprio asse normale, il fascio concorde con la rotazione deve percorrere un tragitto ottico leggermente più lungo rispetto al fascio discorde. La differenza di cammino ottico $\Delta L$ genera uno sfasamento ottico di interferenza $\Delta\phi_S$:

$$
\Delta\phi_S = \frac{8\pi A N}{\lambda_0 c} \, \Omega
$$

dove:
- $A$ è l'area racchiusa da ciascuna spira della bobina.
- $N$ è il numero totale di spire di fibra ottica.
- $\lambda_0$ è la lunghezza d'onda del laser nel vuoto.
- $c$ è la velocità della luce.

Rilevando interferometricamente lo sfasamento $\Delta\phi_S$, il sensore misura la velocità angolare istantanea $\Omega$ con un bias di deriva estremamente contenuto (frazioni di decimi di grado all'ora, $0.01^\circ/\text{h}$), consentendo l'integrazione di rotta per durate temporali notevolmente superiori rispetto ai MEMS.

## Geometria Della Visione Stereoscopica

Nella visione binoculare (citata in [[2. Sensori per la Robotica Mobile#Visione Artificiale E Il Modello Prospettico|2. Sensori per la Robotica Mobile]]), due telecamere identiche sono montate su una struttura rigida con assi ottici paralleli e distanziate orizzontalmente di una distanza nota $b$, detta __baseline__.

I piani immagine delle due telecamere sono complanari (condizione di telecamere rettificate). Un punto dello spazio tridimensionale $P = [X, Y, Z]^T$ (espresso nella terna della camera sinistra di riferimento) viene proiettato sui due sensori nei punti immagine:
- Camera sinistra: $p_L = (u_L, v_L)$
- Camera destra: $p_R = (u_R, v_R)$

Dalle equazioni del modello prospettico ideale a focale $f$:

$$
u_L = f \frac{X}{Z}, \quad u_R = f \frac{X - b}{Z}, \quad v_L = v_R = f \frac{Y}{Z}
$$

### Calcolo Della Disparità E Della Profondità

La differenza tra le ascisse orizzontali sui due piani immagine definisce la __disparità__ $d$:

$$
d = u_L - u_R = f \frac{X}{Z} - f \frac{X - b}{Z} = \frac{f \cdot b}{Z}
$$

Invertendo l'equazione rispetto a $Z$ otteniamo la formula fondamentale della triangolazione stereoscopica:

$$
Z = \frac{f \cdot b}{d}
$$

Conoscendo la profondità $Z$, le coordinate 3D $(X, Y)$ del punto nello spazio si ricostruiscono univocamente:

$$
X = \frac{u_L \cdot Z}{f}, \quad Y = \frac{v_L \cdot Z}{f}
$$

### Analisi Dell'Errore Di Profondità

Differenziando la profondità $Z$ rispetto alla disparità $d$:

$$
\left| \frac{\partial Z}{\partial d} \right| = \frac{f \cdot b}{d^2} = \frac{Z^2}{f \cdot b}
$$

L'incertezza sulla profondità stimata $\Delta Z$ indotta da un errore di quantizzazione della disparità sui pixel $\Delta d$ vale:

$$
\Delta Z = \frac{Z^2}{f \cdot b} \Delta d
$$

Questo evidenzia due limiti fisici strutturali della stereo camera:
1. __Incertezza quadratica con la distanza__: l'errore di profondità cresce con il quadrato della distanza $Z^2$.
2. __Ruolo della baseline $b$__: aumentando la distanza tra le telecamere $b$ si riduce l'errore a lungo raggio, ma aumenta il volume minimo cieco vicino al robot (_blind zone_) e la difficoltà di trovare corrispondenze di feature visive (corrispondenza stereo).

## Modellistica Dello Pseudorange Nei Sistemi GNSS / GPS

Nei sistemi satellitari GNSS (presentati in [[2. Sensori per la Robotica Mobile#Sistemi Di Riferimento Basati Su Beacon E GNSS/GPS|2. Sensori per la Robotica Mobile]]), ciascun satellite $i$-esimo trasmette in continuo un messaggio di navigazione con il proprio vettore di posizione tridimensionale orbitale $\mathbf{X}_i = [X_i, Y_i, Z_i]^T$ e il timestamp di trasmissione $t_{e,i}$ regolato da orologi atomici al cesio o rubidio.

Il ricevitore a terra registra il tempo di arrivo del segnale $t_r$ tramite il proprio oscillatore locale (al quarzo). Poiché l'orologio locale del ricevitore è economico e presenta un disallineamento temporale (bias d'orologio) $\delta t_{\text{rx}}$ rispetto al tempo universale GPS, la misura grezza calcolata moltiplicando per la velocità della luce $c$ non è la distanza geometrica vera, ma viene definita __pseudorange__ $\rho_i$:

$$
\rho_i = c \cdot (t_r - t_{e,i})
$$

### Equazione Di Misura A Quattro Incognite

Esplicitando la distanza euclidea tra satellite e ricevitore posto in $\mathbf{x} = [x, y, z]^T$:

$$
\rho_i = \sqrt{(X_i - x)^2 + (Y_i - y)^2 + (Z_i - z)^2} + c \cdot \delta t_{\text{rx}} + \epsilon_i
$$

dove $\epsilon_i$ raggruppa i disturbi ambientali di propagazione:
- Ritardo ionosferico e troposferico.
- Errori di effemeridi residue del satellite.
- Rumore termico di ricezione e riflessioni multipath.

Poiché le incognite dello stato da stimare sono __quattro__:

$$
\mathbf{s} = [x, \; y, \; z, \; c \cdot \delta t_{\text{rx}}]^T
$$

è geometricamente indispensabile ricevere contemporaneamente il segnale da un numero di satelliti:

$$
n_{\text{sat}} \ge 4
$$

Risolvendo il sistema non lineare con algoritmi di minimizzazione ai minimi quadrati iterati (Gauss-Newton o Filtro di Kalman esteso), il ricevitore stima contemporaneamente la posizione tridimensionale metrica $(x, y, z)$ e sincronizza perfettamente il proprio orologio locale con il tempo atomico GPS.

### Principio Operativo Dell'RTK (Real Time Kinematic)

Nelle applicazioni di robotica agricola o veicolare (come la piattaforma Agrobot di ISARLab), la precisione metrica standard di $3 - 5\text{ m}$ è insufficiente per condurre un veicolo tra i filari. Si impiega pertanto la tecnologia __RTK (Real Time Kinematic)__.

Il sistema RTK prevede:
1. Una __Stazione Base fissa__ a terra, installata su un punto geodetico di coordinate millimetriche note.
2. Il __Rover mobile__ montato a bordo del robot.

Anziché limitarsi a decodificare i bit del codice pseudo-casuale (PRN) del segnale, i ricevitori RTK tracciano la __fase dell'onda portante radio__ a frequenza $L_1 = 1575.42\text{ MHz}$, la cui lunghezza d'onda nello spazio vale appena:

$$
\lambda = \frac{c}{f} = \frac{3 \times 10^8\text{ m/s}}{1.57542 \times 10^9\text{ Hz}} \approx 19.03\text{ cm}
$$

Misurando lo sfasamento della frazione di ciclo dell'onda con risoluzione inferiore all'1%, e risolvendo in tempo reale il problema dell'__ambiguità intera di fase__ (il numero intero incognito $N$ di cicli d'onda completi interposti tra satellite e antenna mediante tecniche a doppie differenze tra Base e Rover), il sistema cancella quasi integralmente gli errori atmosferici e di satellite comuni.

La stima della posizione relativa del rover rispetto alla base fissa raggiunge un'accuratezza cinematica istantanea nell'ordine di __$1\text{ centimetro}$__.

## Parametri Metrologici Avanzati E Fisica Dei Sensori

Questa sezione approfondisce le definizioni metrologiche e i modelli fisici accennati nell'[[2. Sensori per la Robotica Mobile#Appendice: Caratteristiche Metrologiche E Sensori Fisici|Appendice della Lezione 5]].

### Quantificazione Del Dynamic Range In Decibel

Il range dinamico descrive la capacità del sensore di misurare contemporaneamente segnali di debole intensità e segnali di fondo scala senza saturazione:

- __Per grandezze energetiche o di potenza__ (ad esempio l'intensità luminosa catturata dai fotodiodi del LiDAR o la potenza dei segnali RF):

  $$
  \text{DR}_{\text{power}} = 10 \log_{10} \left( \frac{P_{\max}}{P_{\min}} \right) \quad [\text{dB}]
  $$

- __Per grandezze di ampiezza, tensione o campo__ (tensioni dei piezometri, segnali elettrici dei ponti di Wheatstone):

  $$
  \text{DR}_{\text{voltage}} = 20 \log_{10} \left( \frac{V_{\max}}{V_{\min}} \right) \quad [\text{dB}]
  $$

Un sensore ToF con un range dinamico di $80\text{ dB}$ in tensione è in grado di discriminare segnali il cui rapporto di ampiezza è di $10^{80/20} = 10^4 = 10.000:1$.

### Risoluzione Di Quantizzazione Nei Sensori Digitali (ADC)

La maggior parte dei trasduttori fisici genera una tensione o carica analogica che viene convertita in un dato digitale tramite un convertitore Analogico-Digitale (ADC) a $b$ bit. Se l'intervallo di fondo scala dell'ADC è $[0, V_{\text{FS}}]$, la tensione è suddivisa in $2^b$ intervalli discreti.

La risoluzione teorica minima di quantizzazione $\Delta V$ vale:

$$
\Delta V = \frac{V_{\text{FS}}}{2^b}
$$

L'operazione di quantizzazione introduce un rumore uniformemente distribuito nell'intervallo $[-\frac{\Delta V}{2}, +\frac{\Delta V}{2}]$, con una varianza teorica intrinseca di rumore di quantizzazione:

$$
\sigma_q^2 = \frac{(\Delta V)^2}{12}
$$

### Distorsioni Hard-Iron E Soft-Iron Nelle Bussole Magnetiche

I magnetometri a stato solido rilevano il vettore del campo magnetico terrestre $\mathbf{B}_{\text{earth}}$. In un ambiente privo di metalli e correnti parassite, ruotando il sensore sul piano orizzontale di $360^\circ$ le letture $(B_x, B_y)$ descrivono una circonferenza perfetta centrata nell'origine:

$$
B_x^2 + B_y^2 = \|\mathbf{B}_{\text{earth}}\|^2
$$

Sul robot reale intervengono due effetti parassiti:

1. __Distorsione Hard-Iron__: generata da corpi ferromagnetici permanentemente magnetizzati montati a bordo del robot (altoparlanti, viti ferrose, telaio in acciaio, magneti permanenti dei motori DC). Produce un campo magnetico costante $\mathbf{b}_{\text{hard}}$ solidale alla terna del robot che trasla il centro della circonferenza:

   $$\mathbf{B}_{\text{misurato}} = \mathbf{B}_{\text{reale}} + \mathbf{b}_{\text{hard}}$$

2. __Distorsione Soft-Iron__: generata da materiali ad alta permeabilità magnetica passivi (ferro dolce, schermature metalliche, piste di rame con correnti variabili) che deflettono e comprimono le linee di flusso del campo magnetico esterno a seconda dell'orientamento. È descritta da una matrice di deformazione $3 \times 3$ simmetrica $M_{\text{soft}}$, che deforma la circonferenza in un'ellisse inclinata.

Il modello completo di misura della bussola è:

$$
\mathbf{B}_{\text{misurato}} = M_{\text{soft}} \, \mathbf{B}_{\text{earth}} + \mathbf{b}_{\text{hard}}
$$

#### Procedura Di Calibrazione Ad Ellisse

Per calibrare il magnetometro:
1. Si fa compiere al robot una rotazione lenta di $360^\circ$ raccogliendo un insieme di punti sul piano.
2. Si esegue un fitting di regressione ai minimi quadrati per individuare i parametri dell'ellisse (centro $\mathbf{b}_{\text{hard}}$, assi principali e inclinazione della matrice $M_{\text{soft}}$).
3. Si applica la trasformazione inversa:

   $$\mathbf{B}_{\text{calibrato}} = M_{\text{soft}}^{-1} (\mathbf{B}_{\text{misurato}} - \mathbf{b}_{\text{hard}})$$

   riportando i dati su un cerchio unitario centrato nell'origine da cui ricavare l'angolo di rotta assoluto privo di offset:

   $$\theta = \text{atan2}(B_{y,\text{calibrato}}, B_{x,\text{calibrato}})$$

### Meccanica Dei Micro-Giroscopi MEMS E Forza Di Coriolis

I giroscopi miniaturizzati realizzati con tecnologia microelettro-meccanica (MEMS) non possono includere rotori rotanti ad alta velocità a causa dell'usura per attrito e dei limiti di fabbricazione microscopica. Sfruttano invece __strutture oscillanti risonanti__ (diapason, pettini elettrostatici capacitivi o campane semisferiche al silicio).

Una massa sismica microscopica $m$ viene mantenuta in oscillazione sinusoidale continua a frequenza di risonanza $\omega_r$ lungo un asse primario di attuazione $x$ con velocità istantanea:

$$
\mathbf{v}(t) = [v_x(t), 0, 0]^T
$$

Quando il telaio del robot ruota attorno all'asse perpendicolare $z$ con velocità angolare $\boldsymbol{\omega} = [0, 0, \Omega_z]^T$, nel sistema di riferimento non inerziale della massa si sviluppa la __forza di Coriolis__ apparente:

$$
\mathbf{F}_c = -2m (\boldsymbol{\omega} \times \mathbf{v})
$$

Calcolando il prodotto vettoriale:

$$
\boldsymbol{\omega} \times \mathbf{v} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 0 & 0 & \Omega_z \\ v_x & 0 & 0 \end{vmatrix} = [0, \Omega_z v_x, 0]^T
$$

La forza di Coriolis agisce interamente lungo l'asse ortogonale $y$:

Questa forza ciclica induce un'oscillazione secondaria lungo l'asse $y$. La deflessione ortogonale viene misurata con elevata sensibilità rilevando la variazione differenziale di capacità $\Delta C$ tra elettrodi microscopici a pettine, fornendo un segnale di tensione proporzionale alla velocità angolare esterna $\Omega_z$.

---

## Derivazione Analitica Del Line Fitting (OLS E WLS) in Coordinate Polari

Nel contesto del rilevamento di ostacoli piani da scansioni LiDAR, la rappresentazione esplicita cartesiana $y = mx + q$ fallisce quando la retta è parallela all'asse $y$ ($m \to \infty$). Si adotta la __forma normale di Hesse__:

$$
x \cos\alpha + y \sin\alpha - r = 0
$$

dove $r \ge 0$ è la distanza minima ortogonale dall'origine alla retta e $\alpha \in [-\pi, \pi]$ è l'angolo del vettore normale orientato.

### Formulazione Del Problema Di Ottimizzazione OLS

Dato un insieme di $N$ punti misurati nel piano $\{ (x_i, y_i) \}_{i=1}^N$, la distanza ortogonale con segno (residuo geometrico) tra il generico punto $P_i$ e la retta candidata è:

$$
d_i = x_i \cos\alpha + y_i \sin\alpha - r
$$

L'obiettivo dei Minimi Quadrati Ordinari (OLS, _Total Least Squares_) è minimizzare la somma dei quadrati delle distanze perpendicolari:

$$
S(\alpha, r) = \sum_{i=1}^N d_i^2 = \sum_{i=1}^N \left( x_i \cos\alpha + y_i \sin\alpha - r \right)^2
$$

#### 1. Ottimizzazione Rispetto Al Parametro Distanza $r$

Calcoliamo la derivata parziale prima di $S$ rispetto a $r$ e poniamola uguale a zero:

$$
\frac{\partial S}{\partial r} = -2 \sum_{i=1}^N \left( x_i \cos\alpha + y_i \sin\alpha - r \right) = 0
$$

Dividendo per $-2N$:

$$
\frac{1}{N}\sum_{i=1}^N x_i \cos\alpha + \frac{1}{N}\sum_{i=1}^N y_i \sin\alpha - r = 0
$$

Definendo il baricentro (media campionaria) dei punti misurati come:

$$
\bar{x} = \frac{1}{N} \sum_{i=1}^N x_i, \quad \bar{y} = \frac{1}{N} \sum_{i=1}^N y_i
$$

Otteniamo la relazione fondamentale in forma chiusa per $r$:

$$
r = \bar{x} \cos\alpha + \bar{y} \sin\alpha
$$

__Interpretazione geometrica__: la retta ottima stimata passa inderogabilmente per il baricentro $(\bar{x}, \bar{y})$ dei punti misurati.

---

#### 2. Ottimizzazione Rispetto all'Angolo Della Normale $\alpha$

Sostituendo l'espressione di $r$ all'interno del residuo $d_i$:

$$
d_i = (x_i - \bar{x}) \cos\alpha + (y_i - \bar{y}) \sin\alpha
$$

Definiamo per brevità le coordinate scarto dal baricentro:

$$
\tilde{x}_i = x_i - \bar{x}, \quad \tilde{y}_i = y_i - \bar{y}
$$

La funzione di costo $S$ dipende ora unicamente da $\alpha$:

$$
S(\alpha) = \sum_{i=1}^N \left( \tilde{x}_i \cos\alpha + \tilde{y}_i \sin\alpha \right)^2 = \sum_{i=1}^N \left( \tilde{x}_i^2 \cos^2\alpha + \tilde{y}_i^2 \sin^2\alpha + 2 \tilde{x}_i \tilde{y}_i \cos\alpha \sin\alpha \right)
$$

Sfruttando le note identità trigonometriche di duplicazione degli angoli:
- $\cos^2\alpha = \frac{1 + \cos(2\alpha)}{2}$
- $\sin^2\alpha = \frac{1 - \cos(2\alpha)}{2}$
- $2 \cos\alpha \sin\alpha = \sin(2\alpha)$

Raggruppiamo i termini:

$$
S(\alpha) = \frac{1}{2} \sum_{i=1}^N (\tilde{x}_i^2 + \tilde{y}_i^2) + \frac{1}{2} \cos(2\alpha) \sum_{i=1}^N (\tilde{x}_i^2 - \tilde{y}_i^2) + \sin(2\alpha) \sum_{i=1}^N (\tilde{x}_i \tilde{y}_i)
$$

Deriviamo $S(\alpha)$ rispetto ad $\alpha$ e imponiamo la condizione di stazionarietà $\frac{d S}{d \alpha} = 0$:

$$
\frac{d S}{d \alpha} = -\sin(2\alpha) \sum_{i=1}^N (\tilde{x}_i^2 - \tilde{y}_i^2) + 2 \cos(2\alpha) \sum_{i=1}^N (\tilde{x}_i \tilde{y}_i) = 0
$$

Separando le variabili trigonometriche:

$$
\sin(2\alpha) \sum_{i=1}^N (\tilde{x}_i^2 - \tilde{y}_i^2) = 2 \cos(2\alpha) \sum_{i=1}^N (\tilde{x}_i \tilde{y}_i)
$$

Dividendo per $\cos(2\alpha)$:

$$
\tan(2\alpha) = \frac{2 \sum_{i=1}^N \tilde{x}_i \tilde{y}_i}{\sum_{i=1}^N (\tilde{x}_i^2 - \tilde{y}_i^2)} = \frac{-2 \sum_{i=1}^N (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^N (y_i - \bar{y})^2 - \sum_{i=1}^N (x_i - \bar{x})^2}
$$

L'angolo della normale $\alpha$ viene calcolato senza ambiguità di quadrante tramite la funzione $\text{atan2}$:

$$
\alpha = \frac{1}{2} \text{atan2}\left( -2 \sum_{i=1}^N \tilde{x}_i \tilde{y}_i, \; \sum_{i=1}^N (\tilde{y}_i^2 - \tilde{x}_i^2) \right)
$$

Se il valore calcolato di $r = \bar{x}\cos\alpha + \bar{y}\sin\alpha$ risulta negativo, si inverte la direzione della normale ($\alpha \leftarrow \alpha + \pi$, $r \leftarrow -r$) per preservare la convenzione standard $r \ge 0$.

---

### Estensione Ai Minimi Quadrati Pesati (WLS)

Quando i singoli punti $P_i$ presentano varianze eterogenee $\sigma_i^2$ (ad esempio a causa della dispersione radiale LiDAR che cresce con la distanza misurata $\rho_i$), si introduce il peso stocastico:

$$
w_i = \frac{1}{\sigma_i^2}
$$

La funzione di costo WLS vale:

$$
S_w(\alpha, r) = \sum_{i=1}^N w_i \left( x_i \cos\alpha + y_i \sin\alpha - r \right)^2
$$

Il baricentro pesato si ottiene come:

$$
\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i}, \quad \bar{y}_w = \frac{\sum w_i y_i}{\sum w_i} \implies r = \bar{x}_w \cos\alpha + \bar{y}_w \sin\alpha
$$

E l'orientamento della normale diventa:

$$
\tan(2\alpha) = \frac{-2 \sum_{i=1}^N w_i (x_i - \bar{x}_w)(y_i - \bar{y}_w)}{\sum_{i=1}^N w_i (y_i - \bar{y}_w)^2 - \sum_{i=1}^N w_i (x_i - \bar{x}_w)^2}
$$

---

### Propagazione Delle Incertezze E Matrice Jacobiana $F_{PQ}$

I punti di misura laser non sono grandezze deterministiche, ma variabili aleatorie raggruppate nel vettore di misura $\mathbf{P} \in \mathbb{R}^{2N}$:

$$
\mathbf{P} = \begin{bmatrix} \rho_1 & \theta_1 & \rho_2 & \theta_2 & \dots & \rho_N & \theta_N \end{bmatrix}^T
$$

con matrice di covarianza congiunta a blocchi diagonali $C_P \in \mathbb{R}^{2N \times 2N}$. Di conseguenza, anche i parametri stimati della retta $\mathbf{Q} = [\alpha, r]^T \in \mathbb{R}^2$ sono variabili aleatorie con matrice di covarianza $C_Q = C_{AR} \in \mathbb{R}^{2 \times 2}$:

$$
C_{AR} = \begin{bmatrix} \sigma_\alpha^2 & \sigma_{\alpha r} \\ \sigma_{\alpha r} & \sigma_r^2 \end{bmatrix}
$$

Applicando la legge di propagazione lineare delle covarianze mediante il Jacobiano della trasformazione di stima:

$$
C_{AR} = F_{PQ} \, C_P \, F_{PQ}^T
$$

dove $F_{PQ} \in \mathbb{R}^{2 \times 2N}$ è la matrice Jacobiana delle funzioni di stima $\alpha(\mathbf{P})$ e $r(\mathbf{P})$ rispetto al vettore delle misure $\mathbf{P}$:

$$
F_{PQ} = \begin{bmatrix}
\frac{\partial \alpha}{\partial \rho_1} & \frac{\partial \alpha}{\partial \theta_1} & \dots & \frac{\partial \alpha}{\partial \rho_N} & \frac{\partial \alpha}{\partial \theta_N} \\[8pt]
\frac{\partial r}{\partial \rho_1} & \frac{\partial r}{\partial \theta_1} & \dots & \frac{\partial r}{\partial \rho_N} & \frac{\partial r}{\partial \theta_N}
\end{bmatrix}
$$

La conoscenza esplicita di $C_{AR}$ è indispensabile nei filtri di localizzazione e SLAM (es. EKF-SLAM basato su linee): consente al robot di calcolare l'ellisse di confidenza e la distanza di Mahalanobis tra le rette osservate all'istante $t$ e le pareti già censite nella mappa globale.

## Formulazione Matriciale Dell'Histogram Filter Come Catena Di Markov

Nel capitolo [[5. Localizzazione con Histogram Filter|5. Localizzazione con Histogram Filter]] abbiamo espresso l'aggiornamento dell'Histogram Filter tramite cicli iterativi `for` sulle singole celle $x_k$ e $x_i$. Quando lo spazio delle pose viene discretizzato in un numero finito $K$ di celle, il filtro di Bayes discreto può essere formulato con notevole eleganza e potenza computazionale attraverso l'algebra lineare delle __Catene di Markov a tempo discreto (DTMC)__.

### Vettore Di Stato E Matrice Di Transizione Stocastica

Rappresentiamo la distribuzione di probabilità dell'intero spazio all'istante $t$ come un vettore colonna di probabilità $\mathbf{p}_t \in \mathbb{R}^K$:

$$
\mathbf{p}_t = \begin{bmatrix} p_{1,t} \\ p_{2,t} \\ \vdots \\ p_{K,t} \end{bmatrix} = \begin{bmatrix} bel_t(x_1) \\ bel_t(x_2) \\ \vdots \\ bel_t(x_K) \end{bmatrix}
$$

con i vincoli di non negatività $p_{k,t} \ge 0$ e conservazione della massa probabilistica $\sum_{k=1}^K p_{k,t} = \mathbf{1}^T \mathbf{p}_t = 1$, dove $\mathbf{1} = [1, 1, \dots, 1]^T$.

Definiamo la __matrice di transizione di stato__ $T(u_t) \in \mathbb{R}^{K \times K}$ associata al comando di controllo $u_t$:

$$
T_{k, i}(u_t) := p(X_t = x_k \mid X_{t-1} = x_i, u_t, M)
$$

L'elemento $T_{k, i}$ rappresenta la probabilità di transizione dalla cella di partenza $i$ (colonna) alla cella di destinazione $k$ (riga). La matrice $T$ gode della proprietà fondamentale di essere __colonna-stocastica__ (ogni colonna somma a 1):

$$
\sum_{k=1}^K T_{k, i}(u_t) = 1, \quad \forall i \in \{1, \dots, K\} \iff \mathbf{1}^T T(u_t) = \mathbf{1}^T
$$

### Passo Di Predizione Come Prodotto Matrice-Vettore

L'equazione di predizione del filtro discreto (sommatoria su tutti gli stati antecedenti $x_i$) si riscrive come un unico prodotto matrice-vettore:

$$
\overline{p}_{k,t} = \sum_{i=1}^K T_{k, i}(u_t) \, p_{i, t-1} \implies \overline{\mathbf{p}}_t = T(u_t) \, \mathbf{p}_{t-1}
$$

Poiché $T(u_t)$ è colonna-stocastica, la conservazione della probabilità a priori è garantita automaticamente dall'algebra lineare:

$$
\mathbf{1}^T \overline{\mathbf{p}}_t = \mathbf{1}^T (T(u_t) \, \mathbf{p}_{t-1}) = (\mathbf{1}^T T(u_t)) \, \mathbf{p}_{t-1} = \mathbf{1}^T \mathbf{p}_{t-1} = 1
$$

### Struttura A Banda E Ottimizzazione Sparsa

Nel caso di moto con rumore gaussiano stazionario, la probabilità $T_{k, i}$ decade esponenzialmente all'aumentare della distanza tra le celle $|x_k - (x_i + u_x)|$. Di conseguenza:
- In un ambiente 1D con moto uniforme, $T(u_t)$ assume la struttura di una __matrice di Toeplitz a banda__;
- Ponendo a zero le transizioni oltre la soglia $3\sigma_x$ (dove la densità gaussiana è trascurabile), la matrice diventa sparsa con larghezza di banda $W \ll K$;
- La complessità computazionale del passo di predizione crolla da $O(K^2)$ a $O(K \cdot W)$, consentendo implementazioni ad alte prestazioni tramite librerie di algebra lineare sparsa (es. `scipy.sparse`).

### Passo Di Correzione E Prodotto Di Hadamard

Definiamo il vettore di verosimiglianza delle misure sensoriali $\mathbf{l}_t \in \mathbb{R}^K$, il cui $k$-esimo elemento è la densità valutata sull'ipotesi $x_k$:

$$
\mathbf{l}_t = \begin{bmatrix} p(z_t \mid X_t = x_1, M) \\ p(z_t \mid X_t = x_2, M) \\ \vdots \\ p(z_t \mid X_t = x_K, M) \end{bmatrix}
$$

Il passo di aggiornamento di misura corrisponde al __prodotto elemento per elemento di Hadamard__ (indicato con $\odot$) tra il vettore di likelihood e il vettore di predizione, riscalato dal fattore di normalizzazione $\eta$:

$$
\mathbf{p}_t = \eta \left( \mathbf{l}_t \odot \overline{\mathbf{p}}_t \right)
$$

dove il coefficiente scalare di normalizzazione $\eta$ è il reciproco del prodotto interno:

$$
\eta = \frac{1}{\mathbf{1}^T \left( \mathbf{l}_t \odot \overline{\mathbf{p}}_t \right)} = \frac{1}{\mathbf{l}_t^T \overline{\mathbf{p}}_t}
$$

### Dinamica Asintotica E Teorema Di Perron-Frobenius

Se il robot si muove nell'ambiente senza effettuare alcuna misura correttiva ($z_t$ assente per $N$ passi consecutivi), il belief evolve come:

$$
\mathbf{p}_t = T^N \, \mathbf{p}_0
$$

Se la matrice di transizione è irriducibile e aperiodica (condizione tipica garantita dal rumore gaussiano che connette debolmente ogni stato a tutti gli altri), il __teorema di Perron-Frobenius__ assicura che $T$ ammette un unico autovalore dominante $\lambda_1 = 1$, e che per $N \to \infty$ il vettore $\mathbf{p}_t$ converge all'autovettore stazionario $\mathbf{p}_\infty$:

$$
\lim_{N \to \infty} \mathbf{p}_t = \mathbf{p}_\infty \quad \text{con} \quad T \mathbf{p}_\infty = \mathbf{p}_\infty
$$

Nel caso di rumore di traslazione simmetrico con pareti riflettenti o periodiche, tale stato asintotico corrisponde alla __distribuzione uniforme__ $\mathbf{p}_\infty = [1/K, \dots, 1/K]^T$: in assenza di retroazione sensoriale, l'accumulo ininterrotto dell'incertezza odometrica cancella ogni informazione pregressa conducendo alla totale perdita di localizzazione.

## Derivazione Formale Della Traiettoria Completa Nel Particle Filter

Nella trattazione standard della localizzazione robotica (Monte Carlo Localization), il filtro a particelle calcola ricorsivamente la distribuzione di probabilità a posteriori della sola posa istantanea:

$$
bel(x_t) = p(x_t \mid z_{1:t}, u_{1:t})
$$

Tuttavia, dal punto di vista dell'analisi teorica dei processi stocastici (come illustrato nelle lezioni avanzate del Prof. Valigi, slide 38–39), il Particle Filter trova la sua giustificazione analitica più rigorosa estendendo lo stato all'intera sequenza storica delle pose attraversate dal robot:

$$
x_{0:t} = \{ x_0, x_1, \dots, x_t \}
$$

Il belief della traiettoria completa è definito come la densità congiunta condizionata a tutte le osservazioni e azioni passate:

$$
bel(x_{0:t}) = p(x_{0:t} \mid z_{1:t}, u_{1:t})
$$

### Espansione Ricorsiva Tramite Regola Di Bayes E Proprietà Di Markov

Isoliamo l'osservazione più recente $z_t$ dal set di tutte le misure sensoriali $z_{1:t} = \{ z_t, z_{1:t-1} \}$:

$$
bel(x_{0:t}) = p(x_{0:t} \mid z_t, z_{1:t-1}, u_{1:t})
$$

Applicando la regola di Bayes considerando $z_t$ come l'evidenza osservata condizionata alla traiettoria $x_{0:t}$, alla storia delle misure passate $z_{1:t-1}$ e ai comandi $u_{1:t}$:

$$
bel(x_{0:t}) = \frac{p(z_t \mid x_{0:t}, z_{1:t-1}, u_{1:t}) \, p(x_{0:t} \mid z_{1:t-1}, u_{1:t})}{p(z_t \mid z_{1:t-1}, u_{1:t})} = \eta \, p(z_t \mid x_{0:t}, z_{1:t-1}, u_{1:t}) \, p(x_{0:t} \mid z_{1:t-1}, u_{1:t})
$$

Sfruttiamo l'__assunzione markoviana del modello di misura__: la lettura del sensore $z_t$ all'istante $t$ è condizionatamente indipendente da tutte le pose passate $x_{0:t-1}$, dalle misure pregresse $z_{1:t-1}$ e dai comandi di controllo $u_{1:t}$, una volta nota la posa istantanea attuale $x_t$:

$$
p(z_t \mid x_{0:t}, z_{1:t-1}, u_{1:t}) = p(z_t \mid x_t)
$$

Sostituendo nella formulazione del belief:

$$
bel(x_{0:t}) = \eta \, p(z_t \mid x_t) \, p(x_{0:t} \mid z_{1:t-1}, u_{1:t})
$$

Scomponiamo ora il termine congiunto $p(x_{0:t} \mid z_{1:t-1}, u_{1:t})$ applicando la definizione di probabilità condizionata per isolare l'ultimo stato $x_t$ rispetto alla storia $x_{0:t-1}$:

$$
p(x_{0:t} \mid z_{1:t-1}, u_{1:t}) = p(x_t \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) \, p(x_{0:t-1} \mid z_{1:t-1}, u_{1:t})
$$

Applichiamo nuovamente l'__assunzione markoviana del modello di moto__:
1. Lo stato attuale $x_t$ dipende unicamente dalla posa immediatamente precedente $x_{t-1}$ e dal comando di attuazione corrente $u_t$:

   $$
   p(x_t \mid x_{0:t-1}, z_{1:t-1}, u_{1:t}) = p(x_t \mid x_{t-1}, u_t)
   $$

2. La storia passata delle pose $x_{0:t-1}$ è indipendente dall'azione futura $u_t$:

   $$
   p(x_{0:t-1} \mid z_{1:t-1}, u_{1:t}) = p(x_{0:t-1} \mid z_{1:t-1}, u_{1:t-1}) = bel(x_{0:t-1})
   $$

Ricongiungendo tutti i termini, otteniamo l'equazione ricorsiva fondamentale per il belief della traiettoria:

$$
bel(x_{0:t}) = \eta \, p(z_t \mid x_t) \, p(x_t \mid x_{t-1}, u_t) \, bel(x_{0:t-1})
$$

Definendo il belief a priori della traiettoria (dopo il comando di moto ma prima della misura) come:

$$
\overline{bel}(x_{0:t}) = p(x_t \mid x_{t-1}, u_t) \, bel(x_{0:t-1})
$$

L'espressione si compatta nella forma canonica:

$$
bel(x_{0:t}) = \eta \, p(z_t \mid x_t) \, \overline{bel}(x_{0:t})
$$

### Corrispondenza Tra Target, Proposal E Pesi Di Importanza

Questa derivazione analitica mostra esattamente la convergenza matematica con la teoria dell'__Importance Sampling__:
- La __distribuzione target__ (quella reale da cui vorremmo campionare) è la posterior congiunta $f(x_{0:t}) = bel(x_{0:t})$;
- La __distribuzione proposal__ (quella operativa da cui siamo capaci di campionare ricorsivamente per propagazione stocastica) è la prior congiunta $g(x_{0:t}) = \overline{bel}(x_{0:t})$;
- Il __fattore di importanza analitico__ è il rapporto puntuale tra le due distribuzioni:

$$
w(x_{0:t}) = \frac{f(x_{0:t})}{g(x_{0:t})} = \frac{bel(x_{0:t})}{\overline{bel}(x_{0:t})} = \frac{\eta \, p(z_t \mid x_t) \, \overline{bel}(x_{0:t})}{\overline{bel}(x_{0:t})} = \eta \, p(z_t \mid x_t)
$$

Poiché nelle applicazioni pratiche il fattore di normalizzazione $\eta$ viene calcolato a valle tramite somma empirica sui pesi estratti:

$$
\eta = \left( \sum_{m=1}^M w_t^{[m]} \right)^{-1}
$$

Il peso non normalizzato assegnato a ciascuna particella $m$-esima al passo $t$ coincide esattamente con la verosimiglianza di misura valutata sulla posa corrente:

$$
w_t^{[m]} = p(z_t \mid x_t^{[m]})
$$

### Marginalizzazione E Riduzione Al Filtro Sulla Posa Istantanea

Nelle applicazioni di localizzazione robotica ordinaria, memorizzare l'intera traiettoria $x_{0:t}$ per ciascuna delle $M$ particelle comporterebbe un consumo lineare di memoria $O(M \cdot t)$ che divergerebbe nel tempo.

Poiché il robot necessita esclusivamente di conoscere dove si trova all'istante corrente $t$ per pianificare il controllo, la distribuzione di interesse $bel(x_t)$ si ottiene __marginalizzando__ il belief congiunto rispetto a tutte le pose passate $x_{0:t-1}$:

$$
bel(x_t) = \int \dots \int bel(x_{0:t}) \, \mathrm{d}x_0 \dots \mathrm{d}x_{t-1}
$$

Nell'approssimazione a particelle, questa marginalizzazione corrisponde a un'operazione computazionale a costo zero: è sufficiente __dimenticare la storia passata__ delle particelle e memorizzare unicamente il vettore dello stato corrente $x_t^{[m]}$ per $m = 1, \dots, M$. Ogni particella al passo $t$ è un campione estratto dalla densità marginale corretta $bel(x_t)$.

## Implementazione Industriale Di AMCL in ROS: Analisi Del Codice C Sorgente

Nel framework robotico __ROS / ROS2 (Nav2)__, il package di localizzazione 2D per robot mobili su mappe a griglia è `amcl` (all'interno del repository `ros-planning/navigation`).

L'implementazione in linguaggio C originaria fonde congiuntamente l'adattamento della cardinalità $M$ tramite __KLD-Sampling__ e il recupero dal rapimento tramite __Augmented MCL__. Analizziamo le quattro funzioni e routine cardine del sorgente di `amcl`.

### 1. Calcolo Del Limite Dinamico KLD: `pf_resample_limit`

La funzione `pf_resample_limit(pf_t *pf, int k)` calcola il numero di particelle necessario $n$ dato il numero $k$ di bin non vuoti nell'istogramma KD-Tree:

```c
// Compute the required number of samples, given that there are k
// bins with samples in them. This is taken directly from Fox et al.
int pf_resample_limit(pf_t *pf, int k)
{
    double a, b, c, x;
    int n;
    
    if (k <= 1)
        return pf->max_samples;
        
    a = 1.0;
    b = 2.0 / (9.0 * ((double) k - 1.0));
    c = sqrt(2.0 / (9.0 * ((double) k - 1.0))) * pf->pop_z;
    x = a - b + c;
    
    n = (int) ceil((k - 1.0) / (2.0 * pf->pop_err) * x * x * x);
    
    if (n < pf->min_samples) 
        return pf->min_samples;
    if (n > pf->max_samples) 
        return pf->max_samples;
        
    return n;
}
```

- `pf->pop_err`: corrisponde al parametro $\epsilon$ (`kld_err`, default $0.05$);
- `pf->pop_z`: quantile normale $z_{1-\delta}$ (`kld_z`, default $0.99 \implies 2.326$);
- Il risultato viene saturato tra `min_samples` (default 500) e `max_samples` (default 5000).

### 2. Aggiornamento Pesi E Filtri Esponenziali: `pf_update_sensor`

All'arrivo di una nuova scansione laser, la funzione valuta il modello di verosimiglianza per ciascun campione e aggiorna le medie mobili esponenziali a lungo e breve termine ($w_{\text{slow}}$ e $w_{\text{fast}}$):

```c
void pf_update_sensor(pf_t *pf, pf_sensor_model_fn_t sensor_fn, void *sensor_data)
{
    int i;
    pf_sample_set_t *set;
    pf_sample_t *sample;
    double total = 0.0, w_avg = 0.0;
    
    set = pf->sets + pf->current_set;
    
    // Calcolo del peso e accumulo della somma
    for (i = 0; i < set->sample_count; i++)
    {
        sample = set->samples + i;
        sample->weight = (*sensor_fn)(sensor_data, sample->pose);
        total += sample->weight;
    }
    
    // Normalizzazione dei pesi e calcolo della verosimiglianza media
    for (i = 0; i < set->sample_count; i++)
    {
        sample = set->samples + i;
        w_avg += sample->weight;
        sample->weight /= total;
    }
    w_avg /= set->sample_count;
    
    // Aggiornamento filtri Augmented MCL (Probabilistic Robotics, p. 258)
    if (pf->w_slow == 0.0)
        pf->w_slow = w_avg;
    else
        pf->w_slow += pf->alpha_slow * (w_avg - pf->w_slow);
        
    if (pf->w_fast == 0.0)
        pf->w_fast = w_avg;
    else
        pf->w_fast += pf->alpha_fast * (w_avg - pf->w_fast);
}
```

### 3. Ricampionamento Con Iniezione Casuale: `pf_update_resample`

La funzione genera la nuova popolazione alternando il campionamento proporzionale alla CDF all'iniezione di pose casuali:

```c
void pf_update_resample(pf_t *pf)
{
    pf_sample_set_t *set_a, *set_b;
    pf_sample_t *sample_a, *sample_b;
    double *c, r, w_diff;
    int i;
    
    set_a = pf->sets + pf->current_set;
    set_b = pf->sets + (pf->current_set + 1) % 2;
    
    // Costruzione della tabella di probabilità cumulativa (CDF)
    c = (double *) malloc(sizeof(double) * (set_a->sample_count + 1));
    c[0] = 0.0;
    for (i = 0; i < set_a->sample_count; i++)
        c[i + 1] = c[i] + set_a->samples[i].weight;
        
    // Calcolo della discrepanza tra filtro veloce e lento
    w_diff = 1.0 - pf->w_fast / pf->w_slow;
    if (w_diff < 0.0)
        w_diff = 0.0;
        
    set_b->sample_count = 0;
    
    while (set_b->sample_count < pf->max_samples)
    {
        sample_b = set_b->samples + set_b->sample_count++;
        
        // Iniezione probabilistica di pose casuali nello spazio libero
        if (drand48() < w_diff)
        {
            sample_b->pose = (pf->random_pose_fn)(pf->random_pose_data);
        }
        else
        {
            // Campionamento su CDF
            r = drand48();
            for (i = 0; i < set_a->sample_count; i++)
            {
                if ((c[i] <= r) && (r < c[i + 1]))
                    break;
            }
            sample_a = set_a->samples + i;
            sample_b->pose = sample_a->pose;
        }
        
        sample_b->weight = 1.0;
        // Inserimento nel KD-Tree per determinare k e il limite KLD
        pf_kdtree_insert(set_b->kdtree, sample_b->pose, sample_b->weight);
        
        // Verifica del limite di campioni dinamico KLD
        if (set_b->sample_count > pf_resample_limit(pf, set_b->kdtree->leaf_count))
            break;
    }
    
    // Reset delle medie per evitare derive divergenti
    if (w_diff > 0.0)
        pf->w_slow = pf->w_fast = 0.0;
        
    free(c);
}
```

### 4. Configurazione Dei Parametri in ROS Launch File

Nel file di configurazione (`amcl.launch` o `nav2_params.yaml`) i parametri chiave governano direttamente queste routine:

```xml
<launch>
  <node pkg="amcl" type="amcl" name="amcl" output="screen">
    <!-- Popolazione di particelle adattiva KLD -->
    <param name="min_particles" value="500"/>
    <param name="max_particles" value="5000"/>
    <param name="kld_err" value="0.05"/>
    <param name="kld_z" value="0.99"/>
    
    <!-- Modello odometrico di moto -->
    <param name="odom_model_type" value="diff"/>
    <param name="odom_alpha1" value="0.2"/>
    <param name="odom_alpha2" value="0.2"/>
    <param name="odom_alpha3" value="0.8"/>
    <param name="odom_alpha4" value="0.2"/>
    
    <!-- Modello sensoriale (Likelihood Field preferito) -->
    <param name="laser_model_type" value="likelihood_field"/>
    <param name="laser_z_hit" value="0.95"/>
    <param name="laser_z_rand" value="0.05"/>
    <param name="laser_sigma_hit" value="0.2"/>
    <param name="laser_likelihood_max_dist" value="2.0"/>
    
    <!-- Recupero dal rapimento (Augmented MCL) -->
    <param name="recovery_alpha_slow" value="0.001"/>
    <param name="recovery_alpha_fast" value="0.1"/>
  </node>
</launch>
```

## Dettaglio Analitico Dei Modelli Di Misura Beam E Stima MLE Dei Parametri

Nel [[7. Modelli di Misura per la Localizzazione#Modello a Raggio Fisico (Beam Model)|Capitolo 7]] abbiamo introdotto il modello a fascio composto da quattro distribuzioni. Esplicitiamo qui le formule di normalizzazione analitiche e l'algoritmo di stima dei parametri.

### Normalizzazione Delle Componenti Del Beam Model

Ciascuna densità di probabilità deve integrare a 1 sull'intervallo di misura consentito dal sensore $[0, z_{\max}]$:

1. __Componente Gaussiana Locale ($p_{\text{hit}}$)__:

   $$
   \int_0^{z_{\max}} p_{\text{hit}}(z_k \mid x_t, m) \, \mathrm{d}z_k = 1 \implies \eta_{\text{hit}} = \left( \int_0^{z_{\max}} \frac{1}{\sqrt{2\pi \sigma_{\text{hit}}^2}} \exp\left( - \frac{(z_k - z_t^{k*})^2}{2\sigma_{\text{hit}}^2} \right) \mathrm{d}z_k \right)^{-1}
   $$

   In termini della funzione errore gaussiana $\text{erf}(\cdot)$:

   $$
   \eta_{\text{hit}} = \left[ \frac{1}{2} \left( \text{erf}\left(\frac{z_{\max} - z_t^{k*}}{\sqrt{2}\sigma_{\text{hit}}}\right) - \text{erf}\left(\frac{-z_t^{k*}}{\sqrt{2}\sigma_{\text{hit}}}\right) \right) \right]^{-1}
   $$

2. __Componente Esponenziale per Ostacoli Imprevisti ($p_{\text{short}}$)__:

   $$
   \int_0^{z_t^{k*}} \eta_{\text{short}} \lambda_{\text{short}} \mathrm{e}^{-\lambda_{\text{short}} z_k} \, \mathrm{d}z_k = 1 \implies \eta_{\text{short}} = \frac{1}{1 - \mathrm{e}^{-\lambda_{\text{short}} z_t^{k*}}}
   $$

### Stima Dei Parametri Tramite Algoritmo Expectation-Maximization (EM)

Sia dato un dataset di calibrazione formato da $J$ misurazioni note in cui il robot si trova in pose note: $Z = \{z_j\}_{j=1}^J$ con valori ideali attesi $Z^* = \{z_j^*\}_{j=1}^J$. Vogliamo stimare i pesi $\mathbf{\alpha} = (\alpha_{\text{hit}}, \alpha_{\text{short}}, \alpha_{\text{max}}, \alpha_{\text{rand}})^T$ e i parametri $\sigma_{\text{hit}}, \lambda_{\text{short}}$.

Poiché per ciascuna lettura $z_j$ non conosciamo a quale dei quattro fenomeni fisici sia imputabile, introduciamo quattro variabili indicatrici latenti binarie $\mathbf{e}_j = [e_{j,\text{hit}}, e_{j,\text{short}}, e_{j,\text{max}}, e_{j,\text{rand}}]^T \in \{0, 1\}^4$ tali che $\sum_i e_{j,i} = 1$.

L'algoritmo EM itera due passi fino a convergenza:

1. __Expectation Step (E-step)__: calcolo delle responsabilità a posteriori per ogni misura $j$:

   $$
   \gamma_{j,i} = \mathbb{E}[e_{j,i}] = \frac{\alpha_i \, p_i(z_j \mid z_j^*)}{\sum_{k \in \{\text{hit},\text{short},\text{max},\text{rand}\}} \alpha_k \, p_k(z_j \mid z_j^*)}
   $$

2. __Maximization Step (M-step)__: aggiornamento in forma chiusa dei parametri:
   - Aggiornamento dei pesi di miscela:

     $$
     \alpha_i = \frac{1}{J} \sum_{j=1}^J \gamma_{j,i}
     $$

   - Aggiornamento della deviazione standard del rumore di misura:

     $$
     \sigma_{\text{hit}} = \sqrt{ \frac{\sum_{j=1}^J \gamma_{j,\text{hit}} (z_j - z_j^*)^2}{\sum_{j=1}^J \gamma_{j,\text{hit}}} }
     $$

   - Aggiornamento del parametro di decadimento esponenziale:

     $$
     \lambda_{\text{short}} = \frac{\sum_{j=1}^J \gamma_{j,\text{short}}}{\sum_{j=1}^J \gamma_{j,\text{short}} \, z_j}
     $$

Questo ciclo converge a un massimo locale della log-verosimiglianza del dataset di calibrazione, fornendo una taratura statisticamente fondata per il modello sensoriale del veicolo.

## Derivazione Formale Del Filtro Di Kalman Lineare Dalla Teoria Bayesiana

Nel [[8. Filtro di Kalman Lineare#Interpretazione Bayesiana del Filtro di Kalman|Capitolo 8]] abbiamo enunciato le formule di aggiornamento del Filtro di Kalman. Riportiamo qui la derivazione analitica rigorosa basata sul completamento del quadrato matriciale e sulla minimizzazione dell'errore quadratico medio.

### Passo Di Correzione: Completamento Del Quadrato Matriciale

Sia dato il belief a priori:

$$
\overline{bel}(x_t) = \frac{1}{(2\pi)^{n/2} |P_{t|t-1}|^{1/2}} \exp\left( -\frac{1}{2} (x_t - \hat{x}_{t|t-1})^T P_{t|t-1}^{-1} (x_t - \hat{x}_{t|t-1}) \right)
$$

e la verosimiglianza di misura lineare $y_t = C_t x_t + v_t$:

$$
p(y_t \mid x_t) = \frac{1}{(2\pi)^{p/2} |R_t|^{1/2}} \exp\left( -\frac{1}{2} (y_t - C_t x_t)^T R_t^{-1} (y_t - C_t x_t) \right)
$$

La posterior bayesiana non normalizzata ha all'esponente la forma quadratica:

$$
J(x_t) = (x_t - \hat{x}_{t|t-1})^T P_{t|t-1}^{-1} (x_t - \hat{x}_{t|t-1}) + (y_t - C_t x_t)^T R_t^{-1} (y_t - C_t x_t)
$$

Espandendo i prodotti matriciali:

$$
J(x_t) = x_t^T P_{t|t-1}^{-1} x_t - 2 x_t^T P_{t|t-1}^{-1} \hat{x}_{t|t-1} + \hat{x}_{t|t-1}^T P_{t|t-1}^{-1} \hat{x}_{t|t-1} + x_t^T C_t^T R_t^{-1} C_t x_t - 2 x_t^T C_t^T R_t^{-1} y_t + y_t^T R_t^{-1} y_t
$$

Raggruppiamo i termini quadratici e lineari in $x_t$:

$$
J(x_t) = x_t^T \underbrace{\left( P_{t|t-1}^{-1} + C_t^T R_t^{-1} C_t \right)}_{P_{t|t}^{-1}} x_t - 2 x_t^T \underbrace{\left( P_{t|t-1}^{-1} \hat{x}_{t|t-1} + C_t^T R_t^{-1} y_t \right)}_{\mathbf{b}_t} + \text{costante}
$$

Dall'algebra delle gaussiane multivariate, se l'esponente ha forma $x_t^T P_{t|t}^{-1} x_t - 2 x_t^T \mathbf{b}_t$, la matrice di covarianza a posteriori vale:

$$
P_{t|t} = \left( P_{t|t-1}^{-1} + C_t^T R_t^{-1} C_t \right)^{-1}
$$

e la media a posteriori è:

$$
\hat{x}_{t|t} = P_{t|t} \, \mathbf{b}_t = P_{t|t} \left( P_{t|t-1}^{-1} \hat{x}_{t|t-1} + C_t^T R_t^{-1} y_t \right)
$$

### Equivalenza Con Il Guadagno Di Kalman Tramite Il Lemma Di Inversione Di Woodbury

Applicando l'identità matriciale di Woodbury all'inversa della covarianza:

$$
(A + B C D)^{-1} = A^{-1} - A^{-1} B (C^{-1} + D A^{-1} B)^{-1} D A^{-1}
$$

Ponendo $A = P_{t|t-1}^{-1}$, $B = C_t^T$, $C = R_t^{-1}$, $D = C_t$:

$$
P_{t|t} = P_{t|t-1} - P_{t|t-1} C_t^T \left( R_t + C_t P_{t|t-1} C_t^T \right)^{-1} C_t P_{t|t-1}
$$

Definendo la covarianza dell'innovazione $S_t = C_t P_{t|t-1} C_t^T + R_t$ e il guadagno ottimo $L_t = P_{t|t-1} C_t^T S_t^{-1}$:

$$
P_{t|t} = P_{t|t-1} - L_t C_t P_{t|t-1} = (I - L_t C_t) P_{t|t-1}
$$

Sostituendo nell'espressione della media a posteriori $\hat{x}_{t|t}$:

$$
\hat{x}_{t|t} = \hat{x}_{t|t-1} + L_t \left( y_t - C_t \hat{x}_{t|t-1} \right)
$$

Questo completa la dimostrazione analitica dell'equivalenza esatta tra il teorema di Bayes e le equazioni del filtro di Kalman.

### Minimizzazione Della Varianza dell'Errore E Derivazione Di $L_t$

Consideriamo uno stimatore lineare generico con guadagno $L_t$ arbitrario:

$$
\hat{x}_{t|t} = \hat{x}_{t|t-1} + L_t (y_t - C_t \hat{x}_{t|t-1})
$$

L'errore a posteriori $\tilde{x}_{t|t} = x_t - \hat{x}_{t|t}$ evolve come:

$$
\tilde{x}_{t|t} = (I - L_t C_t) \tilde{x}_{t|t-1} - L_t v_t
$$

Calcolando la covarianza d'errore (forma di Joseph, valida per qualsiasi $L_t$):

$$
P_{t|t} = (I - L_t C_t) P_{t|t-1} (I - L_t C_t)^T + L_t R_t L_t^T
$$

Vogliamo trovare la matrice $L_t$ che minimizza l'errore quadratico medio $\mathbb{E}[\|\tilde{x}_{t|t}\|^2] = \text{Tr}(P_{t|t})$.

Calcoliamo la derivata matriciale rispetto a $L_t$ sfruttando le identità $\frac{\partial}{\partial X} \text{Tr}(X A X^T) = 2 X A$ e $\frac{\partial}{\partial X} \text{Tr}(A X B) = A^T B^T$:

$$
\frac{\partial \text{Tr}(P_{t|t})}{\partial L_t} = -2 P_{t|t-1} C_t^T + 2 L_t \left( C_t P_{t|t-1} C_t^T + R_t \right)
$$

Ponendo il gradiente uguale a zero:

$$
-2 P_{t|t-1} C_t^T + 2 L_t \left( C_t P_{t|t-1} C_t^T + R_t \right) = 0
$$

$$
L_t \left( C_t P_{t|t-1} C_t^T + R_t \right) = P_{t|t-1} C_t^T
$$

Poiché $R_t > 0$ e $P_{t|t-1} \ge 0$, la matrice $S_t = C_t P_{t|t-1} C_t^T + R_t$ è simmetrica strettamente definita positiva e dunque invertibile:

$$
L_t = P_{t|t-1} C_t^T \left( C_t P_{t|t-1} C_t^T + R_t \right)^{-1}
$$

La matrice $L_t$ del filtro di Kalman è dunque dimostrabilmente il minimizzatore globale unico della varianza d'errore di stima.

## Esempio Didattico Di Localizzazione 1D Con Extended Kalman Filter

Nelle lezioni 14 e 15 (lucidi 41–43) viene introdotto un modello di benchmark unidimensionale che permette di comprendere l'impatto della linearizzazione dell'EKF nel caso più semplice possibile, isolando la non-linearità della misura senza le complessità trigonometriche dello spazio $SE(2)$.

Questo modello costituisce il riferimento teorico diretto per la classe software `ExtendedKalmanFilter1D` implementata in `scripts_python/Particle_gemini_lecture_v4.py`.

### Cinematica Scalare E Modello Di Misura Range-Only

Consideriamo un robot vincolato a muoversi lungo un binario rettilineo o un corridoio 1D coordinato da $x \in [0, L]$.

Il comando di controllo è una traslazione $u = u_x$. Il moto reale è corrotto da un disturbo gaussiano additivo a media nulla con varianza $\sigma_x^2$:

$$
x_t = x_{t-1} + u_x + \nu_t, \quad \nu_t \sim \mathcal{N}\left(0, \sigma_x^2\right)
$$

Poiché la cinematica è strettamente lineare, le derivate del moto rispetto allo stato e al controllo sono banali:

$$
F_x = \frac{\partial f}{\partial x} = 1, \qquad F_u = \frac{\partial f}{\partial u} = 1
$$

Il passo di predizione propaga quindi la media e la varianza in forma esatta:

$$
\hat{x}_{t|t-1} = \hat{x}_{t-1|t-1} + u_x
$$

$$
P_{t|t-1} = P_{t-1|t-1} + \sigma_x^2
$$

L'ambiente contiene un insieme di beacon puntiformi noti situati a coordinate fisse $m_j$ ($j = 1, \dots, M$). Il robot dispone di un sensore di distanza (telemetro o ricevitore ToF) che misura la distanza euclidea assoluta dal beacon $m_1$:

$$
z_{1,t} = \|x_{r,t} - m_1\| + \mu_t = |x_{r,t} - m_1| + \mu_t = \sqrt{(x_{r,t} - m_1)^2} + \mu_t
$$

con $\mu_t \sim \mathcal{N}(0, \sigma_z^2)$.

### Linearizzazione Del Modulo E Gestione Della Singolarità

La funzione di misura è $h(x) = |x - m_1|$. Questa funzione è continua ovunque ma presenta un punto angoloso (non derivabile nel senso classico) in $x = m_1$.

Per applicare l'Extended Kalman Filter calcoliamo lo Jacobiano di misura valutato nella stima a priori $\hat{x}_{t|t-1}$:

$$
H_x = \left.\frac{\partial h}{\partial x}\right|_{x = \hat{x}_{t|t-1}} = \left.\frac{\partial |x - m_1|}{\partial x}\right|_{x = \hat{x}_{t|t-1}} = \operatorname{sgn}\left(\hat{x}_{t|t-1} - m_1\right) = \frac{\hat{x}_{t|t-1} - m_1}{|\hat{x}_{t|t-1} - m_1|}
$$

Si presentano due regimi operativi distinti:
1. __Robot a destra del beacon__ ($\hat{x}_{t|t-1} > m_1$):
   $$H_x = +1$$
   All'aumentare di $x$, la distanza dal beacon aumenta;
2. __Robot a sinistra del beacon__ ($\hat{x}_{t|t-1} < m_1$):
   $$H_x = -1$$
   All'aumentare di $x$, la distanza dal beacon diminuisce.

Nel punto esatto di coincidenza $\hat{x}_{t|t-1} = m_1$, la derivata classica non esiste. Nel calcolo numerico si adotta la convenzione del subgradiente scegliendo un valore all'interno dell'intervallo $[-1, +1]$:

$$
\partial |x - m_1| \Big|_{x=m_1} \in [-1, +1]
$$

Nel software si imposta una soglia di tolleranza $|\hat{x} - m_1| < 10^{-6}$ associando convenzionalmente il gradiente destro $H_x = +1.0$ per evitare divisioni per zero o instabilità computazionali.

### Equazioni Di Correzione Scalare E Forma Di Joseph

Calcoliamo l'innovazione scalare della misura:

$$
\tilde{y}_t = z_{1,t} - h\left(\hat{x}_{t|t-1}\right) = z_{1,t} - |\hat{x}_{t|t-1} - m_1|
$$

La varianza dell'innovazione $S_t$ vale:

$$
S_t = H_x P_{t|t-1} H_x^T + \sigma_z^2 = H_x^2 P_{t|t-1} + \sigma_z^2
$$

Poiché $H_x = \pm 1$, abbiamo $H_x^2 = 1$ indipendentemente da quale lato del beacon si trovi il robot:

$$
S_t = P_{t|t-1} + \sigma_z^2
$$

Il guadagno di Kalman scalare $K_t$ assume l'espressione:

$$
K_t = P_{t|t-1} H_x S_t^{-1} = \frac{P_{t|t-1} \operatorname{sgn}\left(\hat{x}_{t|t-1} - m_1\right)}{P_{t|t-1} + \sigma_z^2}
$$

Osserviamo il comportamento fisico del segno del guadagno $K_t$:
- Se il robot è a destra del beacon ($H_x = +1$) e misura una distanza superiore all'attesa ($\tilde{y}_t > 0$), il robot è più a destra di quanto stimato: $K_t > 0$ e la stima viene incrementata verso destra ($\hat{x} \uparrow$);
- Se il robot è a sinistra del beacon ($H_x = -1$) e misura una distanza superiore all'attesa ($\tilde{y}_t > 0$), il robot si trova in realtà più a sinistra: $K_t < 0$, dunque $K_t \tilde{y}_t < 0$ e la stima viene decrementata verso sinistra ($\hat{x} \downarrow$).

L'aggiornamento dello stato a posteriori è:

$$
\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t \tilde{y}_t
$$

L'aggiornamento della varianza d'errore (forma standard):

$$
P_{t|t} = (1 - K_t H_x) P_{t|t-1} = \left( 1 - \frac{P_{t|t-1} H_x^2}{P_{t|t-1} + \sigma_z^2} \right) P_{t|t-1} = \frac{P_{t|t-1} \sigma_z^2}{P_{t|t-1} + \sigma_z^2}
$$

Notiamo che la riduzione di incertezza $P_{t|t} < P_{t|t-1}$ è identica su entrambi i lati del beacon, riflettendo la simmetria geometrica dell'informazione sensoriale.

Per garantire incondizionatamente la semidefinita positività numerica nei calcoli a virgola mobile, si impiega la forma simmetrica stabilizzata di Joseph:

$$
P_{t|t} = (1 - K_t H_x)^2 P_{t|t-1} + K_t^2 \sigma_z^2
$$

### Estensione A Più Beacon E Connessione Al Codice Python

Quando sono visibili simultaneamente $M$ beacon $m = [m_1, \dots, m_M]^T$, le misure compongono un vettore $z_t \in \mathbb{R}^M$.

Il modello di misura vettoriale diviene:

$$
h(x) = \begin{bmatrix} |x - m_1| \\ \vdots \\ |x - m_M| \end{bmatrix}, \qquad H_x = \begin{bmatrix} \operatorname{sgn}(x - m_1) \\ \vdots \\ \operatorname{sgn}(x - m_M) \end{bmatrix} \in \mathbb{R}^{M \times 1}
$$

La matrice di covarianza d'innovazione $S_t \in \mathbb{R}^{M \times M}$ e il vettore di guadagno $K_t \in \mathbb{R}^{1 \times M}$ valgono:

$$
S_t = P_{t|t-1} (H_x H_x^T) + \operatorname{diag}\left(\sigma_{z,1}^2, \dots, \sigma_{z,M}^2\right)
$$

$$
K_t = P_{t|t-1} H_x^T S_t^{-1}
$$

La distanza di Mahalanobis quadratica associata a ciascun beacon $j$ corrisponde alla componente normalizzata:

$$
\mu_j = \frac{\tilde{y}_j^2}{S_{jj}} = \frac{\left(z_{j,t} - |\hat{x}_{t|t-1} - m_j|\right)^2}{P_{t|t-1} + \sigma_{z,j}^2}
$$

Questa formulazione matriciale scalare-vettore è implementata integralmente nel metodo `passo_correzione` della classe `ExtendedKalmanFilter1D` in `scripts_python/Particle_gemini_lecture_v4.py`, garantendo perfetta consistenza teorica ed efficienza computazionale $O(M^3)$ (con $M$ pari al numero di beacon, tipicamente $M=2$, dunque istantaneo).

