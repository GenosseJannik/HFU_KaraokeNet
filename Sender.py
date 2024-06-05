import socket
import pickle
from . import compareClass
from . import speech_comparison
from . import mfcc_comparison


def main():
    while(True):
        receive()

def send(compare_object: compareClass):
    url = "192.168.43.151"
    port = 1337

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((url, port))
            serialized_karaoke = pickle.dumps(compare_object)
            s.sendall(serialized_karaoke)
            print("wav File was send successfully.")
    except(socket.error, pickle.PickleError) as e:
        print(f"Error: {e}")

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
                received_karaoke.percentage_mfcc = mfcc_comparison.compare_mfcc(received_karaoke.karaoke_wav, received_karaoke.compared_song)
                recognized_lyrics = speech_comparison.transcribe(received_karaoke.karaoke_wav)
                received_karaoke.percentage_speech = speech_comparison.compare_speech(received_karaoke.compared_song, recognized_lyrics)
                send(received_karaoke)

    except (socket.error, pickle.PickleError) as e:
        raise RuntimeError(e)

if __name__ == "__main__":
    main()
