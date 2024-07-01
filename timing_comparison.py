import librosa
import numpy as np

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

def compare_timings(onsets_original, onsets_cover, tolerance=0.1):
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

original_file = r"C:\Users\julia\Desktop\KaraokeNet\Musikbeispiel\In_The_End_(Original)\vocals_original.mp3"
cover_file = r"C:\Users\julia\Desktop\KaraokeNet\Musikbeispiel\In_The_End_(Cover)\vocals_cover.mp3"
    
# Load audios
y_original, sr_original = load_audio(original_file)
y_cover, sr_cover = load_audio(cover_file)
    
# Extract onsets
onsets_original = extract_onsets(y_original, sr_original)
onsets_cover = extract_onsets(y_cover, sr_cover)
    
# Define tolerance
tolerance = 0.1  # in seconds
    
# Compare timings
differences = compare_timings(onsets_original, onsets_cover, tolerance)
    
# Calculate score
score = calculate_score(differences, tolerance)
    
# Print results
for i, diff in enumerate(differences):
    if abs(diff) > tolerance:
        print(f"Note {i+1}: {diff:.2f} seconds {'early' if diff < 0 else 'late'}")
    else:
        print(f"Note {i+1}: On time")
    
print(f"Timing Score: {score:.2f}%")