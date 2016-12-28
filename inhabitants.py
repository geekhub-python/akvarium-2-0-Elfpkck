from utils import possible_food


class Inhabitant:
    def __init__(self, weight):
        self.weight = weight
        self.ate = 0

    def eating(self, aquarium, food):
        self.weight += food.weight
        self.ate += 1
        try:
            aquarium.remove(food)
        except ValueError:
            print("Нельзя съесть отсутствующий в аквариуме объект")


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
