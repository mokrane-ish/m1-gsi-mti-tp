class Module:
    """Represents a teaching module with pedagogical and evaluation attributes."""

    def __init__(
        self,
        name: str = "",  # module code
        title: str = "",
        coef: int = 1,
        credit: int = 1,
        hours_lecture: float = 1.5,
        hours_td: float = 0,
        hours_tp: float = 0,
        teaching_mode: str = "In-person",  # "Distance" or "In-person"
        continous_percent: int = 40,
        exam_percent: int = 60,
    ):
        self._WEEKS = 15  # private attribute
        
        # Basic attributes
        self.name = name
        self.title = title
        self.coef = coef
        self.credit = credit

        # Workload distribution
        self.hours_lecture = hours_lecture
        self.hours_td = hours_td
        self.hours_tp = hours_tp

        # Teaching and evaluation mode
        self.teaching_mode = teaching_mode
        self.evaluation_continous_percent = continous_percent
        self.evaluation_exam_percent = exam_percent

        # Total hours per semester
        self.total_hours = self._WEEKS * (
            self.hours_lecture + self.hours_td + self.hours_tp
        )
        self._grades = {"tp": None, "td": None, "exam": None}

    def set_grade(self, tp=None, td=None, exam=None):
        """Controlled access to set grades."""
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
        tp = self._grades["tp"]
        td = self._grades["td"]
        exam = self._grades["exam"]

        percent_exam = self.evaluation_exam_percent
        percent_tp = percent_td = 0

        # Weight distribution logic
        if self.hours_tp and self.hours_td:
            percent_tp = percent_td = self.evaluation_continous_percent / 2
        elif self.hours_td:
            percent_td = self.evaluation_continous_percent
        elif self.hours_tp:
            percent_tp = self.evaluation_continous_percent

        tp_val = tp if tp is not None else 0
        td_val = td if td is not None else 0
        exam_val = exam if exam is not None else 0

        return (
            tp_val * percent_tp / 100 +
            td_val * percent_td / 100 +
            exam_val * percent_exam / 100
        )

    def calculate_credits(self):
        """Returns module credits if average >= 10, otherwise 0."""
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return 0


# Execution / Test for Question 3
if __name__ == "__main__":
    mti = Module(
        name="MTI",
        title="Methods and Technologies of Implementation",
        coef=3,
        credit=5,
        hours_lecture=1.5,
        hours_tp=1.5,
        teaching_mode="In-person"
    )
    
    # Setting grades: TP = 14, Exam = 12
    mti.set_grade(tp=14, exam=12)
    
    print("=== Question 3 Test ===")
    print(mti.summary())
    print("\n--- Evaluation Results ---")
    print(f"Module Average: {mti.calculate_average():.2f}")
    print(f"Credits Obtained: {mti.calculate_credits()}")