import speech_recognition as spr
import os
import importlib
import json
from fuzzywuzzy import fuzz

# Gets all commands
with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)

# Get a list of all files in the folder
module_files = [f for f in os.listdir('commands') if f.endswith('.py')]
# Import each module
for module_file in module_files:
    module = importlib.import_module(f"commands.{module_file[:-3]}")
    globals()[module_file[:-3]] = module  # Make the module available in the global namespace

# init of recognizer
sr = spr.Recognizer()
sr.pause_threshold = 0.5

# using Levenshtein algorithm
def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in command_list.items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc

#listens commands
def listen_command():
    with spr.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(mic)
        command = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()[14:-3]
        command = recognize_cmd(command)
        if command['cmd'] in command_list:
            globals()[command['cmd']].command()

#cycle
while True:
    listen_command()