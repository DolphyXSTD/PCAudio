import speech_recognition as spr
import os
import importlib
import json
import time

import modules

isWorking = False
# Gets all commands
with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)
    interface_cmd_list = command_list
    del command_list['start']
    print(command_list)
with open("numbers.json", "r", encoding='utf-8') as file:
    number_list = json.load(file)
# Get a list of all files in the folder
module_files = [f for f in os.listdir('commands') if f.endswith('.py')]
# Import each module
for module_file in module_files:
    module = importlib.import_module(f"commands.{module_file[:-3]}")
    globals()[module_file[:-3]] = module  # Make the module available in the global namespace

# init of recognizer
sr = spr.Recognizer()
sr.non_speaking_duration = 0.05
sr.pause_threshold = 0.05

start_work = 0
work_time = 5
#listens commands
def listen_command():
    global start_work, work_time, isWorking
    if start_work > 0:
        if time.time() > start_work + work_time:
            isWorking = False
            sr.non_speaking_duration = 0.02
            sr.pause_threshold = 0.02
            print('turn_off')
    with spr.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=1)
        audio = sr.listen(mic)
        raw_voice = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()[14:-3]
        print(raw_voice)
        voice = raw_voice
        voice = voice.split()
        for t, n in number_list.items():
            if t in voice:
                voice.remove(t)
        voice = "".join(voice)
        command = modules.levenshtein(voice, command_list)
        print(command)
        if isWorking:
            if command['cmd'] in command_list:
                if command['arg'] != '':
                    globals()[command['cmd']].command(command['arg'])
                else:
                    globals()[command['cmd']].command(raw_voice)
        if command['cmd'] == "start":
            start_work = time.time()
            isWorking = True
            sr.non_speaking_duration = 0.5
            sr.pause_threshold = 0.5
            print('turn_on')

#cycle
while True:
    listen_command()