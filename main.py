import asyncio
import json
import random
from aquarium import aquarium
from inhabitants import Fish, Predator, Alga, Snail

with open("config.json") as f:
    config = json.load(f)

MIN_FISH_WEIGHT = config["MIN_FISH_WEIGHT"]
MAX_FISH_WEIGHT = config["MAX_FISH_WEIGHT"]
MIN_SNAIL_WEIGHT = config["MIN_SNAIL_WEIGHT"]
MAX_SNAIL_WEIGHT = config["MAX_SNAIL_WEIGHT"]
MIN_ALGA_WEIGHT = config["MIN_ALGA_WEIGHT"]
MAX_ALGA_WEIGHT = config["MAX_ALGA_WEIGHT"]
PREDATOR_WEIGHT = config["PREDATOR_WEIGHT"]
MIN_INHABITANTS = config["MIN_INHABITANTS"]


def inhabitants_generator():
    fishes = [Fish(random.randrange(MIN_FISH_WEIGHT, MAX_FISH_WEIGHT + 1))
              for i in range(random.randrange(1, 25))]
    predators = [Predator(PREDATOR_WEIGHT)
                 for i in range(random.randrange(1, 25))]
    seaweed = [Alga(random.randrange(MIN_ALGA_WEIGHT, MAX_ALGA_WEIGHT + 1))
               for i in range(random.randrange(1, 25))]
    snails = [Snail(random.randrange(MIN_SNAIL_WEIGHT, MAX_SNAIL_WEIGHT + 1))
              for i in range(random.randrange(1, 25))]
    if sum(map(len, [fishes, predators, seaweed, snails])) < MIN_INHABITANTS:
        return inhabitants_generator()
    return fishes, predators, seaweed, snails

if __name__ == '__main__':
    for inhabitants in inhabitants_generator():
        aquarium.get_inhabitants(inhabitants)
    loop = asyncio.get_event_loop()
    tasks = [
        aquarium.start(),
        aquarium.start2()]
    loop.run_until_complete(asyncio.wait(tasks))
    aquarium.result()