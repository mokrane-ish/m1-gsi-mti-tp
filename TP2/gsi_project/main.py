from module import Module
from unit import Unit
from semester import Semester


def main():
    # --- UEF11 ---
    rcb = Module("RCB", "Réseaux des couches basses", coef=3, credit=6, hours_lecture=1.5, hours_td=1.5, hours_tp=1.5)
    algo = Module("AlgoAv", "Algorithmique Avancée et Complexité", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0)
    uef11 = Unit("UEF11", "Unité Fondamentale 11", [rcb, algo])

    # --- UEF12 ---
    se = Module("SE", "Système d'exploitation", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0)
    amsi = Module("AMSI", "Architectures Modernes des Systèmes Informatiques", coef=2, credit=4, hours_lecture=1.5, hours_td=1.5, hours_tp=0)
    uef12 = Unit("UEF12", "Unité Fondamentale 12", [se, amsi])

    # --- UEM11 ---
    aabd = Module("AABD", "Architecture et administration des bases de données", coef=2, credit=4, hours_lecture=1.5, hours_td=0, hours_tp=1.5)
    mti = Module("MTI", "Méthodes et Technologies d'Implémentation", coef=3, credit=5, hours_lecture=1.5, hours_td=0, hours_tp=1.5)
    uem11 = Unit("UEM11", "Unité Méthodologique 11", [aabd, mti])

    # --- UED11 ---
    scvv = Module("scvv", "Systèmes de Communication Vocaux et Vidéos", coef=2, credit=2, hours_lecture=1.5, hours_td=0, hours_tp=1.5)
    ued11 = Unit("UED11", "Unité Découverte 11", [scvv])

    # --- UET11 ---
    cloud = Module("cloud", "Cloud Computing", coef=1, credit=1, hours_lecture=1.5, hours_td=0, hours_tp=0, continous_percent=0, exam_percent=100)
    uet11 = Unit("UET11", "Unité Transversale 11", [cloud])

    # Set student grades
    rcb.set_grade(tp=12, td=14, exam=11)
    algo.set_grade(td=10, exam=9)
    se.set_grade(td=11, exam=12)
    amsi.set_grade(td=13, exam=10)
    aabd.set_grade(tp=14, exam=8)
    mti.set_grade(tp=15, exam=13)
    scvv.set_grade(tp=10, exam=11)
    cloud.set_grade(exam=14)

    # Build Semester
    s1 = Semester("S1", "Semestre 1 GSI", [uef11, uef12, uem11, ued11, uet11])

    # Display Report
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


if __name__ == "__main__":
    main()