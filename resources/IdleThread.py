import time

def idle_thread_loop(parent, info_callback):
    while True:
        time.sleep(1)  # tick every second

        update_resources(parent, info_callback)

        if parent.game_closed:
            return

def update_resources(parent, info_callback):
    for resource_name in parent.resources.data['resources']:
        rate = parent.resources.data['resource_rates'].get(resource_name, 0)
        if rate != 0:
            parent.resources.data['resources'][resource_name] += rate
            resource_quantity = parent.resources.data['resources'][resource_name]

            info_callback.emit(['update-resource', resource_name, resource_quantity, rate])