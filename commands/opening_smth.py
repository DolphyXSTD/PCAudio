import json
from pathlib import Path

import commands.open_website as open_website
import levenshtein


with open("websites.json", "r", encoding='utf-8') as file:
    websites = json.load(file)
#with open("websites_and_apps/apps.json", "r", encoding='utf-8') as file:
#    apps = json.load(file)

def command(cmd):
    website = levenshtein.recognize_cmd(cmd, websites)
    if website['cmd'] in websites:
        open_website.command(website['cmd'])