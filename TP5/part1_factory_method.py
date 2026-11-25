from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
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


class ShapeFactory(ABC):
    @abstractmethod
    def createShape(self, shape_type):
        pass


class ShapeFactory_SCT(ShapeFactory):
    def createShape(self, shape_type):
        if shape_type == "Square":
            return Square()
        elif shape_type == "Circle":
            return Circle()
        elif shape_type == "Triangle":
            return Triangle()
        else:
            print("ShapeFactory_SCT cannot create: " + shape_type)
            return None


class ShapeFactory_SCR(ShapeFactory):
    def createShape(self, shape_type):
        if shape_type == "Square":
            return Square()
        elif shape_type == "Circle":
            return Circle()
        elif shape_type == "Rectangle":
            return Rectangle()
        else:
            print("ShapeFactory_SCR cannot create: " + shape_type)
            return None


if __name__ == "__main__":
    print("--- Testing ShapeFactory_SCT ---")
    factory_sct = ShapeFactory_SCT()
    for name in ["Square", "Circle", "Triangle", "Rectangle"]:
        shape = factory_sct.createShape(name)
        if shape:
            shape.draw()
            shape.erase()

    print("\n--- Testing ShapeFactory_SCR ---")
    factory_scr = ShapeFactory_SCR()
    for name in ["Square", "Circle", "Triangle", "Rectangle"]:
        shape = factory_scr.createShape(name)
        if shape:
            shape.draw()
            shape.erase()