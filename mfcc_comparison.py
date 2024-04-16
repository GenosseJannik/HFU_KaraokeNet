import os
import librosa
import numpy as np

original_file = r"KaraokeNet\Musikbeispiel\In The End (Original)\vocals_original.mp3"
cover_file = r"KaraokeNet\Musikbeispiel\In The End (Cover)\vocals_cover.mp3"

def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return mfccs

def equalize_length(array1, array2):
    # Bestimme die maximale Länge der beiden Arrays
    max_length = max(array1.shape[1], array2.shape[1])
    
    # Passe die Form der kürzeren Arrays an, indem sie auf die Länge der längeren Arrays verlängert werden
    if array1.shape[1] < max_length:
        array1 = np.pad(array1, ((0, 0), (0, max_length - array1.shape[1])), mode='constant')
    elif array2.shape[1] < max_length:
        array2 = np.pad(array2, ((0, 0), (0, max_length - array2.shape[1])), mode='constant')
    
    return array1, array2

def compare_mfcc(original_file, cover_file):
    original_mfcc = extract_features(original_file)
    cover_mfcc = extract_features(cover_file)

    original_mfcc, cover_mfcc = equalize_length(original_mfcc, cover_mfcc)
    
    # Berechne die kosinusbasierte Ähnlichkeit zwischen den beiden MFCCs
    cosine_similarity = np.dot(original_mfcc.flatten(), cover_mfcc.flatten()) / (np.linalg.norm(original_mfcc) * np.linalg.norm(cover_mfcc))
    
    # Wandle kosinusbasierte Ähnlichkeit in Prozent um
    similarity_percentage = 0.5 * (cosine_similarity + 1) * 100

    return similarity_percentage

similarity_percentage = compare_mfcc(original_file, cover_file)
print("Ähnlichkeit der beiden Audiodateien: {:.2f}%".format(similarity_percentage))