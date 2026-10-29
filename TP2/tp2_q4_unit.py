class Module:
    """Represents an individual module."""

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
        self.name = name
        self.title = title
        self.coef = coef
        self.credit = credit
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent
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


class Unit:
    """Represents a teaching unit (Unité d'Enseignement) containing multiple modules."""

    def __init__(self, name: str, title: str, modules=None):
        self.name = name
        self.title = title
        self._modules = modules if modules is not None else []

    def add_module(self, module: Module):
        """Adds a module object to the teaching unit."""
        self._modules.append(module)

    def calculate_average(self):
        """Calculates the weighted average of all modules in the unit."""
        if not self._modules:
            return 0.0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = sum(m.coef for m in self._modules)
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        """
        Calculates total credits acquired for the unit:
        - If unit average >= 10: acquiring ALL module credits (compensation principle).
        - If unit average < 10: acquiring credits ONLY for modules where average >= 10.
        """
        if not self._modules:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return sum(m.credit for m in self._modules)
        else:
            return sum(m.calculate_credits() for m in self._modules)


# Execution / Test for Question 4
if __name__ == "__main__":
    m1 = Module("MTI", "Methods & Technologies of Implementation", coef=3, credit=5, hours_tp=1.5)
    m2 = Module("AABD", "Database Architecture & Administration", coef=2, credit=4, hours_tp=1.5)

    # Set student grades
    m1.set_grade(tp=14, exam=12)  # MTI Average = 12.8
    m2.set_grade(tp=8, exam=6)    # AABD Average = 6.8

    u1 = Unit("UEM11", "UE Méthodologie", [m1, m2])

    print("=== Question 4 Test: Unit Class ===")
    print(f"Unit Name: {u1.name} ({u1.title})")
    print(f"Module 1 ({m1.name}) Average: {m1.calculate_average():.2f}")
    print(f"Module 2 ({m2.name}) Average: {m2.calculate_average():.2f}")
    print(f"Unit Average: {u1.calculate_average():.2f}")
    print(f"Unit Total Credits Obtained: {u1.calculate_credits()}")