from transformers import pipeline
import numpy as np
import librosa
from pitch_comparison_transposition import trim_silence

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")  # base model laden


def compare_speech(song, user_lyrics):
    # Formatiert die originalen Lyrics
    cleaned_original_lyrics_words = format_lyrics(song.lyrics)
    # Formatiert den KI-generierten Text des Benutzers
    cleaned_user_lyrics_words = format_lyrics(user_lyrics)

    # Berechnet die Anzahl an Wörtern, die sich der KI-generierte Text des Benutzers vom originalen Text unterscheidet
    word_distance = levenshtein_distance(cleaned_original_lyrics_words, cleaned_user_lyrics_words)
    # Anzahl an Wörter, die sich der KI-generierte Text des original-Liedes vom originalen Text unterscheidet
    word_distance_original = song.word_distance
    # Gesamte Anzahl an Wörtern im originalen Songtext
    word_length_original = len(cleaned_original_lyrics_words)

    # Lineare Interpolation, die die Anzahl falsch erkannter Wörter einer Prozentzahl zuordnet
    accuracy_percentage = 100 * max(0, 1 - (word_distance - word_distance_original) / (word_length_original - word_distance_original))

    return accuracy_percentage


def format_lyrics(lyrics):
    new_lyrics = lyrics.lower()
    new_lyrics = ' '.join(new_lyrics.replace(',', '').replace('.', '').split())
    return new_lyrics.split()


def transcribe(audio_path):
    y, sr = librosa.load(audio_path)
    # Schneidet den Anfang raus, damit die KI nicht aus Hintergrundrauschen irgendwelche Wörter erkennt
    trimmed_y, _, _ = trim_silence(y, sr)

    trimmed_y = trimmed_y.astype(np.float32)  # Umwandlung der Frequenzen von int zu float für transcriber
    trimmed_y /= np.max(np.abs(y))  # Normieren auf Werte zwischen 0 und 1

    return transcriber({"sampling_rate": sr, "raw": y})["text"]


def levenshtein_distance(words1, words2):  # Erwartet 2 Listen, in denen die Wörter der Texte sind
    matrix = np.zeros((len(words1) + 1, len(words2) + 1))  # Anzahl der Wörter in words1 = Anzahl der Zeilen

    for i in range(len(words1) + 1):  # Initialisierung der ersten Zeile und Spalte
        matrix[i][0] = i
    for j in range(len(words2) + 1):
        matrix[0][j] = j

    for i in range(1, len(words1) + 1):
        for j in range(1, len(words2) + 1):
            cost = 0 if words1[i - 1] == words2[j - 1] else 1  # cost=0, falls die aktuellen Zeichen übereinstimmen
            matrix[i][j] = min(matrix[i - 1][j] + 1,  # Löschung, z.B. wenn Länge der Wörter verschieden
                               matrix[i][j - 1] + 1,  # Einfügung
                               matrix[i - 1][j - 1] + cost  # Ersetzung
                               )
    return int(matrix[len(words1)][len(words2)])  # Der letzte Eintrag in der Matrix = Anzahl der verschiedenen Wörter

