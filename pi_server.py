# Server script in the client-server connection
# Meant to run on the miniROV RaspberryPi

import socket
import time
import picamera
import io
import threading
import traceback

class distributor():
    def __init__(self):
        self.connections = {}

    def write(self,data):
        try:
            #print('Writing: ', len(self.connections.keys()))
            for connection in self.connections:
                try:
                    connection.write(data)
                except Exception as e:
                    self.remove_client(connection)
                    try:
                        connection.close()
                    except:
                        pass
                    print('Connection closed:', e,'. Removed connection')
                    break
        except Exception as e:
            print('Error with write: ',e)
            traceback.print_exc()
    def add_client(self,client):
        self.connections[client] = 0

    def remove_client(self,client):
        try:
            del self.connections[client]
        except Exception as e:
            print('Error with remove_client: ',e)
            traceback.print_exc()

def TCP(d):
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,720)
            camera.framerate = 30
            camera.brightness = 50
            # Start a preview, let the camera warm up for 2 seconds, and then record
            camera.start_preview()
            time.sleep(2)
            camera.start_recording(d, format='h264')
            #print('Starting feed...')
            '''
            message = input('Stop feed? [y/n]: ')
            while True:
                if message == 'y':
                    break
                message = input('Stop feed? [y/n]: ')
            '''
            while True:
                time.sleep(1)
            #camera.stop_recording()

    except Exception as e:
        print('Error: ', e)

if __name__ == '__main__':
    d = distributor()
    thread = threading.Thread(target = TCP, args = (d,))
    thread.start()
    
    print('Listening for incoming connections...')
    host = '0.0.0.0'    # listening for all ip addresses
    port = 8000         # using port 8000 for the connection

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host,port))
    server_socket.listen(0) # might need to change the listen(#) number for multiple clients

    while True:
        (client, addr) = server_socket.accept()
        print("Connected to:", str(addr[0]))
        # Make a file-like object out of the connection
        connection = client.makefile('wb')
        d.add_client(connection)
        
    
