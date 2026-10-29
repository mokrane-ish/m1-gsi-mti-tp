from academicelement import AcademicElement
from module import Module


class Unit(AcademicElement):
    """Represents a teaching unit (Unité d'Enseignement) containing multiple modules."""

    def __init__(self, name: str, title: str, modules=None):
        super().__init__(name, title)
        self._modules = modules if modules is not None else []

    def add_module(self, module: Module):
        """Adds a module object to the teaching unit."""
        self._modules.append(module)

    @property
    def coef(self):
        """Calculates total coefficients of modules in the unit."""
        return sum(m.coef for m in self._modules)

    @property
    def credit(self):
        """Calculates total credits of modules in the unit."""
        return sum(m.credit for m in self._modules)

    def calculate_average(self):
        """Calculates the weighted average of all modules in the unit."""
        if not self._modules:
            return 0.0
        total = sum(m.calculate_average() * m.coef for m in self._modules)
        coef_sum = self.coef
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
            return self.credit
        else:
            return sum(m.calculate_credits() for m in self._modules)