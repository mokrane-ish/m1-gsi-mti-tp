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
        pass

    @abstractmethod
    def calculate_credits(self):
        pass


class Module(AcademicElement):
    """Represents a teaching module in the Master 1 GSI canvas."""

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
    """Represents a teaching unit (UE) containing multiple modules."""

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
    """Represents an academic semester containing multiple UEs."""

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
        if not self._units:
            return 0.0
        total = sum(u.calculate_average() * u.coef for u in self._units)
        coef_sum = self.coef
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        if not self._units:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return sum(u.calculate_credits() for u in self._units)


# =====================================================================
# Building the Master 1 GSI Curriculum Structure
# =====================================================================
def build_gsi_s1():
    # UEF11
    rcb = Module("RCB", "Réseaux des couches basses", coef=3, credit=6, hours_lecture=1.5, hours_td=1.5, hours_tp=1.5, continous_percent=40, exam_percent=60)
    algo = Module("AlgoAv", "Algorithmique Avancée et Complexité", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0, continous_percent=40, exam_percent=60)
    uef11 = Unit("UEF11", "Unité Fondamentale 11", [rcb, algo])

    # UEF12
    se = Module("SE", "Système d'exploitation", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0, continous_percent=40, exam_percent=60)
    amsi = Module("AMSI", "Architectures Modernes des Systèmes Informatiques", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0, continous_percent=40, exam_percent=60)
    uef12 = Unit("UEF12", "Unité Fondamentale 12", [se, amsi])

    # UEM11
    aabd = Module("AABD", "Architecture et administration des bases de données", coef=2, credit=4, hours_lecture=1.5, hours_td=0, hours_tp=1.5, continous_percent=40, exam_percent=60)
    mti = Module("MTI", "Méthodes et Technologies d'Implémentation", coef=3, credit=5, hours_lecture=1.5, hours_td=0, hours_tp=1.5, continous_percent=40, exam_percent=60)
    uem11 = Unit("UEM11", "Unité Méthodologique 11", [aabd, mti])

    # UED11
    scvv = Module("scvv", "Systèmes de Communication Vocaux et Vidéos", coef=2, credit=2, hours_lecture=1.5, hours_td=0, hours_tp=1.5, continous_percent=40, exam_percent=60)
    ued11 = Unit("UED11", "Unité Découverte 11", [scvv])

    # UET11
    cloud = Module("cloud", "Cloud Computing", coef=1, credit=1, hours_lecture=1.5, hours_td=0, hours_tp=0, continous_percent=0, exam_percent=100)
    uet11 = Unit("UET11", "Unité Transversale 11", [cloud])

    # Assign student grades for S1
    rcb.set_grade(tp=12, td=14, exam=11)
    algo.set_grade(td=10, exam=9)
    se.set_grade(td=11, exam=12)
    amsi.set_grade(td=13, exam=10)
    aabd.set_grade(tp=14, exam=8)
    mti.set_grade(tp=15, exam=13)
    scvv.set_grade(tp=10, exam=11)
    cloud.set_grade(exam=14)

    return Semester("S1", "Semestre 1 GSI", [uef11, uef12, uem11, ued11, uet11])


# =====================================================================
# Main Execution / Academic Report
# =====================================================================
if __name__ == "__main__":
    s1 = build_gsi_s1()

    print("==========================================================")
    print(f"       MASTER 1 GSI - ACADEMIC REPORT ({s1.name})")
    print("==========================================================")
    print(f"Total Coef: {s1.coef} | Total Credits Target: {s1.credit}\n")

    for unit in s1._units:
        print(f"[{unit.name}] {unit.title}")
        print(f"  -> UE Average: {unit.calculate_average():.2f} / 20")
        print(f"  -> UE Credits Earned: {unit.calculate_credits()} / {unit.credit}")
        print("  Modules:")
        for m in unit._modules:
            print(f"     * {m.name} ({m.title}): Avg = {m.calculate_average():.2f} | Coef = {m.coef} | Credits = {m.calculate_credits()}/{m.credit}")
        print("-" * 58)

    print("\n==========================================================")
    print(f" SEMESTER OVERALL AVERAGE : {s1.calculate_average():.2f} / 20")
    print(f" SEMESTER CREDITS EARNED  : {s1.calculate_credits()} / {s1.credit}")
    print("==========================================================")