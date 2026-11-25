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


class Triangle(Shape):
    def draw(self):
        print("Triangle.draw")

    def erase(self):
        print("Triangle.erase")


class Rectangle(Shape):
    def draw(self):
        print("Rectangle.draw")

    def erase(self):
        print("Rectangle.erase")


def create_shape(shape_type):
    if shape_type == "Circle":
        return Circle()
    elif shape_type == "Square":
        return Square()
    elif shape_type == "Triangle":
        return Triangle()
    elif shape_type == "Rectangle":
        return Rectangle()
    else:
        print("Bad shape creation: " + shape_type)
        return None


if __name__ == "__main__":
    for name in ["Circle", "Square", "Triangle", "Rectangle"]:
        shape = create_shape(name)
        if shape:
            shape.draw()
            shape.erase()