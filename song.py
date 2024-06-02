from speech_comparison import transcribe, levenshtein_distance, format_lyrics
import demucs.separate
import os
from mutagen.mp3 import MP3

# songs_dir besteht aus den 4 Unterverzeichnissen Songs, Animations, Lyrics und Word Distances
songs_dir = r"C:/Users/20edu/Softwareprojekt/pythonProject1/Songs"
seperated_songs_dir = r"C:/Users/20edu/Softwareprojekt/pythonProject1/separated/mdx_q"


class Song:
    def __init__(self, name, length):
        self.name = name
        self.length = length
        self.song_path = f"{songs_dir}/Songs/{name}.mp3"
        self.lyrics_path = f"{songs_dir}/Lyrics/{name}.txt"
        self.lyrics = self.set_lyrics()
        self.animation_path = f"{songs_dir}/Animations/{name}.mp4"
        self.instrumental_path = f"{seperated_songs_dir}/{name}/no_vocals.mp3"
        self.vocal_path = f"{seperated_songs_dir}/{name}/vocals.mp3"
        self.word_distance = None

    # diese Methode berechnet, wie viele Wörter des Liedes von der KI für konkret jedes Lied falsch erkannt werden
    def set_word_distance(self):
        file_path = songs_dir + "/Word Distances/" + self.name + ".txt"
        if not os.path.exists(file_path):
            transcribed_lyrics = format_lyrics(transcribe(self.vocal_path))
            original_lyrics = format_lyrics(self.lyrics)
            word_distance = levenshtein_distance(transcribed_lyrics.split(), original_lyrics.split())
            with open(file_path, "w") as file:
                file.write(str(word_distance))
        with open(file_path, "r") as word_distance_file:
            self.word_distance = word_distance_file.read()

    def separate_song(self):
        if not os.path.exists(self.vocal_path) and os.path.exists(self.instrumental_path):
            demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_q", "-j", "2", self.song_path])

    def set_lyrics(self):
        with open(self.lyrics_path, "r") as lyrics:
            lyrics = lyrics.read()
        return lyrics


# Dictionary, mit den Song-Namen als Keys und Song-Objekten als Values
songs = {}


# Im Folgenden werden automatisiert und nur bei Bedarf Song-Objekte erstellt auf Basis von den Liedern, die im
# angegebenen Verzeichnis hinterlegt sind, wobei auch leicht neue hinzugefügt werden können
def set_song_objects():
    folder_path = songs_dir + "/Songs"  # Ordner, in dem die Lieder sind
    for filename in os.listdir(folder_path):
        song_name, extension = os.path.splitext(filename)  # entfernt die Endung .mp3
        if song_name not in songs:  # Überprüfe, ob der Song bereits im Dictionary vorhanden ist
            song_length = MP3(os.path.join(folder_path, filename)).info.length
            songs[song_name] = Song(song_name, song_length)
            songs[song_name].separate_song()
            songs[song_name].set_word_distance()


set_song_objects()
