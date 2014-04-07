import math

class Vector():
    def __init__(self, *components):
        self.components = components

    def __str__(self):
        """
        >>> a = Vector(3,4,5)
        >>> print(a)
        (3, 4, 5)
        >>> a = Vector()
        >>> print(a)
        ()
        """

        return str(self.components)

    # Defines getting components of a vector
    def __getitem__(self, index):
        """
        >>> a = Vector(3,4,5)
        >>> a[2]
        5
        >>> a[0]
        3
        """

        return self.components[index]

    def __len__(self):
        """
        >>> a = Vector(3,4)
        >>> len(a)
        2
        >>> b = Vector()
        >>> len(b)
        0
        """

        return len(self.components)

    def __iter__(self):
        """
        >>> a = Vector(1,2,3)
        >>> print([i for i in a])
        [1, 2, 3]
        >>> b = Vector()
        >>> print([i for i in b])
        []
        """

        return iter(self.components)

    def __add__(self, other):
        """
        >>> a = Vector(1,2,3)
        >>> b = Vector(4,5,6)
        >>> print(a + b)
        (5, 7, 9)
        >>> c = Vector()
        >>> print(c + c)
        ()
        """

        if not isinstance(other, Vector):
            raise ValueError("cannot subtract object of type {} from Vector".format(type(other)))

        if len(self) != len(other):
            raise ValueError("Operation Undefined for Vectors of Different Dimension")

        return Vector(*(x + y for x,y in zip(self, other)))

    # Defines Vector Subtraction
    def __sub__(self, other):
        """
        >>> a = Vector(1,2,3)
        >>> print(a - a)
        (0, 0, 0)
        >>> b = Vector(4,5,6)
        >>> print(b - a)
        (3, 3, 3)
        """

        if not isinstance(other, Vector):
            raise ValueError("cannot subtract object of type {} from Vector".format(type(other)))

        if len(self) != len(other):
            raise ValueError("Operation Undefined for Vectors of Different Dimension")

        return Vector(*(x - y for x,y in zip(self, other)))

    # Defines a vector dot product operation
    def __mul__(self, other):
        """
        >>> a = Vector(1,2,3)
        >>> b = Vector(4,5,6)
        >>> c = Vector(0,0,0)
        >>> a*b
        32
        >>> b*c
        0
        >>> print(a*2)
        (2, 4, 6)
        """

        if isinstance(other, int) or isinstance(other, float):
            return Vector(*(int(x*other) for x in self))

        if len(self) != len(other):
            raise ValueError("Operation Undefined for Vectors of Different Dimension")

        return sum(int(x*y) for x,y in zip(self, other))

    def __truediv__(self, other):
        """
        >>> a = Vector(1,2,3)
        >>> print(a/3)
        (0.3333333333333333, 0.6666666666666666, 1.0)
        """

        if not (isinstance(other, int) or isinstance(other, float)):
            raise ValueError("Can only divide a Vector by a number, not a {}".format(type(other)))

        # We make it an int for discrete pixels
        return Vector(*(int(x/other) for x in self))

    # Defines the euclidean norm (lenght) of a vector
    def norm(self):
        """
        >>> a = Vector(1,0,0)
        >>> a.norm()
        1.0
        """

        return math.sqrt(self*self)

    def angle(self, other):
        return (self*other)/(self.norm()*other.norm())