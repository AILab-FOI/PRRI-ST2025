from inventory import Inventory, InventoryItem
import json

class MockInventoryData:
    def __init__(self, entity_name):
        self.inventory = Inventory()
        with open("./mockData/mockInventoryData.json", 'r') as file:
            data = json.load(file)

            for entity in data['entities']:
                if entity['entityName'] == entity_name:
                    for item in entity['inventory']:
                        inventory_item = InventoryItem(item['itemName'], item['imgPath'])
                        self.inventory.add_item(inventory_item)