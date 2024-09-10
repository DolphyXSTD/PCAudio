import speech_recognition as spr
import os
import importlib
import json

import levenshtein

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

#listens commands
def listen_command():
    with spr.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(mic)
        voice = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()[14:-3]
        command = levenshtein.recognize_cmd(voice, command_list)
        if command['cmd'] in command_list:
            globals()[command['cmd']].command(voice)

#cycle
while True:
    listen_command()