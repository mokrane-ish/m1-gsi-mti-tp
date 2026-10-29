from abc import ABC, abstractmethod


class AcademicElement(ABC):
    """Abstract base class for academic entities (Module, Unit, Semester)."""

    def __init__(self, name: str, title: str):
        self.name = name
        self.title = title
        self._WEEKS = 15
        self._coef = 0
        self._credit = 0

    @property
    def coef(self):
        return self._coef

    @coef.setter
    def coef(self, value):
        self._coef = value

    @property
    def credit(self):
        return self._credit

    @credit.setter
    def credit(self, value):
        self._credit = value

    @abstractmethod
    def calculate_average(self):
        """Abstract method to calculate weighted average."""
        pass

    @abstractmethod
    def calculate_credits(self):
        """Abstract method to calculate acquired credits."""
        pass


class Module(AcademicElement):
    """Represents a teaching module."""

    def __init__(
        self,
        name: str = "",
        title: str = "",
        coef: int = 1,
        credit: int = 1,
        hours_lecture: float = 1.5,
        hours_td: float = 0,
        hours_tp: float = 0,
        teaching_mode: str = "In-person",
        continous_percent: int = 40,
        exam_percent: int = 60,
    ):
        super().__init__(name, title)
        self.coef = coef
        self.credit = credit
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent
        self.total_hours = self._WEEKS * (
            self.hours_lecture + self.hours_td + self.hours_tp
        )
        self._grades = {"tp": None, "td": None, "exam": None}

    def set_grade(self, tp=None, td=None, exam=None):
        if tp is not None:
            self._grades["tp"] = tp
        if td is not None:
            self._grades["td"] = td
        if exam is not None:
            self._grades["exam"] = exam

    def calculate_average(self):
        tp = self._grades["tp"] if self._grades["tp"] is not None else 0
        td = self._grades["td"] if self._grades["td"] is not None else 0
        exam = self._grades["exam"] if self._grades["exam"] is not None else 0

        percent_exam = self.evaluation_exam_percent
        percent_tp = percent_td = 0

        if self.hours_tp and self.hours_td:
            percent_tp = percent_td = self.evaluation_continous_percent / 2
        elif self.hours_td:
            percent_td = self.evaluation_continous_percent
        elif self.hours_tp:
            percent_tp = self.evaluation_continous_percent

        return (
            tp * percent_tp / 100 +
            td * percent_td / 100 +
            exam * percent_exam / 100
        )

    def calculate_credits(self):
        return self.credit if self.calculate_average() >= 10 else 0


class Unit(AcademicElement):
    """Represents a teaching unit (Unité d'Enseignement) containing multiple modules."""

    def __init__(self, name: str, title: str, modules=None):
        super().__init__(name, title)
        self._modules = modules if modules is not None else []

    def add_module(self, module: Module):
        self._modules.append(module)

    @property
    def coef(self):
        return sum(m.coef for m in self._modules)

    @property
    def credit(self):
        return sum(m.credit for m in self._modules)

    def calculate_average(self):
        if not self._modules:
            return 0.0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = self.coef
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        if not self._modules:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return sum(m.calculate_credits() for m in self._modules)


class Semester(AcademicElement):
    """Represents an academic semester containing multiple teaching units."""

    def __init__(self, name: str, title: str, units=None):
        super().__init__(name, title)
        self._units = units if units is not None else []

    def add_unit(self, unit: Unit):
        self._units.append(unit)

    @property
    def coef(self):
        return sum(u.coef for u in self._units)

    @property
    def credit(self):
        return sum(u.credit for u in self._units)

    def calculate_average(self):
        """Calculates the weighted average across all teaching units in the semester."""
        if not self._units:
            return 0.0
        total = sum(u.calculate_average() * u.coef for u in self._units)
        coef_sum = self.coef
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        """
        Calculates total credits acquired for the semester:
        - If semester average >= 10: acquires 30 credits (full semester validation by compensation).
        - If semester average < 10: acquires sum of credits earned per unit.
        """
        if not self._units:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return sum(u.calculate_credits() for u in self._units)


# Execution / Test for Question 11
if __name__ == "__main__":
    # Unit 1: UE Méthodologie
    m1 = Module("MTI", "Methods & Tech Impl", coef=3, credit=5, hours_tp=1.5)
    m1.set_grade(tp=10, exam=12)  # Average = 11.20

    m2 = Module("AABD", "Database Admin", coef=2, credit=4, hours_tp=1.5)
    m2.set_grade(tp=8, exam=6)    # Average = 6.80

    u1 = Unit("UEM11", "UE Méthodologie", [m1, m2])  # Average = 9.44, Credits = 5

    # Unit 2: UE Fondamentale 1
    m3 = Module("RCB", "Reseaux Couches Basses", coef=3, credit=6, hours_td=1.5, hours_tp=1.5)
    m3.set_grade(tp=14, td=12, exam=11)  # Average = 11.70

    m4 = Module("AlgoAv", "Algorithmique Avancee", coef=2, credit=4, hours_td=1.5)
    m4.set_grade(td=10, exam=10)         # Average = 10.00

    u2 = Unit("UEF11", "UE Fondamentale 1", [m3, m4])  # Average = 11.08, Credits = 10

    # Semester S1
    s1 = Semester("S1", "Semestre 1 GSI", [u1, u2])

    print("=== Question 11 Test: Semester Class ===")
    print(f"Unit 1 ({u1.name}) Average: {u1.calculate_average():.2f} | Credits: {u1.calculate_credits()}")
    print(f"Unit 2 ({u2.name}) Average: {u2.calculate_average():.2f} | Credits: {u2.calculate_credits()}")
    print("---------------------------------------")
    print(f"Semester ({s1.name}) Overall Average: {s1.calculate_average():.2f}")
    print(f"Semester Total Credits Obtained: {s1.calculate_credits()} / {s1.credit}")