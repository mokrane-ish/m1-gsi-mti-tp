from abc import ABC, abstractmethod


class Compte(ABC):
    def __init__(self, username):
        self.username = username

    @abstractmethod
    def afficher_droits(self):
        pass


class Gestionnaire(Compte):
    def afficher_droits(self):
        print(f"[Gestionnaire - {self.username}] Full access: manage stock, prices, and users.")


class Vendeur(Compte):
    def afficher_droits(self):
        print(f"[Vendeur - {self.username}] Sales access: view stock and register sales.")


class Visiteur(Compte):
    def afficher_droits(self):
        print(f"[Visiteur - {self.username}] Read-only access: browse available products.")


class CompteFactory:
    @staticmethod
    def create_compte(role, username):
        role_normalized = role.strip().lower()
        if role_normalized == "gestionnaire":
            return Gestionnaire(username)
        elif role_normalized == "vendeur":
            return Vendeur(username)
        elif role_normalized == "visiteur":
            return Visiteur(username)
        else:
            print(f"Unknown account role: {role}")
            return None


if __name__ == "__main__":
    users = [
        ("Gestionnaire", "Amine"),
        ("Vendeur", "Sara"),
        ("Visiteur", "Karim"),
    ]

    for role, name in users:
        compte = CompteFactory.create_compte(role, name)
        if compte:
            compte.afficher_droits()