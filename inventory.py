class Inventory:
    def __init__(self, entity_name, items):
        self.entity_name = entity_name
        self.items = items
        self.selected_item = None

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_items(self):
        return self.items

class InventoryItem:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon