# Server script in the client-server connection
# Meant to run on the miniROV RaspberryPi

import socket
import time
import picamera
import io

class distributor():
    def __init__(self):
        self.connections = {}

    def write(self,data):
        for connection in self.connections:
            connection.write(data)

    def add_client(self,client):
        self.connections[client] = 0

    def remove_client(self,client):
        print('Closing connection to:', str(addr[0]))
        del self.connections[client]

def TCP():
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640,480)
            #camera.resolution = camera.MAX_IMAGE_RESOLUTION
            camera.framerate = 30
            camera.brightness = 50
            # Start a preview, let the camera warm up for 2 seconds, and then record
            camera.start_preview()
            time.sleep(2)
            camera.start_recording(d, format='h264')
            message = input('Stop feed? [y/n]: ')
            while True:
                if message == 'y':
                    break
                message = input('Stop feed? [y/n]: ')
            camera.stop_recording()
    finally:
        d.remove_client(connection)
        connection.close()
        server_socket.close()

if __name__ == '__main__':
    print('Listening for incoming connections...')
    host = '0.0.0.0'    # listening for all ip addresses
    port = XXXX         # using port 8000 for the connection

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(0) # might need to change the listen(#) number for multiple clients

    # will definitely need to adjust the object's accept() call for multiple clients
    (client, addr) = server_socket.accept()
    print("Connected to:", str(addr[0]))
    
    # Make a file-like object out of the connection
    connection = client.makefile('wb')

    d = distributor()
    d.add_client(connection)
    TCP()
