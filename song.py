from speech_comparison import transcribe, levenshtein_distance, format_lyrics
import demucs.separate
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import shutil
import time

# songs_dir besteht aus den 4 Unterverzeichnissen Songs, Animations, Lyrics und Word Distances
songs_dir = r"Songs"
# seperated_songs_dir enthält ein Ordner für jedes Lied, in dem die Audiodateien vocals.mp3 und no_vocals.mp3 sind
seperated_songs_dir = r"separated/mdx_q"


class Song:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.song_path = f"{songs_dir}/Songs/{name}.mp3"
        self.lyrics_path = f"{songs_dir}/Lyrics/{name}.txt"
        self.lyrics = self.set_lyrics()
        self.transcribed_lyrics = None
        self.word_distance_path = f"{songs_dir}/Word_Distances/{name}.txt"
        self.video_path = f"{songs_dir}/Videos/{name}.mp4"
        self.instrumental_path = f"{seperated_songs_dir}/{name}/no_vocals.mp3"
        self.vocal_path = f"{seperated_songs_dir}/{name}/vocals.mp3"
        self.word_distance = None

    def set_lyrics(self):
        if os.path.exists(self.lyrics_path):
            with open(self.lyrics_path, "r") as lyrics:
                lyrics = lyrics.read()
                return lyrics
        return None

    # Bei einem neuen Lied muss aus dem Video zunächst der Song extrahiert und abgespeichert werden
    def create_song_file(self):
        if os.path.exists(self.song_path):
            return
        with VideoFileClip(self.video_path) as video:  # Video wird gespeichert
            song = video.audio  # Enthält das extrahierte Lied
            song.write_audiofile(self.song_path, codec='mp3')  # Speichert das Lied an seinem Pfad
            song.close()

    # Verwendung von demucs, wobei wir nur das Lied nur in Instrumental und Karaoke separieren müssen.
    # Durch mdx_q wird eine niedrigere Qualität zugunsten schnellerer Rechenzeit genutzt.
    def separate_song(self):
        if not (os.path.exists(self.vocal_path) and os.path.exists(self.instrumental_path)):
            demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_q", "-j", "2", self.song_path])

    def create_lyrics(self):
        self.lyrics = self.transcribed_lyrics
        with open(self.lyrics_path, "w") as lyrics_file:
            lyrics_file.write(self.lyrics)
        self.word_distance = 0
        return

    # Diese Methode berechnet, wie viele Wörter von dem originalen Sänger des Liedes von der KI falsch erkannt werden
    # und speichert dies in einer .txt-Datei ab, damit diese Daten persistent sind
    def set_word_distance(self):
        if not os.path.exists(self.word_distance_path):  # Falls das Lied neu hinzugefügt wurde
            # Speicher den formatierten Originaltext
            original_lyrics = format_lyrics(self.lyrics)
            # Speicher den formatierten KI-generierten Text des originalen Sängers
            transcribed_lyrics = format_lyrics(self.transcribed_lyrics)
            # Berechne, wie viele Wörter des originalen Sängers falsch erkannt wurden
            word_distance = levenshtein_distance(transcribed_lyrics, original_lyrics)
            # Speichere die Word Distanz in der entsprechenden Datei
            with open(self.word_distance_path, "w") as file:
                file.write(str(word_distance))
        # Ansonsten kann die Word Distanz aus der Datei ausgelesen werden
        with open(self.word_distance_path, "r") as word_distance_file:
            word_distance = int(word_distance_file.read())
        self.word_distance = word_distance

    # Diese Methode überschreibt das Audio des alten Videos mit der Instrumental-Version
    def overwrite_video(self):
        # Temporärer Pfad wo das neue Video zwischengespeichert wird
        temp_video_path = f"{songs_dir}/Videos/{self.name} [temp].mp4"
        with VideoFileClip(self.video_path) as video:
            with AudioFileClip(self.instrumental_path) as instrumental:
                # Erstellen des neuen Videos mit der neuen Audiodatei
                new_video = video.set_audio(instrumental)
                # Speichern des neuen Videos an einem temporären Ort
                new_video.write_videofile(temp_video_path, codec="libx264", audio_codec="aac")

        time.sleep(1)  # Sicherstellen, dass die Ressourcen (das Video) freigegeben werden

        # Ersetzen des alten Videos durch das neue Video, nachdem sie geschlossen wurden
        if os.path.exists(temp_video_path):
            try:
                os.remove(self.video_path)
                shutil.move(temp_video_path, self.video_path)  # altes Video mit neuem ersetzen
            except PermissionError:
                time.sleep(1)  # Zusätzliche Wartezeit
                os.remove(self.video_path)
                shutil.move(temp_video_path, self.video_path)

    # Diese Methode wird nur genutzt, wenn der Benutzer ein neues Lied hinzufügen will
    def create_new_song(self):
        self.create_song_file()  # Zuerst das Lied extrahieren
        self.separate_song()  # Dann aus dem Lied Instrumental- und Karaoke-Version extrahieren
        self.transcribed_lyrics = transcribe(self.vocal_path)
        if not os.path.exists(self.lyrics_path):
            self.create_lyrics()
        self.overwrite_video()  # Audio des alten Videos mit Instrumental-Version überschreiben


# Dictionary, mit den Song-Namen als Keys und Song-Objekten als Values
songs = {}


# Im Folgenden werden automatisiert die Song-Objekte erstellt auf Basis von den Musikvideos, die im entsprechenden
# Verzeichnis zu finden sind. Falls das Musikvideo neu ist, wird zusätzlich die Methode create_new_song() aufgerufen.
def set_song_objects():
    videos_folder_path = songs_dir + "/Videos"  # Ordner, in dem die Musikvideos sind
    for filename in os.listdir(videos_folder_path):
        song_name, extension = os.path.splitext(filename)  # Entfernt die Endung .mp3
        if song_name not in songs:  # Überprüft, ob der Song bereits im Dictionary vorhanden ist
            with VideoFileClip(os.path.join(videos_folder_path, filename)) as video:
                song_length = video.duration - 2  # Verkürzt die Länge, die das Lied auf der Website abgespielt wird,
                # da es sonst zu Komplikationen mit globalen Variablen kommt
            songs[song_name] = Song(song_name, song_length)
            if not (os.path.exists(songs[song_name].vocal_path) and os.path.exists(songs[song_name].instrumental_path)
                    and os.path.exists(songs[song_name].song_path) and os.path.exists(songs[song_name].lyrics_path)
                    and os.path.exists(songs[song_name].word_distance_path)):
                songs[song_name].create_new_song()
            songs[song_name].set_word_distance()


set_song_objects()
