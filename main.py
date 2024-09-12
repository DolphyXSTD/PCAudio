import os
import importlib
import json
import time
import vosk
import sounddevice as sd
import queue

import modules

model = vosk.Model("model_big")
samplerate = 16000
device = 1
q = queue.Queue()


isWorking = False
start_work = 0
work_time = 15

# Gets all commands and jsons
with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)
    interface_cmd_list = command_list
    del command_list['start']
    print(command_list)
with open("numbers.json", "r", encoding='utf-8') as file:
    number_list = json.load(file)

module_files = [f for f in os.listdir('commands') if f.endswith('.py')]
for module_file in module_files:
    module = importlib.import_module(f"commands.{module_file[:-3]}")
    globals()[module_file[:-3]] = module  # Make the module available in the global namespace


#queue adding text
def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

#records voice
def listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"], True)
            else:
                callback(json.loads(rec.PartialResult())["partial"], False)

#listens commands
def listen_command(raw_voice, fullCommand):
    global start_work, work_time, isWorking
    if start_work > 0:
        if time.time() > start_work + work_time:
            isWorking = False
            print('turn_off')

    voice = raw_voice
    voice = voice.split()
    for t, n in number_list.items():
        if t in voice:
            voice.remove(t)
    voice = "".join(voice)
    command = modules.levenshtein(voice, command_list)
    print(command)
    if isWorking and fullCommand:
        if command['cmd'] in command_list:
            if command['arg'] != '':
                globals()[command['cmd']].command(command['arg'])
            else:
                globals()[command['cmd']].command(raw_voice)
    if not fullCommand and command['cmd'] == "start":
        start_work = time.time()
        isWorking = True
        print('turn_on')

listen(listen_command)
