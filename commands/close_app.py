import psutil
import json
import tts_module
from start_config import command_list_dir

def command(app):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app:
            try:
                tts_module.speak(command_list['close_app'][app]['assistant'])
                proc.terminate()
            except:
                pass
