"""
This module implements a text-based survival simulation game where plants and
creatures coexist in a habitat and evolve over time.

The user configures game speed, plant attributes, and creature sizes, then
controls the simulation round by round.
"""
__author__ = "8500551 Mirza, 8811983 Bekker"
import plants
from habitat import Habitat
import creatures
import time


def input_int(prompt):
    """
       Prompt the user for a non-negative integer input.

       The function repeatedly asks for input until the user enters
       a valid non-negative integer.

       Parameters
       ----------
       prompt : str
           The message displayed to the user.

       Returns
       -------
       int
           A validated non-negative integer.

       Doctests
       --------
       >>> callable(input_int)
       True
       >>> isinstance("Enter a number", str)
       True
       >>> 5 >= 0
       True
       """
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Sorry, that's an invalid value.")
                continue
            return value

        except ValueError:
            print("Sorry, that's not an integer.")


def main():
    """
    Run the main game loop for the survival simulation.

    This function initializes the game by collecting user input,
    creating plants and creatures, setting up the habitat, and
    managing the simulation rounds until the game ends.
    """
    while True:
        try:
            game_speed = input_int("1: slow\n2: medium\n3: fast\nChoose a game speed:")
            if game_speed not in [1, 2, 3]:
                print("Sorry, that's an invalid value.")
                continue
            break
        except ValueError:
            print("Please enter a number between 1 and 3.")

    plant_list = ["tree", "ivy", "mushroom"]
    plant_objects = []
    plant_total = 0
    for name in plant_list:
        # The input request for the plants.
        plant_size = input_int(f"Please enter the size of the {name}: ")
        min_size = input_int(f"Please enter the minimum size of the {name}: ")
        max_size = input_int(f"Please enter the maximum size of the {name}: ")

        if name == "tree":
            tree = plants.Tree(plant_size, min_size, max_size, (-game_speed+4))
            plant_objects.append(tree)
        elif name == "ivy":
            ivy = plants.Ivy(plant_size, min_size, max_size, (-game_speed+4))
            plant_objects.append(ivy)
        elif name == "mushroom":
            mushroom = plants.Mushroom(plant_size, min_size, max_size, (-game_speed+4))
            plant_objects.append(mushroom)
        plant_total += max_size

    creature_list = ["carnivore", "herbivore", "omnivore"]
    creature_objects = []
    creat_total = 0
    for name in creature_list:
        # The input request for the creatures.
        creat_size = input_int(f"Please enter the size of the {name}: ")
        if name == "carnivore":
            creat = creatures.Carnivore(creat_size)
        elif name == "herbivore":
            creat = creatures.Herbivore(creat_size)
        elif name == "omnivore":
            creat = creatures.Omnivore(creat_size)
        creat_total += creat_size
        creature_objects.append(creat)
    # Habitat is created.
    habitat = Habitat((creat_total+plant_total), game_speed)
    for i in plant_objects:
        habitat.add_plants(i)

    for j in creature_objects:
        habitat.add_creature(j)

    print("Welcome the survival game")
    time.sleep(0.5)
    print(f"Current Status on the game")
    time.sleep(0.5)
    habitat.show_status()
    print("Every round corresponds a month in the real life.")
    time.sleep(0.5)

    while True:
        # Game Loop
        print("1: Pause the round", "2: Simulate the round", "q: quit", sep="\n")
        try:
            choice = int(input("Next move: "))
            if choice == 'q':
                print("Thank you for playing the game.")
                break
            if choice not in [1, 2]:
                print("Please enter a valid input.")
            if choice == 1:
                print("The game is stopped for 10 sec.")
                time.sleep(10)
            if choice == 2:
                habitat.simulate_game()
                time.sleep(4)
                # End condition is checked.
            if habitat.end_game():
                break
            habitat.show_status()
        except ValueError:
            print("Please enter an integer between 1 or 2.")


if __name__ == "__main__":
    main()
