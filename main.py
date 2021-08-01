from tkinter import *
import pafy
import threading

# hover effects for buttons
def download_button_enter(e):
    download_button.config(background="#6e7c8c")

def download_button_leave(e):
    download_button.config(background="#596573")

# focus effect for entry
def url_entry_focusin(e):
    if url_entry["fg"] == "grey":
        url_entry.delete(0, END)
        url_entry.config(fg="#ffffff")

# audio download function
def audio_download_func(x):
    # disabling all the widgets when we hit the download buttons
    for i in audio_frame.winfo_children():
        i.configure(state="disable")

    for i in video_frame.winfo_children():
        i.configure(state="disable")
    
    for i in top_frame.winfo_children():
        i.configure(state="disable")

    x.download(meta=True)

    # enabling all the widgets when the download is completetd
    for i in audio_frame.winfo_children():
        i.configure(state="normal")
    
    for i in video_frame.winfo_children():
        i.configure(state="normal")

    for i in top_frame.winfo_children():
        i.configure(state="normal")

# video download function
def video_download_func(x):
    # disabling all the widgets when we hit the download buttons
    for i in video_frame.winfo_children():
        i.configure(state="disable")

    for i in audio_frame.winfo_children():
        i.configure(state="disable")
    
    for i in top_frame.winfo_children():
        i.configure(state="disable")

    x.download(meta=True)

    # enabling all the widgets when the download is completetd
    for i in video_frame.winfo_children():
        i.configure(state="normal")
    
    for i in audio_frame.winfo_children():
        i.configure(state="normal")
    
    for i in top_frame.winfo_children():
        i.configure(state="normal")

def youtube_downloader(): 
    # removing the widgets from the frame each time we press the download button and renew them
    for i in detail_frame.winfo_children():
        i.destroy()
    
    for i in audio_frame.winfo_children():
        i.destroy()
    
    for i in video_frame.winfo_children():
        i.destroy()

    top_frame.winfo_children()[3].destroy()

    e_label = Label(top_frame,
                    fg="red",
                    font=("Arial", 10),
                    background="#333b46")
    

    try:
        # loading the youtube link
        url_variable = url_entry.get()  
        youtube = pafy.new(url_variable)

        audio = youtube.audiostreams
        video = youtube.streams

        # ------------ link details ------------  
        details = {"Author": youtube.author,
                   "Title": youtube.title,
                   "Duration": youtube.duration,
                   "Rate": "{:.2f}".format(youtube.rating),
                   "View Count": "{:,}".format(youtube.viewcount)}
    
    except ValueError:
        e_label.config(text="Enter a valid link!")
        e_label.pack()
    
    except IOError:
        e_label.config(text="No internet connection!")
        e_label.pack()

    else:
        for k, v in details.items():
            author_label = Label(detail_frame,
                                text="{} : {}".format(k, v),
                                background="#404a57",
                                fg="#ffffff")
            author_label.pack(pady=5, padx=5)
        detail_frame.pack(expand=YES, fill=X, padx=5, pady=5)

        # ------------ audio details ------------ 
        audio_counter = 0
        for i in audio:
            audio_counter = audio_counter + 1
            audio_label = Label(audio_frame,
                                background="#404a57",
                                fg="#ffffff",
                                text=(audio_counter, ".", i.bitrate, "|", i.extension, "|", "{:.3f}".format(i.get_filesize() * pow(10, -6)), "Mb"))
            audio_label.grid(row=audio_counter, column=0, pady=5)
            audio_download_button = Button(audio_frame,
                                        text="Download",
                                        bd=0,
                                        fg="#dddddd",
                                        background="#404a57",
                                        activebackground="#404a57",
                                        command=lambda i=i:audio_thread(i)) # calling the multithread functions
            audio_download_button.grid(row=audio_counter, column=1, pady=5, padx=30)
        audio_frame.pack(expand=YES, fill=X, padx=5, pady=5)

        # ------------ video details ------------
        video_counter = 0
        for i in video:
            video_counter = video_counter + 1
            video_label = Label(video_frame,
                                background="#404a57",
                                fg="#ffffff",
                                text=(video_counter, ".", i.resolution, "|", i.extension, "|", "{:.3f}".format(i.get_filesize() * pow(10, -6)), "Mb"))
            video_label.grid(row=video_counter, column=0, pady=5)
            video_download_button = Button(video_frame,
                                        text="Download",
                                        bd=0,
                                        fg="#dddddd",
                                        background="#404a57",
                                        activebackground="#404a57",
                                        command=lambda i=i:video_thread(i)) # calling the multithread functions
            video_download_button.grid(row=video_counter, column=1, pady=5, padx=30)
        video_frame.pack(expand=YES, fill=X, padx=5, pady=5)


# multi threading the download function so they wouldn't stuck when we run them
def thread():    
    x = threading.Thread(target=youtube_downloader)
    x.start()

def audio_thread(z):
    x = threading.Thread(target=audio_download_func, args=(z,))  
    x.start()

def video_thread(z):
    x = threading.Thread(target=video_download_func, args=(z,))
    x.start()
    
window = Tk()

window.title("YouTube Downloader v0.4")

window.config(background="#333b46")

#icon = PhotoImage(file=("C:\\Users\\Ali\\Desktop\\New folder (2)\\youtube.png"))
#window.iconphoto(True, icon)

top_frame = Frame(window,
                  background="#333b46")
top_frame.pack()

url_label = Label(top_frame,
                  text="YouTube Downloader",
                  font=("Arial", 10, "bold"),
                  background="#333b46",
                  fg="#ffffff")
url_label.pack()

entry_label = Label(top_frame,
                    background="#404a57")
entry_label.pack(padx=15, pady=5)

url_entry = Entry(entry_label,
                  font=("Arial", 10),
                  background="#404a57",
                  bd=0,
                  fg="grey",
                  width=50)
url_entry.insert(0, "Enter youtube link")
url_entry.bind("<FocusIn>", url_entry_focusin)
url_entry.pack(pady=5)

download_button = Button(top_frame,
                         text="Download",
                         bd=0,
                         command=thread,
                         background="#596573",
                         fg="#ffffff",
                         activebackground="#4f5966",
                         activeforeground="#ffffff",
                         padx=20,
                         pady=5)
download_button.bind("<Enter>", download_button_enter)
download_button.bind("<Leave>", download_button_leave)
download_button.pack(pady=5)

error_label = Label(top_frame,
                    fg="red",
                    background="#333b46")

detail_frame = LabelFrame(window,
                            text="Details",
                            borderwidth=2,
                            background="#404a57",
                            foreground="#ffffff")

audio_frame = LabelFrame(window,
                         text="Audio",
                         borderwidth=2,
                         background="#404a57",
                         foreground="#ffffff")

video_frame = LabelFrame(window,
                         text="Video",
                         borderwidth=2,
                         foreground="#ffffff",
                         background="#404a57")

window.resizable(False, False)

window.mainloop()