import gradio as gr
from gradio import components
from song import songs
import wave
import pyaudio
from mfcc_comparison import compare_mfcc
from speech_comparison import compare_speech
import pandas as pd
from speech_comparison import transcribe
from pitch_comparison_transposition import compare_avg_notes


# Ordner, in dem die Karaoke-Version des Benutzers gespeichert wird
vocals_user_dir = r"C:/Users/20edu/Softwareprojekt/pythonProject1/vocals_user/[Karaoke] "
song_names = list(songs.keys())  # Liste, in der die Namen aller Lieder sind

# Globale Variablen, die wichtig sind, wenn das Video abgebrochen wird (ungültige Karaoke-Version)
paused = False
aborted_recording = False
finished_recording = False


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
        return {error_txt: gr.Textbox(visible=True)}
    song_audio = components.Audio(value=songs[song_chosen].song_path, visible=True)
    instrumental_audio = gr.Audio(value=songs[song_chosen].instrumental_path, visible=True)
    lyrics = components.Textbox(label=song_chosen, value=songs[song_chosen].lyrics, visible=True)
    return {song_out: song_audio, instrumental_out: instrumental_audio, lyrics_out: lyrics,
            error_txt: gr.Textbox(visible=False)}


def change_layout(song_chosen):
    if song_chosen is None:
        return {error_txt: gr.Textbox(visible=True)}
    animation_video = components.Video(value=songs[song_chosen].animation_path, visible=True)
    return {starting_layout: gr.Row.update(visible=False), testing_layout: gr.Column(visible=False),
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


def estimate_result(song_chosen):
    global finished_recording
    if not finished_recording:
        return {error_txt: gr.Textbox(value="Du darfst nicht vorzeitig abbrechen.", visible=True)}
    karaoke_vocals = vocals_user_dir + song_chosen + ".wav"
    result_singing = compare_mfcc(karaoke_vocals, songs[song_chosen].song_path)
    recognized_lyrics = transcribe(karaoke_vocals)
    result_speech = compare_speech(songs[song_chosen], recognized_lyrics)
    result_bar_chart = pd.DataFrame(
        {
            "Kriterium": ["Gesang", "Aussprache"],
            "Schulnote": [result_singing, result_speech],
        })
    result_singing = components.Textbox(value=result_singing, visible=True)
    result_speech = components.Textbox(value=result_speech, visible=True)
    bar_chart = components.BarPlot(value=result_bar_chart, x="Kriterium", y="Schulnote", x_title="Kriterium",
                                   y_title="Schulnote", tooltip=["Kriterium", "Schulnote"], vertical=False,
                                   visible=True)
    result_recognized_lyrics = components.Textbox(value=recognized_lyrics, visible=True)
    avg_semitones_difference, b, c, d = compare_avg_notes(karaoke_vocals, songs[song_chosen].song_path)
    result_avg_semitones = components.Textbox(value=avg_semitones_difference, visible=True)
    return {singing_layout: gr.Column(visible=False),
            result_singing_out: result_singing,
            result_speech_out: result_speech,
            result_bar_chart_out: bar_chart,
            result_recognized_lyrics_out: result_recognized_lyrics,
            result_avg_semitones_out: result_avg_semitones,
            error_txt: components.Textbox(visible=False)
            }


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # KaraokeNet
        Wähle ein Lied aus und gebe dein bestes es so gut wie möglich nachzusingen.
        """)
    error_txt = gr.Textbox(label="Error", value="Du musst zuerst ein Lied auswählen", visible=False)
    with gr.Row() as starting_layout:
        song_chosen_inp = gr.Dropdown(song_names, label="Wähle ein Lied aus")
        with gr.Column():
            train_song_btn = gr.Button("Lerne und übe das Lied")
            ready_to_begin_btn = gr.Button("Klicke hier zum Starten")

    with gr.Column() as testing_layout:
        song_out = gr.Audio(label="Song", visible=False)
        instrumental_out = gr.Audio(label="Instrumentalversion", visible=False)
        lyrics_out = components.Textbox(visible=False)

    with gr.Column() as singing_layout:
        recording_animation_video = gr.PlayableVideo(visible=False, interactive=False)
        get_result_btn = gr.Button(value="Klicke mich um das Ergebnis auszuwerten", visible=False)

    with gr.Row() as result_layout:
        with gr.Column():
            result_singing_out = components.Textbox(label="Gesang", visible=False)
            result_speech_out = components.Textbox(label="Aussprache", visible=False)
        result_bar_chart_out = components.BarPlot(label="Bewertung", visible=False)
    result_recognized_lyrics_out = components.Textbox(label="KI-generierte Lyrics deiner Aufnahme", visible=False)
    result_avg_semitones_out = components.Textbox(label="Durchschnittler Unterschied in Seminoten", visible=False)

    train_song_btn.click(fn=train_song, inputs=[song_chosen_inp], outputs=[song_out, instrumental_out, lyrics_out,
                                                                           error_txt])
    ready_to_begin_btn.click(fn=change_layout, inputs=[song_chosen_inp], outputs=[starting_layout, testing_layout,
                                                                                  recording_animation_video,
                                                                                  get_result_btn, error_txt])

    recording_animation_video.play(fn=start, inputs=[song_chosen_inp], outputs=[])
    recording_animation_video.pause(fn=pause, inputs=[], outputs=[])

    get_result_btn.click(fn=estimate_result, inputs=[song_chosen_inp], outputs=[singing_layout,
                                                                                result_singing_out,
                                                                                result_speech_out, result_bar_chart_out,
                                                                                result_recognized_lyrics_out,
                                                                                result_avg_semitones_out,
                                                                                error_txt])

if __name__ == "__main__":
    demo.launch()
