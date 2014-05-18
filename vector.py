from math import sqrt

class Vector():
    """
    Class implementing a standard vector with some basic vector operations like
    adding, subtracting, the dot product, scalar multiplication, and the like.
    """

    def __init__(self, *components):
        """
        Given a list of n components, __init__ creates an n dimensional vector.
        """

        self.components = components
        self.dimension = len(components)

    def __str__(self):
        """
        Prints the elements of the vector in tuple like fashion.

        >>> a = Vector(3,4,5)
        >>> print(a)
        Vector(3, 4, 5)
        >>> a = Vector()
        >>> print(a)
        Vector()
        """

        return "Vector{}".format(str(self.components))

    def __getitem__(self, index):
        """
        Indexes a component in the Vector.

        >>> a = Vector(3,4,5)
        >>> a[2]
        5
        >>> a[0]
        3
        """

        return self.components[index]

    def __len__(self):
        """
        Calculates the length of a vector (its dimension).

        >>> a = Vector(3,4)
        >>> len(a)
        2
        >>> b = Vector()
        >>> len(b)
        0
        """

        return self.dimension

    def __iter__(self):
        """
        Iterates through the components of a vector.

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
        Sums the components of two vectors together.

        >>> a = Vector(1,2,3)
        >>> b = Vector(4,5,6)
        >>> print(a + b)
        Vector(5, 7, 9)
        >>> c = Vector()
        >>> print(c + c)
        Vector()
        """

        if isinstance(other, Vector):
            # Addition is undefined for vectors of differing dimension.
            if self.dimension != other.dimension:
                raise ValueError("""Addition Undefined for Vectors
                                    of Different Dimension""")

            return Vector(*(x + y for x,y in zip(self, other)))

        raise ValueError("""cannot add object of
                            type {} from Vector""".format(type(other)))

    def __sub__(self, other):
        """
        Subtracts the components of one vector from another.

        >>> a = Vector(1,2,3)
        >>> print(a - a)
        Vector(0, 0, 0)
        >>> b = Vector(4,5,6)
        >>> print(b - a)
        Vector(3, 3, 3)
        """

        if isinstance(other, Vector):
            if self.dimension != other.dimension:
                raise ValueError("""Subtraction Undefined for Vectors
                                    of Different Dimension""")

            return Vector(*(x - y for x,y in zip(self, other)))

        raise ValueError("""cannot subtract object of type
                            {} from Vector""".format(type(other)))

    def __mul__(self, other):
        """
        Multiplies a vector, either with a scalar as a multiple of its
        components, or with two vectors as the dot product.

        >>> a = Vector(1,2,3)
        >>> b = Vector(4,5,6)
        >>> c = Vector(0,0,0)
        >>> a*b
        32
        >>> b*c
        0
        >>> print(a*2)
        Vector(2, 4, 6)
        """

        if isinstance(other, int) or isinstance(other, float):
            return Vector(*(x*other for x in self))

        if isinstance(other, Vector):
            if self.dimension != other.dimension:
                raise ValueError("""Dot-Product is Undefined for Vectors
                                    of Differing Dimension""")

            return sum(x*y for x,y in zip(self, other))

        raise ValueError("""Cannot multiply a vector
                            by a {}""".format(type(other)))

    def __rmul__(self, other):
        """
        Implements multiplication of vectors from the right, which is the same
        as multiplication from the left as the operations are symmetric.
        """

        return self*other

    def __truediv__(self, other):
        """
        Divides a Vector by a scalar quantity.

        >>> a = Vector(1,2,3)
        >>> print(a/3)
        Vector(0.3333333333333333, 0.6666666666666666, 1.0)
        """

        if isinstance(other, int) or isinstance(other, float):
            return Vector(*(x/other for x in self))

        raise ValueError("""Can only divide a Vector by
                            a number, not a {}""".format(type(other)))

    def norm(self):
        """
        Defines the Euclidean Norm of a vector - in other words, its length.

        >>> a = Vector(1,0,0)
        >>> a.norm()
        1.0
        >>> b = Vector(0,0,0)
        >>> b.norm()
        0.0
        """

        return sqrt(self*self)

    def in_range(self, self_radius, other, other_radius):
        """
        Given two vectors, which we can see as circles/spheres/hypermegaspheres
        if given a radius, this function tests whether the two vectors with
        these radii overlap given a position and size.

        >>> a = Vector(0, 0)
        >>> a.in_range(5, a, 5)
        True
        >>> b = Vector(10,0)
        >>> a.in_range(10, b, 10)
        True
        >>> a.in_range(9, b, 9)
        True
        """

        if isinstance(other, Vector):
            return (self - other).norm() < self_radius + other_radius

        raise ValueError("""Cannot define in_range
                            on type {}""".format(type(other)))