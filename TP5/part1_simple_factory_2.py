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


class ShapeFactory:
    @staticmethod
    def createShape(type):
        if type == "Circle":
            return Circle()
        elif type == "Square":
            return Square()
        elif type == "Triangle":
            return Triangle()
        elif type == "Rectangle":
            return Rectangle()
        else:
            print("Bad shape creation: " + type)
            return None


if __name__ == "__main__":
    for name in ["Circle", "Square", "Triangle", "Rectangle"]:
        shape = ShapeFactory.createShape(name)
        if shape:
            shape.draw()
            shape.erase()