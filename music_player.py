from tkinter import*
import tkinter as tk
from tkinter import ttk , filedialog 
from pygame import mixer 
import os
import random
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from PIL import ImageTk, Image
from io import BytesIO
#import stagger

root=Tk()
root.title('Music Player')
root.geometry('920x640')
root.configure(bg='#ffd3c9')
root.resizable(False,False)

global directory
global is_stopped
is_stopped = False

mixer.init()

#VolumeLabel
vol_now=Label(root,text="",font=("arial",15),fg="#ff1548",bg="#ffd3c9")
vol_now.place(x=155,y=350,anchor="center")

def open_folder():
    path = filedialog.askdirectory()
    if path:
        os.chdir(path)
        songs=os.listdir(path)      
    for song in songs:
        if song.endswith(".mp3"):
            #song = song.replace(".mp3", "")
            playlist.insert(END,song)
        if song.endswith(".wav"):
            #song = song.replace(".mp3", "")
            playlist.insert(END,song)
    #print(len(songs))

def add_songs():
    global directory
    songs = filedialog.askopenfilenames(initialdir='music_files/', title="Select songs to add", filetypes=(("Audio Files", "*.mp3"), ))
    for song in songs:
        directory = os.path.split(song)[0]
        os.chdir(directory)
        #print(directory)
        song = song.replace(directory+"/", "")
        playlist.insert(END, song)

'''
def shuffle():
    global songs
    shuffle_song = random.randint(0, len(songs))
    play_song(shuffle_song)
    #selection change
    playlist.selection_clear(0, END)
    playlist.activate(shuffle_song)
    playlist.selection_set(shuffle_song, last=None)
'''
def shuffle():
    stop_song()
    all_songs = playlist.get(0, END)
    all_songs = list(all_songs)
    random.shuffle(all_songs)
    playlist.delete(0, END)
    for song in all_songs:
        playlist.insert(END, song)

'''
def play_song():
    if playlist.selection_set(0, last=None):
        playlist.selection_set(1, last=None)

    music_name= playlist.get(ACTIVE)
    #mixer.music.load(f'{music_name}.mp3')
    mixer.music.load(music_name)
    mixer.music.play(loops=0)
    music.config(text=music_name)
    
    play_time()

    music_mutagen = MP3(music_name)
    artist.config(text=music_mutagen['TPE1'].text[0])
'''

def play_song(to_play = ACTIVE):
    global is_stopped
    global directory
    is_stopped = False
    music_name = playlist.get(to_play)

    #play song
    #mixer.music.load(f'{directory}/{music_name}')
    mixer.music.load(music_name)
    mixer.music.play(loops=0)

    #set selection to first song by default
    if len(playlist.curselection()) == 0:
        playlist.activate(ACTIVE)
        playlist.selection_set(0, last=None)
    
    #update song info
    music.config(text=music_name)   #name
    play_time()                     #time
    #music_mutagen = MP3(f'{directory}/{music_name}')
    music_mutagen = MP3(music_name) 
    artist.config(text=music_mutagen['TPE1'].text[0])   #artist
    album.config(text=music_mutagen['TALB'].text[0])    #album

    #display album art
    art_data = ID3(music_name).get("APIC:").data
    im = Image.open(BytesIO(art_data))
    im = im.resize((200,200))
    art_img = ImageTk.PhotoImage(im)
    album_art.config(image=art_img)
    album_art.photo = art_img

    album_art.place(x=800,y=120, anchor="center")

    '''
    #stagger 
    mp3 = stagger.read_tag(music_name)
    by_data = mp3[stagger.id3.APIC][0].data
    im = BytesIO(by_data)
    art=ImageTk.PhotoImage(Image.open(im))
    album_art.config(image=art)
    album_art.photo = art
    '''

def stop_song():
    global is_stopped
    mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    playlist.activate(0)

    is_stopped = True
    album_art.place_forget()
    duration.config(text='')
    music.config(text='')
    album.config(text='')
    artist.config(text='')

    
def next_song():
    #check if first song
    if len(playlist.curselection()) == 0:
        next_song = 1
    else:
        next_song = playlist.curselection()
        next_song = next_song[0]+1

    play_song(next_song)
    
    #selection change
    playlist.selection_clear(0, END)
    playlist.activate(next_song)
    playlist.selection_set(next_song, last=None)

def prev_song():
    prev_song = playlist.curselection()
    prev_song = prev_song[0]-1

    play_song(prev_song)

    #selection change
    playlist.selection_clear(0, END)
    playlist.activate(prev_song)
    playlist.selection_set(prev_song, last=None)

def play_time():
    global is_stopped
    current_time = mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    music_name = playlist.get(ACTIVE)

    #music_mutagen = MP3(f'{directory}/{music_name}')
    music_mutagen = MP3(music_name)
    music_len = music_mutagen.info.length
    converted_song_len = time.strftime('%M:%S', time.gmtime(music_len))

    if not is_stopped:
        duration.config(text=f'{converted_current_time} / {converted_song_len}')
        duration.after(1000, play_time)

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True

def set_vol(val):
    volume=float(val)
    volume2 = int(100 * (float("%.2f" % volume)))
    mixer.music.set_volume(volume)
    vol_now.config(text=f'Volume: {volume2}%')
        
#icon 
image_icon=PhotoImage(file='logo.png')
root.iconphoto(False,image_icon)

Top=PhotoImage(file='top.png')
Label(root,image=Top,bg='#ffd3c9').pack()

#logo 
Logo=PhotoImage(file='logo.png')
Label(root,image=Logo,bg='#ffd3c9').place(x=65,y=115)

#buttons 
play_button=PhotoImage(file='play.png')
Button(root,image=play_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=play_song).place(x=100,y=435)

stop_button=PhotoImage(file='stop.png')
Button(root,image=stop_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=stop_song).place(x=115,y=535)

shuffle_button=PhotoImage(file='shuffle.png')
Button(root,image=shuffle_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=shuffle).place(x=30,y=535)

pause_button=PhotoImage(file='pause.png')
Button(root,image=pause_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=lambda: pause(paused)).place(x=200,y=535)

next_button=PhotoImage(file='next.png')
Button(root,image=next_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=next_song).place(x=200,y=450)

prev_button=PhotoImage(file='prev.png')
Button(root,image=prev_button,bg='#ffd3c9',activebackground='#ffd3c9',cursor='hand2',bd=0,command=prev_song).place(x=30,y=450)

#volume slider
style = ttk.Style()

trough=PhotoImage(file='trough.png')
slider=PhotoImage(file='slider.png')
style.element_create('custom.Scale.trough', 'image', trough)
style.element_create('custom.Scale.slider', 'image', slider)

style.layout('custom.Horizontal.TScale',
              [('custom.Scale.trough', {'sticky': 'we'}),
               ('custom.Scale.slider',
                {'side': 'left', 'sticky': '',
                 'children': [('custom.Horizontal.Scale.label', {'sticky': ''})]
                })])
style.configure('custom.Horizontal.TScale', background='#ffd3c9')


hs = ttk.Scale(root, orient="horizontal", cursor="hand2",  style="custom.Horizontal.TScale", command=set_vol)
hs.set(0.5)  #default_val
mixer.music.set_volume(0.5)
hs.place(x=155, y=390, width= 180, anchor="center")


'''
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.place(x=155,y=370,anchor="center")
'''

#---METADATA---

#album_art
album_art = Label(root, bg='#ffd3c9', image = "")
album_art.place_forget()

#title_label
music=Label(root,text="",font=("arial",18),fg="#ffd3c9",bg="#ff1548")
music.place(x=500,y=80,anchor="center")

#duration_label
duration=Label(root,text="",font=("arial",8),fg="#ffd3c9",bg="#ff1548")
duration.place(x=500,y=175,anchor="center")

#ArtistLabel
artist=Label(root,text="",font=("arial",15),fg="#ffd3c9",bg="#ff1548")
artist.place(x=500,y=130,anchor="center")

#album_label
album=Label(root,text="",font=("arial",10),fg="#ffd3c9",bg="#ff1548")
album.place(x=500,y=155,anchor="center")

#---


#playlist_box
music_frame=Frame(root,bd=0,relief=RIDGE)
music_frame.place(x=330,y=350,width=560,height=250)

#Add songs buttons
Button(root,text='Scan Folder',width=15,height=2,font=('arial',10,'bold'),fg='#ffd3c9',bg='#ff1548',command=open_folder).place(x=330,y=280)

Button(root,text='Add songs',width=15,height=2,font=('arial',10,'bold'),fg='#ffd3c9',bg='#ff1548',command=add_songs).place(x=500,y=280)

scroll = Scrollbar(music_frame)
playlist=Listbox(music_frame,width=100,font=('arial',10),bg='#ff1548',fg='#ffd3c9',selectbackground='#ffd3c9',selectforeground='#ff1548',cursor='hand2',bd=0,yscrollcommand=scroll.set)

scroll.config(command=playlist.yview)
scroll.pack(side=RIGHT,fill=Y)
playlist.pack(side=LEFT,fill=BOTH)



root.mainloop()