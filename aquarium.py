#!/usr/bin/env python3

import functools
import random

MIN_FISH_WEIGHT = 1
MAX_FISH_WEIGHT = 9
MIN_SNAIL_WEIGHT = 1
MAX_SNAIL_WEIGHT = 5
MIN_ALGA_WEIGHT = 1
MAX_ALGA_WEIGHT = 3
PREDATOR_WEIGHT = 10
MIN_INHABITANTS = 20
MAX_INHABITANTS = 100


def possible_food(food_type):
    def decorator_factory(f):
        @functools.wraps(f)
        def wrapper(self, aquarium, food):
            if food_type == food.type:
                return f(self, aquarium, food)
            if self.type == 'fish' and food.type == 'predator':
                food.eating(aquarium, self)
        return wrapper
    return decorator_factory


def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


class Inhabitant:
    def __init__(self, type, weight):
        self.type = type
        self.weight = weight

    def eating(self, aquarium, food):
        self.weight += food.weight
        aquarium.remove(food)


class Fish(Inhabitant):
    def __init__(self, weight):
        super().__init__('fish', weight)

    @possible_food('alga')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Predator(Inhabitant):
    def __init__(self, weight):
        super().__init__('predator', weight)

    @possible_food('fish')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Snail(Inhabitant):
    def __init__(self, weight):
        super().__init__("snail", weight)

    @possible_food('alga')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Alga(Inhabitant):
    def __init__(self, weight):
        super().__init__('alga', weight)


@singleton
class Aquarium:
    def __init__(self):
        self.aquarium = []

    def get_inhabitants(self, inhabitants):
        for inhabitant in inhabitants:
            self.aquarium.append(inhabitant)

    def give_random_except_self(self, current):
        while True:
            inhabitant = random.choice(self.aquarium)
            if inhabitant is not current:
                break
        return inhabitant

    def start(self):
        while any(type(x).__name__ in ["Fish", "Alga"] for x in self.aquarium):
            for inhabitant in self.aquarium:
                food = self.give_random_except_self(inhabitant)
                inhabitant.eating(self.aquarium, food)

    def result(self):
        print(self.aquarium)
        self.aquarium.sort(key=lambda x: -x.weight)
        print(self.aquarium)
        for item in self.aquarium:
            print(item.weight)


if __name__ == '__main__':
    aquarium = Aquarium()
    fishes = [Fish(random.randrange(MIN_FISH_WEIGHT, MAX_FISH_WEIGHT + 1)) for i in range(random.randrange(1, 20))]
    predators = [Predator(PREDATOR_WEIGHT) for i in range(random.randrange(1, 20))]
    seaweed = [Alga(random.randrange(MIN_ALGA_WEIGHT, MAX_ALGA_WEIGHT + 1)) for i in range(random.randrange(1, 10))]
    snails = [Snail(random.randrange(MIN_SNAIL_WEIGHT, MAX_SNAIL_WEIGHT + 1)) for i in range(random.randrange(1, 20))]
    aquarium.get_inhabitants(fishes)
    aquarium.get_inhabitants(predators)
    aquarium.get_inhabitants(seaweed)
    aquarium.get_inhabitants(snails)
    aquarium.start()
    aquarium.result()