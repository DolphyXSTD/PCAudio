from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import json
import tts_module
import modules
from start_config import command_list_dir

with open(modules.find_path('numbers.json'), "r", encoding='utf-8') as file:
    number_list = json.load(file)

def command(voice):
    numbers, level = modules.get_number(voice)
    text = modules.create_text_of_nums(number_list, numbers)
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)

    if level != "None":
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level/100, None)
        tts_module.speak(command_list['set_volume']["assistant"] + text)