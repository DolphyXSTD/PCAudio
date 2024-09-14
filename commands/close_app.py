import psutil
import json
import tts_module

with open("command_list.json", "r", encoding='utf-8') as file:
    command_list = json.load(file)
def command(app):
    name = command_list['close_app'][app][1]
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app:
            try:
                print(proc.info)
                proc.terminate()
                print(f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
                tts_module.speak(f'команда выполнена: {name}')
            except:
                pass
