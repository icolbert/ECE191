from picamera import PiCamera
import socket
from time import sleep

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('ip', X_insert_port_X))

connetion = client_socket.makefile('wb')

try:
    with PiCamera() as camera:
        camera.resolution = (1920, 1080)
        print("Displaying camera feed...")
        camera.rotation = 0
        camera.framerate = 30
        camera.brightness = 50
        camera.start_preview()
        sleep(2)
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()

finally:
    connection.close()
    client_socket.close()
