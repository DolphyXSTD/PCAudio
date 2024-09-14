import wmi
import modules
import tts_module
import json

with open("numbers.json", "r", encoding='utf-8') as file:
    number_list = json.load(file)

def command(voice):
    numbers, level = modules.get_number(voice)
    text = modules.create_text_of_nums(number_list, numbers)
    if level != "None":
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)
        tts_module.speak(f'команда выполнена: яркость установлена на {text}')
