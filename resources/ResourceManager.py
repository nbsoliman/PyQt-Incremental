import json, os, sys

class ResourceManager:
    def __init__(self):
        self.data = ''
        self.colors = {
            "bg": "#272727",
            "light-text": "#c4c4c4",
            "red": "#f7918a",
            "orange": "#f7c28a",
            "orellow": "#f7d68a",
            "yellow": "#f6f78a",
            "green": "#8af7b4",
            "blue": "#8AB4F7",
            "purple": "#c58af7",
            "pink": "#f78af1",
        }

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create(self):
        data = {
            "resources": {
                "people": 1,
                "gold": 100,
                "wood": 0,
                "stone": 0
            },
            "workers": {
                "builders": {
                    "1": 0
                },
                "lumbermen": {
                    "1": 0
                },
                "miners": {
                    "1": 0
                },
                "merchants": {
                    "1": 0
                },
                "military": {
                    "1": 0
                }
            },
            "buildings": {
                "Town Hall": {
                    "level": 1,
                    "internal_upgrade_1": 0,
                    "location" : {
                        "x" : 0,
                        "y" : 0
                    },
                    "icon": 'assets/icons/town-hall.svg'
                },
                "Miner": {
                    "level": 1,
                    "internal_upgrade_1": 0,
                    "location": {
                        "x": 1,
                        "y": 1
                    },
                    "icon": 'assets/icons/coin.svg'
                },
                "Lumberjack": {
                    "level": 1,
                    "internal_upgrade_1": 0,
                    "location": {
                        "x": 0,
                        "y": 1
                    },
                    "icon": 'assets/icons/town-hall.svg'
                }
            }
        }

        self.data = data

        with open(self.resource_path('data.json'), 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        with open(self.resource_path('data.json'), 'r') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.resource_path('data.json'), 'w') as f:
            json.dump(self.data, f, indent=2)