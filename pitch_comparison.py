import os
import librosa
import numpy as np

original_file = r"KaraokeNet\Musikbeispiel\In The End (Original)\vocals_original.mp3"
cover_file = r"KaraokeNet\Musikbeispiel\In The End (Cover)\vocals_cover.mp3"

def extract_pitch(audio_file, frame_length=2048, hop_length=512):
    y, sr = librosa.load(audio_file, sr=None)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, S=None, n_fft=frame_length, hop_length=hop_length)
    pitch_indices = np.abs(pitches).argmax(axis=0)
    pitch_signs = np.sign(pitches[pitch_indices, np.arange(pitches.shape[1])])
    pitch = pitch_signs * pitches[pitch_indices, np.arange(pitches.shape[1])]
    return pitch

def equalize_length(array1, array2):
    # Bestimme die maximale Länge der beiden Arrays
    max_length = max(array1.shape[0], array2.shape[0])
    
    # Passe die Form der kürzeren Arrays an, indem sie auf die Länge der längeren Arrays verlängert werden
    if array1.shape[0] < max_length:
        padding = ((0, max_length - array1.shape[0]), *[(0, 0)] * (len(array1.shape) - 1))
        array1 = np.pad(array1, padding, mode='constant')
    elif array2.shape[0] < max_length:
        padding = ((0, max_length - array2.shape[0]), *[(0, 0)] * (len(array2.shape) - 1))
        array2 = np.pad(array2, padding, mode='constant')
    
    return array1, array2

def compare_pitch(original_file, cover_file):
    original_pitch = extract_pitch(original_file)
    cover_pitch = extract_pitch(cover_file)
    original_pitch, cover_pitch = equalize_length(original_pitch, cover_pitch)
    
    # Berechne die durchschnittliche Abweichung zwischen den Tonhöhen
    pitch_difference = original_pitch - cover_pitch
    
    # Bestimme die Richtung der Tonhöhenabweichung
    deviation_direction = "Gut gesungen"
    if np.any(pitch_difference > 0):  # Es gibt Abweichungen, bei denen das eingesungene Audio zu tief ist
        deviation_direction = "Zu tief gesungen"
    elif np.any(pitch_difference < 0):  # Es gibt Abweichungen, bei denen das eingesungene Audio zu hoch ist
        deviation_direction = "Zu hoch gesungen"
    
    return deviation_direction, np.mean(np.abs(pitch_difference))

deviation_direction, pitch_difference_value = compare_pitch(original_file, cover_file)
print("Durchschnittliche Tonhöhendifferenz: {:.2f}".format(pitch_difference_value))
print("Gesangliche Abweichung: {}".format(deviation_direction))