import json
from inventory import Inventory, InventoryItem

inventory_file_path = "./data/inventoryData.json"
item_file_path = "./data/itemData.json"
inventories = []
item_data = {}

def load_items(file_path):
    global item_data
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        item_data = {item['itemName']: item for item in data['items']}

def load_inventories(file_path):
    global inventories
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
        inventories = [
            Inventory(
                entity_name=entity['entityName'],
                items=[
                    InventoryItem(
                        name=item['itemName'],
                        icon=item_data[item['itemName']]['imgPath']
                    ) for item in entity['inventory']
                ]
            ) for entity in data['entities']
        ]

def get_inventory_by_entity_name(entity_name):
    for inventory in inventories:
        if inventory.entity_name == entity_name:
            return inventory
        
def switch_items_from_inventories(from_entity, to_entity, item_name):
    inventory_1 = get_inventory_by_entity_name(from_entity)
    inventory_2 = get_inventory_by_entity_name(to_entity)

    item_to_switch = None

    for item in inventory_1.get_items():
        if item.name == item_name:
            item_to_switch = item
            break

    if item_to_switch:
        inventory_1.remove_item(item_to_switch)
        inventory_2.add_item(item_to_switch)

def create_item(item_name):
    if item_name in item_data:
        item_info = item_data[item_name]
        return InventoryItem(name=item_info['itemName'], icon=item_info['imgPath'])
    else:
        raise ValueError(f"Item '{item_name}' not found in item data.")

load_items(item_file_path)
load_inventories(inventory_file_path)