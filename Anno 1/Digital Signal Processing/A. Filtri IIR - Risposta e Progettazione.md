# A. Filtri IIR - Risposta e Progettazione

Questo capitolo analizza la risposta dinamica dei filtri IIR nel dominio del tempo e della frequenza, approfondendo le metodologie di progettazione basate sul posizionamento geometrico di poli e zeri sul piano complesso Z per filtri del primo ordine (smoother), risuonatori del secondo ordine, equalizzatori parametrici, filtri notch e filtri a pettine.

## Risposta Sinusoidale a Regime

Data una sinusoide complessa persistente a frequenza angolare $\omega_0$:

$$
x(n) = \mathrm{e}^{j\omega_0 n}, \quad -\infty < n < +\infty
$$

applicando la convoluzione lineare con la risposta impulsiva $h(n)$ di un filtro IIR stabile:

$$
\begin{align}
y(n) &= \sum_{m=-\infty}^{\infty} h(m) x(n-m) = \sum_{m=-\infty}^{\infty} h(m) \mathrm{e}^{j\omega_0 (n-m)} \\
&= \mathrm{e}^{j\omega_0 n} \underbrace{\sum_{m=-\infty}^{\infty} h(m) \mathrm{e}^{-j\omega_0 m}}_{\text{DTFT } H(\omega_0)} = H(\omega_0) \mathrm{e}^{j\omega_0 n}
\end{align}
$$

L'uscita a regime permanente ha la medesima frequenza dell'ingresso, con ampiezza riscaldata dal modulo $|H(\omega_0)|$ e fase traslata di $\arg H(\omega_0)$:

$$
y(n) = |H(\omega_0)| \mathrm{e}^{j\left(\omega_0 n + \arg H(\omega_0)\right)}
$$

### Ritardo di Fase e Ritardo di Gruppo

Lo sfasamento introdotto dal filtro si traduce in un ritardo temporale:
- Il __ritardo di fase__ $d(\omega)$ misura il ritardo temporale subito dalla portante sinusoidale a frequenza $\omega$:
  $$d(\omega) = -\frac{\arg H(\omega)}{\omega} \iff \arg H(\omega) = -\omega d(\omega)$$
- Il __ritardo di gruppo__ $d_g(\omega)$ misura il ritardo temporale subito dall'inviluppo di modulazione di un pacchetto d'onda a banda stretta:
  $$d_g(\omega) = -\frac{\mathrm{d}}{\mathrm{d}\omega} \arg H(\omega)$$

Nei filtri FIR simmetrici il ritardo è rigorosamente indipendente dalla frequenza ($d(\omega) = d_g(\omega) = D = \frac{N-1}{2}$), garantendo perfetta linearità della fase:

$$
\mathrm{e}^{j\omega n} \xrightarrow{\mathcal{H}} |H(\omega)| \mathrm{e}^{j\omega (n - D)}
$$

Nel caso dei filtri IIR, non è matematicamente possibile ottenere una fase perfettamente lineare sull'intero intervallo di Nyquist $[-\pi, \pi]$. È tuttavia possibile progettare filtri IIR che approssimino una fase lineare limitatamente alla banda passante (come i filtri a ritardo massimamente piatto di Bessel).

## Risposta al Transitorio e Stabilità

Nel mondo reale ogni segnale viene applicato a partire da un istante iniziale ($n = 0$). L'ingresso sinusoidale è quindi causale:

$$
x(n) = \mathrm{e}^{j\omega_0 n} u(n) \xrightarrow{\mathcal{Z}} X(z) = \frac{1}{1 - \mathrm{e}^{j\omega_0} z^{-1}}, \quad \text{ROC: } |z| > 1
$$

Dato un filtro IIR causale e stabile con $M$ poli strettamente interni al cerchio unitario ($|p_i| < 1$):

$$
H(z) = \frac{N(z)}{(1 - p_1 z^{-1})(1 - p_2 z^{-1}) \dots (1 - p_M z^{-1})}
$$

La trasformata Z dell'uscita è:

$$
Y(z) = H(z) X(z) = \frac{N(z)}{\left(1 - \mathrm{e}^{j\omega_0} z^{-1}\right) \prod_{i=1}^{M} (1 - p_i z^{-1})}
$$

Scomponendo in fratti parziali:

$$
Y(z) = \frac{C}{1 - \mathrm{e}^{j\omega_0} z^{-1}} + \sum_{i=1}^{M} \frac{B_i}{1 - p_i z^{-1}}
$$

Il residuo $C$ associato al polo del segnale vale:

$$
C = \left[ (1 - \mathrm{e}^{j\omega_0} z^{-1}) Y(z) \right]_{z = \mathrm{e}^{j\omega_0}} = H(\mathrm{e}^{j\omega_0}) = H(\omega_0)
$$

Antitrasformando causalmente per $n \ge 0$:

$$
y(n) = \underbrace{H(\omega_0) \mathrm{e}^{j\omega_0 n}}_{\text{risposta a regime permanente}} + \underbrace{\sum_{i=1}^{M} B_i p_i^n}_{\text{risposta transitoria}}
$$

Poiché tutti i poli del filtro soddisfano $|p_i| < 1$, i termini $p_i^n$ decadono esponenzialmente a zero per $n \to \infty$:

$$
y(n) \to H(\omega_0) \mathrm{e}^{j\omega_0 n} \quad \text{per } n \to \infty
$$

Se anche un solo polo cadesse all'esterno del cerchio unitario ($|p_k| > 1$), il termine corrispondente $p_k^n$ divergerebbe esponenzialmente, rendendo il sistema incontrollabile e instabile.

### Costante Temporale Effettiva

La durata temporale del transitorio è determinata dal polo che decade più lentamente, ossia quello avente modulo massimo (__polo dominante__):

$$
\rho = \max_{i} |p_i|
$$

Fissata una soglia percentuale di tolleranza $\varepsilon$ (tipicamente l'1%, $\varepsilon = 0.01$), la __durata effettiva del transitorio__ $n_{\text{eff}}$ (numero di campioni necessari affinché il transitorio scenda al di sotto di $\varepsilon$) si ricava da:

$$
\rho^{n_{\text{eff}}} = \varepsilon \implies n_{\text{eff}} = \frac{\ln \varepsilon}{\ln \rho} = \frac{\ln(1/\varepsilon)}{\ln(1/\rho)}
$$

Più il polo dominante si avvicina alla circonferenza unitaria ($\rho \to 1$), più la costante temporale cresce e più lungo sarà il tempo di assestamento del filtro.

## Filtri di Primo Ordine (Smoother)

I filtri di primo ordine (smoother) costituiscono i blocchi passa-basso o passa-alto elementari con un singolo polo e un singolo zero a valori reali:

$$
H(z) = \frac{G(1 + b z^{-1})}{1 - a z^{-1}}
$$

dove $a$ è la posizione del polo ($0 < a < 1$ per stabilità causale) e $b$ è la posizione dello zero.

Valutando la risposta in frequenza alle pulsazioni estreme dell'intervallo di Nyquist ($z = \mathrm{e}^{j0} = 1$ e $z = \mathrm{e}^{j\pi} = -1$):

$$
H(0) = \frac{G(1 + b)}{1 - a}
$$

$$
H(\pi) = \frac{G(1 - b)}{1 + a}
$$

Il rapporto di attenuazione tra la massima frequenza ($\pi$) e la frequenza continua ($0$) vale:

$$
\frac{H(\pi)}{H(0)} = \frac{(1 - b)(1 - a)}{(1 + b)(1 + a)}
$$

> [!EXAMPLE] Progetto di uno Smoother Passa-Basso
> Assegnate le specifiche:
> 1. Durata del transitorio: $n_{\text{eff}} = 20$ campioni con soglia $\varepsilon = 0.01$;
> 2. Rapporto di attenuazione: $\frac{H(\pi)}{H(0)} = \frac{1}{21}$.
> 
> Calcolo del polo $a$:
> 
> $$
> a = \varepsilon^{1/n_{\text{eff}}} = (0.01)^{1/20} \approx 0.8
> $$
> 
> Calcolo dello zero $b$:
> 
> $$
> \frac{(1 - b)(1 - 0.8)}{(1 + b)(1 + 0.8)} = \frac{1}{21} \implies \frac{0.2(1 - b)}{1.8(1 + b)} = \frac{1}{21} \implies b = 0.4
> $$
> 
> La funzione di trasferimento risultante è:
> 
> $$
> H(z) = \frac{G(1 + 0.4z^{-1})}{1 - 0.8z^{-1}}
> $$
> 
> Esplicitando la relazione tra le trasformate $Y(z) = H(z) X(z)$:
> 
> $$
> (1 - 0.8z^{-1}) Y(z) = G(1 + 0.4z^{-1}) X(z)
> $$
> 
> Antitrasformando nel dominio temporale si ottiene l'equazione alle differenze:
> 
> $$
> y(n) = 0.8y(n-1) + G\left(x(n) + 0.4x(n-1)\right)
> $$
> 
> Questa struttura richiede solo 3 moltiplicazioni e accumuli (__MACS__) per ciascun campione elaborato.

## Filtri di Secondo Ordine (Resonator)

I filtri __resonator__ di secondo ordine presentano una risposta in frequenza dominata da un picco risonante a una specifica frequenza nominale $\omega_0$:

![[immagini/resonator 1.png|center mid]]

Per posizionare la risonanza a $\omega = \omega_0$, si colloca una coppia di poli complessi coniugati sul piano Z a raggio $R$ ($0 < R < 1$):

$$
p = R \mathrm{e}^{j\omega_0}, \quad p^* = R \mathrm{e}^{-j\omega_0}
$$

La funzione di trasferimento è:

$$
H(z) = \frac{G}{(1 - R \mathrm{e}^{j\omega_0} z^{-1})(1 - R \mathrm{e}^{-j\omega_0} z^{-1})} = \frac{G}{1 + a_1 z^{-1} + a_2 z^{-2}}
$$

I coefficienti del denominatore si ricavano direttamente dalle relazioni trigonometriche:

$$
a_1 = -2R \cos\omega_0, \quad a_2 = R^2
$$

### Calcolo del Guadagno di Normalizzazione $G$

Per normalizzare il picco di risonanza al guadagno unitario ($|H(\omega_0)| = 1$, corrispondente a $0\text{ dB}$):

$$
|H(\omega_0)| = \frac{G}{|(1 - R)(1 - R \mathrm{e}^{-2j\omega_0})|} = 1
$$

da cui si ricava la formula analitica per il guadagno $G$:

$$
G = (1 - R) \sqrt{1 - 2R \cos(2\omega_0) + R^2}
$$

### Risposta in Modulo e Larghezza di Banda a 3 dB

Il modulo quadro della risposta in frequenza è espresso da:

$$
|H(\omega)|^2 = \frac{G^2}{\left(1 - 2R \cos(\omega - \omega_0) + R^2\right) \left(1 - 2R \cos(\omega + \omega_0) + R^2\right)}
$$

La __larghezza di banda a metà potenza__ (frequenze a $-3\text{ dB}$, $\Delta\omega = \omega_2 - \omega_1$) è definita dalla condizione:

$$
|H(\omega)|^2 = \frac{1}{2} |H(\omega_0)|^2 = \frac{1}{2} \iff 20 \log_{10} \left| \frac{H(\omega)}{H(\omega_0)} \right| = -3\text{ dB}
$$

Per poli sufficientemente vicini al cerchio unitario ($R \approx 1$), la larghezza di banda è legata al raggio $R$ dalla relazione approssimata:

$$
\Delta\omega \simeq 2(1 - R)
$$

> [!IMPORTANT] Compromesso Risoluzione - Transitorio nel Resonator
> Più il raggio $R$ si avvicina a $1$:
> - Più la larghezza di banda $\Delta\omega$ si restringe, rendendo il picco risonante selettivo;
> - Più la costante temporale del transitorio $n_{\text{eff}}$ aumenta, rendendo lenta la risposta a variazioni dell'ingresso.

### Risposta Impulsiva ed Equazione alle Differenze

La risposta impulsiva causale analitica del risuonatore è:

$$
h(n) = \frac{G}{\sin\omega_0} R^n \sin(\omega_0 n + \omega_0), \quad n \ge 0
$$

L'equazione alle differenze ricorsiva per il calcolo in tempo reale è:

$$
y(n) = -a_1 y(n-1) - a_2 y(n-2) + G x(n)
$$

> [!EXAMPLE] Progetto Numerico di un Risuonatore
> Dati di specifica: frequenza di risonanza $f_0 = 500\text{ Hz}$, larghezza di banda $\Delta f = 32\text{ Hz}$, frequenza di campionamento $f_s = 10\text{ kHz}$.
> 
> Calcolo delle frequenze normalizzate:
> 
> $$
> \omega_0 = \frac{2\pi f_0}{f_s} = \frac{2\pi \cdot 500}{10000} = 0.1\pi
> $$
> 
> $$
> \Delta\omega = \frac{2\pi \Delta f}{f_s} = \frac{2\pi \cdot 32}{10000} = 0.0064\pi \approx 0.02
> $$
> 
> Determinazione del raggio $R$:
> 
> $$
> 2(1 - R) = 0.02 \implies R = 0.99
> $$
> 
> Calcolo dei coefficienti del filtro:
> 
> $$
> a_1 = -2(0.99) \cos(0.1\pi) = -1.8831
> $$
> 
> $$
> a_2 = (0.99)^2 = 0.9801
> $$
> 
> $$
> G = (1 - 0.99) \sqrt{1 - 2(0.99)\cos(0.2\pi) + (0.99)^2} = 0.0062
> $$
> 
> Funzione di trasferimento:
> 
> $$
> H(z) = \frac{0.0062}{1 - 1.8831z^{-1} + 0.9801z^{-2}}
> $$

## Equalizzatore Parametrico

L'equalizzatore parametrico generalizza la struttura del risuonatore introducendo una coppia di zeri complessi coniugati allineati sulla stessa direzione angolare $\omega_0$ dei poli:

$$
z_1 = r \mathrm{e}^{j\omega_0}, \quad z_1^* = r \mathrm{e}^{-j\omega_0}
$$

dove $r$ ($0 \le r \le 1$) è il raggio degli zeri e $R$ ($0 \le R < 1$) è il raggio dei poli.

La funzione di trasferimento è:

$$
H(z) = \frac{(1 - r \mathrm{e}^{j\omega_0} z^{-1})(1 - r \mathrm{e}^{-j\omega_0} z^{-1})}{(1 - R \mathrm{e}^{j\omega_0} z^{-1})(1 - R \mathrm{e}^{-j\omega_0} z^{-1})} = \frac{1 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}}
$$

con coefficienti:

$$
\begin{align}
b_1 &= -2r \cos\omega_0, & b_2 &= r^2 \\
a_1 &= -2R \cos\omega_0, & a_2 &= R^2
\end{align}
$$

Il comportamento in frequenza dipende dal confronto tra i due raggi:
- Se $r < R$: il polo è più vicino al cerchio unitario rispetto allo zero $\implies$ si ottiene un'__enfatizzazione (boost / guadagno in dB)__ attorno a $\omega_0$;
- Se $r > R$: lo zero è più vicino al cerchio unitario rispetto al polo $\implies$ si ottiene un'__attenuazione (cut / valle in dB)__ attorno a $\omega_0$.

![[immagini/eq_param_pole_zero_pattern.png|center mid]]

### Filtro Notch

Nel caso limite in cui gli zeri vengono posizionati esattamente sulla circonferenza unitaria ($r = 1$):

![[immagini/notch.png|center mid]]

la risposta in frequenza si annulla esattamente alla pulsazione $\omega_0$ ($|H(\omega_0)| = 0$). I coefficienti del numeratore diventano:

$$
b_1 = -2\cos\omega_0, \quad b_2 = 1
$$

$$
a_1 = R b_1 = -2R \cos\omega_0, \quad a_2 = R^2
$$

La funzione di trasferimento del filtro notch può essere espressa sinteticamente come:

$$
H(z) = \frac{1 + b_1 z^{-1} + b_2 z^{-2}}{1 + a_1 z^{-1} + a_2 z^{-2}} = \frac{N(z)}{N(R^{-1} z)}
$$

dove il numeratore fattorizzato è:

$$
N(z) = 1 - 2\cos\omega_0 z^{-1} + z^{-2} = (1 - \mathrm{e}^{j\omega_0} z^{-1})(1 - \mathrm{e}^{-j\omega_0} z^{-1})
$$

### Filtro a Pettine (Comb)

Il filtro a pettine estende il principio del notch a un insieme di $M$ frequenze armoniche multiple $\omega_i$:

$$
N(z) = \prod_{i=1}^{M} (1 - \mathrm{e}^{j\omega_i} z^{-1})
$$

Il denominatore introduce poli collocati sulle stesse direzioni radiali degli zeri, ma ritirati all'interno del cerchio unitario al raggio $\rho$ ($0 < \rho < 1$):

$$
D(z) = N(\rho^{-1} z) = \prod_{i=1}^{M} (1 - \mathrm{e}^{j\omega_i} \rho z^{-1})
$$

La funzione di trasferimento espansa è:

$$
H(z) = \frac{N(z)}{N(\rho^{-1} z)} = \frac{1 + b_1 z^{-1} + \dots + b_M z^{-M}}{1 + \rho b_1 z^{-1} + \dots + \rho^M b_M z^{-M}}
$$

I coefficienti del denominatore sono versioni scalate dei coefficienti del numeratore:

$$
a_i = \rho^i b_i, \quad i = 1, \dots, M
$$

Se $\rho \lesssim 1$, le coppie polo-zero si stringono e le tacche di attenuazione diventano estremamente strette e selettive:

![[immagini/comb.png|center mid]]

> [!NOTE] Filtro a Pettine Inverso (Inverted Comb)
> Invertendo la posizione reciproca di poli e zeri (spingendo gli zeri all'interno rispetto ai poli), la funzione si capovolge trasformando le valli di soppressione in picchi di risonanza periodica:
> 
> ![[immagini/comb_inverso.png|center mid]]
