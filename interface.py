from tkinter import *
from tkinter import ttk
import time
import json
import sys

import modules
from start_config import user_prefs_dir, command_list_dir

with open(user_prefs_dir, 'r', encoding='utf-8') as file:
    user_prefs = json.load(file)
with open(command_list_dir, 'r', encoding='utf-8') as file:
    command_list = json.load(file)
if getattr(sys, 'frozen', False):
    exe_path = sys.executable

STATIC_STATES = ['home', 'settings']
DYNAMIC_STATES = ['show_commands', "change_voice_commands", "change_assistant_respond"]
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
    speakerSpinBox = ttk.Spinbox(frame, values=ALL_SPEAKERS, textvariable=chosenSpeaker, command= lambda: change_settings('speaker', chosenSpeaker.get()), wrap=True)
    speakerSpinBox.pack()
    frames['settings'] = frame

    #home
    frame = ttk.Frame(window)
    SoftName = ttk.Label(frame, text="PCAudio", font=("Arial", 25))
    SoftName.pack()
    frames['home'] = frame


def create_dynamic_state(state):
    global command_list
    if state == 'show_commands':
        frame = Frame(window)

        columns = ("name", "v1", "v2", "v3", "v4", "v5", "r1")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=500)
        tree.pack(side=LEFT, anchor=NW)

        # определяем заголовки
        tree.heading("name", text="Команда")
        tree.heading("v1", text="Вариант 1")
        tree.heading("v2", text="Вариант 2")
        tree.heading("v3", text="Вариант 3")
        tree.heading("v4", text="Вариант 4")
        tree.heading("v5", text="Вариант 5")
        tree.heading("r1", text="Ответ")
        tree.column("#1", stretch=NO, width=140)
        tree.column("#2", stretch=NO, width=115)
        tree.column("#3", stretch=NO, width=115)
        tree.column("#4", stretch=NO, width=115)
        tree.column("#5", stretch=NO, width=115)
        tree.column("#6", stretch=NO, width=115)
        tree.column("#7", stretch=NO, width=260)
        for c, v in command_list.items():
            if not 'user' in v:
                for c1, v1 in v.items():
                    name = v1['name']
                    voices = [""] * 5
                    for i in range(len(v1['user'])):
                        voices[i] = v1['user'][i]
                    respond = v1['assistant']
                    command = (name, voices[0], voices[1], voices[2], voices[3], voices[4], respond)
                    tree.insert("", END, values=command)
            else:
                name = v['name']
                voices = [""] * 5
                for i in range(len(v['user'])):
                    voices[i] = v['user'][i]
                respond = v['assistant']
                command = (name, voices[0], voices[1], voices[2], voices[3], voices[4], respond)
                tree.insert("",END,values=command)
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=LEFT)
    elif state == "change_voice_commands":
        pass
    elif state == "change_assistant_respond":
        pass
    frames[state] = frame


def set_state(state):
    print(frames)
    for key, frame in frames.items():
        if key in DYNAMIC_STATES:
            for widget in frame.winfo_children():
                print(1)
                widget.destroy()
            frame.destroy()
        else:
            frame.pack_forget()
    if state in DYNAMIC_STATES:
        create_dynamic_state(state)
    frames[state].pack(fill='both', expand=True)


def main():
    global window, frames
    window = Tk()
    window.title('PCAudio')

    simulate_loading()

    window.geometry('1000x500')
    window.protocol("WM_DELETE_WINDOW", close_app)

    menu_bar = Menu(window)
    window.config(menu=menu_bar)
    settings_exit = Menu(menu_bar, tearoff=0)
    commands_settings = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Меню', menu=settings_exit)
    settings_exit.add_command(label="Главная", command=lambda: set_state('home'))
    settings_exit.add_command(label="Настройки", command=lambda: set_state('settings'))
    settings_exit.add_command(label="Выход", command=close_app)
    menu_bar.add_cascade(label='Команды', menu=commands_settings)
    commands_settings.add_command(label="Список команд", command=lambda: set_state('show_commands'))
    frames = {}
    create_states()
    set_state('home')

    window.mainloop()