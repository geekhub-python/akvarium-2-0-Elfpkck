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


def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Aquarium:
    def __init__(self):
        self.aquarium = []

    def get_inhabitant(self, inhabitants):
        for inhabitant in inhabitants:
            self.aquarium.append(inhabitant)


if __name__ == '__main__':
    aquarium = Aquarium()
    alga = Alga(5)
    snail = Snail(15)
    predator = Predator(13)
    fish = Fish(100)
    aquarium.get_inhabitant([fish, snail, predator, alga])
    print(aquarium.aquarium)

    print(fish.weight)
    fish.eating(aquarium.aquarium, alga)
    print(fish.weight)
    fish.eating(aquarium.aquarium, snail)
    print(fish.weight)
    print(aquarium.aquarium)
    print(predator.weight)
    fish.eating(aquarium.aquarium, predator)
    print(aquarium.aquarium)
    print(predator.weight)