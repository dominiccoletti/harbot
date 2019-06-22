from .base import Module
import csv
import random


class Fightyalebot(Module):
    DESCRIPTION = "Generate Elizabethan insults for our favorite chatbot"
    primary_adjectives = []
    secondary_adjectives = []
    nouns = []

    def response(self, query=None, message=None):
        if len(self.primary_adjectives) == 0:
            with open("resources/insults.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.primary_adjectives.append(row[0])
                    self.secondary_adjectives.append(row[1])
                    self.nouns.append(row[2])
        return "Yalebot, thou {primary_adjective}, {secondary_adjective} {noun}!".format(primary_adjective=random.choice(self.primary_adjectives),
                                                                                secondary_adjective=random.choice(self.secondary_adjectives),
                                                                                noun=random.choice(self.nouns))
