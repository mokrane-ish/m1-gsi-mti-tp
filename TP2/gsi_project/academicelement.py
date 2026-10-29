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