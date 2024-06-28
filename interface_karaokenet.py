import gradio as gr
from gradio import components
from song import songs
import wave
import pyaudio
from . import mfcc_comparison
from . import speech_comparison
from mfcc_comparison import compare_mfcc
from speech_comparison import compare_speech
import pandas as pd
from speech_comparison import transcribe
from pitch_comparison_transposition import compare_avg_notes
import Sender
import compareClass
import socket
import pickle




# Ordner, in dem die Karaoke-Version des Benutzers gespeichert wird
vocals_user_dir = r"C:/Users/20edu/Softwareprojekt/pythonProject1/vocals_user/[Karaoke] "
song_names = list(songs.keys())  # Liste, in der die Namen aller Lieder sind

# Globale Variablen, die wichtig sind, wenn das Video abgebrochen wird (ungültige Karaoke-Version)
paused = False
aborted_recording = False
finished_recording = False

def receive(): 
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", 1337))
        server_socket.listen(1)
        print("Waiting for connection...")

        while True: 
            client_socket, _ = server_socket.accept()
            with client_socket:
                in_data = client_socket.recv(1024)
                received_karaoke = pickle.loads(in_data)
    except (socket.error, pickle.PickleError) as e:
        raise RuntimeError(e)


def record_audio(length_in_seconds, output_file_name, frames_per_buffer=1024, format=pyaudio.paInt16, channels=1,
                 rate=44100):
    global paused
    paused = False
    global finished_recording
    finished_recording = False
    global aborted_recording
    aborted_recording = False  # reset auf False (wenn Aufnahme mehrmals neu gestartet wird)

    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    frames_per_buffer=frames_per_buffer,
                    channels=channels,
                    rate=rate,
                    input=True)
    frames = []

    for i in range(0, int(rate / frames_per_buffer * length_in_seconds)):
        data = stream.read(frames_per_buffer)  # 1024 frames werden in einer Iteration gelesen
        frames.append(data)
        if paused:  # Aufnahme abbrechen, wenn der Benutzer das Video pausiert hat
            aborted_recording = True
            break

    # Datenfluss bzw. Aufnahme stoppen
    stream.stop_stream()
    stream.close()
    p.terminate()

    if not aborted_recording:  # Aufnahme nur dann speichern, wenn die Karaoke-Version vollständig ist
        output_file_path = vocals_user_dir + output_file_name + ".wav"
        obj = wave.open(output_file_path, "wb")  # wb = write binary
        obj.setnchannels(channels)
        obj.setsampwidth(p.get_sample_size(format))
        obj.setframerate(rate)
        obj.writeframes(b''.join(frames))
        obj.close()
        finished_recording = True


def train_song(song_chosen):
    if song_chosen is None:
        return {error_txt: components.Textbox(visible=True)}
    song_audio = gr.Audio(value=songs[song_chosen].song_path, visible=True)
    instrumental_audio = gr.Audio(value=songs[song_chosen].instrumental_path, visible=True)
    lyrics = components.Textbox(label=song_chosen, value=songs[song_chosen].lyrics, visible=True)
    return {testing_layout: gr.Column(visible=True), song_out: song_audio, instrumental_out: instrumental_audio,
            lyrics_out: lyrics, error_txt: gr.Textbox(visible=False)}


def change_layout(song_chosen):
    if song_chosen is None:
        return {error_txt: components.Textbox(visible=True)}
    animation_video = components.Video(value=songs[song_chosen].animation_path, visible=True)
    return {singing_layout: gr.Column(visible=True),
            starting_layout: gr.Row.update(visible=False), testing_layout: gr.Column(visible=False),
            recording_animation_video: animation_video,
            get_result_btn: components.Button(visible=True), error_txt: components.Textbox(visible=False)}


def start(song_chosen):
    global paused
    paused = False  # reset auf False
    record_audio(songs[song_chosen].length, songs[song_chosen].name)
    return {}


def pause():
    global paused
    paused = True


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def plot_results(result_dict):
    labels = list(result_dict.keys())
    values = list(result_dict.values())

    fig, ax = plt.subplots(figsize=(13, 3), dpi=300)

    bars_color_hex = rgb_to_hex((37, 150, 190))
    ax.barh(labels, values, color=bars_color_hex)
    ax.set_xlim(0, 100)
    ax.set_xticks([0, 50, 100])  # nur bei dem Wert 0, 50 und 100 werden die labels angezeigt

    background_color_hex = rgb_to_hex((34, 41, 54))
    ax.set_xticklabels(["Ausbaufähig", "Befriedigend", "Sehr gut"])
    ax.set_facecolor(background_color_hex)
    fig.patch.set_facecolor(background_color_hex)
    ax.tick_params(axis='x', colors="white")
    ax.tick_params(axis='y', colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    return fig


def estimate_result(song_chosen):
    global finished_recording
    if not finished_recording:
        return {error_txt2: components.Textbox(visible=True)}
    user_vocals = vocals_user_dir + song_chosen + ".wav"
    # save wav file as object to transfer to server
    # karaoke_wav = wave.open(karaoke_vocals)
    # song_wav = wave.open(songs[song_chosen].song_path)
    # comparisonObject = compareClass.compareClass(karaoke_wav, song_wav)
    # Sender.send(comparisonObject)
    # karaoke_wav.close()
    # song_wav.close()
    # Compare the current notes between the two audio files
    overall_semitone_difference, semitone_differences, notes_original, notes_cover = compare_current_notes(
        songs[song_chosen].vocal_path, user_vocals)

    # Automatically determine transposition
    transposition = auto_transpose_avg_notes(notes_original, notes_cover)

    # Transpose the cover notes
    transposed_cover_notes = transpose_notes(notes_cover, -transposition)

    # Calculate the average differences in semitones for the transposed cover notes
    overall_transposed_semitone_difference, transposed_semitone_differences = calculate_diff(notes_original,
                                                                                             transposed_cover_notes)

    # Calculate the percentage score based on the transposed average difference in semitones
    result_singing_percentage = calculate_grade(overall_semitone_difference)

    recognized_lyrics = transcribe(user_vocals)
    result_speech_percentage = compare_speech(songs[song_chosen], recognized_lyrics)
    result_rhythm_percentage = 70
    result_dict = {"Aussprache": result_speech_percentage, "Rhythmik": result_rhythm_percentage,
                   "Gesang": result_singing_percentage}
    fig = plot_results(result_dict)

    result_recognized_lyrics = components.Textbox(value=recognized_lyrics, visible=True)

    if transposition == 1:
        result_transposition = components.Textbox(
            value=f"Das Lied wurde um {transposition} Halbtonschritt transponiert.\n"
                  f"Abweichung in Halbtonschritten: {overall_transposed_semitone_difference}",
            visible=True)
    else:
        result_transposition = components.Textbox(
            value=f"Das Lied wurde um {transposition} Halbtonschritte transponiert.\n"
                  f"Abweichung in Halbtonschritten: {overall_transposed_semitone_difference}",
            visible=True)
    return {result_layout: gr.Column(visible=True),
            singing_layout: gr.Column(visible=False),
            result_plot: components.Plot(value=fig, visible=True),
            result_recognized_lyrics_out: result_recognized_lyrics,
            result_avg_semitones_out: result_transposition,
            restart_btn: components.Button(visible=True),
            error_txt2: components.Textbox(visible=False)
            }


def restart():
    global finished_recording
    global paused
    global aborted_recording

    finished_recording = False
    paused = False
    aborted_recording = False

    return {result_layout: gr.Column(visible=False),
            starting_layout: gr.Row(visible=True),
            song_chosen_inp: components.Dropdown(value=None, label="Wähle ein Lied aus", visible=True),
            recording_animation_video: components.Video(value=None)
            }


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # KaraokeNet
        Bringe deine Karaoke Skills auf ein neues Level.
        """)
    error_txt = components.Textbox(label="Error", value="Du musst zuerst ein Lied auswählen", visible=False)
    with gr.Row() as starting_layout:
        song_chosen_inp = components.Dropdown(song_names, label="Wähle ein Lied aus")
        with gr.Column():
            train_song_btn = components.Button("Lerne und übe das Lied")
            ready_to_begin_btn = components.Button("Klicke hier zum Starten")

    with gr.Column() as testing_layout:
        song_out = components.Audio(label="Song", visible=False, min_width=100, show_download_button=False)
        instrumental_out = components.Audio(label="Instrumentalversion (KI-generiert)", visible=False, min_width=100,
                                            show_download_button=False)
        lyrics_out = components.Textbox(visible=False)

    with gr.Column() as singing_layout:
        recording_animation_video = components.Video(visible=False, interactive=False, show_download_button=False)
        error_txt2 = components.Textbox(label="Error", value="Du musst zum gesamten Lied singen.", visible=False)
        get_result_btn = components.Button(value="Ergebnis auswerten", visible=False)

    with gr.Column() as result_layout:
        result_plot = components.Plot(label="Bewertung", visible=False)
        result_avg_semitones_out = components.Textbox(label="Detaillierte Analyse des Gesangs", visible=False)
        result_recognized_lyrics_out = components.Textbox(label="KI-generierte Lyrics deiner Aufnahme", visible=False)
        restart_btn = components.Button(value="Startmenü", visible=False)

    train_song_btn.click(fn=train_song, inputs=[song_chosen_inp], outputs=[testing_layout, song_out, instrumental_out,
                                                                           lyrics_out, error_txt])
    ready_to_begin_btn.click(fn=change_layout, inputs=[song_chosen_inp], outputs=[singing_layout, starting_layout,
                                                                                  testing_layout,
                                                                                  recording_animation_video,
                                                                                  get_result_btn, error_txt])

    recording_animation_video.play(fn=start, inputs=[song_chosen_inp], outputs=[])
    recording_animation_video.pause(fn=pause, inputs=[], outputs=[])

    get_result_btn.click(fn=estimate_result, inputs=[song_chosen_inp], outputs=[result_layout,
                                                                                singing_layout,
                                                                                result_plot,
                                                                                result_recognized_lyrics_out,
                                                                                result_avg_semitones_out,
                                                                                restart_btn,
                                                                                error_txt2])
    restart_btn.click(fn=restart, inputs=[], outputs=[result_layout, starting_layout, song_chosen_inp,
                                                      recording_animation_video])

if __name__ == "__main__":
    demo.launch()

