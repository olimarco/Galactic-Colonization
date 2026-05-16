[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23930652&assignment_repo_type=AssignmentRepo)
# Progetto Algoritmi e Strutture Dati

## Galactic Colonization: Deep Space Explorer

### Descrizione del Progetto

Si chiede di implementare un simulatore di esplorazione spaziale in cui un Eroe al comando di una navicella deve colonizzare settori galattici per raccogliere risorse. La missione si svolge in un universo vasto e incognito dove la gestione del carburante è il vincolo principale per la sopravvivenza. Il Team si dovrà occupare di:

* Implementare la creazione dell'Universo in maniera procedurale e randomica, garantendo che ogni simulazione presenti una topologia di settori differente.

* Implementare un registro delle scoperte (Catalogo Galattico) che permetta di monitorare le risorse estratte, i settori visitati e le rotte iperspaziali conosciute.

* Implementare la disposizione casuale delle risorse e delle galassie all'interno dei settori generati, bilanciando la difficoltà in base al carburante disponibile.

* Implementare il sistema di gioco a turni e le relative interazioni tra utente e ambiente di gioco, inclusa la gestione degli imprevisti ambientali.

Il gioco può essere implementato sia con interfaccia grafica che in modalità testo terminale a scelta del team.
Il team dovrà utilizzare gli strumenti di Github per la gestione del progetto e dovrà produrre una relazione tecnica da consegnare 5 giorni prima della prova scritta. La relazione dovrà contenere:
* Una descrizione delle scelte architetturali e algoritmi adottate
* Una descrizione della suddivisione del lavoro

N.B. Ogni membro del team dovrà lavorare in maniera autonoma a uno o più issue. Sia dalla relazione che dalle Issue si dovrà evincere il contributo di ogni componente. Non saranno accettati lavori in cui non sia possibile risalire al reale autore di ogni parte di codice.

### Struttura del Turno e Imprevisti

Il gioco si svolge in una sequenza di turni. In ogni turno la navicella effettua uno spostamento verso un settore adiacente (consumando il relativo carburante).

Gestione Imprevisti:
* Al momento dell'ingresso in un nuovo settore, il sistema deve calcolare se si verifica un imprevisto in base al "Livello di Pericolo" del settore stesso.

* Gli imprevisti sono creati a discrezione degli studenti (es. tempeste solari, pirati spaziali, anomalie gravitazionali).

* Ogni imprevisto deve comportare una perdita supplementare di carburante, riducendo l'autonomia della navicella oltre al costo standard dello spostamento.

Al termine dello spostamento (e dell'eventuale imprevisto), il sistema deve permettere all'utente di scegliere tra le seguenti azioni:

* Consultare il Catalogo Galattico: Visualizzare l'elenco delle galassie già visitate, le risorse accumulate e le rotte scoperte.

* Scansione del Settore: Effettuare un'analisi dei collegamenti iperspaziali del settore attuale per conoscere il numero di galassie collegate non ancora visitate e il loro livello di pericolo relativo.

* Proseguire l'Esplorazione: Scegliere automaticamente (Deve essere un algoritmo a determinarlo e non una scelta dell'utente) il prossimo settore verso cui spostarsi tra quelli collegati.

### Vincoli della Generazione

La generazione del sistema galattico dovrà tenere conto dei fattori descritti di seguito:

#### Creazione dell'Universo

L'universo dovrà essere creato ad ogni avvio del gioco in maniera randomica ma con alcuni vincoli strutturali:

* Connettività: Ogni settore generato deve avere da 1 a 5 collegamenti iperspaziali verso altri settori.

* Raggiungibilità: Non possono esistere settori isolati; deve sempre esistere almeno un cammino tra qualsiasi coppia di settori.

* Livello di Pericolo: Ad ogni settore deve essere associato un valore da 0 a 100 che rappresenta la probabilità percentuale che si verifichi un imprevisto entrando in quel settore.

* Costi di Spostamento: Ogni collegamento iperspaziale deve essere associato a un costo di carburante variabile, che influisce sulla pianificazione del percorso.

* Settore di Partenza: Una sola galassia dovrà essere indicata come "Punto di Lancio" iniziale.

* Obiettivo di Colonizzazione: Le risorse totali sono distribuite in modo randomico (valore 0-100 per galassia). Lo scopo è massimizzare il recupero delle risorse prima che la navicella esaurisca la quota di carburante assegnata inizialmente.

### Istruzioni per la Gestione del Progetto

Il gioco può essere implementato sia con interfaccia grafica che in modalità testo terminale a scelta del team.

Non è consetito l'uso di strutture dati già implementate in librerie Python, per ogni Struttura Dati necessaria e affrontata nel corso sarà necessario eseguire una implementazione ad oggetti.

Il team dovrà utilizzare gli strumenti di Github per la gestione del progetto (Issue, Branch, Commit, Pull Request) e dovrà produrre una relazione tecnica da consegnare 5 giorni prima della prova scritta. La relazione dovrà contenere:
* Una descrizione delle scelte architetturali e algoritmi adottate
* Una descrizione della suddivisione del lavoro

N.B. Ogni membro del team dovrà lavorare in maniera autonoma a uno o più issue. Sia dalla relazione che dalle Issue si dovrà evincere il contributo di ogni componente. Non saranno accettati lavori in cui non sia possibile risalire al reale autore di ogni parte di codice.
