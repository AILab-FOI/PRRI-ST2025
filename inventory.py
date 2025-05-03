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
    
    def get_item(self, item_name):
        for i in self.items:
            if i.name == item_name:
                return i
        return None
    
    def contains_item(self, item_name):
        for i in self.items:
            if i.name == item_name:
                return True
        return False
    
    def contains_items(self, items):
        required_counts = {}
        for item_name in items:
            if item_name in required_counts:
                required_counts[item_name] += 1
            else:
                required_counts[item_name] = 1

        inventory_counts = {}
        for item in self.items:
            if item.name in inventory_counts:
                inventory_counts[item.name] += 1
            else:
                inventory_counts[item.name] = 1

        for item_name, count in required_counts.items():
            if inventory_counts.get(item_name, 0) < count:
                return False

        return True

class InventoryItem:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon