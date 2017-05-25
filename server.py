import socket
import subprocess
from time import sleep

# start socket listening for connections on 0.0.0.0:X_insert_port_X

print("Connecting to Raspberry Pi...")
sleep(5)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0',X_insert_port_X))

# accept a single connection and make a file-like object
try:
    # use mplayer
    cmd = ['mplayer', '-fps', '20', '-cache', '1024', '-']
    player = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    print("Displaying video feed...")
    sleep(5)

    while True:

        data = server_socket.recv(130000)
        if not data:
            break
        player.stdin.write(data)

finally:
    # connection.close()
    server_socket.close()
    player.terminate()
    print("Connection feed terminated and socket closed!")
