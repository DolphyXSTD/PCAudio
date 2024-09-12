import speech_recognition as spr
import os
import importlib
import json

import modules

isWorking = True
# Gets all commands
with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)
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
sr.pause_threshold = 0.5

#listens commands
def listen_command():
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
        else:
            if command['cmd'] == "start":
                pass
#cycle
while True:
    listen_command()