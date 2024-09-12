import os

def command(arg):
    if arg == "turn_off":
        os.system("shutdown /s /t 1")
    elif arg == "restart_pc":
        os.system("shutdown /r /t 1")
    elif arg == "sleep_mode":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")