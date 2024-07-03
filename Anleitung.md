# Anleitung zur Installation

Hier befindet sich die Anleitung dafür, wie Sie die Software auch auf Ihrem Computer zum Laufen bringen können.

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass die folgenden Softwarekomponenten auf Ihrem Computer installiert sind:

- Python 3.7 oder höher --> https://www.python.org/downloads/
- pip (Python Package Installer) --> https://pypi.org/project/pip/
- Git --> https://git-scm.com/downloads


1. **Repository klonen**:

   Öffnen Sie ein Terminal und führen Sie die folgenden Befehle einzeln nacheinander aus, um das Repository zu klonen und sich zu diesem zu navigieren:

   ```sh
   git clone https://github.com/GenosseJannik/HFU_KaraokeNet
   
   cd HFU_KaraokeNet
   ```
   
2. **Bibliotheken installieren**

   Wenn sie sich in einem Terminal zum Github Repository navigiert haben, können sie mit dem folgenden Befehl die für das Projekt notwendigen Bibliotheken installieren.
   ```sh
   pip install -r requirements.txt
   ```
   
3. **Neue Lieder hinzufügen (Optional)**:

   Die bestehende Software kann um weitere Lieder erweitert werden, indem Sie in den Unterverzeichnissen von [Songs](./Songs) die entsprechenden Dateien hinzufügen.
   Zu den Dateien, die sie hinzufügen müssen gehören:

   [Songs/Videos](./Songs/Videos): An diesem Ort sind die Videos, die die Texte der Lieder visualisieren, als .mp4-Datei abzulegen. Diese Datei ist zwingend notwendig.

   [Songs/Lyrics](./Songs/Lyrics): Damit die Bewertung der Aussprache besser funktioniert, speichern Sie hier die Songtexte als .txt-Datei ab. Wenn sie hier keine Datei abspeichern,
   so wird der KI-generierte Text des Original Liedes zur Bewertung genommen.

   Wenn Sie beide Dateien ablegen ist es wichtig, dass sie ihnen bis auf die Endung den gleichen Namen geben. Nur so kann das System einem Lied seinen Text zuordnen.

   Die Dateien in dem Ordner [Songs/Word Distances](./Songs/Word_Distances) beinhalten die Anzahl an Wörtern, die von dem originalen Sänger des Liedes von WhisperAI falsch erkannt wurden.
   Diese Dateien werden dementsprechend von der Software selbst erstellt, weshalb sie hier *keine* eigene Datei anfertigen sollen. Ebenfalls werden auch die .mp3-Dateien in
   [Songs/Songs](./Songs/Songs) automatisch aus der entsprechenden Video-Datei extrahiert. Wie genau das Integrieren eines neuen Liedes erfolgt, [erfahren sie hier](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/song.py#L98-L105).



4. **Interface starten**

   Alles bis hierhin erledigt? Gut, nun müssen Sie sich nur noch in einem Terminal zum Github Repository navigieren und folgenden Befehl ausführen.
   ```sh
   python interface_karaokenet.py
   ```
   Wie Sie sich auf der Website unserer Software zurechtfinden können erfahren Sie [hier](./README.md).
