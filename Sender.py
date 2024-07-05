import socket
import pickle
import compareClass
import speech_comparison
import pitch_comparison

#This file handles the communication with the Client


def main():
    while(True):
        receive()

def send(compare_object: compareClass):
    #ip of Client
    url = "141.28.73.17"
    port = 1337

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((url, port))  #connect to the server Socket of Client
            serialized_karaoke = pickle.dumps(compare_object)   #dump information of compare_object into a sendable object
            s.sendall(serialized_karaoke)   #sends all the information to the serverSocket
            print("wav File was send successfully.")
    except(socket.error, pickle.PickleError) as e:
        print(f"Error: {e}")

def receive():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", 1337)) #bind Socket to localHost
        server_socket.listen(1) #Listen at localHost if anything tries to connect
        print("Waiting for connection...")

        while True: 
            client_socket, _ = server_socket.accept()   #accept any incoming connections
            with client_socket:
                in_data = client_socket.recv(1024)  #get data from pickled object
                received_karaoke = pickle.loads(in_data)    #extract all information of pickle object back into compare_object
                received_karaoke.overall_transposed_semitone_difference, received_karaoke.transposition, received_karaoke.result_singing_percentage = (pitch_comparison.compare_pitch
                            (received_karaoke.compared_song, received_karaoke.karaoke_wav))
                recognized_lyrics = speech_comparison.transcribe(received_karaoke.karaoke_wav)
                received_karaoke.percentage_speech = speech_comparison.compare_speech(received_karaoke.compared_song, recognized_lyrics)
                send(received_karaoke)

    except (socket.error, pickle.PickleError) as e:
        raise RuntimeError(e)

if __name__ == "__main__":
    main()
