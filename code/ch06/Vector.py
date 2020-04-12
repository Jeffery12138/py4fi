# class 的魔法方法


class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector(%r, %r, %r)' % (self.x, self.y, self.z)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar,
                      self.y * scalar,
                      self.z * scalar)

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if item in [0, -3]:
            return self.x
        elif item in [1, -2]:
            return self.y
        elif item in [2, -1]:
            return self.z
        else:
            raise IndexError('Index out of range.')

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]


v1 = Vector(1, 1, 1)
v2 = Vector(2, 2, 2)

# __repr__
print(v1, v2)
# __abs__
print(abs(v1), abs(v2))
# __bool__
print(bool(abs(v1)), bool(abs(v2)))
# __add__
print(v1+v2)
# __mul__
print(v1*3, v2*5)
# __len__
print(len(v1), len(v2))
# __getitem__
for i in range(len(v1)):
    print(v1[i], v2[i])
# __iter__
for v in v1:
    print(v)



