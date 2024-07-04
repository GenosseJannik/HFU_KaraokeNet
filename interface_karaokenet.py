import gradio as gr
from gradio import components
from song import songs
import wave
import pyaudio
import os
import matplotlib.pyplot as plt
from speech_comparison import compare_speech, transcribe
from pitch_comparison_transposition import compare_pitch
from timing_comparison import compare_timing
from scripts import js, css


# Ermittelt das Arbeitsverzeichnis
project_root = os.path.dirname(os.path.abspath(__file__))

#
images = os.path.join(project_root, 'Icons/')

# Ordner, in dem die Karaoke-Version des Benutzers gespeichert wird
vocals_user_dir = os.path.join(project_root, r"Vocals_User/[Karaoke] ")
song_names = list(songs.keys())  # Liste, in der die Namen aller Lieder sind

# Globale Variablen, die wichtig sind, wenn das Video abgebrochen wird (ungültige Karaoke-Version)
paused = False
aborted_recording = False
finished_recording = False
uploaded_cover = False


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


def upload(song_chosen):
    if song_chosen is None:  # Fehler, wenn der Benutzer kein Lied ausgewählt hat
        return {song_chosen_error: components.Textbox(visible=True)}
    global uploaded_cover
    uploaded_cover = True  # Kennzeichnung, dass die Datei hochgeladen und nicht gesungen wurde
    txt_to_display = f"Insert your cover of {song_chosen} as an .wav-file in the box below."
    explanation_out = components.Markdown(label="", value=txt_to_display, visible=True)
    return {upload_layout: gr.Column(visible=True),
            starting_layout: gr.Row(visible=False), training_layout: gr.Column(visible=False),
            explanation_md: explanation_out,
            song_chosen_error: components.Textbox(visible=False),
            }


# Wechselt das Layout zum Layout, in dem gesungen wird
def singing(song_chosen):
    if song_chosen is None:  # Fehler, wenn der Benutzer kein Lied ausgewählt hat
        return {song_chosen_error: components.Textbox(visible=True)}
    # Initialisiert das Video mit dem zum Lied gehörigen Video
    video = components.Video(value=songs[song_chosen].video_path, visible=True)
    return {singing_layout: gr.Column(visible=True),
            starting_layout: gr.Row(visible=False), training_layout: gr.Column(visible=False),
            recording_video_out: video, get_result_recording_btn: components.Button(visible=True),
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
    ax.set_xticklabels(["Poor", "Average", "Good"])
    ax.set_facecolor(background_color_hex)
    fig.patch.set_facecolor(background_color_hex)
    ax.tick_params(axis='x', colors="white")  # Alle Umrandungen in weißer Farbe
    ax.tick_params(axis='y', colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("white")

    return fig


def estimate_result(song_chosen, uploaded_cover_path):
    global finished_recording
    if finished_recording:  # Falls der Nutzer das Lied vollständig gesungen hat
        print("finished")
        user_vocal_path = vocals_user_dir + song_chosen + ".wav"  # Pfad zur gerade erstellten Aufnahme des Benutzers
    elif not uploaded_cover:  # Aufnahme nicht vollständig, aber angefangen
        print("not uploaded")
        return {cancel_error: components.Textbox(visible=True)}
    elif uploaded_cover_path is None:  # Es wurde auf "Evaluate result" gedrückt ohne eine Datei hochzuladen
        return {upload_error: components.Textbox(visible=True)}
    else:  # Es wurde eine Datei hochgeladen
        user_vocal_path = uploaded_cover_path  # Pfad zur hochgeladenen Karaoke-Version

    # Bewertung des Gesangs
    overall_transposed_semitone_difference, transposition, result_singing_percentage = (
        compare_pitch(songs[song_chosen].vocal_path, user_vocal_path))

    # Bewertung des Timings
    result_timing_percentage = compare_timing(songs[song_chosen].vocal_path, user_vocal_path)

    # Bewertung der Aussprache
    recognized_lyrics = transcribe(user_vocal_path)
    result_speech_percentage = compare_speech(songs[song_chosen], recognized_lyrics)

    # Dictionary, in dem die Kriterien die keys und die dazugehörigen Ergebnisse die values sind
    result_criteria_dict = {"Speech": result_speech_percentage, "Timing": result_timing_percentage,
                            "Singing": result_singing_percentage}

    fig = plot_results(result_criteria_dict)  # Erstellt das Balkendiagramm

    # Textbox, in der die KI-generierten Lyrics des Benutzers angezeigt werden
    result_recognized_lyrics = gr.Textbox(value=recognized_lyrics, visible=True)

    result_transposition = components.Textbox(
        value=f"The song was transposed by {transposition} semitone{'s' if transposition != 1 else ''}.\n"
              f"Deviation in semitones: {overall_transposed_semitone_difference}",
        visible=True
    )

    result_criteria_dict = {
        result_layout: gr.Column(visible=True),
        result_plot_out: components.Plot(value=fig, visible=True),
        result_recognized_lyrics_out: result_recognized_lyrics,
        result_singing_detailed_out: result_transposition,
        restart_btn: components.Button(visible=True),
    }

    # Je nach upload oder singen müssen die Outputs angepasst werden
    if uploaded_cover_path is None:
        result_criteria_dict[singing_layout] = gr.Column(visible=False)
        result_criteria_dict[cancel_error] = components.Textbox(visible=False)
    else:
        result_criteria_dict[upload_layout] = gr.Column(visible=False)
        result_criteria_dict[upload_error] = components.Textbox(visible=False)

    return result_criteria_dict


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
            recording_video_out: components.Video(value=None),
            cover_upload_audio: components.Audio(value=None)
            }


with gr.Blocks(js=js, css=css) as demo:
    # Fehleranzeige, falls kein Lied ausgewählt ist
    song_chosen_error = components.Textbox(label="Error", value="You must first select a song", visible=False)

    # starting_layout dient als Container für die Startoptionen
    with gr.Row(elem_classes="gr-row") as starting_layout:
        # Dropdown-Menü zur Auswahl des Songs. Nachdem der Benutzer seine Wahl getroffen hat,
        # wird in song_chosen_inp der Name des ausgewählten Liedes gespeichert.
        song_chosen_inp = gr.Dropdown(song_names, label="Select a song", elem_classes="gr-dropdown")

        with gr.Column(elem_classes="gr-column"):
            # Button zum Üben des ausgewählten Songs
            training_icon = images + "practice.png"
            with gr.Row(elem_classes="gr-button-container"):
                train_song_btn = components.Button("", icon=training_icon, elem_classes="gr-button")
                components.Markdown("**Practice the song**", elem_classes="gr-button-tooltip gr-button-tooltip-right")
                components.Markdown("**Practice the song**", elem_classes="gr-button-tooltip")

            # Button zum Starten der Aufnahme
            microphone_icon = images + "mikro_icon.png"
            with gr.Row(elem_classes="gr-button-container"):
                singing_btn = components.Button("", icon=microphone_icon, elem_classes="gr-button")
                components.Markdown("**Start recording**", elem_classes="gr-button-tooltip gr-button-tooltip-right")
                components.Markdown("**Start recording**", elem_classes="gr-button-tooltip")

            # Button, um eine bereits vorhandene Cover-Version einzufügen
            upload_icon = images + "upload_icon.png"
            with gr.Row(elem_classes="gr-button-container"):
                upload_cover_btn = components.Button("", icon=upload_icon, elem_classes="gr-button")
                components.Markdown("**Upload a Cover**", elem_classes="gr-button-tooltip gr-button-tooltip-right")
                components.Markdown("**Upload a Cover**", elem_classes="gr-button-tooltip")

    with gr.Column(visible=False) as upload_layout:
        explanation_md = components.Markdown()
        cover_upload_audio = components.Audio(sources=["upload"], type="filepath", show_label=False)
        upload_error = components.Textbox(label="Error", value="You must first upload the cover.", visible=False)
        get_result_upload_btn = components.Button(value="Evaluate result")

    # Container für die Testoptionen
    with gr.Column() as training_layout:
        with gr.Row(elem_classes="gr-audio-container"):
            # Audio-Ausgabe für den Song
            song_out = components.Audio(label="Song", visible=False, show_download_button=False,
                                        elem_classes="gr-audio")
        with gr.Row(elem_classes="gr-audio-container"):
            # Audio-Ausgabe für die Instrumentalversion
            instrumental_out = components.Audio(label="Instrumental (AI-generated)", visible=False,
                                                show_download_button=False, elem_classes="gr-audio")
        # Textbox für die Anzeige der Lyrics
        lyrics_out = components.Textbox(visible=False)

    # Container für die Aufnahmeoptionen
    with gr.Column() as singing_layout:
        # Video-Komponente für die Aufnahmeanimation
        recording_video_out = components.Video(visible=False, interactive=False, show_download_button=False,
                                               show_label=False)
        # Fehleranzeige, falls nicht zum gesamten Lied gesungen wird
        cancel_error = components.Textbox(label="Error", value="You must sing the entire song", visible=False)
        # Button zur Ergebnisauswertung
        get_result_recording_btn = components.Button(value="Evaluate result", visible=False)

    # Container für die Ergebnisanzeige
    with gr.Column() as result_layout:
        # Balkendiagramm zur Bewertung der Karaoke-Version des Benutzers
        result_plot_out = components.Plot(show_label=False, visible=False)
        # Textbox für die detaillierte Analyse des Gesangs
        result_singing_detailed_out = components.Textbox(label="Detailed analysis of the singing", visible=False)
        result_recognized_lyrics_out = components.Textbox(label="AI-generated lyrics of your recording", visible=False)
        restart_btn = components.Button(value="Start menu", visible=False)

    # Bei Klick auf den "Train Song"-Button wird die train_song-Funktion mit den angegebenen inputs
    # als Eingabewerten aufgerufen. Die Rückgabewerte der Funktion werden den outputs zugewiesen.
    train_song_btn.click(fn=training, inputs=[song_chosen_inp], outputs=[training_layout, song_out, instrumental_out,
                                                                         lyrics_out, song_chosen_error])
    # Bei Klick auf den start_singing_btn Button wird die Aufnahme gestartet
    singing_btn.click(fn=singing, inputs=[song_chosen_inp],
                      outputs=[singing_layout, starting_layout, training_layout, recording_video_out,
                               get_result_recording_btn, song_chosen_error])
    # Durch Klick des Buttons wird die vom Benutzer abgelegte Audio zur Bewertung verarbeitet
    upload_cover_btn.click(fn=upload, inputs=[song_chosen_inp],
                           outputs=[upload_layout, starting_layout, training_layout, explanation_md,
                                    song_chosen_error])

    # Startet die Aufnahme, wenn das Musikvideo abgespielt wird
    recording_video_out.play(fn=start, inputs=[song_chosen_inp], outputs=[])
    # Pausiert die Aufnahme, wenn das Musikvideo pausiert wird
    recording_video_out.pause(fn=pause, inputs=[], outputs=[])
    # Bei Klick auf den "Evaluate result"-Button wird die estimate_result-Funktion aufgerufen
    get_result_recording_btn.click(fn=estimate_result, inputs=[song_chosen_inp],
                                   outputs=[result_layout, singing_layout, result_plot_out, result_recognized_lyrics_out,
                                            result_singing_detailed_out, restart_btn, cancel_error])
    get_result_upload_btn.click(fn=estimate_result, inputs=[song_chosen_inp, cover_upload_audio],
                                outputs=[result_layout, upload_layout, result_plot_out, result_recognized_lyrics_out,
                                result_singing_detailed_out, restart_btn, upload_error])
    # Bei Klick auf den "Start menu"-Button wird das Layout zurückgesetzt
    restart_btn.click(fn=restart, inputs=[], outputs=[result_layout, starting_layout, song_chosen_inp,
                                                      recording_video_out, cover_upload_audio])

if __name__ == "__main__":
    demo.launch()
