# zz. Argomenti extra

Questo documento raccoglie dimostrazioni, approfondimenti matematici e argomenti collaterali utili alla comprensione completa degli argomenti del corso di *Autonomous Robotics*, ma non strettamente richiesti come parte teorica principale d'esame.

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

Nelle Unità di Misura Inerziali (trattate in [[2. Sensori per la Robotica Mobile#Unità Di Misura Inerziale (IMU)|2. Sensori per la Robotica Mobile]]), la stima della posizione mediante navigazione inerziale pura (*dead reckoning*) richiede la doppia integrazione delle accelerazioni lineari depurate dalla gravità:

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

L'errore angolare nel giroscopio provoca quindi una deriva di posizione che cresce addirittura come **$O(t^3)$** a causa dell'accoppiamento con la gravità.

### Bias Costante Dell'Accelerometro E Deriva Quadratica $O(t^2)$

Se consideriamo invece un bias residuo costante proprio dell'accelerometro $\Delta a_{\text{bias}}$ (anche assumendo l'orientamento perfettamente noto):

$$
\Delta p(t) = \int_{0}^{t} \int_{0}^{\tau} \Delta a_{\text{bias}} \, ds \, d\tau = \frac{1}{2} \Delta a_{\text{bias}} \, t^2
$$

L'errore di posizione cresce in modo rigorosamente **quadratico $O(t^2)$**.

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

Nelle applicazioni aerospaziali e nei veicoli autonomi ad alta affidabilità si impiegano i giroscopi a fibra ottica (**FOG**, *Fiber Optic Gyro*, come il sensore KVH 1750 citato nel capitolo principale). 

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
1. **Incertezza quadratica con la distanza**: l'errore di profondità cresce con il quadrato della distanza $Z^2$.
2. **Ruolo della baseline $b$**: aumentando la distanza tra le telecamere $b$ si riduce l'errore a lungo raggio, ma aumenta il volume minimo cieco vicino al robot (*blind zone*) e la difficoltà di trovare corrispondenze di feature visive (corrispondenza stereo).

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

Poiché le incognite dello stato da stimare sono **quattro**:

$$
\mathbf{s} = [x, \; y, \; z, \; c \cdot \delta t_{\text{rx}}]^T
$$

è geometricamente indispensabile ricevere contemporaneamente il segnale da un numero di satelliti:

$$
n_{\text{sat}} \ge 4
$$

Risolvendo il sistema non lineare con algoritmi di minimizzazione ai minimi quadrati iterati (Gauss-Newton o Filtro di Kalman esteso), il ricevitore stima contemporaneamente la posizione tridimensionale metrica $(x, y, z)$ e sincronizza perfettamente il proprio orologio locale con il tempo atomico GPS.

### Principio Operativo Dell'RTK (Real Time Kinematic)

Nelle applicazioni di robotica agricola o veicolare (come la piattaforma Agrobot di ISARLab), la precisione metrica standard di $3 - 5\text{ m}$ è insufficiente per condurre un veicolo tra i filari. Si impiega pertanto la tecnologia **RTK (Real Time Kinematic)**.

Il sistema RTK prevede:
1. Una **Stazione Base fissa** a terra, installata su un punto geodetico di coordinate millimetriche note.
2. Il **Rover mobile** montato a bordo del robot.

Anziché limitarsi a decodificare i bit del codice pseudo-casuale (PRN) del segnale, i ricevitori RTK tracciano la **fase dell'onda portante radio** a frequenza $L_1 = 1575.42\text{ MHz}$, la cui lunghezza d'onda nello spazio vale appena:

$$
\lambda = \frac{c}{f} = \frac{3 \times 10^8\text{ m/s}}{1.57542 \times 10^9\text{ Hz}} \approx 19.03\text{ cm}
$$

Misurando lo sfasamento della frazione di ciclo dell'onda con risoluzione inferiore all'1%, e risolvendo in tempo reale il problema dell'__ambiguità intera di fase__ (il numero intero incognito $N$ di cicli d'onda completi interposti tra satellite e antenna mediante tecniche a doppie differenze tra Base e Rover), il sistema cancella quasi integralmente gli errori atmosferici e di satellite comuni. 

La stima della posizione relativa del rover rispetto alla base fissa raggiunge un'accuratezza cinematica istantanea nell'ordine di **$1\text{ centimetro}$**.

## Parametri Metrologici Avanzati E Fisica Dei Sensori

Questa sezione approfondisce le definizioni metrologiche e i modelli fisici accennati nell'[[2. Sensori per la Robotica Mobile#Appendice: Caratteristiche Metrologiche E Sensori Fisici|Appendice della Lezione 5]].

### Quantificazione Del Dynamic Range In Decibel

Il range dinamico descrive la capacità del sensore di misurare contemporaneamente segnali di debole intensità e segnali di fondo scala senza saturazione:

- **Per grandezze energetiche o di potenza** (ad esempio l'intensità luminosa catturata dai fotodiodi del LiDAR o la potenza dei segnali RF):
  
  $$
  \text{DR}_{\text{power}} = 10 \log_{10} \left( \frac{P_{\max}}{P_{\min}} \right) \quad [\text{dB}]
  $$

- **Per grandezze di ampiezza, tensione o campo** (tensioni dei piezometri, segnali elettrici dei ponti di Wheatstone):
  
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

1. **Distorsione Hard-Iron**: generata da corpi ferromagnetici permanentemente magnetizzati montati a bordo del robot (altoparlanti, viti ferrose, telaio in acciaio, magneti permanenti dei motori DC). Produce un campo magnetico costante $\mathbf{b}_{\text{hard}}$ solidale alla terna del robot che trasla il centro della circonferenza:
   
   $$\mathbf{B}_{\text{misurato}} = \mathbf{B}_{\text{reale}} + \mathbf{b}_{\text{hard}}$$

2. **Distorsione Soft-Iron**: generata da materiali ad alta permeabilità magnetica passivi (ferro dolce, schermature metalliche, piste di rame con correnti variabili) che deflettono e comprimono le linee di flusso del campo magnetico esterno a seconda dell'orientamento. È descritta da una matrice di deformazione $3 \times 3$ simmetrica $M_{\text{soft}}$, che deforma la circonferenza in un'ellisse inclinata.

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

I giroscopi miniaturizzati realizzati con tecnologia microelettro-meccanica (MEMS) non possono includere rotori rotanti ad alta velocità a causa dell'usura per attrito e dei limiti di fabbricazione microscopica. Sfruttano invece **strutture oscillanti risonanti** (diapason, pettini elettrostatici capacitivi o campane semisferiche al silicio).

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

$$
F_{c,y}(t) = -2m \, \Omega_z \, v_x(t)
$$

Questa forza ciclica induce un'oscillazione secondaria lungo l'asse $y$. La deflessione ortogonale viene misurata con elevata sensibilità rilevando la variazione differenziale di capacità $\Delta C$ tra elettrodi microscopici a pettine, fornendo un segnale di tensione proporzionale alla velocità angolare esterna $\Omega_z$.

