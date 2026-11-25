from abc import ABC, abstractmethod


# --- Product ---
class Car:
    def __init__(self, model, base_price=20000):
        self.model = model
        self.package_name = "Custom Package"
        self.options = []
        self.total_price = base_price

    def add_option(self, description, price=0):
        self.options.append(description)
        self.total_price += price

    def show(self):
        print(f"Model: {self.model} [{self.package_name}]")
        print(f"  Equipment : {', '.join(self.options)}")
        print(f"  Total     : ${self.total_price:,}")


# --- Abstract Builder ---
class CarBuilder(ABC):
    @property
    @abstractmethod
    def car(self) -> Car:
        pass

    @abstractmethod
    def set_package_name(self, name):
        pass

    @abstractmethod
    def add_standard_engine(self):
        pass

    @abstractmethod
    def add_turbo_engine(self):
        pass

    @abstractmethod
    def add_manual_transmission(self):
        pass

    @abstractmethod
    def add_automatic_transmission(self):
        pass

    @abstractmethod
    def add_gps(self):
        pass

    @abstractmethod
    def add_sunroof(self):
        pass

    @abstractmethod
    def add_leather_seats(self):
        pass

    @abstractmethod
    def add_parking_sensors(self):
        pass


# --- Concrete Builder ---
class CarOrderBuilder(CarBuilder):
    def __init__(self, model="Sedan X1", base_price=20000):
        self.model = model
        self.base_price = base_price
        self.reset()

    def reset(self):
        self._car = Car(self.model, self.base_price)

    @property
    def car(self) -> Car:
        product = self._car
        self.reset()
        return product

    def set_package_name(self, name):
        self._car.package_name = name

    def add_standard_engine(self):
        self._car.add_option("1.6L Standard Engine", 0)

    def add_turbo_engine(self):
        self._car.add_option("2.0L Turbo Engine", 3500)

    def add_manual_transmission(self):
        self._car.add_option("Manual Transmission", 0)

    def add_automatic_transmission(self):
        self._car.add_option("Automatic Transmission", 1500)

    def add_gps(self):
        self._car.add_option("GPS Navigation System", 800)

    def add_sunroof(self):
        self._car.add_option("Panoramic Sunroof", 1200)

    def add_leather_seats(self):
        self._car.add_option("Heated Leather Seats", 1400)

    def add_parking_sensors(self):
        self._car.add_option("360-Degree Parking Sensors & Camera", 900)


# --- Director ---
class CarDirector:
    def __init__(self):
        self._builder = None

    @property
    def builder(self) -> CarBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: CarBuilder):
        self._builder = builder

    def build_basic_car(self):
        self._builder.set_package_name("Basic Package")
        self._builder.add_standard_engine()
        self._builder.add_manual_transmission()

    def build_full_option_car(self):
        self._builder.set_package_name("Full-Option Package")
        self._builder.add_turbo_engine()
        self._builder.add_automatic_transmission()
        self._builder.add_gps()
        self._builder.add_sunroof()
        self._builder.add_leather_seats()
        self._builder.add_parking_sensors()


if __name__ == "__main__":
    director = CarDirector()
    builder = CarOrderBuilder(model="Atlas GT", base_price=22000)
    director.builder = builder

    print("--- 1. Basic Package (via Director) ---")
    director.build_basic_car()
    builder.car.show()

    print("\n--- 2. Full-Option Package (via Director) ---")
    director.build_full_option_car()
    builder.car.show()

    print("\n--- 3. Custom Option Package (Direct Builder) ---")
    builder.set_package_name("Custom Comfort Package")
    builder.add_standard_engine()
    builder.add_automatic_transmission()
    builder.add_gps()
    builder.add_parking_sensors()
    builder.car.show()