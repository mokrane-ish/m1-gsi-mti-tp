from abc import ABC, abstractmethod


# --- Product ---
class Sandwich:
    def __init__(self, label="Custom Sandwich"):
        self.label = label
        self.ingredients = []

    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def show(self):
        print(f"{self.label}: {', '.join(self.ingredients)}")


# --- Abstract Builder ---
class SandwichBuilder(ABC):
    @property
    @abstractmethod
    def sandwich(self) -> Sandwich:
        pass

    @abstractmethod
    def set_label(self, label):
        pass

    @abstractmethod
    def add_bread(self):
        pass

    @abstractmethod
    def add_shawarma(self):
        pass

    @abstractmethod
    def add_ground_meat(self):
        pass

    @abstractmethod
    def add_omelet(self):
        pass

    @abstractmethod
    def add_fries(self):
        pass

    @abstractmethod
    def add_cheese(self):
        pass

    @abstractmethod
    def add_sauce(self, sauce_name="House Sauce"):
        pass


# --- Concrete Builder ---
class FastFoodSandwichBuilder(SandwichBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._sandwich = Sandwich()

    @property
    def sandwich(self) -> Sandwich:
        product = self._sandwich
        self.reset()
        return product

    def set_label(self, label):
        self._sandwich.label = label

    def add_bread(self):
        self._sandwich.add("Baguette Bread")

    def add_shawarma(self):
        self._sandwich.add("Marinated Shawarma Chicken")

    def add_ground_meat(self):
        self._sandwich.add("Grilled Ground Meat")

    def add_omelet(self):
        self._sandwich.add("Omelet")

    def add_fries(self):
        self._sandwich.add("French Fries")

    def add_cheese(self):
        self._sandwich.add("Cheddar Cheese")

    def add_sauce(self, sauce_name="House Sauce"):
        self._sandwich.add(sauce_name)


# --- Director ---
class SandwichDirector:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> SandwichBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: SandwichBuilder):
        self._builder = builder

    def build_shawarma_sandwich(self):
        self._builder.set_label("Shawarma Sandwich")
        self._builder.add_bread()
        self._builder.add_shawarma()
        self._builder.add_sauce("Garlic Sauce")

    def build_ground_meat_sandwich(self):
        self._builder.set_label("Ground Meat Sandwich")
        self._builder.add_bread()
        self._builder.add_ground_meat()
        self._builder.add_cheese()
        self._builder.add_fries()
        self._builder.add_sauce("Algerian Sauce")

    def build_fries_omelet_sandwich(self):
        self._builder.set_label("Fries-Omelet Sandwich")
        self._builder.add_bread()
        self._builder.add_fries()
        self._builder.add_omelet()
        self._builder.add_cheese()
        self._builder.add_sauce("Mayonnaise & Harissa")


if __name__ == "__main__":
    director = SandwichDirector()
    builder = FastFoodSandwichBuilder()
    director.builder = builder

    print("--- Preset Sandwiches (via Director) ---")
    director.build_shawarma_sandwich()
    builder.sandwich.show()

    director.build_ground_meat_sandwich()
    builder.sandwich.show()

    director.build_fries_omelet_sandwich()
    builder.sandwich.show()

    print("\n--- Custom Sandwich (Direct Builder) ---")
    builder.set_label("Mixed Shawarma & Ground Meat")
    builder.add_bread()
    builder.add_shawarma()
    builder.add_ground_meat()
    builder.add_cheese()
    builder.add_sauce("Garlic & Algerian Sauce")
    builder.sandwich.show()