"""
This module defines plant types used in a survival simulation game.
Plants grow depending on seasons, consume habitat capacity, and
can be eaten by creatures.
"""
__author__ = "8500551 Mirza, 8811983 Bekker"

class Plant:
    """
    Base class representing a plant in the habitat.
    """
    def __init__(self, size, min_size, max_size, growth_rate):
        """
        Initialize a plant with size and growth constraints.
        """
        self.size = size
        self.min_size = min_size
        self.max_size = max_size
        self.growth_rate = growth_rate
        self.isalive = True
        self.habitat = None

    def grow(self):
        """
        Grow the plant. Simple test: size increases if alive.


        >>> class H:
        ...     def get_seasons(self): return "Spring"
        ...     def has_free_spaces(self, g): return True
        ...     used_capacity = 0
        >>> p = Plant(2, 1, 5, 1)
        >>> p.habitat = H()
        >>> old = p.size
        >>> p.grow()
        >>> p.size > old
        True
        >>> p.size <= p.max_size
        True
        >>> p.isalive
        True
        """
        if not self.isalive:
            return
        old_size = self.size
        growth = self.growth_rate
        if self.habitat.get_season() != "Winter" and self.habitat.get_season() != "Autumn":
            if self.habitat.get_season() == "Spring":
                growth += 1
                # if the growth rate exceeds the max_size.
            if self.size + growth >= self.max_size:
                growth = self.max_size - self.size
                # if the habitat has free space.
            if self.habitat.has_free_space(growth):
                self.size += growth
                self.habitat.used_capacity += growth

        if self.size != old_size:
            print(f"{self.__class__.__name__} grew from {old_size} to {self.size}")
        else:
            return

    def eaten(self, quantity):
        """
        Reduce plant size when eaten by creatures.


        >>> class H: used_capacity = 10
        >>> p = Plant(4, 1, 6, 1)
        >>> p.habitat = H()
        >>> p.eaten(2)
        >>> p.size
        2
        """
        if self.size >= quantity:
            pass
        else:
            # if the quantity is more than size, then quantity = self.size
            quantity = self.size
        self.size -= quantity
        if self.size <= self.min_size:
            self.isalive = False
        print(f"The {quantity} of {self.__class__.__name__} is dead ")
        self.habitat.used_capacity -= quantity

    def get_size(self):
        """ Return the current size of the plant. """
        return self.size


class Tree(Plant):
    """ A tree plant type """
    def __init__(self, size, min_size, max_size, growth_rate):
        """ Initialize a Tree instance. """
        super().__init__(size, min_size, max_size, growth_rate)

    def grow(self):
        """
        Grow the tree using Plant growth rules.
        """
        super().grow()


class Ivy(Plant):
    """  An ivy plant type.  """

    def __init__(self, size, min_size, max_size, growth_rate):
        """Initialize an Ivy instance."""
        super().__init__(size, min_size, max_size, growth_rate)

    def grow(self):
        """Grow ivy using Plant growth rules."""
        super().grow()


class Mushroom(Plant):
    """  A mushroom plant type. """
    def __init__(self, size, min_size, max_size, growth_rate):
        """Initialize a Mushroom instance."""
        super().__init__(size, min_size, max_size, growth_rate)

    def grow(self):
        """ Grow mushroom using Plant growth rules. """
        super().grow()
