"""
This module defines the Habitat class, which manages the environment of a
survival simulation game. It controls plants, creatures, seasons, disasters,
and game progression.
"""
__author__ = "8500551 Mirza, 8811983 Bekker"
import random
import time


class Habitat:
    """
        Represent a habitat where plants and creatures live and interact.

        The habitat tracks capacity usage, seasons, disasters, and
        manages simulation rounds.

        Doctests
        --------
        >>> h = Habitat(100, 2)
        >>> h.capacity == 100
        True
        >>> h.round == 0
        True
        >>> h.season == "Spring"
        True
        """
    def __init__(self, capacity, game_speed):
        """
        Initialize the habitat with capacity and game speed.

        Parameters:
        capacity : int
            Maximum allowed capacity of the habitat.
        game_speed : int
            Speed of the simulation.
        """
        # Habitat management
        self.capacity = capacity
        self.used_capacity = 0
        self.plants = []
        self.creatures = []
        self.season = "Spring"
        self.round = 0
        self.disaster_probability = False
        self.game_speed = game_speed

    def add_plants(self, plant):
        """
        Add a plant to the habitat if capacity allows.

        Doctests
        --------
        >>> class P: size = 10
        >>> h = Habitat(20, 1)
        >>> p = P()
        >>> h.add_plants(p)
        >>> h.used_capacity
        10
        """
        # Add plant if space allows
        if plant not in self.plants:
            if self.used_capacity + plant.size <= self.capacity:
                self.plants.append(plant)
                self.used_capacity += plant.size
                plant.habitat = self
                return
        print("The plant has been already added.")

    def remove_plants(self, plant):
        """
       Remove a plant from the habitat.

       Doctests
       --------
       >>> class P: size = 5
       >>> h = Habitat(20, 1)
       >>> p = P()
       >>> h.add_plants(p)
       >>> h.remove_plants(p)
       >>> h.used_capacity
       0
        """
        # remove the plant class if is dead
        if plant in self.plants:
            self.plants.remove(plant)
            self.used_capacity -= plant.size

    def add_creature(self, creature):
        """
        Add a creature to the habitat.

        Doctests
        --------
        >>> class C: size = 8
        >>> h = Habitat(20, 1)
        >>> c = C()
        >>> h.add_creature(c)
        >>> h.used_capacity
        8
        """
        if creature not in self.creatures:
            self.creatures.append(creature)
            creature.habitat = self
            self.used_capacity += creature.size
            return
        print("The creature has been added")

    def remove_creature(self, creature):
        """
        Remove a creature from the habitat.

        Doctests
        --------
        >>> class C: size = 6
        >>> h = Habitat(20, 1)
        >>> c = C()
        >>> h.add_creature(c)
        >>> h.remove_creature(c)
        >>> h.used_capacity
        0
        """
        # remove creature if is dead
        if creature in self.creatures:
            self.creatures.remove(creature)
            self.used_capacity -= creature.size

    def update_season(self):
        """
        Update the season based on the current round.

        Doctests
        --------
        >>> h = Habitat(10, 1)
        >>> h.round = 3
        >>> h.update_season()
        >>> h.season
        'Summer'
        """
        # Change season every 3 round.
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        season_index = (self.round // 3) % 4
        self.season = seasons[season_index]

    def get_season(self):
        """
        Return the current season.
        """
        return self.season

    def get_space(self):
        """

        :return: Return the used capacity.
        """
        return self.used_capacity

    def update_disaster_probability(self):
        """
        Randomly determine whether a disaster occurs.

        Doctests
        >>> h = Habitat(10, 1)
        >>> h.disaster_probability
        False
        >>> h.update_disaster_probability() is None
        True
        """
        possibility = random.random()
        if possibility >= 0.95:
            self.disaster_probability = True
            print("There have been a disaster occurred!!")

    def has_free_space(self, growth):
        """
        Randomly determine whether a disaster occurs.

        Doctests
        --------
        >>> h = Habitat(10, 1)
        >>> h.disaster_probability
        False
        >>> h.update_disaster_probability() is None
        True
        """
        if growth + self.used_capacity <= self.capacity:
            return True
        return False

    def simulate_game(self):
        """
        Simulate one round of the game.

        Doctests
        --------
        >>> h = Habitat(10, 1)
        >>> h.round
        0
        >>> h.simulate_game()
        >>> h.round
        1
        """
        print("The game is simulating...")
        self.round += 1
        self.update_season()
        self.update_disaster_probability()  # Getting disaster status
        for creature in self.creatures[:]:
            creature.starvation_check()  # Getting the starvation status of creatures.
            if self.disaster_probability and creature in self.creatures:
                # Creatures are going to be effected due to disaster.
                creature.disaster_effect()
            creature.eat()  # Hunting protokoll
        self.disaster_probability = False
        for plant in self.plants[:]:
            plant.grow()
        for plants in self.plants[:]:
            if not plants.isalive:
                self.remove_plants(plants)
        for creatures in self.creatures[:]:
            if not creatures.is_alive:
                self.remove_creature(creatures)
        if self.get_season() == "Winter":
            # Info for the player the changes that comes through seasons
            print("The season is Winter! There will be no grow and hunt.")  #
            print("Creatures are going to winter sleep except Herbivore.")
        if self.get_season() == "Autumn":
            print("The season is Autumn! There will be no grow")
        if self.get_season() == "Spring":
            print("The season is Spring! The Plants grow more. .")

    def end_game(self):
        """
        Check if the game has ended.


        >>> h = Habitat(10, 1)
        >>> h.end_game()
        True
        """
        if not any(plant.isalive for plant in self.plants):
            print("All plants are dead. Game over!")
            return True
        if not any(creature.is_alive for creature in self.creatures):
            print("All creatures are dead. Game over!")
            return True

        return False

    def show_status(self):
        """
        Display the current habitat status.


        >>> h = Habitat(10, 1)
        >>> h.show_status() is None
        True
        """
        print(f"Round: {self.round}")
        time.sleep(0.5)
        print(f"Habitat Capacity: {self.capacity}")
        time.sleep(0.5)
        print(f"Habitat Occupied Capacity: {self.get_space()}")
        time.sleep(0.5)
        print(f"Season: {self.get_season()}")
        time.sleep(0.5)

        for plant in self.plants:
            plant_name = plant.__class__.__name__
            print(f"Capacity of {plant_name}: {plant.size}")
            time.sleep(0.5)

        for creature in self.creatures:
            creature_name = creature.__class__.__name__
            print(f"Capacity of {creature_name}: {creature.size}")
            time.sleep(0.5)
