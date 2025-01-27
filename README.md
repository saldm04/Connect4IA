# Connect4IA

Connect4IA è un'applicazione desktop sviluppata per il corso di Fondamenti di Intelligenza Artificiale (2024/2025). L'obiettivo del progetto è creare un'esperienza coinvolgente in cui gli utenti possono giocare a Connect Four contro un'intelligenza artificiale. Il gioco include diversi livelli di difficoltà, permettendo ai giocatori di sfidare un agente che utilizza strategie sempre più avanzate.

## Caratteristiche
- Modalità giocatore singolo contro l'IA.
- Livelli di difficoltà personalizzabili.
- Algoritmi avanzati per la strategia dell'IA.
- Interfaccia grafica semplice e intuitiva.

## Requisiti di sistema
- Python 3.9 o superiore
- Pipenv per la gestione delle dipendenze e degli ambienti virtuali
    ```bash 
    pip install pipenv
     ```
  
## Installazione
Segui questi passaggi per configurare l'ambiente di sviluppo ed eseguire l'applicazione:

1. Clona il repository:
   ```bash
   git clone https://github.com/saldm04/Connect4IA.git
   cd Connect4IA
   ```

2. Crea un ambiente virtuale:
   ```bash
   python3 -m venv .venv
   ```
   oppure
    ```bash
   python -m venv .venv
   ```

3. Installa le dipendenze con Pipenv:
   ```bash
   pipenv install
   ```

4. Attiva l'ambiente virtuale:
   ```bash
   pipenv shell
   ```

5. Avvia il programma dalla shell virtualizzata:
    - Entra nella cartella `Implementazione`:
      ```bash
      cd Implementazione
      ```
    - Esegui l'applicazione:
      ```bash
      python main.py
      ```

6. Avvia il test per simulare la partita tra due agenti intelligenti (opzionale):
    - Entra nella cartella `Implementazione`:
      ```bash
      cd Implementazione
      ```
    - Esegui il test:
      ```bash
      python difficulty_test.py
      ```

### Utilizzo con IDE
Se utilizzi un IDE come IntelliJ o PyCharm:
1. Configura l'interprete Python basato sull'ambiente virtuale `.venv` creato nella directory del progetto.
2. Avvia il programma utilizzando l'apposito pulsante di esecuzione del tuo IDE.

## Autori
- [Luca Del Bue](https://github.com/lukedge86)
- [Salvatore Di Martino](https://github.com/saldm04)

## Struttura delle Directory e Moduli
- **Implementazione**: Contiene il progetto Python con tutti i moduli e le directory necessarie per il funzionamento. Include i seguenti elementi principali:
    - **`board`**: Modulo dedicato alla gestione della griglia di gioco, contenente costanti e funzioni specifiche.
    - **`algorithms`**: Directory che include le implementazioni degli algoritmi di intelligenza artificiale utilizzati nel gioco.
    - **`states`**: Directory che raccoglie i moduli per rappresentare i diversi stati del gioco. Ogni modulo integra sia la logica che l'interfaccia grafica relativa allo stato specifico.
    - **`main`**: Modulo principale responsabile dell'avvio del gioco.
    - **`game_assets`**: Directory contenente gli elementi grafici utilizzati per costruire l'interfaccia utente.
    - **`utils`**: Modulo che fornisce funzioni ausiliarie per la gestione dell'interfaccia grafica e per la selezione del livello di difficoltà.
    - **`difficulty_test`**: Modulo per il test.

- **Documentazione**: Contiene il report del progetto, con una descrizione dettagliata delle funzionalità, dell'architettura e delle scelte progettuali.