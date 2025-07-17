def upgrade_pressed_button(button, cost_dict, parent):
    # Extract the upgrade ID from the button's object name
    upgrade_id = button.objectName().replace('_button', '')
    
    if can_afford(parent.resources.user_data['resources'], cost_dict):
        # print("CAN AFFORD")
        
        button.setText("Upgraded")
    else:
        # print("CANNOT")
        button.setText("Insufficient Resources")

def can_afford(resources, cost_dict):
    for resource, amount in cost_dict.items():
        if resources.get(resource, 0) < amount:
            return False
    return True

def transaction(parent, build_cost):
    resources = parent.resources.user_data['resources']
    insufficient_resources = []

    # Check which resources are insufficient
    for resource_required, amount_required in build_cost.items():
        if resources.get(resource_required, 0) < amount_required:
            print(f'not enough {resource_required}')
            insufficient_resources.append(resource_required)

    # Emit callbacks for all insufficient resources and exit early
    if insufficient_resources:
        for res in insufficient_resources:
            parent.info_callback(['not-enough-of-resource', res])
        return False

    # If we reach here, we have enough of all resources – subtract the cost
    for resource_required, amount_required in build_cost.items():
        resources[resource_required] -= amount_required
        return True