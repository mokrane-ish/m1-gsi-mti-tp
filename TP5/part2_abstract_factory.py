from abc import ABC, abstractmethod


# --- Abstract Products ---
class Circle(ABC):
    @abstractmethod
    def draw(self):
        pass


class Square(ABC):
    @abstractmethod
    def draw(self):
        pass


# --- Concrete Products: 2D Family ---
class Circle2D(Circle):
    def draw(self):
        print("Drawing a 2D Circle")


class Square2D(Square):
    def draw(self):
        print("Drawing a 2D Square")


# --- Concrete Products: 3D Family ---
class Circle3D(Circle):
    def draw(self):
        print("Drawing a 3D Circle (Sphere)")


class Square3D(Square):
    def draw(self):
        print("Drawing a 3D Square (Cube)")


# --- Abstract Factory ---
class ShapeFactory(ABC):
    @abstractmethod
    def create_circle(self) -> Circle:
        pass

    @abstractmethod
    def create_square(self) -> Square:
        pass


# --- Concrete Factories ---
class ShapeFactory2D(ShapeFactory):
    def create_circle(self) -> Circle:
        return Circle2D()

    def create_square(self) -> Square:
        return Square2D()


class ShapeFactory3D(ShapeFactory):
    def create_circle(self) -> Circle:
        return Circle3D()

    def create_square(self) -> Square:
        return Square3D()


# --- Client Code ---
def render_shapes(factory: ShapeFactory):
    circle = factory.create_circle()
    square = factory.create_square()
    circle.draw()
    square.draw()


if __name__ == "__main__":
    print("--- 2D Shape Factory ---")
    render_shapes(ShapeFactory2D())

    print("\n--- 3D Shape Factory ---")
    render_shapes(ShapeFactory3D())