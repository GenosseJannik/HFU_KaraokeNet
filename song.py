from song_lyrics import song_lyrics
from speech_comparison import transcribe, levenshtein_distance, format_lyrics
import demucs.separate


music_directory = "C:/Users/20edu/Softwareprojekt/pythonProject1/separated/mdx_q"
animation_directory = "C:/Users/20edu/Softwareprojekt/pythonProject1/animations"


class Song:
    def __init__(self, name, length, lyrics):
        self.name = name
        self.length = length
        self.instrumental_path = f"{music_directory}/{name}/no_vocals.mp3"
        self.vocal_path = f"{music_directory}/{name}/vocals.mp3"
        self.song_path = f"{music_directory}/{name}/song.mp3"
        self.lyrics = lyrics
        self.animation = f"{animation_directory}/{name}.mp4"
        self.word_distance = self.set_word_distance()

    # diese Methode berechnet, wie viele Wörter des Liedes von der KI für konkret jedes Lied falsch erkannt werden
    def set_word_distance(self):
        transcribed_lyrics = format_lyrics(transcribe(self.vocal_path))
        original_lyrics = format_lyrics(self.lyrics)
        word_distance = levenshtein_distance(transcribed_lyrics.split(), original_lyrics.split())
        return word_distance

    def separate_song(self):
        demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_q", "-j", "2", self.song_path])


# Dictionary, mit den Song-Namen als Keys und Song-Objekten als Values
songs = {"Linkin Park - In the End": Song("Linkin Park - In the End", 20, song_lyrics["Linkin Park - In the End"])}
