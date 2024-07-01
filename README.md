# HFU_KaraokeNet
Repository for semesterproject about a tool that will help you improve your skills at karaoke


# Willkommen zu unserer Karaokesoftware!
Herzlich willkommen zu unserer revolutionären Karaokesoftware! Hier erleben Sie Karaoke wie nie zuvor, unterstützt durch modernste Technologien und benutzerfreundliche Schnittstellen. Wir haben eine leistungsstarke Kombination von Tools integriert, um Ihnen ein unvergessliches Karaoke-Erlebnis zu bieten.

## Unsere Technologien
### Gradio – Benutzerfreundliches Interface
Unsere Software verwendet [Gradio für die Benutzeroberfläche](./interface_karaokenet.py#L227-L299). Gradio ist ein intuitives Framework, das es uns ermöglicht, interaktive Webanwendungen zu erstellen. Mit Gradio können Sie ganz einfach durch unsere Liederauswahl navigieren und das Karaoke-Erlebnis starten – alles in einer übersichtlichen und benutzerfreundlichen Umgebung.

### Demucs – Musikalische Trennung
Wir setzen Demucs, ein fortschrittliches neuronales Netz, ein, um Songs in ihre Bestandteile zu zerlegen. [Demucs trennt das Lied in Instrumental- und Karaoke-Versionen](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/song.py#L44-48), sodass Sie nur die Instrumentalmusik hören, während der Text angezeigt wird. Dies ermöglicht Ihnen ein authentisches Karaoke-Erlebnis mit hoher Klangqualität. Die Karaoke-Verions wird genutzt, um ihre Karaoke-Version mit der des Originalliedes zu vergleichen.

### Librosa – Bewertung der Gesangsleistung
Um Ihre gesangliche Leistung zu bewerten, verwenden wir Librosa, eine leistungsstarke Bibliothek für die Audioanalyse. [Librosa analysiert die Tonhöhe](./pitch_comparison_transposition.py#L56-L81), das Timing und andere Aspekte Ihres Gesangs, um Ihnen ein detailliertes Feedback zu geben. So können Sie Ihre Fähigkeiten verbessern und Ihre Karaoke-Performance optimieren.

### WhisperAI – Spracherkennung
Für die [Erkennung ihrer Aussprache](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/speech_comparison.py#L34-L42) während des Singens nutzen wir WhisperAI. Diese leistungsstarke Spracherkennungssoftware sorgt dafür, dass Ihre gesungenen Worte präzise erkannt werden. Im Anschluss wird berechnet, inwieweit der durch WhisperAi generierte Text ihrer Aufnahme ähnlich zu dem WhisperAi generierten Text des Originalliedes ist, wofür die [Anzahl an unterschiedlichen Wörter berechnet wird](https://github.com/GenosseJannik/HFU_KaraokeNet/blob/main/speech_comparison.py#L45-L60).


## Anleitung
### So funktioniert es
1. Lied auswählen: Starten Sie die Software und wählen Sie Ihr Lieblingslied aus der Liste.

![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/ada17e06-8cfd-4115-832d-0ed615805e01)

2. Ausprobieren: Bevor sie mit dem richtigen Versuch loslegen, besteht für sie die Möglichkeit das Lied welches sie singen möchten, vorher zu proben. Hier können sie sich den Text des Liedes sowie die Rhytmik und Melodien des Gesangs einprägen.
   
![Vorlesung04_KI_und_Musik_KW44_WiSe2023](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/0d8804d8-b919-41ae-8e89-391ded1a9a53)
  
3. Starten: Klicken Sie auf "Starten", um das Video mit der Instrumentalversion und dem Text zu starten.

![starten](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/88941996-e89a-4d63-a297-4c87c341f3a3)
   
4. Singen: Singen Sie mit dem angezeigten Text mit. Ihre Stimme wird ab Start des Videos bis zum Ende aufgenommen. Dabei ist es wichtig, dass sie zu Beginn von Sekunde 0 an starten und bis zur letzten Sekunde das Video abspielen lassen. Andernfalls erhalten sie keine Bewertung zu ihrer gesungenen Karaoke-Version, sondern nur eine Fehlermeldung.

![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/94164bb3-085f-4a97-897b-c717b87ec248)

5. Bewertung: Sie erhalten sobald sie auf 'Ergebnis auswerten' ihr Ergebnis des gesungenen Liedes. In einem Balkendiagramm wird ihre Stimme im Vergleich zum Original bewertet.
Sie erhalten ebenfalls eine Information, inwiefern die Software ihre Stimme transponieren musste, um ein akkurateres Ergebnis zu erhalten.
![image](https://github.com/GenosseJannik/HFU_KaraokeNet/assets/165167290/dec82589-fb45-41d8-acda-49be52eeca39)

Wenn sie das System auch auf ihrem eigenen Rechner nutzen wollen, finden sie [hier](./Anleitung.md) genau die richtige Anleitung für sie.

Wir wünschen Ihnen viel Spaß und Erfolg mit unserer Karaokesoftware. Lassen Sie uns gemeinsam die Freude am Singen erleben!



