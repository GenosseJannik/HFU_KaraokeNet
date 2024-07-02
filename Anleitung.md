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

   Navigieren sie sich in einem Terminal zum Github Repository und führen Sie folgenden Befehl aus.
   diesem Befehl starten:
   ```sh
   python interface_karaokenet.py
   ```
   Wie Sie sich auf der Website unserer der Software als Sänger zurechtfinden können erfahren Sie [hier](./README.md).
   
5. **Nutzung des Interface mit existierenden Karaoke-Versionen**
   
   Das standartmäßigen Interface ist so vorgesehen, dass der Benutzer zur Laufzeit seine Karaoke-Version erstellt und diese im Nachhinein bewertet wird. Wenn sie selbst nicht singen möchten,
   aber dennoch sehen wollen wie die Software bereits existierende Karaoke-Versionen bewertet, müssen sie folgende Anweisungen beachten.
   1. Da das reine Testen nicht für die Benutzer vorgesehen ist, müssen sie [diesen Befehl](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/interface_karaokenet.py#L252) im
   Interface ändern. Sie ersetzen den Befehl durch:
   ```sh
    with gr.Column() as testing_layout:
   ```
   Dies stellt sicher, dass die Komponente zum Testen angezeigt wird. Implizit bedeutet der Befehl "with gr.Column(visible=True) as testing_layout.

   
   2. Ihr Benutzeroberfläche sollte nun folgendermaßen aussehen:
   ![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/1473c629-2023-4639-add9-8c7c7909d7b2)

   Zunächst wählen sie das Lied aus, dessen existierende Karaoke-Version sie bewerten lassen wollen. Als nächstes fügen sie das Lied als .wav Datei in der unteren Box per Drag-And-Drop ab.

   3. Testing Drücken
   

