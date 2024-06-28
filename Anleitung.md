# Technische Anleitung KaraokeNet

Hier befindet sich die Anleitung dafür, wie Sie unser Projekt auch auf Ihrem Computer zum Laufen bringen können.

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass die folgenden Softwarekomponenten auf Ihrem Computer installiert sind:

- Python 3.7 oder höher
- pip (Python Package Installer)
- Git


1. **Repository klonen**:

   Öffnen Sie ein Terminal und führen Sie die folgenden Befehle aus, um das Repository zu klonen und sich in diesem zu navigieren:

   ```sh
   git clone https://github.com/GenosseJannik/HFU_KaraokeNet
   cd HFU_KaraokeNet
   ```
   
2. **Bibliotheken installieren**

   Wenn sie sich in einem Terminal zum Github Repository navigiert haben, können sie mit dem Folgenden Befehlen, die für das Projekt notwendigen Bibliotheken installieren..
   ```sh
   pip install -r requirements.txt
   ```
   
4. **Neue Lieder hinzufügen (Optional)**:

   Die bestehende Software kann um weitere Lieder erweitert werden, indem Sie in dem Verzeichniss Songs die entsprechenden Dateien hinzufügen.
   Dazu gehört in dem Unterverzeichnis [Songs/Songs](./Songs/Songs) die .mp3-Datei des Liedes, die zwingend erforderlich ist.
   ZUr Bewertung der Aussprache ist es wichtig, dass Sie in dem Ordner [Songs/Lyrics](./Songs/Lyrics) die Songtexte als .txt-Datei abspeichern.
   In [Songs/Video](./Songs/Video) sind die Videos, die die Texte des Liedes visualisieren, als .mp4-Datei abzulegen.
   Die Dateien in dem Ordner [Songs/Word Distances](./Songs/Word Distances) beinhalten die Anzahl an Wörter, die bei der Original-Version eines Liedes von WhisperAI falsch worden sind. Diese
   werden dementsprechend automatisch im [Programm](./Songs.py) erstellt, weshalb sie hier keine eigene Datei anfertigen sollen.
   Bei allen Dateien, die zu einem Lied gehören, ist es wichtig, dass Sie diesen den selben Namen geben, da nur so das Programm den Liedern ihre Texte und Videos zuordnen kann.
   

5. **KaraokeNet starten**

   Alles bis hierhin erledigt? Gut, dann müssen Sie nur noch das Skript interface_karaokenet.py ausführen. Dies können sie entweder in ihrer Entwicklungsumgebung machen, wenn sie das gesamte
   Repository in einem Projekt gespeichert haben, oder aber in einem Terminal, in welchem Sie sich erst zu dem Github Repository navigieren müssen. Im Anschluss können sie das Interface mit
   diesem Befehl starten:
   ```sh
   python interface_karaokenet.py
   ```
   Wie Sie nun das Interface anwenden können erfahren sie [hier](./README.md).
   

