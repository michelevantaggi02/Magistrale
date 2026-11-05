# Guida alla Redazione degli Appunti di Information and Estimation Theory
> Corso di Laurea Magistrale in Ingegneria Informatica e Robotica — Anno 1
> Docenti: Prof. Luca Rugini (Parte I), Docente Parte II | Riferimenti Ufficiali: S. Kay (Vol. I & II), T. Cover & J. Thomas, Paper Scientifici

## 1. Perimetro del Corso e Fonti Didattiche

Questo documento stabilisce le linee guida operative, strutturali e stilistiche per la redazione degli appunti della materia **Information and Estimation Theory** (Anno 1), conformemente alle specifiche generali del vault definite in `STRUTTURA_E_GUIDA_APPUNTI.md`.

Il corso è articolato in due grandi macro-aree didattiche connesse:

1. **Parte I: Teoria della Stima e della Rilevazione (Estimation and Detection Theory)**:
   - **Docente**: Prof. Luca Rugini.
   - **Testi di Riferimento Ufficiali**:
     - Steven M. Kay, _Fundamentals of Statistical Signal Processing, Volume I: Estimation Theory_, Prentice Hall, 1993.
     - Steven M. Kay, _Fundamentals of Statistical Signal Processing, Volume II: Detection Theory_, Prentice Hall, 1998.
   - **Materiale Sorgente**:
     - `notes/Part I Notes (Estimation and Detection)/estimation_theory_final_2026.pdf` (105 lucidi).
     - `notes/Part I Notes (Estimation and Detection)/detection_theory_final_2026.pdf` (66 lucidi).

2. **Parte II: Teoria dell'Informazione (Information Theory)**:
   - **Testo di Riferimento Ufficiale**:
     - Thomas M. Cover and Joy A. Thomas, _Elements of Information Theory_, 2nd Edition, Wiley-Interscience, 2006.
   - **Materiale Sorgente**:
     - Archivio compresso `notes/Part II Notes (Information).zip` contenente 10 lezioni tematiche (`lec01` .. `lec09`).
     - Script ed esempi interattivi in `notes/MATLAB Examples.zip`.
     - Paper scientifici originali estratti in `notes/papers/`: Shannon (1948), Golomb (1966), Ziv & Lempel (LZ77, LZ78), Welch (LZW 1984), Linde-Buzo-Gray (LBG 1980), Goyal (2001).

---

## 2. Politica di Gestione degli Archivi ZIP e dei Paper

1. **Decompressione On-Demand e Mirata**:
   - Gli archivi compressi `.zip` vengono estratti **esclusivamente quando si giunge alla trattazione della relativa parte**.
   - Ciascuna estrazione risiede tassativamente in una sottocartella dedicata dentro `notes/` (es. `notes/Part I Notes (Estimation and Detection)/`).
   - Gli archivi compressi originali restano intatti.
2. **Integrazione dei Paper Scientifici**:
   - I paper scientifici forniti dai docenti vengono analizzati per arricchire e chiarire passaggi matematici o algoritmi sintetizzati nelle slide (in particolare per la Teoria dell'Informazione: Shannon, codici LZ77/LZ78/LZW, quantizzazione vettoriale LBG, basi di Goyal, codici di Golomb).
   - Dimostrazioni estese, passaggi algebrici prolissi o modelli non presenti direttamente e letteralmente nelle slide risiedono nel file `zz. Argomenti extra.md`.

---

## 3. Architettura dei File e Mappatura dei Capitoli

La suddivisione della materia segue il principio pedagogico di **separazione tra fondamenti/limiti teorici e metodi/stimatori operativi**, garantendo capitoli compatti e autosufficienti ($\approx 25\text{–}35$ lucidi ciascuno, circa 350–450 righe di Markdown).

La progressione adotta la sequenza decimale continua da `0` a `9` seguita da lettere maiuscole `A`..`E` per coprire l'intero corso (6 capitoli per Parte I, 9 capitoli per Parte II), affiancata dal file `zz. Argomenti extra.md`:

```text
Anno 1/Information and Estimation Theory/
├── 0. Fondamenti di Stima Classica e Limite di Cramer-Rao.md
├── 1. Stimatori Classici - BLUE, MLE e LSE.md
├── 2. Stima Bayesiana - MMSE e LMMSE.md
├── 3. Teoria della Decisione e Criterio di Neyman-Pearson.md
├── 4. Prestazioni del Ricevitore e Rilevatori Bayesiani.md
├── 5. Rilevazione Multipla e Test di Ipotesi Composte (GLRT).md
├── 6. Introduzione alla Teoria dell'Informazione ed Entropia.md
├── 7. Proprietà dell'Entropia e Informazione Mutua.md
├── 8. Proprietà di Equipartizione Asintotica (AEP).md
├── 9. Entropia di Sorgenti con Memoria ed Entropy Rates.md
├── A. Compressione Dati e Codifica di Sorgente.md
├── B. Capacità di Canale e Teorema di Shannon.md
├── C. Entropia Differenziale e Canale Gaussiano.md
├── D. Teoria Rate-Distortion e Quantizzazione Ottima.md
├── E. Codici Universali e Compressione Dizionario.md
├── zz. Argomenti extra.md
├── GUIDA_APPUNTI_INFORMATION_AND_ESTIMATION_THEORY.md
├── immagini/
└── notes/
    ├── Part I Notes (Estimation and Detection)/
    │   ├── estimation_theory_final_2026.pdf
    │   └── detection_theory_final_2026.pdf
    ├── Part I Notes (Estimation and Detection).zip
    ├── Part II Notes (Information).zip
    ├── MATLAB Examples.zip
    └── papers/
        ├── golomb1966_Run-length_encodings_Corresp..pdf
        ├── goyal_Theoretical_foundations_of_transform_coding.pdf
        ├── lindebuzogray_An_Algorithm_for_Vector_Quantizer_Design.pdf
        ├── lz77.pdf
        ├── lz78_Compression_of_individual_sequences_via_variable-rate_coding.pdf
        ├── lzw_welch_1984_technique_for.pdf
        └── shannon_a_mathematical_theory_of_communication.pdf
```

---

## 4. Dettaglio Programmatico: Parte I (Stima e Rilevazione) — 6 Capitoli

### Tabella di Corrispondenza di Parte I

| File Markdown | Slide Sorgente | Pagine PDF | Tipologia | Argomenti e Contenuti d'Esame | Stato |
| :--- | :--- | :---: | :---: | :--- | :---: |
| `0. Fondamenti di Stima Classica e Limite di Cramer-Rao.md` | `estimation_theory` | 1–39 | **Teoria e Limiti** | Modello di misura con rumore, polarizzazione, varianza, compromesso bias-varianza, MVU, regolarità PDF, score function, Informazione di Fisher, CRLB scalare/vettoriale, efficienza statistica, trasformazioni di parametri, line fitting. | **COMPLETATO & CERTIFICATO CONFORME** |
| `1. Stimatori Classici - BLUE, MLE e LSE.md` | `estimation_theory` | 40–69 | **Stimatori Operativi** | **BLUE**: vincolo di linearità, lagrangiana, Teorema di Gauss-Markov, rumore eteroschedastico/colorato diagonale, BLUE vettoriale. **MLE**: likelihood/LLF, score equations, esempio scalare a parametri coincidenti, proprietà asintotiche (consistenza, efficienza, normalità), invarianza di Zehna, MLE vettoriale e modello lineare gaussiano, livello DC con varianza incognita. **LSE**: paradigma deterministico, minimi quadrati lineari, equazioni normali, principio di ortogonalità, matrice di proiezione (Hat Matrix), fit polinomiale su serie reali (mercato elettrico) e line fitting. Guida comparativa operativa. | **COMPLETATO & CERTIFICATO CONFORME** |
| `2. Stima Bayesiana - MMSE e LMMSE.md` | `estimation_theory` | 70–105 | **Teoria e Stimatori Bayesiani** | Cambio di paradigma: parametro $\theta$ come variabile aleatoria con distribuzione a priori $f(\theta)$, Bayesian MSE (BMSE) vs MSE classico. **Stimatore MMSE**: minimizzazione del BMSE e derivazione della media a posteriori $\mathbb{E}[\theta \mid \mathbf{x}]$, livello DC con prior gaussiana (interpretazione di shrinkage / filtro di Kalman scalare), BMSE residuo, MMSE vettoriale per modello lineare gaussiano, non-polarizzazione bayesiana. **Stimatore LMMSE**: vincolo affine $a_0 + \mathbf{a}^T\mathbf{x}$, dipendenza esclusiva dai momenti di $1^\circ$ e $2^\circ$ ordine ($\mathbf{C}_{xx}, \mathbf{c}_{x\theta}$), principio di ortogonalità stocastica nello spazio di Hilbert delle variabili aleatorie, livello DC con prior uniforme (confronto analitico con l'integrale MMSE), estensione vettoriale, due forme dell'inversa (lemma di Woodbury). Tabella sinottica finale comparativa di tutti gli stimatori. | **COMPLETATO & CERTIFICATO CONFORME** |
| `3. Teoria della Decisione e Criterio di Neyman-Pearson.md` | `detection_theory` | 1–32 | **Teoria e Limite Classico** | Modello del ricevitore/rilevatore: spazio delle osservazioni, statistica di test $T(\mathbf{x})$, soglia di decisione $\gamma$, partizione in regioni di decisione $\mathcal{R}_0$ e $\mathcal{R}_1$. Tassonomia (ipotesi semplici vs composte, binarie vs multiple, deterministiche vs bayesiane). Errori di decisione: falso allarme ($P_{\text{FA}}$), rilevazione ($P_{\text{D}}$), mancata rilevazione ($P_{\text{M}} = 1 - P_{\text{D}}$), compromesso geometrico al variare della soglia $\gamma$. Criterio di Neyman-Pearson ($\max P_{\text{D}}$ s.t. $P_{\text{FA}} \le \alpha$), Teorema di Neyman-Pearson e Likelihood Ratio Test (LRT), derivazione lagrangiana, esempio livello DC in AWGN con funzione $Q$. | **COMPLETATO & CERTIFICATO CONFORME** |
| `4. Prestazioni del Ricevitore e Rilevatori Bayesiani.md` | `detection_theory` | 33–48 | **Valutazione e Rilevatori Bayesiani** | **Curva ROC** (Receiver Operating Characteristic): definizione analitica, proprietà fondamentali (passaggio per $(0,0)$ e $(1,1)$, concavità verso il basso, pendenza $\frac{\partial P_{\text{D}}}{\partial P_{\text{FA}}} = \gamma$, area AUC), coefficiente di deflessione $d^2$ (SNR di rilevazione). **Criterio a Minima Probabilità d'Errore**: regola del Massimo a Posteriori (MAP), LRT a soglia pesata dalle prior $\frac{\text{Pr}(H_0)}{\text{Pr}(H_1)}$, caso a priori equiprobabili (ML), calcolo analitico di $P_e$ per segnale DC in AWGN. **Criterio del Rischio di Bayes**: matrice dei costi $C_{ij}$, formulazione del rischio medio $R$, derivazione della regola ottima con LRT a soglia pesata da costi e probabilità a priori. | **COMPLETATO & CERTIFICATO CONFORME** |
| `5. Rilevazione Multipla e Test di Ipotesi Composte (GLRT).md` | `detection_theory` | 49–66 | **Rilevatori Avanzati** | **Rilevazione Multipla ($M > 2$)**: partizione dello spazio vettoriale, regola MAP multi-ipotesi, esempio modulazione ternaria (3-PAM / 3 livelli DC in AWGN) con calcolo delle regioni multi-soglia e probabilità d'errore. **Ipotesi Composte e GLRT**: parametri sconosciuti o di disturbo under $H_0$ e $H_1$, principio del Generalized Likelihood Ratio Test (sostituzione dei parametri con MLE condizionati). Proprietà asintotiche del GLRT (Teorema di Wilks, distribuzioni $\chi^2$ centrale e non-centrale), rilevatore a legge quadratica / rilevatore di energia per livello DC a valore ignoto. Confronto con l'approccio bayesiano (marginalizzazione per integrazione della prior) e quadro sinottico finale di tutti i rilevatori. | **COMPLETATO & CERTIFICATO CONFORME** |

---

## 5. Dettaglio Programmatico Previsto: Parte II (Teoria dell'Informazione) — 9 Capitoli

| File Markdown | Sorgente Primaria | Paper Scientifico Correlato | Temi Chiave | Stato |
| :--- | :--- | :--- | :--- | :---: |
| `6. Introduzione alla Teoria dell'Informazione ed Entropia.md` | `lec01`, `lec02` (1–32) | Shannon (1948) | Definizione di informazione, auto-informazione, entropia di Shannon $H(X)$, unità (bit, nat), interpretazione di incertezza e sorpresa, distribuzioni notevoli (Bernoulli, Binomiale, Poisson con Stirling), entropia congiunta/condizionata, regola della catena, divergenza KL $D(p \parallel q)$, cross-entropia, informazione mutua $I(X; Y)$, diagrammi di Venn informativi e regole della catena multivariate. | **COMPLETATO & CERTIFICATO CONFORME** |
| `7. Proprietà dell'Entropia e Disuguaglianze Fondamentali.md` | `lec02` (33–70) | Cover & Thomas (Cap. 2) | Convessità/concavità, test derivata seconda, disuguaglianza di Jensen, disuguaglianza dell'informazione $D(p \parallel q) \ge 0$, non-negatività di $I(X; Y)$, condizionamento riduce l'entropia ($H(X \mid Y) \le H(X)$), massimizzazione dell'uniforme, log-sum inequality, convessità congiunta di $D(p \parallel q)$, concavità di $H(p)$, Data Processing Inequality (DPI), disuguaglianza di Fano. | **COMPLETATO & CERTIFICATO CONFORME** |
| `8. Proprietà di Equipartizione Asintotica (AEP).md` | `lec03` | Shannon (1948) | Teorema AEP e legge debole dei grandi numeri applicata alla sorpresa, insieme tipico $A_\epsilon^{(n)}$, cardinalità e probabilità dell'insieme tipico, implicazioni per la compressione di blocchi. | **COMPLETATO & CERTIFICATO CONFORME** |
| `9. Entropia di Sorgenti con Memoria ed Entropy Rates.md` | `lec04` | Shannon (1948) | Processi stocastici stazionari, catene di Markov discrete, calcolo dell'entropy rate $H(\mathcal{X})$, comportamento asintotico di sequenze linguistiche e dati con memoria. | **COMPLETATO & CERTIFICATO CONFORME** |
| `A. Compressione Dati e Codifica di Sorgente.md` | `lec05a`, `lec06` | Golomb (1966), Huffman (1952) | Codici univocamente decodificabili e istantanei (prefissi), disuguaglianza di Kraft-McMillan, lunghezza media ottima e limite di Shannon, algoritmo di Huffman ottima, codifica run-length e codici di Golomb per distribuzioni geometriche. | **COMPLETATO & CERTIFICATO CONFORME** |
| `B. Capacità di Canale e Teorema di Shannon.md` | `lec05b` | Shannon (1948) | Modelli di canale discreto senza memoria (DMC), canale binario simmetrico (BSC) e con cancellazione (BEC), capacità di canale $C = \max_{p(x)} I(X; Y)$, secondo teorema fondamentale di Shannon (codifica di canale e convergenza a probabilità d'errore nulla). | **COMPLETATO & CERTIFICATO CONFORME** |
| `C. Entropia Differenziale e Canale Gaussiano.md` | `lec07` | Shannon (1948), Cover & Thomas | Estensione a variabili continue: entropia differenziale $h(X)$, proprietà e differenze con l'entropia discreta, massimizzazione dell'entropia sotto vincolo di potenza (distribuzione gaussiana), canale AWGN continuo e formula di Shannon-Hartley per la capacità $C = B \log_2(1 + \text{SNR})$. | **COMPLETATO & CERTIFICATO CONFORME** |
| `D. Teoria Rate-Distortion e Quantizzazione Ottima.md` | `lec08` | Linde-Buzo-Gray (1980), Goyal (2001) | Compressione con perdita (lossy), misure di distorsione (errore quadratico), funzione Rate-Distortion $R(D)$, quantizzazione scalare ottima (Lloyd-Max), quantizzazione vettoriale e algoritmo LBG, fondamenti teorici della codifica per trasformata (Goyal). | **COMPLETATO & CERTIFICATO CONFORME** |
| `E. Codici Universali e Compressione Dizionario.md` | `lec09` | LZ77 (1977), LZ78 (1978), Welch (LZW 1984) | Limiti dei codici dipendenti dalla statistica della sorgente, codici universali a dizionario, principio della finestra scorrevole LZ77, albero dinamico dei prefissi LZ78, algoritmo LZW (Unix compress, GIF, TIFF), analisi di complessità e convergenza asintotica all'entropia. | **COMPLETATO & CERTIFICATO CONFORME** |

---

## 6. Ruolo del File `zz. Argomenti extra.md`

Conformemente alla Sezione 3.12 di `STRUTTURA_E_GUIDA_APPUNTI.md`:
- I capitoli primari (`0.` .. `E.`) mantengono una narrazione agile, pragmatica e direttamente orientata alle lezioni e all'esame, spiegando il significato fisico e intuitivo prima della formula.
- Tutte le dimostrazioni matematiche analitiche estese non presenti letteralmente nelle slide, i passaggi algebrici prolissi e i dettagli costruttivi derivati dai testi di Steven Kay o Cover & Thomas devono risiedere in `zz. Argomenti extra.md`.
- Ogni dimostrazione o approfondimento spostato in `zz. Argomenti extra.md` viene puntualmente collegato nei file principali mediante wikilink espliciti (es. `[[zz. Argomenti extra#Dimostrazione del CRLB tramite Cauchy-Schwarz|zz. Argomenti extra: Dimostrazione del CRLB]]`) o callout dedicati `>[!note] Approfondimento Teorico`.

---

## 7. Pipeline Grafica Lossless e Controlli Anti-Crop

1. **Ritaglio Lossless e Standard 300 DPI**:
   - Per ciascuna figura estratta dai lucidi PDF, si garantisce una risoluzione minima di 150-300 DPI.
   - Si applica tassativamente il controllo analitico anti-crop a 6 fasi: esclusione di intestazioni, loghi universitari e footer, con mantenimento integrale di etichette degli assi, legende e formule interne.
   - Applicazione di un margine neutro di respiro (padding bianco) di almeno 8–15 pixel attorno ai grafici.
2. **Archiviazione e Naming Semantico**:
   - Tutti gli asset grafici risiedono nella cartella `immagini/`.
   - Denominazione standard: `slide_<num>_<descrizione_concisa>.png` (es. `slide_17_bias_variance_targets.png`, `slide_24_crlb_bound_pdf.png`, `slide_34_roc_curve.png`).
3. **Regole Tassative di Inclusione nei Documenti**:
   - Centratura e classe obbligatoria: mai immagini prive di modificatori.
   - Sintassi standard: `![[nome_file.png|center small]]` (prioritaria di default al 45%), `![[nome_file.png|center mid]]` (per grafici con testo denso al 70%), `![[nome_file.png|center big]]` (per confronti a più pannelli).
   - **Affiancamento orizzontale obbligatorio**: Quando compaiono due immagini `small` consecutive, devono essere inserite sulla stessa riga di testo separate da un singolo spazio:
     ```markdown
     ![[figura_1.png|center small]] ![[figura_2.png|center small]]
     ```

---

## 8. Convenzioni Stilistiche e Tipografiche

- **Titoli**: Solo H1 è numerato (`# N. Titolo`), corrispondente esattamente al nome del file `.md`. Tutti i sottotitoli interni (H2, H3, ecc.) sono **puramente descrittivi** (senza numeri né prefissi tipo `1.1` o `2.3`).
- **Enfasi Linter**: Utilizzo del doppio underscore per il grassetto (`__termine__`) e singolo underscore per il corsivo (`_termine_`).
- **Nessuna Linea Orizzontale**: È severamente vietato inserire separatori `---` nel testo delle note.
- **Formule Matematiche**: Espressioni KaTeX isolate su blocchi display `$$ ... $$` con riga vuota prima e dopo. Vettori in grassetto `\mathbf{x}`, differenziali con `\mathrm{d}t`.
- **Integrità degli Elenchi**: Gli elenchi puntati o numerati non devono mai essere interrotti a metà da immagini o callout; ogni elenco va completato prima di inserire elementi di blocco esterni.
- **Voce dell'Autore**: Stile ingegneristico in prima persona ("abbiamo visto", "se applichiamo il vincolo troviamo", "ho un vettore di campioni"), paragrafi snelli (1–4 righe), tono diretto da problem solver.
- **Lingua**: Redazione rigorosamente in lingua italiana, traducendo e rielaborando integralmente i testi originali in inglese.

---

## 9. Protocollo del Loop Iterativo di Revisione con Subagenti Indipendenti

Al termine della redazione di ciascun capitolo si applica tassativamente la regola workspace `[[.agents/rules/revisione_automatica_subagente.md]]`:

1. **Invocazione Automatica (Iterazione $k$)**: L'agente principale, appena terminata la stesura o modifica del file `.md`, avvia un subagente indipendente (`invoke_subagent` con ruolo di *Academic Peer Reviewer*).
2. **Isolamento Cognitivo**: Ciascun subagente opera in un contesto di sessione pulito ed estraneo alla stesura, prevenendo il *confirmation bias* del redattore.
3. **Risorse Fornite al Subagente**:
   - Accesso in sola lettura al file Markdown nello stato aggiornato.
   - Accesso alle slide sorgente in PDF (`estimation_theory_final_2026.pdf` o `detection_theory_final_2026.pdf`).
   - Accesso ai paper scientifici pertinenti (`notes/papers/`) e ai testi di Steven Kay.
   - Accesso alla ricerca internet (`search_web`) per verificare formule, condizioni di regolarità e convenzioni notazionali.
4. **Mandato di Revisione (Focus Esclusivo su Errori, Refusi e Correttezza Scientifica)**:
   - Individuare sviste di calcolo, errori analitici, segni algebrici errati, dimensioni non conformi di matrici/vettori e omissioni di ipotesi matematiche.
   - Verificare la perfetta aderenza alle slide del docente e ai paper scientifici.
   - **Divieto Assoluto di Critica su Stile, Prosa o Formattazione del Vault**: Il revisore non deve giudicare né commentare lo stile del testo, il tono espositivo, la prosa o le convenzioni grafiche/linter del vault (linter, titoli, KaTeX, immagini), limitandosi strettamente all'accuratezza oggettiva dei contenuti.
   - Fornire la correzione esatta per ciascun errore o refuso individuato (diff/drop-in replacement).
5. **Loop Iterativo a Convergenza (Revisione $\to$ Modifica $\to$ Nuova Revisione)**:
   - Se il subagente rileva errori o richiede modifiche, l'agente principale applica tempestivamente le correzioni tramite `edit_file`.
   - **Obbligo di Riavvio del Loop**: Dopo aver applicato le modifiche, l'agente principale **deve obbligatoriamente avviare un NUOVO subagente indipendente (Iterazione $k+1$)** per verificare il file modificato a mente fresca.
   - Il loop si ripete finché un subagente indipendente non certifica formalmente l'esito: **`CONFORME (Zero errori/incongruenze rilevate)`**.
   - Solo a convergenza certificata il capitolo viene presentato all'utente con il riepilogo delle iterazioni e delle migliorie apportate.

