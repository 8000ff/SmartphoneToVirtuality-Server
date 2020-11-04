import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.DatagramPacket;

import javafx.application.Application;

public class Server {
    private ServerSocket serverSocket;
    private static final int port = 4269;
    private static int upd_count = 0;
    private boolean running = true;

    public static final int TYPE_ACCELEROMETER = 1;
    public static final int TYPE_GYROSCOPE = 4;
    public static final int TYPE_PROXIMITY = 8;

    public Server() {
      try {
        serverSocket = new ServerSocket(port);
        print_addr();
        follow_updates();
      }
      catch (IOException ioe) {
          ioe.printStackTrace();
      }
    }

    private void print_addr() {
      try(final DatagramSocket socket = new DatagramSocket()){
        socket.connect(InetAddress.getByName("8.8.8.8"), 10002);
        System.out.println(socket.getLocalAddress().getHostAddress()+":"+port);
      }
      catch (Exception e) {
        e.printStackTrace();
      }
    }

    public void startTCP() {
      try {
        while(true) {
          BufferedReader in = new BufferedReader(new InputStreamReader(serverSocket.accept().getInputStream()));
          String l = in.readLine();
          process(l);
          if(l.equals("STOP")) break;
        }
        serverSocket.close();
      }
      catch (IOException ioe) {
          ioe.printStackTrace();
      }
    }

    public void startUDP() {
      try {
        DatagramSocket socket = new DatagramSocket(port);
        byte[] buf = new byte[256];
        while (running) {
          DatagramPacket packet = new DatagramPacket(buf, buf.length);
          socket.receive(packet);
          upd_count++;
          packet = new DatagramPacket(buf, buf.length, packet.getAddress(), packet.getPort());
          String received = new String(packet.getData(), 0, packet.getLength());
          process(received.substring(0, received.indexOf('\0')));
          buf = new byte[256];
        }
        socket.close();
      }
      catch(Exception e) {
        e.printStackTrace();
      }
    }

    private void process(String s) {
      try {
        String[] splt = s.split("_");
        int type = Integer.parseInt(splt[0]);
        if(type == TYPE_PROXIMITY) GUI.setProximity(Float.parseFloat(splt[1]));
        else {
          String[] coords = splt[1].split(" ");
          float x = Float.parseFloat(coords[0]);
          float y = Float.parseFloat(coords[1]);
          float z = Float.parseFloat(coords[2]);
          if(type == TYPE_ACCELEROMETER) GUI.setAccelerometer(x, y, z);
          else if(type == TYPE_GYROSCOPE) GUI.setGyroscope(x, y, z);
        }
      }
      catch(Exception e) {
        e.printStackTrace();
      }
    }

    private void follow_updates() {
      new Thread() {
        public void run() {
          while(true) {
            try {
              Thread.sleep(1000);
              GUI.setUps(upd_count);
              upd_count = 0;
            }
            catch(Exception e) {
              e.printStackTrace();
            }
          }
        }
      }.start();
    }

    private static void startServer() {
      new Thread() {
        public void run() {
          Server server = new Server();
          server.startUDP();
        }
      }.start();
    }

    public static void main(String[] args) {
      startServer();
      Application.launch(GUI.class, args);
    }
}
