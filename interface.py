from tkinter import *
from tkinter import ttk
import time
import modules

def simulate_loading(progress_bar, label, duration = 5):
    state = 0
    for i in range(101):
        time.sleep(duration / 100)  # Simulate loading time
        if modules.load_models == 0 and state == 0:
            label.config(text='Voice recognizing module loading...')
            state = 1
        elif modules.load_models == 1 and state == 1:
            label.config(text="Voice speaking module loading...")
            state = 2
        elif modules.load_models == 2 and state == 2:
            label.config(text="Finishing...")
            state = 3
            i = 95
        progress_bar['value'] = i
        window.update()
    progress_bar.destroy()
    label.destroy()

def main():
    global window
    window = Tk()
    progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    label = Label(window, text="")
    progress_bar.pack(pady=10)
    label.pack()
    simulate_loading(progress_bar, label)
    window.geometry('800x600')
    window.mainloop()