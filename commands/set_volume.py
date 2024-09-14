from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import json
import tts_module
import modules

with open("numbers.json", "r", encoding='utf-8') as file:
    number_list = json.load(file)

def command(voice):
    numbers, level = modules.get_number(voice)
    text = modules.create_text_of_nums(number_list, numbers)
    if level != "None":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level/100, None)
        tts_module.speak(f'команда выполнена: яркость установлена на {text}')