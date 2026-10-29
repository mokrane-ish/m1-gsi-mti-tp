import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from module import Module
from unit import Unit
from semester import Semester


def test_semester_average_and_credits():
    m1 = Module("M1", "Mod 1", coef=3, credit=5, hours_tp=1.5)
    m1.set_grade(tp=10, exam=12)  # avg = 11.20

    m2 = Module("M2", "Mod 2", coef=2, credit=4, hours_tp=1.5)
    m2.set_grade(tp=8, exam=6)    # avg = 6.80

    u1 = Unit("U1", "UE 1", [m1, m2])  # avg = 9.44, credits = 5

    m3 = Module("M3", "Mod 3", coef=3, credit=6, hours_td=1.5, hours_tp=1.5)
    m3.set_grade(tp=14, td=12, exam=11)  # avg = 11.70

    m4 = Module("M4", "Mod 4", coef=2, credit=4, hours_td=1.5)
    m4.set_grade(td=10, exam=10)         # avg = 10.00

    u2 = Unit("U2", "UE 2", [m3, m4])  # avg = 11.08, credits = 10

    s = Semester("S1", "Semestre 1", [u1, u2])
    assert round(s.calculate_average(), 2) == 10.26
    assert s.calculate_credits() == 19