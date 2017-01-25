#!/usr/bin/env python3

import asyncio
import json
import os
import random
from utils import TooBigAquarium

this_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(this_dir, "config.json")) as f:
    config = json.load(f)

MAX_INHABITANTS = config["MAX_INHABITANTS"]


class Aquarium:
    def __init__(self):
        self.aquarium = []

    def get_inhabitants(self, inhabitants):
        for inhabitant in inhabitants:
            try:
                self.aquarium.append(inhabitant)
                if len(self.aquarium) > MAX_INHABITANTS:
                    raise TooBigAquarium
            except TooBigAquarium:
                print("Всё пропало! В аквариуме больше ста жителей")

    def give_random_except_current(self, current):
        inhabitant = random.choice(self.aquarium)
        while inhabitant is current:
            inhabitant = random.choice(self.aquarium)
        return inhabitant

    async def start(self):
        while any(x.__class__.__name__ in ["Fish", "Alga"]
                  for x in self.aquarium):
            for inhabitant in self.aquarium:
                food = self.give_random_except_current(inhabitant)
                inhabitant.eating(self.aquarium, food)
                await asyncio.sleep(0)

    async def start2(self):
        while any(x.__class__.__name__ in ["Fish", "Alga"]
                  for x in self.aquarium):
            for inhabitant in self.aquarium:
                food = self.give_random_except_current(inhabitant)
                inhabitant.eating(self.aquarium, food)
                await asyncio.sleep(0)

    def result(self):
        self.aquarium.sort(key=lambda x: (x.__class__.__name__, -x.weight))
        for item in self.aquarium:
            name = item.__class__.__name__
            if name == "Predator":
                try:
                    print('Хищник - масса:', item.weight,
                          '| съел рыб:', item.ate)
                except AttributeError as e:
                    print(item, e)
            else:
                text = 'Улитка - масса: {} | съела водорослей: {}'
                try:
                    print(text.format(item.weight, item.ate))
                except AttributeError:
                    print(item)

aquarium = Aquarium()