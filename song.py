from song_lyrics import song_lyrics

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


song_names = {'lp': "Linkin Park - In the End", 'es': "Ed Sheeran - Shape of you"}  # Abkürzung der Songtitel

# Dictionary mit den Song-Namen als Keys und Song-Objekten als Values
songs = {song_names['lp']: Song(song_names['lp'], 20, song_lyrics[song_names['lp']]),
         song_names['es']: Song(song_names['es'], 20, song_lyrics[song_names['es']])}
