from tkinter import *
from tkinter import ttk
import time
import json
import sys

import modules
from start_config import user_prefs_dir

with open(user_prefs_dir, 'r', encoding='utf-8') as file:
    user_prefs = json.load(file)
if getattr(sys, 'frozen', False):
    exe_path = sys.executable

ALL_STATES = ['home', 'settings']
ALL_SPEAKERS = ['aidar', 'baya', 'kseniya', 'xenia']
current_state = ''
closed = False

def simulate_loading(duration = 5):
    state = 0
    end_i = 0

    progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)
    label = Label(window, text="")
    progress_bar.pack(pady=10)
    label.pack()
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
            end_i = i
        if end_i > 0:
            progress_bar['value'] = 95 + i - end_i
        else:
            progress_bar['value'] = i
        if progress_bar['value'] == 100:
            break
        window.update()
    progress_bar.destroy()
    label.destroy()

def close_app():
    global window, closed
    closed = True
    window.destroy()

def change_settings(label, value):
    user_prefs[label] = value
    json_string = json.dumps(user_prefs, indent=4)
    with open(user_prefs_dir, 'w') as file:
        file.write(json_string)

def do_startup_change():
    state = startupVar.get()
    change_settings('isStartup', state)
    if state and exe_path:
        modules.add_to_startup('pcAudio', exe_path)
    else:
        modules.remove_from_startup('pcAudio')

def set_state(state):
    for frame in frames.values():
        frame.pack_forget()
    frames[state].pack(fill='both', expand=True)


def create_states():
    #settings
    frame = ttk.Frame(window)
    label = ttk.Label(frame, text="Настройки", font="Arial 18")
    label.pack()
    global startupVar
    startupVar = BooleanVar(value=user_prefs['isStartup'])
    startupCheckBox = Checkbutton(frame, text="Запускать при старте системы", variable=startupVar, command=do_startup_change)
    startupCheckBox.pack()
    label = ttk.Label(frame, text="Выбери голосового ассистента")
    label.pack()
    global chosenSpeaker
    chosenSpeaker = StringVar(value=user_prefs['speaker'])
    speakerSpinBox = ttk.Spinbox(frame, values=ALL_SPEAKERS, textvariable=chosenSpeaker, command= lambda: change_settings('speaker', chosenSpeaker.get()))
    speakerSpinBox.pack()
    frames['settings'] = frame

    #home
    frame = ttk.Frame(window)
    SoftName = ttk.Label(frame, text="PCAudio", font=("Arial", 25))
    SoftName.pack()
    frames['home'] = frame

def main():
    global window, frames
    window = Tk()
    window.title('PCAudio')

    simulate_loading()

    window.geometry('300x300')
    window.protocol("WM_DELETE_WINDOW", close_app)

    menu_bar = Menu(window)
    window.config(menu=menu_bar)
    settings_exit = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Меню', menu=settings_exit)
    settings_exit.add_command(label="Главная", command=lambda: set_state('home'))
    settings_exit.add_command(label="Настройки", command=lambda: set_state('settings'))
    settings_exit.add_command(label="Выход", command=close_app)

    frames = {}
    create_states()
    set_state('home')


    window.mainloop()