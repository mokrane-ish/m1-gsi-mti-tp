from academicelement import AcademicElement
from unit import Unit


class Semester(AcademicElement):
    """Represents an academic semester containing multiple teaching units."""

    def __init__(self, name: str, title: str, units=None):
        super().__init__(name, title)
        self._units = units if units is not None else []

    def add_unit(self, unit: Unit):
        """Adds a teaching unit object to the semester."""
        self._units.append(unit)

    @property
    def coef(self):
        """Calculates total coefficients of all units in the semester."""
        return sum(u.coef for u in self._units)

    @property
    def credit(self):
        """Calculates total credits of all units in the semester."""
        return sum(u.credit for u in self._units)

    def calculate_average(self):
        """Calculates the weighted average across all units in the semester."""
        if not self._units:
            return 0.0
        total = sum(u.calculate_average() * u.coef for u in self._units)
        coef_sum = self.coef
        return total / coef_sum if coef_sum > 0 else 0.0

    def calculate_credits(self):
        """
        Calculates total credits acquired for the semester:
        - If semester average >= 10: acquiring all semester credits (compensation principle).
        - If semester average < 10: acquiring sum of credits earned per unit.
        """
        if not self._units:
            return 0
        avg = self.calculate_average()
        if avg >= 10:
            return self.credit
        else:
            return sum(u.calculate_credits() for u in self._units)