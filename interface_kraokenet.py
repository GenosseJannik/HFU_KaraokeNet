import gradio as gr
from gradio import components
from song import songs
import threading
import wave
import pygame
import pyaudio
import time

# Pfad, in dem die Karaoke-Version des Benutzers gespeichert wird
vocals_user_path = r"C:/Users/20edu/Softwareprojekt/pythonProject1/vocals_user.wav"
song_names = list(songs.keys())  # Liste, in der die Namen aller Lieder sind


# Globale Variablen, die wichtig sind, wenn das Video abgebrochen wird (ungültige Karaoke-Version)
paused = False
aborted_recording = False


def record_audio(length_in_seconds, output_file_name, frames_per_buffer=1024, format=pyaudio.paInt16, channels=1,
                 rate=44100):
    global paused
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    frames_per_buffer=frames_per_buffer,
                    channels=channels,
                    rate=rate,
                    input=True)
    frames = []

    global aborted_recording
    aborted_recording = False  # reset auf False (wenn Aufnahme mehrmals neu gestartet wird)

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
        obj = wave.open(output_file_name, "wb")  # wb = write binary
        obj.setnchannels(channels)
        obj.setsampwidth(p.get_sample_size(format))
        obj.setframerate(rate)
        obj.writeframes(b''.join(frames))
        obj.close()


def play_audio(audio_file_path):
    global paused
    pygame.init()

    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

    # pausiere die Instrumental-Version, wenn der Benutzer das Video pausiert
    while pygame.mixer.music.get_busy() and not paused:
        time.sleep(0.1)  # Pause, um die CPU-Belastung zu reduzieren

    pygame.mixer.music.stop()


def get_instrumental_get_lyrics(song_chosen):
    if song_chosen is None:
        return {error_txt: gr.Textbox.update(visible=True)}
    instrumental_audio = gr.Audio().update(value=songs[song_chosen].instrumental_path, visible=True)
    lyrics = components.Textbox().update(label=song_chosen, value=songs[song_chosen].lyrics, visible=True)
    return {instrumental_out: instrumental_audio, lyrics_out: lyrics, error_txt: gr.Textbox.update(visible=False)}


def change_layout(song_chosen):
    if song_chosen is None:
        return {error_txt: gr.Textbox.update(visible=True)}
    return {starting_layout: gr.Row.update(visible=False), testing_layout: gr.Column.update(visible=False),
            recording_animation_video: gr.PlayableVideo.update(value=songs[song_chosen].animation, visible=True),
            get_result_btn: gr.Button.update(visible=True), error_txt: gr.Textbox.update(visible=False)}


def start(song_chosen):
    global paused

    paused = False  # reset auf False
    # Erstellen von Threads, damit gleichzeitig die Karaoke- aufgenommen und die Instrumental-Version abgespielt werden
    record_thread = threading.Thread(target=record_audio, args=(songs[song_chosen].length, (song_chosen + ".wav")))
    play_thread = threading.Thread(target=play_audio, args=(songs[song_chosen].instrumental_path,))

    record_thread.start()
    play_thread.start()

    record_thread.join()  # warte in der Funktion bis die beiden Threads fertig sind
    play_thread.join()

    return {}


def pause():
    global paused
    paused = True


def estimate_result(song_name):
    result = compare_mfcc(vocals_user_path, songs[song_name].song_path)  # Hier wird die Vergleichsfunktion aufgerufen
    return {recording_animation_video: gr.PlayableVideo.update(visible=False),
            get_result_btn: gr.Button.update(visible=False), result_out: gr.Textbox.update(value=result, visible=True)}


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
        with gr.Row():
            instrumental_out = gr.Audio(label="Instrumentalversion", visible=False)
        with gr.Row():
            lyrics_out = components.Textbox(visible=False)

    with gr.Column() as singing_layout:
        recording_animation_video = gr.PlayableVideo(visible=False, interactive=True)
        get_result_btn = gr.Button(value="Klicke mich um das Ergebnis auszuwerten", visible=False)
    
    with gr.Column() as result_layout:
        result_out = components.Textbox(label="Ergebnis", visible=False)

    train_song_btn.click(fn=get_instrumental_get_lyrics, inputs=[song_chosen_inp], outputs=[instrumental_out,
                                                                                            lyrics_out, error_txt])
    ready_to_begin_btn.click(fn=change_layout, inputs=[song_chosen_inp], outputs=[starting_layout, testing_layout,
                                                                                  recording_animation_video,
                                                                                  get_result_btn, error_txt])

    recording_animation_video.play(fn=start, inputs=[song_chosen_inp], outputs=[])
    recording_animation_video.pause(fn=pause, inputs=[], outputs=[])

    get_result_btn.click(fn=estimate_result, inputs=[song_chosen_inp], outputs=[recording_animation_video,
                                                                                get_result_btn, result_out])

if __name__ == "__main__":
    demo.launch()
