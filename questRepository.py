from quest import Quest, Stage
import json

quests = []

json_file_path = './data/quests.json'

def load_quests_from_json(file_path=json_file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)

        for quest_data in data['quests']:
            stages = [Stage(stage['id'], stage['objective']) for stage in quest_data['stages']]

            quest = Quest(quest_data["id"], quest_data['name'], quest_data['description'], stages)
            quests.append(quest)

def get_quest_by_id(id):
    for quest in quests:
        if quest.id == id:
            return quest
    return None

def get_all_quests():
    print(quests)

    return quests

def get_active_quests():
    return [quest for quest in quests if quest.is_active]