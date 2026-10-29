from academicelement import AcademicElement


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
        """Set grades for continuous assessment and exam."""
        if tp is not None:
            self._grades["tp"] = tp
        if td is not None:
            self._grades["td"] = td
        if exam is not None:
            self._grades["exam"] = exam

    def summary(self):
        """Return a short textual description of the module."""
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
        """Calculates module average based on continuous and exam evaluation weights."""
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
        """Returns module credits if average >= 10, otherwise 0."""
        return self.credit if self.calculate_average() >= 10 else 0