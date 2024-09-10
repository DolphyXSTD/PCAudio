import json

import commands.open_app as open_app
import commands.open_website as open_website
import modules


with open("websites.json", "r", encoding='utf-8') as file:
    websites = json.load(file)
with open("apps.json", "r", encoding='utf-8') as file:
    apps = json.load(file)

def command(cmd):
    website = modules.recognize_cmd(cmd, websites)
    if website['cmd'] in websites:
        open_website.command(website['cmd'])
    app = modules.recognize_cmd(cmd, apps)
    if app['cmd'] in apps:
        open_app.command(app['cmd'])