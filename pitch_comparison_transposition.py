import librosa
import numpy as np


# Funktion, die den Anfang des Liedes rausschneidet. Kann auch nur mit einem Parameter aufgerufen werden.
# Wenn sie mit zwei Liedern aufgerufen wird, so wird die zweite Version gleich wie die erste gekürzt.
def trim_silence(y_original, y_cover=None, threshold=0.01):
    # Berechnen der Root Mean Square (RMS)-Energie bzw. der Lautstärken
    rms = librosa.feature.rms(y=y_original)[0]

    # Finden des ersten Index, der den Schwellenwert in Lautstärke überschreitet
    frames = np.nonzero(rms > threshold)[0]

    start_sample = 0
    if len(frames) > 0:
        # Berechnen der Anzahl der abgeschnittenen Samples
        start_sample = librosa.frames_to_samples(frames[0])

    # Trim die Audiosignale ab diesem Punkt
    y_original = y_original[start_sample:]

    if y_cover is None:
        return y_original

    y_cover = y_cover[start_sample:]

    return y_original, y_cover


def extract_notes(y, sr, num_sections):
    # Calculate the duration of the audio in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    # Divide the audio into equal-length sections
    section_duration = duration / num_sections
    section_notes = []

    for i in range(num_sections):
        start_time = i * section_duration
        end_time = (i + 1) * section_duration

        # Extract the pitches for the current section
        pitches, magnitudes = librosa.piptrack(y=y[int(start_time * sr):int(end_time * sr)], sr=sr)

        # Filter out zero or negative frequencies
        pitches = pitches[pitches > 0]

        if len(pitches) == 0:
            section_notes.append(None)
            continue

        # Convert pitches to MIDI notes
        notes = librosa.hz_to_midi(pitches)

        # Take the current note of the section instead of averaging
        current_note = notes[0] if len(notes) > 0 else None
        section_notes.append(current_note)

    return section_notes


def compare_current_notes(vocals_original, vocals_user):
    # Laden und Trimmen des Audiosignals
    y_original, sr_original = librosa.load(vocals_original)
    y_cover, sr_cover = librosa.load(vocals_user)

    duration_in_seconds = librosa.get_duration(y=y_original, sr=sr_original)

    # Setzen der Anzahl der Abschnitte basierend auf der Dauer
    sections_per_second = 2  # Je größer, desto mehr Sektionen
    num_sections = int(duration_in_seconds * sections_per_second)

    trimmed_y_original, trimmed_y_cover = trim_silence(y_original, y_cover)

    # Extract current notes for the first audio file
    notes1 = extract_notes(trimmed_y_original, sr_original, num_sections=num_sections)

    # Extract current notes for the second audio file
    notes2 = extract_notes(trimmed_y_cover, sr_cover, num_sections=num_sections)

    # Convert MIDI notes to note names
    notes1_names = [note_num_to_name(note) if note is not None else "None" for note in notes1]
    notes2_names = [note_num_to_name(note) if note is not None else "None" for note in notes2]

    # Combine MIDI notes and note names into tuples
    notes1_with_names = list(zip(notes1, notes1_names))
    notes2_with_names = list(zip(notes2, notes2_names))

    # Calculate the difference in semitones between the two arrays for each section
    overall_semitone_difference, semitone_differences = calculate_diff(notes1_with_names, notes2_with_names)

    return overall_semitone_difference, semitone_differences, notes1_with_names, notes2_with_names

def note_num_to_name(note_num):
    if note_num is None:
        return "None"
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = int(note_num // 12 - 1)
    note = notes[int(note_num % 12)]
    return f"{note}{octave}"

def calculate_diff(avg_notes1, avg_notes2):
    semitone_differences = []

    for note1, note2 in zip(avg_notes1, avg_notes2):
        if note1[0] is None or note2[0] is None:
            semitone_differences.append(None)
            continue
        difference = note2[0] - note1[0]
        semitone_differences.append(difference)

    # Calculate the overall average difference in semitones, ignoring None values
    valid_differences = [diff for diff in semitone_differences if diff is not None]
    overall_semitone_difference = np.mean(valid_differences) if valid_differences else None

    return overall_semitone_difference, semitone_differences

def auto_transpose_avg_notes(avg_notes1_with_names, avg_notes2_with_names):
    avg_notes1 = [note[0] for note in avg_notes1_with_names if note[0] is not None]
    avg_notes2 = [note[0] for note in avg_notes2_with_names if note[0] is not None]

    if not avg_notes1 or not avg_notes2:
        return 0

    avg_diff = np.mean(np.array(avg_notes2) - np.array(avg_notes1))
    semitones = int(round(avg_diff))

    return semitones

def transpose_notes(notes_with_names, semitones):
    transposed_notes = []
    for note, name in notes_with_names:
        if note is not None:
            transposed_note = note + semitones
            transposed_name = note_num_to_name(transposed_note)
            transposed_notes.append((transposed_note, transposed_name))
        else:
            transposed_notes.append((None, name))
    return transposed_notes

def calculate_grade(overall_transposed_semitone_difference):
    if overall_transposed_semitone_difference is None:
        return 0.0

    max_difference = 6  # Maximum difference assumed
    percentage = (1 - abs(overall_transposed_semitone_difference) / max_difference) * 100

    return max(percentage, 0.0)


def compare_pitch(original_vocal_path, user_vocals_path):
    overall_semitone_difference, semitone_differences, notes_original, notes_cover = compare_current_notes(
        original_vocal_path, user_vocals_path)

    # Automatically determine transposition
    transposition = auto_transpose_avg_notes(notes_original, notes_cover)

    # Transpose the cover notes
    transposed_cover_notes = transpose_notes(notes_cover, -transposition)

    # Calculate the average differences in semitones for the transposed cover notes
    overall_transposed_semitone_difference, transposed_semitone_differences = calculate_diff(notes_original,
                                                                                             transposed_cover_notes)

    # Calculate the percentage score based on the transposed average difference in semitones
    result_singing_percentage = calculate_grade(overall_semitone_difference)

    return overall_transposed_semitone_difference, transposition, result_singing_percentage
