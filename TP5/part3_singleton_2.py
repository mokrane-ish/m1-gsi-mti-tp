class FileWriterSingleton:
    _instance = None

    def __new__(cls, filename="tp5_log.txt"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.filename = filename
            cls._instance._file = open(filename, "w", encoding="utf-8")
        return cls._instance

    def write(self, message):
        if self._file and not self._file.closed:
            self._file.write(message + "\n")
            self._file.flush()

    def close(self):
        if self._file and not self._file.closed:
            self._file.close()
            FileWriterSingleton._instance = None


if __name__ == "__main__":
    writer1 = FileWriterSingleton("tp5_log.txt")
    writer2 = FileWriterSingleton("tp5_log.txt")

    assert writer1 is writer2
    print("Same FileWriter instance:", writer1 is writer2)

    writer1.write("Log entry 1 from writer1")
    writer2.write("Log entry 2 from writer2")
    writer1.close()

    with open("tp5_log.txt", "r", encoding="utf-8") as f:
        print("File content:\n" + f.read().strip())