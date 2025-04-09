import json
from inventory import Inventory, InventoryItem

file_path = "./data/inventoryData.json"
inventories = []

def load_inventories(file_path):
    global inventories
    with open(file_path, 'r') as file:
        data = json.load(file)
        inventories = [
            Inventory(
                entity_name=entity['entityName'],
                items=[
                    InventoryItem(
                        name=item['itemName'],
                        icon=item['imgPath'],
                    ) for item in entity['inventory']
                ]
            ) for entity in data['entities']
        ]

def get_inventory_by_entity_name(entity_name):
    for inventory in inventories:
        if inventory.entity_name == entity_name:
            return inventory
        
def switch_items_from_inventories(entity_name_1, entity_name_2, item_name):
    inventory_1 = get_inventory_by_entity_name(entity_name_1)
    inventory_2 = get_inventory_by_entity_name(entity_name_2)

    item_to_switch = None

    for item in inventory_1.get_items():
        if item.name == item_name:
            item_to_switch = item
            break

    if item_to_switch:
        inventory_1.remove_item(item_to_switch)
        inventory_2.add_item(item_to_switch)