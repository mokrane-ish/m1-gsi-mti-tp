class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


if __name__ == "__main__":
    monSingleton1 = Singleton()
    monSingleton2 = Singleton()

    print(monSingleton1, monSingleton2)
    assert monSingleton1 is monSingleton2
    print("Assertion passed: both variables refer to the exact same instance.")