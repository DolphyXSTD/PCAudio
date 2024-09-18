import os
import tts_module
from start_config import command_list_dir
import json

def command(arg):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)

    tts_module.speak(command_list['system_manager'][arg]["assistant"])
    if arg == "turn_off":
        os.system("shutdown /s /t 1")
    elif arg == "restart_pc":
        os.system("shutdown /r /t 1")
    elif arg == "sleep_mode":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")