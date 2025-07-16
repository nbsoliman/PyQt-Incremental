import time

class IdleThread:
    def __init__(self, parent):
        self.parent = parent
        self.start_time = time.time()

    def define_tasks(self, info_callback):
        self.tasks = {
            "update_resources": {
                "func": self.update_resources,
                "args": [info_callback],
                "interval": 1,
                "last_run": 0
            },
            "save_game": {
                "func": self.parent.resources.save,
                "args": [],
                "interval": 30,
                "last_run": 0
            }
        }

    def start_loop(self, info_callback):
        self.define_tasks(info_callback)
        while True:
            current_time = time.time()
            elapsed = current_time - self.start_time

            for task in self.tasks.values():
                if elapsed - task["last_run"] >= task["interval"]:
                    task["func"](*task["args"])
                    task["last_run"] = elapsed

            if self.parent.game_closed:
                return

            time.sleep(1)

    def update_resources(self, info_callback):
        for resource_name in self.parent.resources.user_data['resources']:
            rate = self.parent.resources.user_data['resource_rates'].get(resource_name, 0)
            if rate != 0:
                self.parent.resources.user_data['resources'][resource_name] += rate
                resource_quantity = self.parent.resources.user_data['resources'][resource_name]

                info_callback.emit(['update-resource', resource_name, resource_quantity, rate])