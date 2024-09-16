from tkinter import *
import time
from tkinter import ttk
import json
import modules
from pathfinder import find_path
from create_data import user_prefs_dir
#STATES = ['home','add_command','command_voices','voice_responces', 'add_app', 'add_web']
#current_state = 'home'
closed = False

with open(user_prefs_dir, 'r', encoding='utf-8') as file:
    user_prefs = json.load(file)

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

def settings():
    settings_window = Tk()
    settings_window.title('Settings')
    settings_window.geometry("200x300+200+200")
    checkbox = Checkbutton(settings_window,text="Start with OS", variable=user_prefs['isStartup'])
    checkbox.pack()

def main():
    global window
    window = Tk()
    window.title('PCAudio')

    if user_prefs['isStartup'] == -1:
        modules.add_to_startup("PCAudio", 'start_test.bat')
        change_settings('isStartup', 1)

    simulate_loading()

    window.geometry('800x600')
    window.protocol("WM_DELETE_WINDOW", close_app)

    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    settings_exit = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Menu', menu=settings_exit)
    settings_exit.add_command(label="Settings", command=settings)
    settings_exit.add_command(label="Exit", command=close_app)

    window.mainloop()