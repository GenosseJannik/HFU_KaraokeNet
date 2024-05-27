import java.io.IOException;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class Sender
{
    public static void main(String[] args) {

        String url = "127.0.0.1";
        url = "192.168.43.151";
        try {
            InetAddress address = InetAddress.getByName(url);
            Socket socket = new Socket(address, 1337);
            ObjectOutputStream out = new ObjectOutputStream(socket.getOutputStream());

            out.flush();
            out.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}