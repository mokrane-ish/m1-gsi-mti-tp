import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from module import Module
from unit import Unit


def test_unit_average_and_compensation():
    m1 = Module("MTI", "Methods & Tech", coef=3, credit=5, hours_tp=1.5)
    m1.set_grade(tp=14, exam=12)  # avg = 12.80

    m2 = Module("AABD", "Database Admin", coef=2, credit=4, hours_tp=1.5)
    m2.set_grade(tp=8, exam=6)    # avg = 6.80

    u = Unit("UEM11", "UE Méthodologie", [m1, m2])
    assert round(u.calculate_average(), 2) == 10.40
    assert u.calculate_credits() == 9  # Full unit credits earned via compensation