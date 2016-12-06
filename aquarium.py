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
            if food_type == food.__class__.__name__:
                return f(self, aquarium, food)
            if (self.__class__.__name__ == 'Fish'
                    and food.__class__.__name__ == 'Predator'):
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
    def __init__(self, weight):
        self.weight = weight
        self.ate = 0

    def eating(self, aquarium, food):
        self.weight += food.weight
        self.ate += 1
        aquarium.remove(food)


class Fish(Inhabitant):
    def __init__(self, weight):
        super().__init__(weight)

    @possible_food('Alga')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Predator(Inhabitant):
    def __init__(self, weight):
        super().__init__(weight)

    @possible_food('Fish')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Snail(Inhabitant):
    def __init__(self, weight):
        super().__init__(weight)

    @possible_food('Alga')
    def eating(self, aquarium, food):
        return super().eating(aquarium, food)


class Alga(Inhabitant):
    def __init__(self, weight):
        super().__init__(weight)

    def eating(self, aquarium, food):
        pass


@singleton
class Aquarium:
    def __init__(self):
        self.aquarium = []

    def get_inhabitants(self, inhabitants):
        for inhabitant in inhabitants:
            self.aquarium.append(inhabitant)

    def give_random_except_current(self, current):
        inhabitant = random.choice(self.aquarium)
        while inhabitant is current:
            inhabitant = random.choice(self.aquarium)
        return inhabitant

    def start(self):
        while any(x.__class__.__name__ in ["Fish", "Alga"]
                  for x in self.aquarium):
            for inhabitant in self.aquarium:
                food = self.give_random_except_current(inhabitant)
                inhabitant.eating(self.aquarium, food)

    def result(self):
        self.aquarium.sort(key=lambda x: (x.__class__.__name__, -x.weight))
        for item in self.aquarium:
            name = item.__class__.__name__
            if name == "Predator":
                print('Хищник - масса:', item.weight, '| съел рыб:', item.ate)
            else:
                text = 'Улитка - масса: {} | съела водорослей: {}'
                print(text.format(item.weight, item.ate))


def inhabitants_generator():
    fishes = [Fish(random.randrange(MIN_FISH_WEIGHT, MAX_FISH_WEIGHT + 1))
              for i in range(random.randrange(1, 25))]
    predators = [Predator(PREDATOR_WEIGHT)
                 for i in range(random.randrange(1, 25))]
    seaweed = [Alga(random.randrange(MIN_ALGA_WEIGHT, MAX_ALGA_WEIGHT + 1))
               for i in range(random.randrange(1, 25))]
    snails = [Snail(random.randrange(MIN_SNAIL_WEIGHT, MAX_SNAIL_WEIGHT + 1))
              for i in range(random.randrange(1, 25))]
    if sum(map(len, [fishes, predators, seaweed, snails])) < 20:
        return inhabitants_generator()
    return fishes, predators, seaweed, snails


if __name__ == '__main__':
    aquarium = Aquarium()
    for inhabitants in inhabitants_generator():
        aquarium.get_inhabitants(inhabitants)
    aquarium.start()
    aquarium.result()
