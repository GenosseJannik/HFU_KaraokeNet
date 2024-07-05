##Dies ist die Zusammenfassung der Arbeitsspakete im Laufe des Projekts

#Jannik:
- Aufsetzten der Projektstruktur
- Servererstellung und Wartung
- Kommunikation mit Server und vom Server zum Client

#Fisnik/Naphy:
- Dokumentation der Read Me (In zusammenarbeit mit Eduard)
- Weekly Scrums
- Rechteabklärung bezüglich der Musik
- Organisation des Tag der offenen Tür sowie Tag der Informatik
- Materialorganisation
- Kontakt mit Herr Goßmann (Lief nicht seitens Herr Goßmann)
- Erstellung des Präsentationsmaterials (Powerpoint, Plakate)
- Gegen ende des Projekts etwas Tweaking an Benutzeroberfläche(Mit Eduard)

#Julia:
- Informieren, welche Pakete/Imports sinnvoll sind
- Einarbeitung in Librosa
- Erster allgemeiner Vergleich mittels MFCCs (wird im Endprodukt nicht mehr verwendet)
- extrahieren der Tonhöhen (MIDI-Werte, Frequenzwerte)
- Umwandlung der MIDI-Werte in Notennamen
- automatisches Erkennen, um wieviele Halbtonschritte transponiert wurde
- Transponieren einer Karaoke-Version (um diese bei der Bewertung zu berücksichtigen)
- Rückmeldunng am Ende, um wie viele Halbtonschritte (nach Transposition) "falsch" gesungen wurde
- Aufteilung der Audiospur in mehrere kleine Teile (um die Bewertung genauer zu machen)
- Extrahieren der BPM (im Endprodukt durch onsets ersetzt, da bpm vor allem auf instrumental basieren und daher ungeeignet sind)
- Auslesen der Onsets der Audiospuren (Timestamps, wann der Gesang jeweils beginnt)
- Vergleich der Timestamps (Bwertung anhand prozentualer Anteil der zur richtigen Zeit war)
- Überarbeiten der jeweiligen Toleranzwerte bei der Bewertung (strenge der Bewertung an die Lieder/Anforderungen anpassen)

#Eduard:
- Einarbeitung in Gradio, JavaScript (Zusammenarbeit mit Fisnik) und CSS für das Interface (interface_karaokenet.py)
- Nutzung von WhisperAI zur Spracherkunnung und Implementierung des Sprachvergleichs (speech_comparison.py)
- Automatisierung des Prozesses ein neues Lied hinzuzufügen (Aus Videodatei werden alle für das Systems notwendige Bestandteile extrahiert) (song.py)
- Zusammenführung aller Vergleiche in das Interface (Implementierung der Datenübertragung)
- Hinzufügen der Verzeichnisstruktur mit Beispieldateien, dass jeder auf Basis der Anleitung das System bei sich zum Laufen bringen kann
- Erstellung der README mit Fisnik zusammen
- Erstellung der Anleitung zur Installation
