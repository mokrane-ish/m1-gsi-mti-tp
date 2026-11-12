from abc import ABC, abstractmethod

# --- Part 1: Shape Refactoring & Main Call ---
class Shape(ABC):
    @abstractmethod
    def get_area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, side_length):
        self.side_length = side_length

    def get_area(self):
        return self.side_length * self.side_length

def print_area(shape: Shape):
    print(f"Area: {shape.get_area()}")

# --- Part 2: Person / Student LSP Violation Fix ---
# Scenario Analysis:
# Forcing Student to implement get_salary() or assign_task() violates LSP because
# Student cannot substitute Person without raising runtime errors.
# Fix: Separate employee attributes into an Employee subclass.

class Person:
    def __init__(self, name: str):
        self.name = name

class Employee(Person):
    def __init__(self, name: str, salary: float):
        super().__init__(name)
        self.salary = salary

    def get_salary(self):
        return self.salary

    def assign_task(self, task: str):
        print(f"Task '{task}' assigned to {self.name}.")

class Student(Person):
    def __init__(self, name: str, student_id: str):
        super().__init__(name)
        self.student_id = student_id

    def study(self):
        print(f"Student {self.name} is studying.")

if __name__ == '__main__':
    print("--- Testing Shapes (LSP Corrected) ---")
    rect = Rectangle(5, 10)
    sq = Square(5)
    print_area(rect)
    print_area(sq)

    print("\n--- Testing Person / Student Hierarchy ---")
    emp = Employee("Alice", 3000)
    emp.assign_task("Prepare Lecture")
    print(f"Employee Salary: ${emp.get_salary()}")

    student = Student("Bob", "ST12345")
    student.study()