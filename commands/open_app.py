import subprocess
import json
import tts_module
from start_config import command_list_dir

def command(app):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    subprocess.Popen(app)
    tts_module.speak(command_list['open_app'][app]["assistant"])