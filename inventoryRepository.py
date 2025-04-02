import json
from inventory import Inventory, InventoryItem

file_path = "./mockData/mockInventoryData.json"
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