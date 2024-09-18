import wmi
import modules
import tts_module
import json
from start_config import command_list_dir

with open(modules.find_path('numbers.json'), "r", encoding='utf-8') as file:
    number_list = json.load(file)

def command(voice):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    numbers, level = modules.get_number(voice)
    text = modules.create_text_of_nums(number_list, numbers)

    if level != "None":
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        tts_module.speak(command_list['set_brightness']["assistant"] + text)
