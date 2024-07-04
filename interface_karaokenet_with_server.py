import gradio as gr
from gradio import components
from song import songs
import wave
import pyaudio
import os
import shutil
import matplotlib.pyplot as plt
from speech_comparison import compare_speech, transcribe
from pitch_comparison_transposition import compare_pitch
from timing_comparison import compare_timing
import Sender
import compareClass
import socket
import pickle


# Ermittelt das Arbeitsverzeichnis
project_root = os.path.dirname(os.path.abspath(__file__))

# Ordner, in dem die Karaoke-Version des Benutzers gespeichert wird
vocals_user_dir = os.path.join(project_root, r"Vocals_User/[Karaoke] ")
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


# Erstellt eine Audioaufnahme des Benutzers während er singt und speichert diese mit dem Namen
# [Karaoke] Name_des_Liedes.wav
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

    # Datenfluss bzw. Speichern der Frames stoppen
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
        finished_recording = True  # Hiernach kann der Benutzer ein Ergebnis erhalten


def training(song_chosen):
    if song_chosen is None:  # Fehler, wenn der Benutzer kein Lied ausgewählt hat
        return {song_chosen_error: components.Textbox(visible=True)}
    song = components.Audio(value=songs[song_chosen].song_path, visible=True)
    instrumental = components.Audio(value=songs[song_chosen].instrumental_path, visible=True)
    lyrics = components.Textbox(label=song_chosen, value=songs[song_chosen].lyrics, visible=True)
    return {training_layout: gr.Column(visible=True), song_out: song, instrumental_out: instrumental,
            lyrics_out: lyrics, song_chosen_error: gr.Textbox(visible=False)}


def test_evaluation(song_chosen, cover_audio_path):
    if song_chosen is None:  # Fehler, wenn der Benutzer kein Lied ausgewählt hat
        return {song_chosen_error: components.Textbox(visible=True)}
    global finished_recording
    finished_recording = True  # Damit es bei der Funktion estimate_result zu keinem Problem kommt
    vocals_user = vocals_user_dir + song_chosen + ".wav"
    # Kopiert die vom User per Drag-and-drop hinzugefügt Karaoke-Version zu dem entsprechenden Pfad
    shutil.copyfile(cover_audio_path, vocals_user)
    return {testing_layout: gr.Column(visible=False),
            starting_layout: gr.Column(visible=False), training_layout: gr.Column(visible=False),
            get_result_btn: components.Button(visible=True), song_chosen_error: components.Textbox(visible=False)}


# Wechselt das Layout zum Layout, in dem gesungen wird
def singing(song_chosen):
    if song_chosen is None:  # Fehler, wenn der Benutzer kein Lied ausgewählt hat
        return {song_chosen_error: components.Textbox(visible=True)}
    # Initialisiert das Video mit dem zum Lied gehörigen Video
    video = components.Video(value=songs[song_chosen].video_path, visible=True)
    return {singing_layout: gr.Column(visible=True),
            starting_layout: gr.Column(visible=False), training_layout: gr.Column(visible=False),
            recording_lyrics_video_out: video, get_result_btn: components.Button(visible=True),
            song_chosen_error: components.Textbox(visible=False)}


# Wird aufgerufen, wenn der Benutzer das Video abspielt und damit eine Aufnahme startet
def start(song_chosen):
    global paused
    paused = False  # Reset auf False
    # Starten einer Aufnahme mit der Länge des Liedes und speichern dieser mit dem entsprechenden Namen
    record_audio(songs[song_chosen].length, songs[song_chosen].name)
    return {}


def pause():
    global paused
    paused = True


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def plot_results(result_dict):
    labels = list(result_dict.keys())  # In den labels sind die einzelnen Kriterien
    values = list(result_dict.values())  # Die entsprechenden Werte zu den einzelnen Kriterien

    fig, ax = plt.subplots(figsize=(13, 3), dpi=300)

    bars_color_hex = rgb_to_hex((37, 150, 190))
    ax.barh(labels, values, color=bars_color_hex)  # Ergebnis-Balken mit hellblauer Farbe
    ax.set_xlim(0, 100)  # Werte zwischen 0 und 100, die einzelnen Prozentzahlen als Ergebnis
    ax.set_xticks([0, 50, 100])  # Nur bei dem Wert 0, 50 und 100 werden die labels angezeigt

    background_color_hex = rgb_to_hex((34, 41, 54))  # Dunkleres blau als Hintergrund
    ax.set_xticklabels(["Ausbaufähig", "Befriedigend", "Sehr gut"])
    ax.set_facecolor(background_color_hex)
    fig.patch.set_facecolor(background_color_hex)
    ax.tick_params(axis='x', colors="white")  # Alle Umrandungen in weißer Farbe
    ax.tick_params(axis='y', colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    return fig


def estimate_result(song_chosen):
    global finished_recording
    if not finished_recording:  # Bei ungültiger Version erhält der Nutzer kein Ergebnis
        return {cancel_error: components.Textbox(visible=True)}
    user_vocal_path = vocals_user_dir + song_chosen + ".wav"  # Pfad zur gerade erstellten Aufnahme des Benutzers
    # save wav file as object to transfer to server
    # karaoke_wav = wave.open(karaoke_vocals)
    # song_wav = wave.open(songs[song_chosen].song_path)
    # comparisonObject = compareClass.compareClass(karaoke_wav, song_wav)
    # Sender.send(comparisonObject)
    # karaoke_wav.close()
    # song_wav.close()
    # Compare the current notes between the two audio files
    # Erstellt den KI-generierten Text der Aufnahme des Benutzers
    overall_transposed_semitone_difference, transposition, result_singing_percentage = (
        compare_pitch(songs[song_chosen].vocal_path, user_vocal_path))
    recognized_lyrics = transcribe(user_vocal_path)
    result_speech_percentage = compare_speech(songs[song_chosen], recognized_lyrics)
    result_timing_percentage = compare_timing(songs[song_chosen].vocal_path, user_vocal_path)
    # Dictionary, in dem die Kriterien die keys und die dazugehörigen Ergebnisse die values sind
    result_dict = {"Aussprache": result_speech_percentage, "Timing": result_timing_percentage,
                   "Gesang": result_singing_percentage}

    fig = plot_results(result_dict)  # Erstellt das Balkendiagramm

    # Textbox, in der die KI-generierten Lyrics des Benutzers angezeigt werden
    result_recognized_lyrics = gr.Textbox(value=recognized_lyrics, visible=True)

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
            result_plot_out: components.Plot(value=fig, visible=True),
            result_recognized_lyrics_out: result_recognized_lyrics,
            result_singing_detailed_out: result_transposition,
            restart_btn: components.Button(visible=True),
            cancel_error: components.Textbox(visible=False)
            }


def restart():
    global finished_recording
    global paused
    global aborted_recording

    finished_recording = False
    paused = False
    aborted_recording = False

    return {result_layout: gr.Column(visible=False),
            starting_layout: gr.Column(visible=True),
            song_chosen_inp: components.Dropdown(value=None, label="Wähle ein Lied aus", visible=True),
            recording_lyrics_video_out: components.Video(value=None)
            }


with gr.Blocks() as demo:
    # Titel des Projekts mit Untertitel
    gr.Markdown(
        """
        # KaraokeNet
        Bringe deine Karaoke Skills auf ein neues Level.
        """)

    # Fehleranzeige, falls kein Lied ausgewählt ist
    song_chosen_error = components.Textbox(label="Error", value="Du musst zuerst ein Lied auswählen", visible=False)

    # starting_layout dient als Container für die Startoptionen
    with gr.Column() as starting_layout:
        # Dropdown-Menü zur Auswahl des Songs. Nachdem der Benutzer seien Wahl getroffen hat,
        # wird in song_chosen_inp der Name des ausgewählten Liedes gespeichert.
        with gr.Row():
            song_chosen_inp = components.Dropdown(song_names, label="Wähle ein Lied aus")
            with gr.Column():
                # Button zum Üben des ausgewählten Songs
                train_song_btn = components.Button("Training")
                # Button zum Starten der Aufnahme
                ready_to_begin_btn = components.Button("Aufnahme starten")
                # Button, um eine bereits vorhandene Cover-Version einzufügen

    with gr.Column(visible=False) as testing_layout:
        test_evaluation_btn = components.Button("Testing")
        cover_audio = components.Audio(label="Legen sie das Cover per Drag and Drop ab.", sources=["upload", "microphone"],
                                       type="filepath")

    # Container für die Testoptionen
    with gr.Column() as training_layout:
        # Audio-Ausgabe für den Song
        song_out = components.Audio(label="Song", visible=False, show_download_button=False)
        # Audio-Ausgabe für die Instrumentalversion
        instrumental_out = components.Audio(label="Instrumentalversion (KI-generiert)", visible=False,
                                            show_download_button=False)
        # Textbox für die Anzeige der Lyrics
        lyrics_out = components.Textbox(visible=False)

    # Container für die Aufnahmeoptionen
    with gr.Column() as singing_layout:
        # Video-Komponente für die Aufnahmeanimation
        recording_lyrics_video_out = components.Video(visible=False, interactive=False, show_download_button=False)
        # Fehleranzeige, falls nicht zum gesamten Lied gesungen wird
        cancel_error = components.Textbox(label="Error", value="Du musst zum gesamten Lied singen.", visible=False)
        # Button zur Ergebnisauswertung
        get_result_btn = components.Button(value="Ergebnis auswerten", visible=False)

    # Container für die Ergebnisanzeige
    with gr.Column() as result_layout:
        # Balkendiagramm zur Bewertung der Karaoke-Version des Benutzers
        result_plot_out = components.Plot(label="Bewertung", visible=False)
        # Textbox für die detaillierte Analyse des Gesangs
        result_singing_detailed_out = components.Textbox(label="Detaillierte Analyse des Gesangs", visible=False)
        result_recognized_lyrics_out = components.Textbox(label="KI-generierte Lyrics deiner Aufnahme", visible=False)
        restart_btn = components.Button(value="Startmenü", visible=False)

    # Bei Klick auf den "Lerne und übe das Lied"-Button wird die train_song-Funktion mit den angegebenen inputs
    # als Eingabewerten aufgerufen. Die Rückgabewerte der Funktion werden den outputs zugewiesen.
    train_song_btn.click(fn=training, inputs=[song_chosen_inp], outputs=[training_layout, song_out, instrumental_out,
                                                                         lyrics_out, song_chosen_error])
    # Bei Klick auf den "Klicke hier zum Starten"-Button wird die Aufnahme gestartet
    ready_to_begin_btn.click(fn=singing, inputs=[song_chosen_inp],
                             outputs=[singing_layout, starting_layout, training_layout, recording_lyrics_video_out,
                                      get_result_btn, song_chosen_error])
    # Durch Klick des Buttons wird die vom Benutzer abgelegte Audio zur Bewertung verarbeitet
    test_evaluation_btn.click(fn=test_evaluation, inputs=[song_chosen_inp, cover_audio],
                              outputs=[testing_layout, starting_layout, training_layout, get_result_btn,
                                       song_chosen_error])

    # Startet die Aufnahme, wenn das Musikvideo abgespielt wird
    recording_lyrics_video_out.play(fn=start, inputs=[song_chosen_inp], outputs=[])
    # Pausiert die Aufnahme, wenn das Musikvideo pausiert wird
    recording_lyrics_video_out.pause(fn=pause, inputs=[], outputs=[])
    # Bei Klick auf den "Ergebnis auswerten"-Button wird die estimate_result-Funktion aufgerufen
    get_result_btn.click(fn=estimate_result, inputs=[song_chosen_inp],
                         outputs=[result_layout, singing_layout, result_plot_out, result_recognized_lyrics_out,
                                  result_singing_detailed_out, restart_btn, cancel_error])
    # Bei Klick auf den "Startmenü"-Button wird das Layout zurückgesetzt
    restart_btn.click(fn=restart, inputs=[], outputs=[result_layout, starting_layout, song_chosen_inp,
                                                      recording_lyrics_video_out])

if __name__ == "__main__":
    demo.launch()

