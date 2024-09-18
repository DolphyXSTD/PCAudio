import tts_module
from start_config import command_list_dir
import json

def command(voice):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    tts_module.speak(command_list["greeting"]["assistant"])