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

STATIC_STATES = ['home', 'settings', 'add_app', 'add_website']
DYNAMIC_STATES = ['show_commands', "change_voice_commands", "change_assistant_respond"]
ALL_SPEAKERS = ['aidar', 'baya', 'kseniya', 'xenia']
current_state = ''
command_vars = []
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

def change_voice_command():
    global command_list, command_vars
    temp_dict = {}
    for row in command_vars:
        if not row[0].cget("text") in temp_dict:
            temp_dict[row[0].cget("text")] = {}
        if row[1] == '':
            for i in range (5):
                try:
                    row[3][i] = row[3][i].get()
                except:
                    pass
            temp_dict[row[0].cget("text")]["name"] = row[2].cget('text')
            temp_dict[row[0].cget("text")]["user"] = row[3]
            temp_dict[row[0].cget("text")]["assistant"] = command_list[row[0].cget("text")]["assistant"]
        else:
            temp_dict[row[0].cget("text")][row[1].cget("text")] = {}
            for i in range (5):
                try:
                    row[3][i] = row[3][i].get()
                except:
                    pass
            temp_dict[row[0].cget("text")][row[1].cget("text")]["name"] = row[2].cget('text')
            temp_dict[row[0].cget("text")][row[1].cget("text")]["user"] = row[3]
            temp_dict[row[0].cget("text")][row[1].cget("text")]["assistant"] = command_list[row[0].cget("text")][row[1].cget("text")]["assistant"]
    command_list = temp_dict
    json_string = json.dumps(command_list, indent=4)
    with open(command_list_dir, "w", encoding='utf-8') as f:
        f.write(json_string)

def change_assistant_respond():
    global command_list, command_vars
    temp_dict = {}
    for row in command_vars:
        if not row[0].cget("text") in temp_dict:
            temp_dict[row[0].cget("text")] = {}
        if row[1] == '':
            temp_dict[row[0].cget("text")]["name"] = row[2].cget('text')
            temp_dict[row[0].cget("text")]["user"] = command_list[row[0].cget("text")]["user"]
            temp_dict[row[0].cget("text")]["assistant"] = row[3].get()
        else:
            temp_dict[row[0].cget("text")][row[1].cget("text")] = {}
            temp_dict[row[0].cget("text")][row[1].cget("text")]["name"] = row[2].cget('text')
            temp_dict[row[0].cget("text")][row[1].cget("text")]["user"] = command_list[row[0].cget("text")][row[1].cget("text")]["user"]
            temp_dict[row[0].cget("text")][row[1].cget("text")]["assistant"] = row[3].get()
    command_list = temp_dict
    json_string = json.dumps(command_list, indent=4)
    with open(command_list_dir, "w", encoding='utf-8') as f:
        f.write(json_string)

def add_website(form_data, name, url, command, respond):
    global command_list
    print(form_data[0].get(), form_data[1].get())
    name.pack_forget()
    url.pack_forget()
    command.pack_forget()
    respond.pack_forget()

    exception = False
    if not form_data[0].get():
        name.pack(side=LEFT)
        exception = True
    if not form_data[1].get():
        url.pack(side=LEFT)
        exception = True
    got_command = False
    for i in range(5):
        if form_data[2][i].get() != "":
            got_command = True
            break
    if not got_command:
        command.pack(side=LEFT)
        exception = True
    if not form_data[3].get():
        respond.pack(side=LEFT)
        exception = True
    if exception:
        return

    if not form_data[1].get() in command_list['open_website']:
        temp_dist = {'name': form_data[0].get()}
        for i in range(5):
            try:
                form_data[2][i] = form_data[2][i].get()
            except:
                pass
        temp_dist['user'] = form_data[2]
        temp_dist['assistant'] = form_data[3].get()
        command_list['open_website'][form_data[1].get()] = temp_dist
        print(temp_dist)
        json_string = json.dumps(command_list, indent=4)
        with open(command_list_dir, "w", encoding='utf-8') as file:
            file.write(json_string)

def add_app(form_data, excLeft, excRight):
    print(form_data)
    global command_list

    for i in excLeft:
        i.pack_forget()
    for i in excRight:
        i.pack_forget()

    exception = False
    if not form_data[0][0].get():
        excLeft[0].pack(anchor=W)
        exception = True
    if not form_data[1][0].get():
        excLeft[0].pack(anchor=W)
        exception = True
    got_command = False
    for i in range(5):
        if form_data[0][2][i].get() != "":
            got_command = True
            break
    if not got_command:
        excLeft[2].pack(anchor=W)
        exception = True
    if not form_data[0][3].get():
        excLeft[3].pack(anchor=W)
        exception = True
    if not form_data[1][0].get():
        excRight[0].pack(anchor=W)
        exception = True
    got_command = False
    for i in range(5):
        if form_data[1][2][i].get() != "":
            got_command = True
            break
    if not got_command:
        excRight[2].pack(anchor=W)
        exception = True
    if not form_data[1][3].get():
        excRight[3].pack(anchor=W)
        exception = True
    if exception:
        return

    if not form_data[0][1].get() in command_list['open_app']:
        for i in range(2):
            temp_dist = {'name': form_data[i][0].get()}
            for j in range(5):
                try:
                    form_data[i][2][j] = form_data[i][2][j].get()
                except:
                    pass
            temp_dist['user'] = form_data[i][2]
            temp_dist['assistant'] = form_data[i][3].get()
            if i==0:
                command_list['open_app'][form_data[0][1].get()] = temp_dist
            else:
                command_list['close_app'][form_data[1][1].get().lower()] = temp_dist
        json_string = json.dumps(command_list, indent=4)
        with open(command_list_dir, "w", encoding='utf-8') as file:
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

    #add_app
    frame = ttk.Frame(window)
    Label = ttk.Label(frame, text="Добавить приложение", font=("Arial", 25))
    Label.grid(row=0, column=1, sticky = "n")

    Column1 = ttk.Frame(frame)
    Column1.grid(row=1,column=0,pady=5)
    Column2 = ttk.Frame(frame)
    Column2.grid(row=1, column=2, pady=5)
    DefLabelLeft = ttk.Label(Column1, text="Открыть приложение", font=("Arial", 17))
    DefLabelLeft.pack(side=TOP, anchor=W, pady=5)
    DefLabelRight = ttk.Label(Column2, text="Закрыть приложение", font=("Arial", 17))
    DefLabelRight.pack(side=TOP, anchor=W, pady=5)
    SetNameLabelLeft = ttk.Label(Column1, text="Добавить имя команды", font=("Arial", 15))
    SetNameLabelLeft.pack(side=TOP, anchor=W, pady=5)
    SetNameLabelRight = ttk.Label(Column2, text="Добавить имя команды", font=("Arial", 15))
    SetNameLabelRight.pack(side=TOP, anchor=W, pady=5)
    NameWarningLeft = ttk.Label(Column1, text='заполните это поле', foreground='#ff0000')
    NameWarningRight = ttk.Label(Column2, text='заполните это поле', foreground='#ff0000')
    SetNameEntryLeft = ttk.Entry(Column1, width=50, validate='focusout')
    SetNameEntryLeft.pack(side=TOP, anchor=W, pady=5)
    SetNameEntryRight = ttk.Entry(Column2, width=50, validate='focusout')
    SetNameEntryRight.pack(side=TOP, anchor=W, pady=5)

    SetExeLabel = ttk.Label(Column1, text="Добавить исполняемый файл", font=("Arial", 15))
    SetExeLabel.pack(side=TOP, anchor=W, pady=5)
    ExeWarning = ttk.Label(Column1, text='заполните это поле', foreground='#ff0000')
    SetExeEntry = ttk.Entry(Column1, width=50, validate='focusout')
    SetExeEntry.pack(side=TOP, anchor=W, pady=5)

    SetCommandLabelLeft = ttk.Label(Column1, text="Добавить команды", font=("Arial", 15))
    SetCommandLabelLeft.pack(side=TOP, anchor=W, pady=5)
    SetCommandLabelRight = ttk.Label(Column2, text="Добавить команды", font=("Arial", 15))
    SetCommandLabelRight.pack(side=TOP, anchor=W, pady=5)
    CommandWarningLeft = ttk.Label(Column1, text='заполните это поле', foreground='#ff0000')
    CommandWarningRight = ttk.Label(Column2, text='заполните это поле', foreground='#ff0000')
    entriesLeft = []
    entriesRight = []
    for i in range(5):
        SetCommandEntryLeft = ttk.Entry(Column1, width=50, validate='focusout')
        SetCommandEntryLeft.pack(side=TOP, anchor=W, pady=5)
        SetCommandEntryRight = ttk.Entry(Column2, width=50, validate='focusout')
        SetCommandEntryRight.pack(side=TOP, anchor=W, pady=5)
        entriesLeft.append(SetCommandEntryLeft)
        entriesRight.append(SetCommandEntryRight)

    SetRespondLabelLeft = ttk.Label(Column1, text="Добавить ответ ассистента", font=("Arial", 15))
    SetRespondLabelLeft.pack(side=TOP, anchor=W, pady=5)
    SetRespondLabelRight = ttk.Label(Column2, text="Добавить ответ ассистента", font=("Arial", 15))
    SetRespondLabelRight.pack(side=TOP, anchor=W, pady=5)
    RespondWarningLeft = ttk.Label(Column1, text='заполните это поле', foreground='#ff0000')
    RespondWarningRight = ttk.Label(Column2, text='заполните это поле', foreground='#ff0000')
    SetRespondEntryLeft = ttk.Entry(Column1, width=50, validate='focusout')
    SetRespondEntryLeft.pack(side=TOP, anchor=W, pady=5)
    SetRespondEntryRight = ttk.Entry(Column2, width=50, validate='focusout')
    SetRespondEntryRight.pack(side=TOP, anchor=W, pady=5)

    app_form_data = [(SetNameEntryLeft, SetExeEntry, entriesLeft, SetRespondEntryLeft),(SetNameEntryRight, SetExeEntry, entriesRight, SetRespondEntryRight)]
    exceptionsLeft = (NameWarningLeft, ExeWarning, CommandWarningLeft, RespondWarningLeft)
    exceptionsRight = (NameWarningRight, ExeWarning, CommandWarningRight, RespondWarningRight)
    submit_button = ttk.Button(Column2, text="Добавить", command=lambda: add_app(app_form_data, exceptionsLeft, exceptionsRight))
    submit_button.pack(side=TOP, anchor=W, pady=5)
    frames['add_app'] = frame

    # add_website
    frame = ttk.Frame(window)
    Label = ttk.Label(frame, text="Добавить вебсайт", font=("Arial", 25))
    Label.pack()

    NameFrame = ttk.Frame(frame)
    NameFrame.pack(side=TOP, anchor=W, pady=5)
    SetNameLabel = ttk.Label(NameFrame, text="Добавить имя команды", font=("Arial", 15))
    SetNameLabel.pack(side=LEFT, anchor=W, pady=5, padx=10)
    NameWarning = ttk.Label(NameFrame, text='заполните это поле', foreground='#ff0000')
    SetNameEntry = ttk.Entry(frame, width=50, validate='focusout')
    SetNameEntry.pack(side=TOP, anchor=W, pady=5)

    UrlFrame = ttk.Frame(frame)
    UrlFrame.pack(side=TOP, anchor=W, pady=5)
    SetUrlLabel = ttk.Label(UrlFrame, text="Добавить ссылку на сайт", font=("Arial", 15))
    SetUrlLabel.pack(side=LEFT, padx=10)
    UrlWarning = ttk.Label(UrlFrame, text='заполните это поле', foreground='#ff0000')
    SetUrlEntry = ttk.Entry(frame, width=50, validate='focusout')
    SetUrlEntry.pack(side=TOP, anchor=W, pady=5)

    CommandFrame = ttk.Frame(frame)
    CommandFrame.pack(side=TOP, anchor=W, pady=5)
    SetCommandLabel = ttk.Label(CommandFrame, text="Добавить команды", font=("Arial", 15))
    SetCommandLabel.pack(side=LEFT, padx=10)
    CommandWarning = ttk.Label(CommandFrame, text='заполните это поле', foreground='#ff0000')
    entries = []
    for i in range(5):
        SetCommandEntry = ttk.Entry(frame, width=50, validate='focusout')
        SetCommandEntry.pack(side=TOP, anchor=W, pady=5)
        entries.append(SetCommandEntry)

    RespondFrame = ttk.Frame(frame)
    RespondFrame.pack(side=TOP, anchor=W, pady=5)
    SetRespondLabel = ttk.Label(RespondFrame, text="Добавить ответ ассистента", font=("Arial", 15))
    SetRespondLabel.pack(side=LEFT, pady=5, padx=10)
    RespondWarning = ttk.Label(RespondFrame, text='заполните это поле', foreground='#ff0000')
    SetRespondEntry = ttk.Entry(frame, width=50, validate='focusout')
    SetRespondEntry.pack(side=TOP, anchor=W, pady=5)

    form_data = (SetNameEntry, SetUrlEntry, entries, SetRespondEntry)
    submit_button = ttk.Button(frame, text="Добавить", command=lambda: add_website(form_data, NameWarning, UrlWarning, CommandWarning,RespondWarning))
    submit_button.pack(side=TOP, anchor=W, pady=5)
    frames['add_website'] = frame

def create_dynamic_state(state):
    global command_list, command_vars
    frame = Frame(window)
    if state == 'show_commands':

        columns = ("name", "v1", "v2", "v3", "v4", "v5", "r1")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        tree.grid(row=0, column=0, sticky='nsew')

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
        for v in command_list.values():
            if not 'user' in v:
                for v1 in v.values():
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
        scrollbar.grid(row=0, column=1, sticky='ns')
    elif state == "change_voice_commands":
        command_vars = []
        for c, v in command_list.items():
            if not 'user' in v:
                for c1, v1 in v.items():
                    row = ttk.Frame(frame)
                    row.pack(side=TOP, anchor=NW)
                    command = ttk.Label(row, text=c)
                    arg = ttk.Label(row, text=c1)
                    label = ttk.Label(row, text = v1['name'], width = 30)
                    label.pack(side=LEFT)
                    entries = []
                    for i in range(5):
                        entry_command = ttk.Entry(row, width = 20, validate="focusout", validatecommand=change_voice_command)
                        entry_command.pack(side=LEFT, padx=5)
                        try:
                            entry_command.delete(0, END)
                            entry_command.insert(0, v1['user'][i])
                        except:
                            pass
                        finally:
                            entries.append(entry_command)
                    command_vars.append((command, arg, label, entries))
            else:
                row = ttk.Frame(frame)
                row.pack(side=TOP, anchor=NW)
                command = ttk.Label(row, text=c, width=30)
                label = ttk.Label(row, text=v['name'], width=30)
                label.pack(side=LEFT)
                entries = []
                for i in range(5):
                    entry_command = ttk.Entry(row, width=20,validate="focusout", validatecommand=change_voice_command)
                    entry_command.pack(side=LEFT, padx=5)
                    try:
                        entry_command.delete(0, END)
                        entry_command.insert(0, v['user'][i])
                    except:
                        pass
                    finally:
                        entries.append(entry_command)
                command_vars.append((command, "", label, entries))
    elif state == "change_assistant_respond":
        command_vars = []
        for c, v in command_list.items():
            if not 'user' in v:
                for c1, v1 in v.items():
                    row = ttk.Frame(frame)
                    row.pack(side=TOP, anchor=NW)
                    command = ttk.Label(row, text=c)
                    arg = ttk.Label(row, text=c1)
                    label = ttk.Label(row, text=v1['name'], width=30)
                    label.pack(side=LEFT)
                    entry_command = ttk.Entry(row, width=100, validate="focusout",validatecommand=change_assistant_respond)
                    entry_command.pack(side=LEFT, padx=5)
                    entry_command.delete(0, END)
                    entry_command.insert(0, v1['assistant'])
                    command_vars.append((command, arg, label, entry_command))
            else:
                row = ttk.Frame(frame)
                row.pack(side=TOP, anchor=NW)
                command = ttk.Label(row, text=c, width=30)
                label = ttk.Label(row, text=v['name'], width=30)
                label.pack(side=LEFT)
                entry_command = ttk.Entry(row, width=100, validate="focusout", validatecommand=change_assistant_respond)
                entry_command.pack(side=LEFT, padx=5)
                entry_command.delete(0, END)
                entry_command.insert(0, v['assistant'])
                command_vars.append((command, "", label, entry_command))
    frames[state] = frame


def set_state(state):
    for key, frame in frames.items():
        if key in DYNAMIC_STATES:
            frame.destroy()
        else:
            frame.pack_forget()
    if state in DYNAMIC_STATES:
        create_dynamic_state(state)
    try:
        frames[state].pack(fill='both', expand=True)
    except:
        frames[state].grid(row=0, column=0)


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
    commands_settings.add_command(label="Изменить голосовые команды", command=lambda: set_state('change_voice_commands'))
    commands_settings.add_command(label="Изменить реакцию ассистента", command=lambda: set_state('change_assistant_respond'))
    commands_settings.add_command(label="Добавить приложения", command=lambda: set_state('add_app'))
    commands_settings.add_command(label="Добавить вебсайт", command=lambda: set_state('add_website'))

    frames = {}
    create_states()
    set_state('home')

    window.mainloop()