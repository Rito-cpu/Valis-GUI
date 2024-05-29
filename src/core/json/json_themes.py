import json
import os

from .json_settings import Settings
from ..app_config import *

# APP THEMES
class Themes(object):
    # LOAD SETTINGS
    setup_settings = Settings()
    _settings = setup_settings.items

    # APP PATH
    json_file = f"src/gui/themes/{_settings['theme_name']}.json"
    settings_path = os.path.abspath(os.path.join(APP_ROOT, json_file))
    if not os.path.isfile(settings_path):
        print(f"WARNING: \"gui/themes/{_settings['theme_name']}.json\" not found! check in the folder {settings_path}")

    # INIT SETTINGS
    def __init__(self):
        super(Themes, self).__init__()

        # DICTIONARY WITH SETTINGS
        self.items = {}

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    def serialize(self):
        # WRITE JSON FILE
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    # DESERIALIZE JSON
    def deserialize(self):
        # READ JSON FILE
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings