import os
import json
from pathlib import Path
from pathfinder import find_path
import shutil

app_name = "PCAudio"
home_dir = Path.home()
command_list_dir = home_dir / "AppData" / "Roaming" / app_name / "command_list.json"
user_prefs_dir = home_dir / "AppData" / "Roaming" / app_name / "user_prefs.json"
def on_load():
    # Get the current user's home directory
    global home_dir

    # Construct the path to the AppData\Roaming directory
    appdata_dir = home_dir / "AppData" / "Roaming" / app_name

    # Check if the directory exists, if not, create it
    if not appdata_dir.exists():
        appdata_dir.mkdir(parents=True, exist_ok=True)

        start_command_list_path = find_path("command_list.json")
        start_user_prefs_path = find_path("user_prefs.json")
        command_list_path = appdata_dir / "command_list.json"
        user_prefs_path = appdata_dir / "user_prefs.json"

        shutil.copyfile(start_command_list_path, command_list_path)
        shutil.copyfile(start_user_prefs_path, user_prefs_path)





