from pytube import Playlist, YouTube
from moviepy.editor import *
import youtube_dlc
import os
from tkinter import *
from tkinter.ttk import Progressbar
import threading

stop_download = False

def check_url_video(url):
    ydl = youtube_dlc.YoutubeDL({'quiet': True})
    try:
        info = ydl.extract_info(url, download=False)
        return True
    except Exception:
        return False

def download(update_progress):
    global stop_download
    stop_download = False
    link.config(state=DISABLED)
    playlist_link = link.get()
    playlist = Playlist(playlist_link)


    total_videos = len(playlist.video_urls)
    progress['maximum'] = total_videos
    for i, video_url in enumerate(playlist.video_urls, start=1):
        if stop_download:
            break
        try:
            if check_url_video(video_url):
                video = YouTube(video_url)
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_file = audio_stream.download()
                audio = AudioFileClip(audio_file)
                audio.write_audiofile(video.title + ".mp3", bitrate="192k")
                os.remove(video.title + ".mp4")
                update_progress(True, video.title)
            else:
                update_progress(False, video.title)
        except Exception:
            update_progress(False, video.title)
        progress['value'] = i
        progress.update()

def stop():
    global stop_download
    stop_download = True

root = Tk()
root.title("Baixa Playlist do Youtube")
root.resizable(True, True)
root.geometry("500x500")

link_label = Label(root, text="Link da playlist:")
link_label.config(font=("Arial", 25))
link_label.pack()

link = Entry(root)
link.config(font=("Arial", 16), width=50)
link.pack()

download_button = Button(root, text="Baixar", command=lambda: threading.Thread(target=download, args=(update_progress,)).start())
download_button.config(font=("Arial", 26))
download_button.pack()

stop_button = Button(root, text="Cancelar", command=stop)
stop_button.config(font=("Arial", 26))
stop_button.pack()

progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=10)

file_list = Listbox(root, width=450)
file_list.pack(pady=(0, 10))

def update_progress(success, filename):
    if success:
        file_list.insert(END, filename)
        file_list.itemconfig(END, {'fg': 'green'})
    else:
        file_list.insert(END, filename)
        file_list.itemconfig(END, {'fg': 'red'})

root.mainloop()
