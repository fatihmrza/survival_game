"""
This module defines creature types used in a survival simulation game.
Creatures interact with plants, other creatures, seasons, disasters,
and starvation mechanics.
"""
__author__ = "8500551 Mirza, 8811983 Bekker"
import random


class Creature:
    """
    Base class for all creatures in the simulation.
    """
    def __init__(self, size):
        """
        Initialize a creature with a given size.
        """
        self.habitat = None
        self.size = size
        self.is_alive = True
        self.hungry_days = 0

    def eaten(self, quantity):
        """
        Reduce creature size when eaten.



        >>> c = Creature(5)
        >>> c.eaten(2)
        >>> c.size
        3
        >>> c.is_alive
        True
        """
        self.size -= quantity
        if self.size <= 0:
            self.is_alive = False
            print(f"The {self.__class__.__name__} are dead")

    def eat(self):
        """
        Perform eating behavior.
        """
        pass

    def disaster_effect(self):
        """
       Apply disaster damage if a disaster occurs in the habitat.



       >>> class H: disaster_probability = False
       >>> c = Creature(5)
       >>> c.habitat = H()
       >>> c.disaster_effect()
       False
       """
        if self.habitat.disaster_probability:
            if self.size >= 3:
                quantity = 3
            else:
                # if there are fewer creatures than disaster outcome.
                quantity = self.size
            self.size -= quantity
            if self.size <= 0:
                self.is_alive = False
                print(f"{self.__class__.__name__} are due to disaster all dead.")
                return
            print(f"{quantity} {self.__class__.__name__} are due to disaster dead ")
        else:
            return False

    def starvation_check(self):
        """
       Kill the creature if starvation limit is exceeded.



       >>> c = Creature(4)
       >>> c.hungry_days = 3
       >>> c.starvation_check()
       >>> c.is_alive
       False
        """
        if self.__class__.__name__ == "Herbivore" and self.hungry_days >= 2:
            self.is_alive = False
            print(f"{self.__class__.__name__} are dead of starvation.")
        if self.hungry_days >= 3:
            self.is_alive = False
            print(f"{self.__class__.__name__} are dead of starvation.")


class Herbivore(Creature):
    """
    A creature that eats plants only.
    """
    def eat(self):
        """
        Attempt to eat a plant from the habitat.



        >>> h = Herbivore(5)
        >>> h.habitat = type("H", (), {"plants": []})()
        >>> h.eat() is None
        True
        """
        if not self.is_alive:
            return

        if not self.habitat.plants:
            return

        plant = random.choice(self.habitat.plants)
        if plant.size > 6:
            # if the regarding plant number is more than 6, %20 less chance.
            hunter_chance = 0.45
        else:
            hunter_chance = 0.65
        if random.random() <= hunter_chance:
            plant.eaten(self.habitat.game_speed)
            self.hungry_days = 0
        else:
            self.hungry_days += 1

    def eaten(self, quantity):
        return


class Omnivore(Creature):
    """
    A creature that eats both plants and animals.
    """
    def eat(self):
        """
        Perform eating behavior unless it is winter.



        >>> o = Omnivore(5)
        >>> o.habitat = type("H", (), {"season": "Winter"})()
        >>> o.eat() is None
        True
        """
        if not self.is_alive:
            return

        if self.habitat.season == "Winter":
            return

        choice = random.choice(["plant", "animal"])

        if choice == "plant":
            if not self.habitat.plants:
                return

            plant = random.choice(self.habitat.plants)
            if plant.size > 6:
                hunter_chance = 0.4
            else:
                hunter_chance = 0.6
            if random.random() <= hunter_chance:
                plant.eaten(self.habitat.game_speed)
                self.hungry_days = 0
            else:
                self.hungry_days += 1
            return
        # The list of the rest creatures without own species.
        prey = [
            c for c in self.habitat.creatures
            if c is not self and c.is_alive
        ]

        if not prey:
            self.hungry_days += 1
            return

        creat = random.choice(prey)
        if random.random() < 0.6:
            creat.eaten(self.habitat.game_speed)
            self.hungry_days = 0
        else:
            self.hungry_days += 1

    def eaten(self, quantity):
        """
        Apply damage when eaten by carnivores.


        >>> o = Omnivore(5)
        >>> o.habitat = type("H", (), {"used_capacity": 10})()
        >>> o.eaten(2)
        >>> o.size
        3
        """
        super().eaten(quantity)
        print(f"The {quantity} of Omnivores are eaten from Carnivores")
        self.habitat.used_capacity -= quantity


class Carnivore(Creature):
    """
    A creature that hunts other creatures.
    """
    def eat(self):
        """
       Attempt to hunt prey unless it is winter.


       >>> a = Carnivore(5)
       >>> a.habitat = type("H", (), {"season": "Winter"})()
       >>> a.eat() is None
       True
       """
        if not self.is_alive:
            return

        if self.habitat.season == "Winter":
            return

        prey = [
            c for c in self.habitat.creatures
            if c is not self and not isinstance(c, Carnivore) and c.is_alive
        ]

        if not prey:
            self.hungry_days += 1
            return

        creat = random.choice(prey)

        # Jagderfolg
        if random.random() < 0.6:
            creat.eaten(self.habitat.game_speed)
            self.hungry_days = 0
        else:
            self.hungry_days += 1

    def eaten(self, quantity):
        """
        Apply damage when eaten by omnivores.


        >>> c = Carnivore(6)
        >>> c.habitat = type("H", (), {"used_capacity": 10})()
        >>> c.eaten(3)
        >>> c.size
        3
        """
        super().eaten(quantity)
        print(f"The {quantity} of Carnivores are eaten from Omnivores")
        self.habitat.used_capacity -= quantity
