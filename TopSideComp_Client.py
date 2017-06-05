# Client script in the client-server connection
# Meant to be on top-side RaspberryPi/"Remote" laptop
'''
ffmpeg -i test.h264 -c:v copy test.mp4
scp pi_server.py pi@169.254.170.31:~
'''
import socket
import subprocess
import time
import os

# host = '169.254.170.31' # ip address of the Raspberry Pi through eth0
host = '192.168.0.48'   # ip address of the Raspberry Pi through the wlan0
port = XXXX             # using port 8000 for the connection
cwd = os.getcwd()       # gets current working directory to save videos into file

# Use the os package to time-stamp the videos stored
date_stamp = time.strftime('%y-%d-%m')
time_stamp = time.strftime('%I-%M')
directory = os.path.join(cwd,date_stamp)
video_h264 = os.path.join(directory,time_stamp+'.h264')

# Uses TCP protocol to recieve live stream from the pi
def TCP():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host,port))

    video_file = open(video_h264,'wb')
    connection = client_socket.makefile('rb')
    try:
        # Run mplayer with the following command line
        frame_rate = ['-fps','30']
        cache = ['-cache','1024']
        #cmdline = ['mplayer', '-fps', '30', '-cache', '1024','-']
        cmdline = ['mplayer']+frame_rate+cache+['-']
        player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
        while True:
            # reads 1k of data and writes it into mplayer's stdin
            data = connection.read(1024)
            if not data:
                break
            video_file.write(data)
            player.stdin.write(data)
            
    finally:
        connection.close()
        client_socket.close()
        player.terminate()
        video_file.close()

def convert(video):
    try: 
        video_mp4 = os.path.join(directory,time_stamp+'.mp4')
        cmdline = ['ffmpeg', '-i', video_h264, '-c:v', 'copy', video_mp4]
        convert = subprocess.call(cmdline)
    finally:
        os.remove(video)

if __name__ == '__main__':
    print('Connecting to Raspberry Pi...')
    if not os.path.exists(directory):
        os.makedirs(directory)
    TCP()
    convert(video_h264)
    
