from abc import ABC, abstractmethod

# --- Part 1: Printer Interfaces ---
class Printable(ABC):
    @abstractmethod
    def print_document(self, document):
        pass

class Scannable(ABC):
    @abstractmethod
    def scan_document(self, document):
        pass

class Faxable(ABC):
    @abstractmethod
    def fax_document(self, document):
        pass

class BasicPrinter(Printable):
    def print_document(self, document):
        print(f"Printing: {document}")

class AdvancedPrinter(Printable, Scannable, Faxable):
    def print_document(self, document):
        print(f"Printing: {document}")

    def scan_document(self, document):
        print(f"Scanning: {document}")

    def fax_document(self, document):
        print(f"Faxing: {document}")

# --- Part 2: University Academic System ---
class Teacher(ABC):
    @abstractmethod
    def teach(self):
        pass

class Researcher(ABC):
    @abstractmethod
    def research(self):
        pass

class MedicalPractitioner(ABC):
    @abstractmethod
    def practice_medicine(self):
        pass

class ProfessorResearcher(Teacher, Researcher):
    def teach(self):
        print("Professor is teaching university classes.")

    def research(self):
        print("Professor is conducting academic research.")

class FullTimeResearcher(Researcher):
    def research(self):
        print("Full-Time Researcher is conducting full-time research.")

class ProfessorHospitalResearcher(Teacher, Researcher, MedicalPractitioner):
    def teach(self):
        print("Hospital Professor is teaching medical students.")

    def research(self):
        print("Hospital Professor is conducting medical research.")

    def practice_medicine(self):
        print("Hospital Professor is treating patients.")

if __name__ == '__main__':
    print("--- Testing Printer System ---")
    basic = BasicPrinter()
    advanced = AdvancedPrinter()
    basic.print_document("Doc1.pdf")
    advanced.scan_document("Doc2.pdf")

    print("\n--- Testing Academic System ---")
    prof = ProfessorResearcher()
    ft_researcher = FullTimeResearcher()
    hosp_prof = ProfessorHospitalResearcher()

    prof.teach()
    ft_researcher.research()
    hosp_prof.practice_medicine()