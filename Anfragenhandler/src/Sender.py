import socket
import pickle
import wave

def main():
    karaoke_file = wave.open("output.wav", "r")
    url = "192.168.43.151"
    port = 1337

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((url, port))
            serialized_karaoke = pickle.dumps(karaoke_file)
            s.sendall(serialized_karaoke)
            print("wav File was send successfully.")
    except(socket.error, pickle.PickleError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()