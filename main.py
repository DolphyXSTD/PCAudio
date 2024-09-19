import importlib
import json
import os
import queue
import time
import threading

from start_config import *
on_load()

import sounddevice as sd
import vosk

import modules
import interface

#interface thread
interface_thread = threading.Thread(target=interface.main, args=())
interface_thread.start()

import tts_module

#tts model init
model = vosk.Model(find_path("stt_model"))
sample_rate = 16000
device = 1
q = queue.Queue()
rec = vosk.KaldiRecognizer(model, sample_rate)
modules.load_models += 1

isWorking = False
start_work = 0
work_time = 15
#load data
with open(modules.find_path("numbers.json"), "r", encoding='utf-8') as file:
    number_list = json.load(file)
module_files = [f for f in os.listdir(find_path('commands')) if f.endswith('.py')]
for module_file in module_files:
    module = importlib.import_module(f"commands.{module_file[:-3]}")
    globals()[module_file[:-3]] = module  # Make the module available in the global namespace


#queue adding text
def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

#records voice
def listen(rec, callback):
    global loading_models
    with sd.RawInputStream(samplerate=sample_rate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"], True)
            else:
                callback(json.loads(rec.PartialResult())["partial"], False)
            if interface.closed:
                sys.exit(0)

#listens commands
def listen_command(raw_voice, fullCommand):
    toggle = interface.ToggleBot.get()
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    global start_work, work_time, isWorking
    if start_work > 0:
        if time.time() > start_work + work_time:
            isWorking = False
    voice = raw_voice
    voice = voice.split()
    for t, n in number_list.items():
        if t in voice:
            voice.remove(t)
    voice = "".join(voice)
    command = modules.levenshtein(voice, command_list)
    if toggle:
        if isWorking and fullCommand:
            try:
                if command['cmd'] in command_list and command['cmd'] != 'start':
                    if command['arg'] != '':
                        globals()[command['cmd']].command(command['arg'])
                    else:
                        globals()[command['cmd']].command(raw_voice)
            except Exception as e:
                with open(f"{home_dir}/AppData/Roaming/{app_name}/error_log.txt", "a") as f:
                    f.write(f"{e}\n")
        if not fullCommand and command['cmd'] == "start":
            start_work = time.time()
            isWorking = True

listening_thread = threading.Thread(target=listen, args=(rec, listen_command))
listening_thread.start()