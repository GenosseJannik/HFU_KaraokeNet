# [Anleitung zur Installation](./Anleitung.md)


# Willkommen zu unserer Karaokesoftware!
Herzlich willkommen zu unserer revolutionären Karaokesoftware! Hier erleben Sie Karaoke wie nie zuvor, unterstützt durch modernste Technologien und benutzerfreundliche Schnittstellen. Wir haben eine leistungsstarke Kombination von Tools integriert, um Ihnen ein unvergessliches Karaoke-Erlebnis zu bieten.




## Unsere Technologien
### Gradio – Benutzerfreundliches Interface
Unsere Software verwendet [Gradio für die Benutzeroberfläche](./interface_karaokenet.py#L225-L321). Gradio ist ein intuitives Framework, das es uns ermöglicht, interaktive Webanwendungen zu erstellen. Mit Gradio können Sie ganz einfach durch unsere Liederauswahl navigieren und das Karaoke-Erlebnis starten – alles in einer übersichtlichen und benutzerfreundlichen Umgebung.

### Demucs – Musikalische Trennung
Wir setzen Demucs, ein fortschrittliches neuronales Netz, ein, um Songs in ihre Bestandteile zu zerlegen. [Demucs trennt das Lied in Instrumental- und Karaoke-Versionen](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/song.py#L45-L51), sodass Sie nur die Instrumentalmusik hören, während der Text angezeigt wird. Dies ermöglicht Ihnen ein authentisches Karaoke-Erlebnis mit hoher Klangqualität. Die Karaoke-Verions wird genutzt, um ihre Karaoke-Version mit der des Originalliedes zu vergleichen.

### Librosa – Bewertung der Gesangsleistung
Um Ihre gesangliche Leistung zu bewerten, verwenden wir Librosa, eine leistungsstarke Bibliothek für die Audioanalyse. Librosa analysiert die [Tonhöhe](./pitch_comparison_transposition.py#L30-L59), das [Timing](./timing_comparison.py#L21-L27) und andere Aspekte Ihres Gesangs, um Ihnen ein detailliertes Feedback zu geben. So können Sie Ihre Fähigkeiten verbessern und Ihre Karaoke-Performance optimieren.

### WhisperAI – Spracherkennung
Für die [Erkennung ihrer Aussprache](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/speech_comparison.py#L34-L42) während des Singens nutzen wir WhisperAI. Diese leistungsstarke Spracherkennungssoftware sorgt dafür, dass Ihre gesungenen Worte präzise erkannt werden. Im Anschluss wird berechnet, inwieweit der durch WhisperAi generierte Text ihrer Aufnahme ähnlich zu dem WhisperAi generierten Text des Originalliedes ist, wofür die [Anzahl an unterschiedlichen Wörter berechnet wird](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/speech_comparison.py#L45-L60).


## Anleitung
### Vorbereitung
Stellen Sie sicher, dass Sie ein funktionsfähiges Mikrofon an Ihrem Computer angeschlossen haben. Das Mikrofon, das in den Systemeinstellungen als Standard-Ausgabegerät festgelegt ist, wird verwendet. Um dies zu überprüfen oder zu ändern, gehen Sie in die Einstellungen Ihres Betriebssystems und suchen Sie nach den Audio- oder Soundeinstellungen. Hier können Sie das gewünschte Mikrofon als Standardgerät auswählen. Testen Sie anschließend das Mikrofon, um sicherzustellen, dass es ordnungsgemäß funktioniert. 

Zudem müssen Sie bei Apple in den Sicherheitseinstellungen dem Mikrofon erlauben, dass Programme, die im Terminal ausgeführt werden, auf das Mikrofon zugreifen dürfen. Gehen Sie dazu zu den Systemeinstellungen, wählen Sie "Sicherheit" und dann "Datenschutz". Unter dem Abschnitt "Mikrofon" können Sie den Zugriff für Programme aktivieren.

Für Windows-Benutzer gilt ähnliches: Gehen Sie zu den Einstellungen, wählen Sie "Datenschutz" und dann "Mikrofon". Hier können Sie festlegen, welche Anwendungen auf das Mikrofon zugreifen dürfen. Stellen Sie sicher, dass der Zugriff für das Terminal aktiviert ist.


### So funktioniert es
1. Lied auswählen: Starten Sie die Software und wählen Sie Ihr Lieblingslied aus der Liste.


![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/05f8685f-64c2-49b5-a5ac-693fa866c5b7)


2. Ausprobieren: Bevor sie mit dem richtigen Versuch loslegen, besteht für sie die Möglichkeit das Lied welches sie singen möchten, vorher zu proben. Hier können sie sich den Text des Liedes sowie die Rhytmik und Melodien des Gesangs einprägen.
   
   
![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/aeb06ba0-bf50-451a-876f-e8e789f2f96e)



Von hier aus können Sie entweder Schritt 3 befolgen, um selber eine Karaoke-Version zu singen, oder aber Sie laden eine bereits existierende Karaoke-Version hoch, was in Schritt 4 erklärt
wird.



3. Aufnahme starten:
   
   1. Klicken Sie auf das Mikrofon, um das Video mit der Instrumentalversion und dem Text zu laden.
   ![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/9ee65dc2-8ba0-45ef-80a6-697c4a3a3c02)

   2.  Singen Sie mit dem angezeigten Text mit. Ihre Stimme wird ab Start des Videos bis zum Ende aufgenommen. Dabei ist es wichtig, dass sie zu Beginn von Sekunde 0 an starten und bis zur
   letzten Sekunde das Video abspielen lassen. Andernfalls erhalten sie keine Bewertung zu ihrer gesungenen Karaoke-Version.
   
   ![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/833a71e4-ef18-4421-9c53-4e5a7914ccac)

5. Cover Hochladen:
   
   1. Klicken sie auf das Upload-Emoji, um in das Layout zu gelangen, indem sie eine Karaoke-Version des ausgewählten Liedes hochladen können.
   ![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/42f2696c-b5b7-467c-8b98-fa4532282c69)

   2. Ziehen sie ihre bereits existierende Karaoke-Version in .wav-Format per Drag and Drop in die Box rein. Ein paar Beispiele für Cover-Versionen finden Sie in dem Ordner [Cover_Examples](./Cover_Examples).
   ![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/8a6af38e-8bd5-43fd-9955-427b73531563)


6. Bewertung: Sie erhalten sobald Sie auf 'Evaluate result'  drücken ihr Ergebnis des gesungenen oder hochgeladenen Liedes. In einem Balkendiagramm wird ihre Stimme im Vergleich zum Original
anhand von bestimmten Kriterien bewertet. Sie erhalten ebenfalls detaillierte Information darüber, um wie viele Seminoten der Gesang des Covers sich von dem des Originals unterschieden hat.
![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/33d2b0a3-dfd2-4c14-b607-89d28e50ff3b)

7. Durch Klicken auf den 'Start menu' Button gelangen sie zurück zum Startbildschirm und können erneut eine Karaoke-Aufnahme starten oder hochladen.



Wir wünschen Ihnen viel Spaß und Erfolg mit unserer Karaokesoftware. Lassen Sie uns gemeinsam die Freude am Singen erleben!



