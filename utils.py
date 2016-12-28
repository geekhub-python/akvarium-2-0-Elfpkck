import functools


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


class TooBigAquarium(Exception):
    """Raised when aquarium is too big"""
    pass