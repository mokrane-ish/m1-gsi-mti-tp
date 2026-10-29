import sys
from pathlib import Path

# Ensure root directory is in PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from module import Module


def test_module_average_and_credits():
    m = Module("MTI", "Methods and Technologies", coef=3, credit=5, hours_tp=1.5)
    m.set_grade(tp=14, exam=12)
    assert round(m.calculate_average(), 2) == 12.80
    assert m.calculate_credits() == 5


def test_module_failing_credits():
    m = Module("AABD", "Database Admin", coef=2, credit=4, hours_tp=1.5)
    m.set_grade(tp=8, exam=6)
    assert round(m.calculate_average(), 2) == 6.80
    assert m.calculate_credits() == 0