import json, os, sys
import numpy as np

class ResourceManager:
    def __init__(self):
        self.user_data = ''
        with open(self.resource_path('game_data.json'), 'r') as f:
            self.game_data = json.load(f)

        self.planet_size = 11 # 11x11 grid, should be an odd number

        self.colors = {
            "near-black": "#161616",
            "dark-bg": "#1e1e1e",
            "bg": "#232427",
            "old-bg": "#272727",
            "blue-bg": '#202124',
            "selected-filter": "#000000FF",

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
        self.user_data = {
            "resources": {
                "people": 1,
                "gold": 10,
                "carbon": 0,   # Essential building block for constructing basic structures and creating more advanced materials.
                "aluminum": 0, # Lightweight metal, great for constructing frames and structural components.
                "silicon": 0,  # Necessary for creating electronics, solar panels, and glass.
                "iron": 0,      # Strong metal used for heavy construction and tools.
                "hydrogen": 0,  # Fuel for power generation and advanced chemical processes
                "copper": 0,    # Conductive metal essential for electrical systems.
                "titanium": 0,  # Strong and lightweight metal for advanced structures and vehicles..
                "lithium": 0,   # Key for energy storage solutions such as batteries.
                "oxygen": 0,    # Vital for human survival and certain chemical reactions.
            },
            "resource_rates": {
                "people": 0,
                "gold": 0,
                "carbon": 0,
                "aluminum": 0,
                "silicon": 0,
                "iron": 0,
                "hydrogen": 0,
                "copper": 0,
                "titanium": 0,
                "lithium": 0,
                "oxygen": 0
            },
            "workers": {
                "civilian": {
                    "1": 1
                },
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
                "1": {
                    "name": "Base",
                    "level": 1,
                    "search_count": 5,
                    "hidden_objects": 8,
                    "min_asteroid_value": 5,
                    "max_asteroid_value": 10,
                    "highscore": 0,
                    "internal_upgrades": {
                        "1": 1,
                        "2": 1,
                        "3": 1,
                        "4": 1,
                        "5": 1,
                    },
                    "location": {
                        "x": int(self.planet_size/2),
                        "y": int(self.planet_size/2)
                    }
                }
            }
        }

        with open(self.resource_path('user_data.json'), 'w') as f:
            json.dump(self.user_data, f, indent=2)
        
        self.create_building_grid()

    def load(self):
        with open(self.resource_path('user_data.json'), 'r') as f:
            self.user_data = json.load(f)

        self.create_building_grid()

    def save(self):
        print("Saving Game..")
        with open(self.resource_path('user_data.json'), 'w') as f:
            json.dump(self.user_data, f, indent=2)

    def create_building_grid(self):
        self.building_grid = np.full((self.planet_size, self.planet_size), None, dtype=object)

        for building_id, building_info in self.user_data["buildings"].items():
            x = building_info["location"]["x"]
            y = building_info["location"]["y"]
            self.building_grid[x, y] = building_info

    def add_building(self, x, y, name):
        new_id = str(len(self.user_data["buildings"]) + 1)
        new_building = {
            "name": name,
            "level": 1,
            "internal_upgrade_1": 0,
            "icon": self.game_data['buildings'][name]['icon'],
            "location": {
                "x": x,
                "y": y
            }
        }

        self.user_data["buildings"][new_id] = new_building

        if hasattr(self, "building_grid"):
            self.building_grid[x, y] = new_building

        self.save()

    def calculate_resource_rate(self, resource_name):
        rate = 0
        for worker_type, workers in self.user_data['workers'].items():
            for level, count in workers.items():
                if count > 0:
                    rate += self.game_data['workers'][worker_type][level][resource_name] * count
        return rate