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

   Die bestehende Software kann um weitere Lieder erweitert werden, indem Sie in dem Verzeichnis Songs die entsprechenden Dateien hinzufügen.
   Zu den Dateien, die sie hinzufügen müssen gehören:

   
   [Songs/Songs](./Songs/Songs): Hier legen Sie die .mp3-Datei des Liedes ab.
   
   [Songs/Lyrics](./Songs/Lyrics): Damit die Bewertung der Aussprache funktioniert, speichern Sie hier die Songtexte als .txt-Datei ab.

   [Songs/Video](./Songs/Video): An diesem Ort sind die Videos, die die Texte der Lieder visualisieren, als .mp4-Datei abzulegen.

   Bei allen zu einem Lied gehörenden Dateien, ist es wichtig, dass Sie diesen den selben Namen geben, da nur so das Programm den Liedern ihre Texte und Videos zuordnen kann.

   Die Dateien in dem Ordner [Songs/Word Distances](./Songs/Word_Distances) beinhalten die Anzahl an Wörter, die bei der Original-Version eines Liedes von WhisperAI falsch erkannt worden
   sind. Diese Dateien werden dementsprechend von der Software selbst erstellt, weshalb sie hier *keine* eigene Datei anfertigen sollen. 



5. **KaraokeNet starten**

   Alles bis hierhin erledigt? Gut, dann müssen Sie nur noch das Skript interface_karaokenet.py ausführen. Dies können sie entweder in ihrer Entwicklungsumgebung machen, wenn sie das gesamte
   Repository in einem Projekt gespeichert haben, oder aber in einem Terminal, in welchem Sie sich erst zu dem Github Repository navigieren müssen. Im Anschluss können sie das Interface mit
   diesem Befehl starten:
   ```sh
   python interface_karaokenet.py
   ```
   Wie Sie sich nun auf der Website unserer KaraokeNet Software zurechtfinden können erfahren sie [hier](./README.md).
   

