import os
import tts_module
def command(arg):
    if arg == "turn_off":
        tts_module.speak('выключение')
        os.system("shutdown /s /t 1")
    elif arg == "restart_pc":
        tts_module.speak('перезагрузка')
        os.system("shutdown /r /t 1")
    elif arg == "sleep_mode":
        tts_module.speak('спящий режим')
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")