import time

def idle_thread_loop(parent, info_callback):
    import time

    tasks = {
        "update_resources": {
            "func": update_resources,
            "args": [parent, info_callback],
            "interval": 1,
            "last_run": 0
        },
        "save_game": {
            "func": parent.resources.save,
            "args": [],
            "interval": 30,
            "last_run": 0
        }
    }

    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed = current_time - start_time

        for task in tasks.values():
            if elapsed - task["last_run"] >= task["interval"]:
                task["func"](*task["args"])
                task["last_run"] = elapsed

        if parent.game_closed:
            return

        time.sleep(1)

def update_resources(parent, info_callback):
    for resource_name in parent.resources.data['resources']:
        rate = parent.resources.data['resource_rates'].get(resource_name, 0)
        if rate != 0:
            parent.resources.data['resources'][resource_name] += rate
            resource_quantity = parent.resources.data['resources'][resource_name]

            info_callback.emit(['update-resource', resource_name, resource_quantity, rate])