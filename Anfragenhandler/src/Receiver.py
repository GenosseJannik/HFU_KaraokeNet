import socket
import pickle
import wave

def main():
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

if __name__ == "__main__":
    main()