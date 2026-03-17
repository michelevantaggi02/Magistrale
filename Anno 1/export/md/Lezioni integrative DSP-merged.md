# Indice

- [[#Campionamento|Campionamento]]
	- [[#Campionamento#Segnale Matematicamente Equivalente|Segnale Matematicamente Equivalente]]
- [[#Quantizzazione|Quantizzazione]]
- [[#Proprietà Di Linearità|Proprietà Di Linearità]]
- [[#Circuito Tempo Invariante|Circuito Tempo Invariante]]
- [[#Risposta Impulsiva E Impulso Di Dirach|Risposta Impulsiva E Impulso Di Dirach]]
- [[#Risposta in Frequenza|Risposta in Frequenza]]
- [[#Convoluzione Lineare (Integrale Di Convoluzione)|Convoluzione Lineare (Integrale Di Convoluzione)]]
	- [[#Convoluzione Lineare (Integrale Di Convoluzione)#Convoluzione Lineare Nei Segnali Digitali|Convoluzione Lineare Nei Segnali Digitali]]
- [[#Come Leggo Lo Spettro in Frequenza|Come Leggo Lo Spettro in Frequenza]]

# 0. Introduzione

In questi appunti saranno presenti alcuni concetti e argomenti che dovrebbero essere insegnati durante la laurea triennale in ingegneria informatica, e che vengono ripetuti per quegli studenti che non li ricordano abbastanza o che non li hanno fatti per vari motivi.

Concetti da ricordare:
- Trasformata di Fourier
- Transito dei segnali
- Teorema di campionamento
- Processi aleatori

> [!NOTE] Segnale
> Un segnale è tutto ciò che può trasportare informazioni

Ogni informazione che utilizziamo viene prima elaborata da un segnale, dobbiamo essere quindi in grado di elaborarli correttamente.

Nella realtà i segnali sono quasi sempre analogici (es: vedo infinite sfumature di colori).

Fino agli anni '70 i segnali e i circuiti che li elaboravano lavoravano solamente nell'ambiente analogico, successivamente si è iniziato a lavorare in ambiente digitale. Questo perché i componenti analogici sono facilmente soggetti all'invecchiamento ed hanno quindi una durata della vita molto bassa.

I DSP sono dispositivi specializzati per trattare i segnali in real-time, con il tempo i DSP sono diventati sempre più complessi, fino ad essere utilizzati nei SoC come componenti di sistemi più complessi.

In queste lezioni ci occuperemo di rappresentare matematicamente quello che nella realtà è composto da componenti elettronici.

# 1. Segnali

- Un segnale monodimensionale è rappresentato da una funzione continua $x(t)$ , esempio: voce.
- Un segnale bidimensionale è rappresentato da una funzione continua $w(x,y)$, esempio: immagine.
- Un segnale tridimensionale è rappresentato da una funzione continua $w'(x,y,t)$, esempio: video.

Dobbiamo arrivare a trattare il segnale digitale in modo che sia equivalente a quello analogico, arrivando quindi ad avere un segnale che non sia approssimato.

>[!important] Teorema del campionamento
>Posso campionare un segnale analogico in modo che il segnale digitale sia matematicamente equivalente
>Per avere un segnale matematicamente equivalente devo campionare con una frequenza maggiore o uguale al __doppio__ della frequenza massima del segnale

^e56489

## Campionamento

>[!IMPORTANT] Risposta in frequenza
> La descrizione matematica di un output (che normalmente è una funzione del tempo) utilizzando una funzione con variabile la frequenza.
>
> Matematicamente la risposta in frequenza è la trasformazione di Fourier della risposta in impulso.

Non è necessario controllare un segnale continuamente, specialmente dato il fatto che nello spazio digitale ho memoria e dimensioni dei valori limitati. Devo quindi __campionare__ il segnale:

- $x(t)$ segnale analogico
- $T$ tempo (o intervallo) di campionamento

$$
\left. x(t)\right|_{t=nT} \implies x(nT)
$$

- $x(nT)$ __segnale a tempo discreto__

Si può anche mettere $T$ implicito se lo conosco, quindi $x(n)$.

Il primo problema è capire __quanto grande__ deve essere $T$, ovvero il più grande possibile per avere ancora senso.
La __frequenza di campionamento__ è l'_inverso_ del tempo di campionamento:

$$
T = \frac1{f_c}
$$

La frequenza indica __quante volte__ vado a reperire il segnale nell'unità di tempo, per decidere la sua dimensione vado a fare un'_analisi_ della funzione da campionare.

Tutto questo serve a risparmiare risorse di calcolo preziose.

Non possiamo andare a tentativi nel decidere $T$, bisogna seguire il [[#^e56489|teorema del campionamento]].

### Segnale Matematicamente Equivalente

Si intende un segnale campionato in base allo spettro di frequenza di un segnale analogico.

>[!example] segnale sinusoidale
>
>$$
>x(t) = A \cos(2\pi f_0 t + \phi)
>$$
>
>- $A$ ampiezza
>- $f_0$ frequenza
>- $\phi$ fase
>avendo a disposizione la frequenza $f_0$ troviamo quindi
>
>$$
>T_0 \to \frac1{f_0}
>$$
>
>$$
>x(n) = x(t)|_{t=nT} \implies x(n) = A \cos (2 \pi f_0 n T + \phi)
>$$
>
>Per il teorema del campionamento ho un segnale matematicamente equivalente se:
>
>$$
>f_c \to T_c = \frac1{f_c}
>$$
>
>$$
>f_c > 2f_0
>$$

## Quantizzazione

Il segnale tempo discreto è ancora "analogico" per quanto riguarda il valore, devo quindi limitare la quantità di dati forniti in base alla capacità della macchina.

È necessaria quindi un'ulteriore discretizzazione sull'asse delle ampiezze: la quantizzazione.

$$
x(nT) \to Q \to Bbit
$$

A partire dal segnale tempo discreto, questo viene fatto passare nel quantizzatore che restituisce un valore binario di $B$ bit.

# 2. Segnali Nei Sistemi Lineari

In un sistema lineare esiste una correlazione tra il segnale in ingresso e quello di uscita.

![[sis_lin.svg|center mid]]

## Proprietà Di Linearità

Il sistema è detto __lineare__ quando posso applicare il __principio di sovrapposizione degli effetti__:

$$
\alpha x_1(t) + \beta x_2(t) = \alpha y_1(t) + \beta y_2(t)
$$

Non possiamo sovraccaricare gli stadi in ingresso altrimenti il circuito smette di lavorare in modo lineare, bisogna quindi limitare il range di input.

## Circuito Tempo Invariante

Il sistema è detto a __tempo invariante__ se:

$$
x(t + \tau) \to y(t + \tau)
$$

Il circuito risponde alla stessa maniera, indipendentemente da quando applico lo stimolo.

>[!NOTE]
>Nei circuiti __analogici__ questa proprietà non vale sempre, a causa del degrado dei componenti e dalla deriva termica dell'ambiente in cui operano.

## Risposta Impulsiva E Impulso Di Dirach

Se entrambe le proprietà sono rispettate, il sistema può essere caratterizzato univocamente dalla __risposta impulsiva__ $h(t)$.

$$
\delta (t) \to h(t)
$$

$$
\int_{-\infty}^{+\infty}{\delta (t)}\;\mathrm dt = 1
$$

L'__impulso di dirach__ ($\delta (t)$) è un impulso il più breve possibile con l'ampiezza massima possibile, la __risposta impulsiva__ è il segnale ricevuto dato un impulso in ingresso.

## Risposta in Frequenza

La risposta in frequenza è la [[3. Trasformata di Fourier|Trasformata di Fourier]] della risposta impulsiva.

$$
h(t) \to H(f) = \int_{-\infty}^{+\infty}{h(t)e^{-j2\pi ft}}\; \mathrm dt
$$

La risposta in frequenza ci dice come il sistema reagisce alle diverse frequenze fornite dal segnale.

## Convoluzione Lineare (Integrale Di Convoluzione)

$$
\begin{align}
x(t) * h(t) &= \int_{-\infty}^{+\infty}h(\tau)x(t-\tau)\;\mathrm d\tau\\
&= \int_{-\infty}^{+\infty}x(\tau)h(t-\tau)\;\mathrm d\tau
\end{align}
$$

Su sistemi reali non possiamo utilizzare le formule matematiche nel tempo, devo quindi lavorare con le frequenze.

>[!IMPORTANT] Proprietà del Filtraggio
>
>$$
>\begin{align*}
>y(t) & = x(t) *  h(t) \\ \\
>\updownarrow F & \quad \updownarrow F \quad \updownarrow F\\
>\\
>Y(f) & = X(f) \cdot H(f)
>\end{align*}
>$$
>
> Si chiama proprietà del filtraggio perché $H(f)$ ha la funzione di __filtro__ (o maschera) rispetto al segnale di ingresso

![[filtro.svg|center]]

### Convoluzione Lineare Nei Segnali Digitali

Le relazioni che legano ingresso e uscita sono le stesse del dominio analogico, con la differenza che abbiamo un numero finito di valori.

$$
x(n) * h(n) = \sum_{k=0}^{N-1}h(k)x(n-k)
$$

La sommatoria è valida solo dove $h(k) \neq 0$, quindi mi serve uno storico del segnale di grandezza $N$.

Avendo una dimensione finita, ho anche un tempo finito e posso calcolarlo in __tempo reale__ con un sistema in grado di calcolare $N$ somme e moltiplicazioni insieme (Multiply And Accumulate, __MAC__).

# 3. Trasformata Di Fourier

La Trasformata di Fourier serve a trasformare un qualsiasi segnale in una __somma di sinusoidi__, con valori:

$$
x(t) = A_i\cos(2\pi f_0+\phi_i)
$$

- $A_i$ ampiezza
- $f_0$ frequenza
- $\phi_i$ fase

Andremo ad _analizzare_ la Trasformata di Fourier e prenderemo la frequenza più alta, decidendo poi se filtrarla fuori o utilizzarla come base per il campionamento.

>[!NOTE]
>Possiamo utilizzare la Trasformata di Fourier anche per sintetizzare i valori

$$
X(\Omega) = \int_{-\infty}^{+\infty}{x(t)e^{-j\Omega t}}\;\mathrm dt
$$

$$
\Omega = 2 \pi f
$$

$X(\Omega)$ è una __funzione a valori complessi__ di $t$ o $\Omega$

$$
\begin{align*}
x(t) \to x(\Omega) &= ReX(\Omega) + ImX(\Omega) \\
& = \text{abs}(X(\Omega)) \cdot e^{j\text{angle}(X(\Omega))} \\
& = \text{abs}(X(f)) \cdot e^{j\text{angle}(X(f))}
\end{align*}
$$

- $\text{abs}$ ampiezza
- $f$ frequenza
- $\text{angle}$ fase

![[fourier.svg|center big]]

>[!IMPORTANT] Proprietà Hermitiana
>Se un segnale $x(t)$ è a valori __reali__, il _modulo_ avrà valori _pari_, e la _fase_ avrà valori _dispari_.

## Come Leggo Lo Spettro in Frequenza

Lo spettro in frequenza mi indica quante frequenze, fino a quale frequenza e quali sono i valori che compongono il segnale.

La Trasformata di Fourier è esatta se abbiamo un segnale digitale campionato, quantizzato e di durata finita.

Tutti i segnali reali sono a __banda limitata__, e se non lo sono realisticamente lavorano con una banda finita e c'è quindi una soglia di frequenze oltre la quale il segnale può essere filtrato. Nella realtà non conosciamo la formula dello spettro, dobbiamo quindi partire da un intervallo di tempo finito e individuare la frequenza massima del segnale.

>[!EXAMPLE] Sinusoide
> La Trasformata di Fourier di una singola sinusoide è un singolo impulso, con all'asse delle frequenze la singola frequenza del segnale.
>
> $$
> x(t) = A_0\cos (2 \pi f_0 + \phi_0)
> $$

Una volta individuata la frequenza massima del segnale (che chiameremo $f_{max}$), seguiamo il [[1. Segnali#^e56489|teorema del campionamento]] e impostiamo $f_c > 2f_{max}$
