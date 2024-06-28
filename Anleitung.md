# Projektname

Hier befindet sich die Anleitung dafür, wie Sie unser Projekt auch auf Ihrem Computer zum Laufen bringen können.

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass die folgenden Softwarekomponenten auf Ihrem Computer installiert sind:

- Python 3.7 oder höher
- pip (Python Package Installer)
- Git

Zusätzlich benötigen Sie die Python-Bibliotheken, die :

- `gradio`
- `pyaudio`
- `matplotlib`
- `librosa`
- `soundfile`
- `numpy`
- `transformers`

Diese erhal

## Installation

1. **Repository klonen**:

   Öffnen Sie ein Terminal und führen Sie den folgenden Befehl aus, um das Repository zu klonen:

   ```sh
   git clone https://github.com/GenosseJannik/HFU_KaraokeNet
   cd HFU_KaraokeNet
   
2. **Bibliotheken installieren**

   Navigieren Sie sich in einem Terminal zum Github Repository und führen sie folgenden Befehl aus.
   pip install -r requirements.txt

    Dies stellt sicher, dass sie alle relevanten Bibliotheken installiert haben.
   
3. **Neue Lieder hinzufügen (Optional)**:

   Die bestehende Software kann um weitere Lieder erweitert werden, indem Sie in dem Verzeichniss Songs die entsprechenden Dateien hinzufügen.
   Dazu gehört in dem Unterverzeichniss `[Songs/Songs](Songs/Songs)` die .mp3-Datei des Liedes, die zwingend erforderlich ist.
   Für eine verbesserte Bewertung der Aussprache, können Sie in dem Ordner Songs/Lyrics die Songtexte hinzufügen der Lieder als .txt-Datei abspeichern. Wenn sie dies nicht machen,
   wird mit dem KI-generierten Songtext des Liedes bei der Bewertung gearbeitet. In Songs/Videos sind die Videos, die die Texte des Liedes visualisieren, als .mp4-Datei abzulegen. 
   

4. **KaraokeNet starten**

   Alles bis hierhin erledigt? Gut, dann müssen Sie nur noch das Skript interface_karaokenet.py ausführen. Dies können sie entweder in ihrer Entwicklungsumgebung machen, oder aber in einem
   Terminal, in welchem Sie sich erst zu dem Github Repository navigieren müssen. Im Anschluss können Sie mit dem Befehl *python interface_karaokenet.py* das Interface starten.
   Wie sie das Interface zu benutzen haben, erfahren sie hier.
   

