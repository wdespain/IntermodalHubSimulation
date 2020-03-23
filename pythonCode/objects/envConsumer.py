#This is the abstract class that all consumers in this environment should inherit from
class EnvConsumer:

    def __init__(self, i, e):
        #Things that will not change once set
        self.ID = i

        #This that the larger program may signal to change
        self.energyUsePerSec = .4 #in kWh

    def step(self):
        raise NotImplementedError

    def energyUseForStep(self):
        raise NotImplementedError

    def textOutput(self):
        raise NotImplementedError