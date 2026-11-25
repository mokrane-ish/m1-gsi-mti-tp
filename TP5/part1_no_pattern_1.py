class Shape:
    def draw(self):
        pass

    def erase(self):
        pass


class Circle(Shape):
    def draw(self):
        print("Circle.draw")

    def erase(self):
        print("Circle.erase")


class Square(Shape):
    def draw(self):
        print("Square.draw")

    def erase(self):
        print("Square.erase")


def create_shape(shape_type):
    if shape_type == "Circle":
        return Circle()
    elif shape_type == "Square":
        return Square()
    else:
        print("Bad shape creation: " + shape_type)
        return None


if __name__ == "__main__":
    for name in ["Circle", "Square"]:
        shape = create_shape(name)
        if shape:
            shape.draw()
            shape.erase()