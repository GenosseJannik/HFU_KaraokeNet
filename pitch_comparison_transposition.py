import librosa
import numpy as np

def extract_notes(audio_file_path):
    # Load the audio file
    y, sr = librosa.load(audio_file_path)

    # Calculate the duration of the audio in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    # Divide the audio into 10 equal-length sections
    section_duration = duration / 10
    section_notes = []

    for i in range(10):
        start_time = i * section_duration
        end_time = (i + 1) * section_duration

        # Extract the pitches for the current section
        pitches, magnitudes = librosa.piptrack(y=y[int(start_time * sr):int(end_time * sr)], sr=sr)

        # Filter out zero or negative frequencies
        pitches = pitches[pitches > 0]

        # Convert pitches to MIDI notes
        notes = librosa.hz_to_midi(pitches)

        # Calculate the average note of the current section
        avg_note = np.mean(notes) if len(notes) > 0 else None
        section_notes.append(avg_note)

    return section_notes

def note_num_to_name(note_num):
    if note_num is None:
        return "None"
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'H']
    octave = note_num // 12 - 1
    note = notes[note_num % 12]
    return f"{note}{octave}"

def compare_avg_notes(audio_file_path1, audio_file_path2):
    # Extract average notes for the first audio file
    avg_notes1 = extract_notes(audio_file_path1)

    # Extract average notes for the second audio file
    avg_notes2 = extract_notes(audio_file_path2)

    # Convert MIDI notes to note names
    avg_notes1_names = [note_num_to_name(int(note)) for note in avg_notes1]
    avg_notes2_names = [note_num_to_name(int(note)) for note in avg_notes2]

    # Combine MIDI notes and note names into tuples
    avg_notes1_with_names = list(zip(avg_notes1, avg_notes1_names))
    avg_notes2_with_names = list(zip(avg_notes2, avg_notes2_names))

    # Calculate the difference in semitones between the two arrays for each section
    overall_semitone_difference, semitone_differences = calculate_diff(avg_notes1_with_names, avg_notes2_with_names)

    return overall_semitone_difference, semitone_differences, avg_notes1_with_names, avg_notes2_with_names


# Calculate the difference in semitones
def calculate_diff(avg_notes1, avg_notes2):
    # Extract only the MIDI note values
    avg_notes1_values = [note[0] for note in avg_notes1 if note[0] is not None]
    avg_notes2_values = [note[0] for note in avg_notes2 if note[0] is not None]

    # Calculate the difference in semitones between the two arrays for each section
    semitone_differences = []
    for note1, note2 in zip(avg_notes1_values, avg_notes2_values):
        difference = note2 - note1
        semitone_differences.append(difference)

    # Calculate the overall average difference in semitones
    overall_semitone_difference = np.mean([diff for diff in semitone_differences])

    return overall_semitone_difference, semitone_differences


def auto_transpose_avg_notes(avg_notes1_with_names, avg_notes2_with_names):
    # Extract only the MIDI note values
    avg_notes1 = [note[0] for note in avg_notes1_with_names if note[0] is not None]
    avg_notes2 = [note[0] for note in avg_notes2_with_names if note[0] is not None]

    # Calculate the average difference in MIDI notes
    avg_diff = np.mean(np.array(avg_notes2) - np.array(avg_notes1))

    # Round the average difference to the nearest integer
    semitones = int(round(avg_diff))

    return semitones


# Transpose function remains the same as before
def transpose_notes(notes_with_names, semitones):
    transposed_notes = []
    for note, name in notes_with_names:
        if note is not None:
            transposed_note = note + semitones
            if transposed_note < 0:
                transposed_note += 12
            elif transposed_note > 127:
                transposed_note -= 12
            transposed_name = note_num_to_name(int(transposed_note))
            transposed_notes.append((transposed_note, transposed_name))
        else:
            transposed_notes.append((None, name))
    return transposed_notes


# Paths to the audio files
original_file = r"C:\Users\julia\Desktop\KaraokeNet\Musikbeispiel\In_The_End_(Original)\vocals_original.mp3"
cover_file = r"C:\Users\julia\Desktop\KaraokeNet\Musikbeispiel\In_The_End_(Cover)\vocals_cover.mp3"

# Compare the average notes between the two audio files
overall_semitone_difference, semitone_differences, avg_notes_original, avg_notes_cover = compare_avg_notes(original_file, cover_file)

# Automatically determine transposition
transposition = auto_transpose_avg_notes(avg_notes_original, avg_notes_cover)

# Transpose the cover notes
transposed_cover_notes = transpose_notes(avg_notes_cover, -transposition)

# Calculate the average differences in semitones for the transposed cover notes
overall_transposed_semitone_difference, transposed_semitone_differences = calculate_diff(avg_notes_original, transposed_cover_notes)

# Display the results
print("Overall Average Difference in Semitones: \n", overall_semitone_difference)
print("Average Differences in Semitones for Each Section: \n", semitone_differences)
print("Average Notes for Original: \n", avg_notes_original)
print("Average Notes for Cover: \n", avg_notes_cover)

print("After Transposition:")
print("Transposition (in semitones): \n", transposition)
print("Transposed Cover Notes: \n", transposed_cover_notes)
print("Overall Average Difference in Semitones: \n", overall_transposed_semitone_difference)
print("Average Differences in Semitones for Each Section: \n", transposed_semitone_differences)