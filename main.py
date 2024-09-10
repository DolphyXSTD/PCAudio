import speech_recognition as spr
import os
import importlib
import json

with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)

# Get a list of all Python files in the folder
module_files = [f for f in os.listdir('commands') if f.endswith('.py') and f != '__init__.py']
# Import each module
for module_file in module_files:
    module = importlib.import_module(f"commands.{module_file[:-3]}")
    globals()[module_file[:-3]] = module  # Make the module available in the global namespace

sr = spr.Recognizer()
sr.pause_threshold = 0.5

def listen_command():
    with spr.Microphone() as mic:
        sr.adjust_for_ambient_noise(source=mic, duration=0.5)
        audio = sr.listen(mic)
        query = sr.recognize_vosk(audio_data=audio, language="ru-RU").lower()
        for k, v in command_list.items():
            if query[14:-3] in v:
                globals()[k].command()
    print(query)

while True:
    listen_command()