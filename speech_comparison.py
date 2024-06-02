from transformers import pipeline
import numpy as np
import librosa

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")  # base model laden


def compare_speech(song, karaoke_audio_path):
    cleaned_original_lyrics = format_lyrics(song.lyrics)

    recognized_lyrics = transcribe(karaoke_audio_path)  # KI erkannte Lyrics aus den User-Vocals erstellen
    cleaned_recognized_lyrics = format_lyrics(recognized_lyrics)

    cleaned_original_lyrics_words = cleaned_original_lyrics.split()
    cleaned_recognized_lyrics_words = cleaned_recognized_lyrics.split()

    word_distance = levenshtein_distance(cleaned_original_lyrics_words, cleaned_recognized_lyrics_words)
    word_count_original = len(cleaned_original_lyrics_words)  # Anzahl an Wörtern
    # erlaubt, dass 10 % mehr Wörter falsch erkannt werden dürfen als beim Original
    if word_distance < song.word_distance + word_count_original * 0.1:
        return 1  # Schulnote 1
    elif word_distance < 9 + word_count_original * 0.2:
        return 2
    else:
        return 3


def format_lyrics(lyrics):
    new_lyrics = lyrics.lower()
    new_lyrics = ' '.join(new_lyrics.replace(',', '').replace('.', '').split())
    return new_lyrics


def transcribe(audio_path):
    audio = librosa.load(audio_path)
    # hier wäre es ggf. sinnvoll den Anfang der Karaoke-Version zu kürzen, bis angefangen wird zu singen
    y, sr = audio
    y = y.astype(np.float32)  # Umwandlung von int zu float für transcriber
    y /= np.max(np.abs(y))  # normieren auf Werte zwischen 0 und 1

    return transcriber({"sampling_rate": sr, "raw": y})["text"]


def levenshtein_distance(words_1, words_2):  # erwartet 2 Listen, in denen die Wörter der Texte sind
    matrix = np.zeros((len(words_1) + 1, len(words_2) + 1))  # Anzahl der Wörter in words_1 = Anzahl der Zeilen

    for i in range(len(words_1) + 1):  # Initialisierung der ersten Zeile und Spalte
        matrix[i][0] = i
    for j in range(len(words_2) + 1):
        matrix[0][j] = j

    for i in range(1, len(words_1) + 1):
        for j in range(1, len(words_2) + 1):
            cost = 0 if words_1[i - 1] == words_2[j - 1] else 1  # cost=0, falls die aktuellen Zeichen übereinstimmen
            matrix[i][j] = min(matrix[i - 1][j] + 1,  # Löschung, z.B. wenn Länge der Wörter verschieden
                               matrix[i][j - 1] + 1,  # Einfügung
                               matrix[i - 1][j - 1] + cost  # Ersetzung
                               )
    return int(matrix[len(words_1)][len(words_2)])  # der letzte Eintrag in der Matrix = Anzahl der verschiedenen Wörter

