import wmi
import modules

def command(voice):
    level = modules.get_number(voice)
    if level != "None":
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(level, 0)