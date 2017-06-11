#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

import socket
import subprocess
import time
import os
from tkinter import *
import multiprocessing
import threading
import traceback

click = 0
host = ''
port = 8000
cwd = os.getcwd()
e = multiprocessing.Event()
p = None
thread_running = False

def convert(video,directory,time_stamp):
    try: 
        video_mp4 = os.path.join(directory,time_stamp+'.mp4')
        cmdline = ['ffmpeg','-y' ,'-i', video, '-c:v', 'copy', video_mp4]
        convert = subprocess.call(cmdline)
    finally:
        os.remove(video)

def throw_error(label_text):
    win = Toplevel()
    win.wm_title("Error Message")
    l = Label(win,
              text=label_text,
              font=('Veranda',25))
    b = Button(win,
               text='Okay',
               bg='firebrick1',
               fg='white',
               relief=RAISED,
               command=win.destroy)
    l.grid(row=0,column=0)
    b.grid(row=1,column=0)

def record(e):
    global thread_running
    global startbutton
    global click
    
    if click == 0:
        click+=1
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host,port))
        connection = client_socket.makefile('rb')
        date_stamp = time.strftime('%y-%m-%d')
        time_stamp = time.strftime('%I.%M')
        directory = os.path.join(cwd,date_stamp)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        video_h264 = os.path.join(directory,time_stamp+'.h264')
        video_file = open(video_h264,'wb')
        try:
            cmdline = ['mplayer','-fps', '30', '-cache', '1024','-']
            player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
            while True:
                data = connection.read(1024)
                if not data:
                    '''
                    throw_error("Error: Could not grab video stream...\n",
                                "Check:\n",
                                "   -Power source for Raspberry Pi?",
                                "   -Client connection to Rasperry Pi")
                    '''
                    break
                try:
                    video_file.write(data)
                    player.stdin.write(data)

                except Exception as ex:
                    print('Error: ',ex)
                    traceback.print_exc()
                    thread_running = False
                    startbutton.config(highlightbackground='LightBlue1')
                    e.set()
                    #print(e.is_set())

                if e.is_set():
                    player.terminate()
                    video_file.close()
                    convert(video_h264,directory,time_stamp)
                    e.clear()
                    break
                            
        except Exception as ex:
            print('Error: ', ex)
            traceback.print_exc()

def start_record():
    global p
    global thread_running
    global startbutton
    global click

    if thread_running == False:
        thread_running = True
        #print('CONFIGURE BUTTON')
        startbutton.config(highlightbackground='indian red')
        p = threading.Thread(target=record, args=(e,))
        p.start()
    else:
        print('Other thread still running')


def stop_record():
    global click
    global thread_running
    global startbutton
    
    if click == 1:
        click -= 1
        e.set()
        p.join()
        thread_running = False
        startbutton.config(highlightbackground='LightBlue1')


if __name__ == '__main__':
    print('Connecting to Raspberry Pi...')
    root = Tk()
    root.resizable(width=False,height=False)
    root.geometry('{}x{}'.format(250,275))
    root.configure(background='LightBlue1')
    startbutton = Button(root, relief='raised',
                         text='RECORD',bg='LightBlue1',
                         highlightbackground='LightBlue1',
                         command=start_record)
    stopbutton = Button(root,
                        text='STOP',background='LightBlue1',
                        highlightbackground='LightBlue1',
                        command=stop_record)
    quitbutton = Button(root,
                        text='QUIT',bg='LightBlue1',
                        highlightbackground='LightBlue1',
                        command=root.quit)
    title = Label(root,
                  text='TELEDYNE',font=('Veranda',40),
                  fg='RoyalBlue1',bg='LightBlue1')
    subtitle = Label(root,
                     text='Seabotix',font=('Veranda',30),
                     fg='SpringGreen2',bg='LightBlue1')
    title.pack(side=TOP,fill=X,padx=5)
    subtitle.pack(side=TOP,pady=5)
    startbutton.pack(side=TOP)
    stopbutton.pack(side=TOP)
    quitbutton.pack(side=TOP)
    root.mainloop()
    
    
