import librosa
import numpy as np
from pitch_comparison_transposition import trim_silence


def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


def extract_onsets(audio, sr):
    # Extract onset envelope
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    # Detect onsets
    onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    # Convert frame indices to time
    onset_times = librosa.frames_to_time(onsets, sr=sr)
    return onset_times


def compare_timings(onsets_original, onsets_cover):
    differences = []
    for o_cover in onsets_cover:
        closest_original = min(onsets_original, key=lambda o: abs(o - o_cover))
        difference = o_cover - closest_original
        differences.append(difference)
    return np.array(differences)


def calculate_score(differences, tolerance):
    on_time_count = np.sum(np.abs(differences) <= tolerance)
    total_count = len(differences)
    score = (on_time_count / total_count) * 100
    return score


def compare_timing(original_file, cover_file, tolerance=0.2):
    # Load audios
    y_original, sr_original = load_audio(original_file)
    y_cover, sr_cover = load_audio(cover_file)

    # Trim silence
    trimmed_y_original, trimmed_y_cover = trim_silence(y_original, y_cover, tolerance)

    # Extract onsets
    onsets_original = extract_onsets(trimmed_y_original, sr_original)
    onsets_cover = extract_onsets(trimmed_y_cover, sr_cover)

    # Compare timings
    differences = compare_timings(onsets_original, onsets_cover)

    # Calculate score
    score = calculate_score(differences, tolerance)

    return score

