from abc import ABC, abstractmethod


class AcademicElement(ABC):
    """Abstract base class for academic entities (Module, Unit, Semester, etc.)."""

    def __init__(self, name: str, title: str):
        self.name = name
        self.title = title
        self._WEEKS = 15  # Encapsulation: private attribute
        self.coef = 0
        self.credit = 0

        # Workload distribution (volume horaire)
        self.hours_lecture = 0
        self.hours_td = 0
        self.hours_tp = 0

    @abstractmethod
    def calculate_average(self):
        """Abstract method to be implemented by subclasses."""
        pass

    @abstractmethod
    def calculate_credits(self):
        """Abstract method to be implemented by subclasses."""
        pass


class Module(AcademicElement):
    """Represents a teaching module with pedagogical and evaluation attributes."""

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

    def summary(self):
        return (
            f"Module: {self.title} ({self.name})\n"
            f"Coefficient: {self.coef}, Credits: {self.credit}\n"
            f"Hours: total ({self.total_hours}h), ({self.hours_lecture}h Lecture, "
            f"{self.hours_td}h TD, {self.hours_tp}h TP)\n"
            f"Teaching mode: {self.teaching_mode}\n"
            f"Evaluation mode: Continuous: {self.evaluation_continous_percent}%, "
            f"Exam: {self.evaluation_exam_percent}%"
        )

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
    """Represents a teaching unit containing multiple modules."""

    def __init__(self, name: str, title: str, modules=None):
        super().__init__(name, title)
        self._modules = modules if modules is not None else []

    def add_module(self, module: Module):
        self._modules.append(module)

    def calculate_average(self):
        if not self._modules:
            return 0.0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = sum(m.coef for m in self._modules)
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        if not self._modules:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return sum(m.credit for m in self._modules)
        else:
            return sum(m.calculate_credits() for m in self._modules)


# Execution / Test for Question 7
if __name__ == "__main__":
    m1 = Module(
        "MTI",
        "Methods & Technologies of Implementation",
        coef=3,
        credit=5,
        hours_tp=1.5,
        continous_percent=40,
        exam_percent=60,
    )
    m1.set_grade(tp=10, exam=12)

    m2 = Module(
        "AABD",
        "Database architecture and administration",
        coef=2,
        credit=4,
        hours_tp=1.5,
        continous_percent=40,
        exam_percent=60,
    )
    m2.set_grade(tp=8, exam=6)

    u11 = Unit("UEM11", "UE Méthodologie", [m1, m2])

    print("=== Question 7 Test: Abstraction ===")
    print("Module 1 average:", m1.name, m1.calculate_average())
    print("Module 2 average:", m2.name, m2.calculate_average())
    print("Unit average:", u11.calculate_average())
    print("Unit credits:", u11.calculate_credits())