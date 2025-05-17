class Quest():
    def __init__(self, id, name, description, stages):
        self.id = id
        self.name = name
        self.description = description
        self.stages = stages
        self.is_completed = False
        self.is_active = False
        self.current_stage = -1

    def startQuest(self):
        self.is_active = True
        self.is_completed = False
        self.current_stage = 0
    
    def endQuest(self):
        self.is_active = False
        self.is_completed = True
        self.current_stage = -1


    def setStage(self, stage_id):
        self.current_stage = stage_id

        if stage_id >= len(self.stages):
            self.is_completed = True
            self.is_active = False

    def showCurrentObjective(self):
        return self.stages[self.current_stage].objective

class Stage():
    def __init__(self, id, objective):
        self.id = id
        self.objective = objective