import psutil
import json
import tts_module
from start_config import command_list_dir

with open(command_list_dir, "r", encoding='utf-8') as file:
    command_list = json.load(file)
def command(app):
    name = command_list['close_app'][app][1]
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app:
            try:
                tts_module.speak(f'команда выполнена: {name}')
                proc.terminate()
            except:
                pass
