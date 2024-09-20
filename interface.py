from tkinter import *
from tkinter import ttk, messagebox
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

STATIC_STATES = ['home', 'settings', 'help', 'add_app', 'add_website']
DYNAMIC_STATES = ['show_commands', "change_voice_commands", "change_assistant_respond", "show_apps_and_webs"]
ALL_SPEAKERS = ['aidar', 'baya', 'kseniya', 'xenia']
current_state = ''
command_vars = []
closed = False
toggleBot = True

#start loading models progress bar
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

#custom closing function
def close_app(window):
    global closed
    window.destroy()
    closed = True

def toggle_bot():
    global toggleBot
    if toggleBot:
        toggleBot = False
        ToggleButton.configure(text='Включить ассистента')
        ToggleBotLabel.configure(text='Сейчас ассистент неактивен')
    else:
        toggleBot = True
        ToggleButton.configure(text='Выключить ассистента')
        ToggleBotLabel.configure(text='Сейчас ассистент активен')


#saves recent data about all commands
def save_data(command_list):
    json_string = json.dumps(command_list, indent=4)
    with open(command_list_dir, "w", encoding='utf-8') as f:
        f.write(json_string)

#apps and webs listbox showing
def populate_listboxes():
    apps_listbox.delete(0, END)
    webs_listbox.delete(0, END)
    for item in command_list['open_website'].values():
        webs_listbox.insert(END, item['name'])
    for item in command_list['open_app'].values():
        apps_listbox.insert(END, item['name'])

#apps and webs deleting function
def delete_item():
    appSelected = apps_listbox.curselection()
    webSelected = webs_listbox.curselection()
    cnt = 0
    print(appSelected)
    if appSelected != ():
        for key in command_list['open_app'].keys():
            if cnt == appSelected[0]:
                print(1)
                del command_list['open_app'][key]
                del command_list['close_app'][key.lower()]
                break
            cnt += 1
        populate_listboxes()
    elif webSelected != ():
        for key in command_list['open_website'].keys():
            if cnt == webSelected[0]:
                del command_list['open_website'][key]
                break
            cnt += 1
        populate_listboxes()
    else:
        messagebox.showwarning("Не выбран элемент", "Выберите элемент для удаления")
    save_data(command_list)

#settings saving to JSON
def change_settings(label, value):
    user_prefs[label] = value
    json_string = json.dumps(user_prefs, indent=4)
    with open(user_prefs_dir, 'w') as file:
        file.write(json_string)

#voice commands list rewrite
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
    save_data(command_list)

#assistant respond list rewrite
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
    save_data(command_list)

#web adding form with exceptions
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
        save_data(command_list)

#app adding form submit with exceptions
def add_app(form_data, excLeft, excRight):
    print(form_data)
    global command_list

    for i in excLeft:
        i.pack_forget()
    for i in excRight:
        i.pack_forget()

    exception = False
    if not form_data[0][0].get():
        excLeft[0].pack(side=LEFT)
        exception = True
    if not form_data[0][1].get():
        excLeft[1].pack(side=LEFT)
        exception = True
    got_command = False
    for i in range(5):
        if form_data[0][2][i].get() != "":
            got_command = True
            break
    if not got_command:
        excLeft[2].pack(side=LEFT)
        exception = True
    if not form_data[0][3].get():
        excLeft[3].pack(side=LEFT)
        exception = True
    if not form_data[1][0].get():
        excRight[0].pack(side=LEFT)
        exception = True
    got_command = False
    for i in range(5):
        if form_data[1][2][i].get() != "":
            got_command = True
            break
    if not got_command:
        excRight[2].pack(side=LEFT)
        exception = True
    if not form_data[1][3].get():
        excRight[3].pack(side=LEFT)
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
        save_data(command_list)

#startup changing
def do_startup_change():
    state = startupVar.get()
    change_settings('isStartup', state)
    if state and exe_path:
        modules.add_to_startup('pcAudio', exe_path)
    else:
        modules.remove_from_startup('pcAudio')

#creates static states for all session
def create_states():
    #settings
    frame = ttk.Frame(window)
    label = ttk.Label(frame, text="Настройки", font=("Helvetica", 25))
    label.pack(pady=5)
    global startupVar
    startupVar = BooleanVar(value=user_prefs['isStartup'])
    startupCheckBox = Checkbutton(frame, text="Запускать при старте системы", variable=startupVar, command=do_startup_change ,font=("Helvetica", 12))
    startupCheckBox.pack()
    label = ttk.Label(frame, text="Выбери голосового ассистента", font=("Helvetica", 16))
    label.pack(pady=10)
    global chosenSpeaker
    chosenSpeaker = StringVar(value=user_prefs['speaker'])
    speakerSpinBox = ttk.Spinbox(frame, values=ALL_SPEAKERS, textvariable=chosenSpeaker, command= lambda: change_settings('speaker', chosenSpeaker.get()), wrap=True, font=("Helvetica", 12))
    speakerSpinBox.pack()
    frames['settings'] = frame

    #home
    frame = ttk.Frame(window)
    SoftName = ttk.Label(frame, text="PCAudio", font=("Helvetica", 25))
    SoftName.pack(pady=5)
    DescLabel = ttk.Label(frame, text="Начните использовать голосовое управление уже сегодня и сделайте вашу работу за компьютером еще более комфортной и продуктивной!", font=("Helvetica", 12), wraplength=1000, justify="center")
    DescLabel.pack(side = TOP)
    global ToggleButton, ToggleBotLabel
    ToggleButton = Button(frame, text="Выключить ассистента", font=("Helvetica", 16), command=toggle_bot)
    ToggleBotLabel = ttk.Label(frame, text="Cейчас ассистент активен", font=("Helvetica", 16))
    ToggleBotLabel.pack(pady=30)
    ToggleButton.pack()
    frames['home'] = frame

    #help
    with open(modules.find_path('help.txt'), 'r', encoding='utf-8') as file:
        help_text = file.read()
    frame = ttk.Frame(window)
    Label = ttk.Label(frame, text="Руководство пользователя", font=("Helvetica", 25))
    Label.pack(pady=5)
    canvas = Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    label = ttk.Label(scrollable_frame,text=help_text, font=("Helvetica", 10), wraplength=950)
    label.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    frames['help'] = frame

    #add_app
    frame = ttk.Frame(window)
    Label = ttk.Label(frame, text="Добавить приложение", font=("Arial", 25))
    Label.grid(row=0, column=1, sticky = "w")

    Column1 = ttk.Frame(frame)
    Column1.grid(row=1,column=0,pady=5, sticky="w")
    Column2 = ttk.Frame(frame)
    Column2.grid(row=1, column=2, pady=5, sticky="e")
    DefLabelLeft = ttk.Label(Column1, text="Открыть приложение", font=("Arial", 17))
    DefLabelLeft.pack(side=TOP, anchor=W, pady=5)
    DefLabelRight = ttk.Label(Column2, text="Закрыть приложение", font=("Arial", 17))
    DefLabelRight.pack(side=TOP, anchor=W, pady=5)
    NameFrameLeft = ttk.Frame(Column1)
    NameFrameLeft.pack(side=TOP, anchor=W)
    NameFrameRight = ttk.Frame(Column2)
    NameFrameRight.pack(side=TOP, anchor=W)
    SetNameLabelLeft = ttk.Label(NameFrameLeft, text="Добавить имя команды", font=("Arial", 15))
    SetNameLabelLeft.pack(side=LEFT, pady=5)
    SetNameLabelRight = ttk.Label(NameFrameRight, text="Добавить имя команды", font=("Arial", 15))
    SetNameLabelRight.pack(side=LEFT, pady=5)
    NameWarningLeft = ttk.Label(NameFrameLeft, text='заполните это поле', foreground='#ff0000')
    NameWarningRight = ttk.Label(NameFrameRight, text='заполните это поле', foreground='#ff0000')
    SetNameEntryLeft = ttk.Entry(Column1, width=50, validate='focusout')
    SetNameEntryLeft.pack(side=TOP, anchor=W, pady=5)
    SetNameEntryRight = ttk.Entry(Column2, width=50, validate='focusout')
    SetNameEntryRight.pack(side=TOP, anchor=W, pady=5)

    ExeFrame = ttk.Frame(Column1)
    ExeFrame.pack(side=TOP, anchor=W)
    SetExeLabel = ttk.Label(ExeFrame, text="Добавить исполняемый файл", font=("Arial", 15))
    SetExeLabel.pack(side=LEFT, pady=5)
    ExeWarning = ttk.Label(ExeFrame, text='заполните это поле', foreground='#ff0000')
    SetExeEntry = ttk.Entry(Column1, width=50, validate='focusout')
    SetExeEntry.pack(side=TOP, anchor=W, pady=5)

    CommandFrameLeft = ttk.Frame(Column1)
    CommandFrameLeft.pack(side=TOP, anchor=W)
    CommandFrameRight = ttk.Frame(Column2)
    CommandFrameRight.pack(side=TOP, anchor=W)
    SetCommandLabelLeft = ttk.Label(CommandFrameLeft, text="Добавить команды", font=("Arial", 15))
    SetCommandLabelLeft.pack(side=LEFT, pady=5)
    SetCommandLabelRight = ttk.Label(CommandFrameRight, text="Добавить команды", font=("Arial", 15))
    SetCommandLabelRight.pack(side=LEFT, pady=5)
    CommandWarningLeft = ttk.Label(CommandFrameLeft, text='заполните это поле', foreground='#ff0000')
    CommandWarningRight = ttk.Label(CommandFrameRight, text='заполните это поле', foreground='#ff0000')
    entriesLeft = []
    entriesRight = []
    for i in range(5):
        SetCommandEntryLeft = ttk.Entry(Column1, width=50, validate='focusout')
        SetCommandEntryLeft.pack(side=TOP, anchor=W, pady=5)
        SetCommandEntryRight = ttk.Entry(Column2, width=50, validate='focusout')
        SetCommandEntryRight.pack(side=TOP, anchor=W, pady=5)
        entriesLeft.append(SetCommandEntryLeft)
        entriesRight.append(SetCommandEntryRight)

    RespondFrameLeft = ttk.Frame(Column1)
    RespondFrameLeft.pack(side=TOP, anchor=W)
    RespondFrameRight = ttk.Frame(Column2)
    RespondFrameRight.pack(side=TOP, anchor=W)
    SetRespondLabelLeft = ttk.Label(RespondFrameLeft, text="Добавить ответ ассистента", font=("Arial", 15))
    SetRespondLabelLeft.pack(side=LEFT, pady=5)
    SetRespondLabelRight = ttk.Label(RespondFrameRight, text="Добавить ответ ассистента", font=("Arial", 15))
    SetRespondLabelRight.pack(side=LEFT, pady=5)
    RespondWarningLeft = ttk.Label(RespondFrameLeft, text='заполните это поле', foreground='#ff0000')
    RespondWarningRight = ttk.Label(RespondFrameRight, text='заполните это поле', foreground='#ff0000')
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

#creates dynamic state for one time
def create_dynamic_state(state):
    global command_list, command_vars
    frame = Frame(window)
    #all commands table
    if state == 'show_commands':

        columns = ("name", "v1", "v2", "v3", "v4", "v5", "r1")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        tree.grid(row=0, column=0, sticky='nsew')

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

    #voice command changing form
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
    #assistant respond change form
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
    #apps and webs deleting form
    elif state == "show_apps_and_webs":
        global apps_listbox, webs_listbox
        AppLabel = ttk.Label(frame, text="Добавленные приложения", font=('Arial', 18))
        AppLabel.pack(anchor=NW, pady=5)
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(anchor=N, fill=X, expand=True)
        apps_listbox = Listbox(inner_frame, selectmode=SINGLE, height=10)
        apps_listbox.pack(side=LEFT, fill=X, anchor=N, expand=True)

        apps_scrollbar = Scrollbar(inner_frame, orient=VERTICAL, command=apps_listbox.yview)
        apps_scrollbar.pack(side=RIGHT, fill=Y)
        apps_listbox.config(yscrollcommand=apps_scrollbar.set)

        WebLabel = ttk.Label(frame, text="Добавленные вебсайты", font=('Arial', 18))
        WebLabel.pack(anchor=NW, pady=5)
        inner_frame2 = ttk.Frame(frame)
        inner_frame2.pack(anchor=N, fill=X, expand=True)
        webs_listbox = Listbox(inner_frame2, selectmode=SINGLE, height=10)
        webs_listbox.pack(side=LEFT, fill=X,anchor=N, expand=True)

        webs_scrollbar = Scrollbar(inner_frame2, orient=VERTICAL, command=webs_listbox.yview)
        webs_scrollbar.pack(side=RIGHT, fill=Y)
        webs_listbox.config(yscrollcommand=webs_scrollbar.set)

        populate_listboxes()
        delete_button = Button(frame, text="Delete", command=delete_item)
        delete_button.pack(side=LEFT, pady=5)
    frames[state] = frame

#sets state depending on button
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
    window.protocol("WM_DELETE_WINDOW", lambda: close_app(window))
    simulate_loading()
    window.geometry('1000x550')

    #main menu for changing states
    menu_bar = Menu(window)
    window.config(menu=menu_bar)
    settings_exit = Menu(menu_bar, tearoff=0)
    commands_settings = Menu(menu_bar, tearoff=0)
    apps_and_webs = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label='Меню', menu=settings_exit)
    settings_exit.add_command(label="Главная", command=lambda: set_state('home'))
    settings_exit.add_command(label="Настройки", command=lambda: set_state('settings'))
    settings_exit.add_command(label="Помощь", command=lambda: set_state('help'))
    settings_exit.add_command(label="Выход", command=lambda: close_app(window))
    menu_bar.add_cascade(label='Команды', menu=commands_settings)
    commands_settings.add_command(label="Список команд", command=lambda: set_state('show_commands'))
    commands_settings.add_command(label="Изменить голосовые команды", command=lambda: set_state('change_voice_commands'))
    commands_settings.add_command(label="Изменить реакцию ассистента", command=lambda: set_state('change_assistant_respond'))
    menu_bar.add_cascade(label='Приложения и сайты', menu=apps_and_webs)
    apps_and_webs.add_command(label="Добавленные приложения и вебсайты", command=lambda: set_state('show_apps_and_webs'))
    apps_and_webs.add_command(label="Добавить приложение", command=lambda: set_state('add_app'))
    apps_and_webs.add_command(label="Добавить вебсайт", command=lambda: set_state('add_website'))

    frames = {}
    create_states()
    set_state('home')

    window.mainloop()