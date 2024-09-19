import webbrowser
import json
import tts_module
from start_config import command_list_dir

def command(url):
    with open(command_list_dir, "r", encoding='utf-8') as file:
        command_list = json.load(file)
    try:
        webbrowser.open(url)
        tts_module.speak(command_list['open_website'][url]["assistant"])
    except:
        tts_module.speak("ссылка не найдена")
