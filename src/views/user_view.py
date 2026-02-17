from src.views.base_view import BaseView


class UserView(BaseView):
    """Vue pour la gestion des utilisateurs."""

    def display_users_list(self, users):
        self.display_title("Liste des utilisateurs")

        if not users:
            print("Aucun utilisateur trouvé.")
            return

        print()
        print("ID | Nom | Email | Rôle | Créé le")
        print("-" * 60)

        for user in users:
            created = user.created_at.strftime("%d/%m/%Y")
            print(f"{user.id} | {user.full_name} | {user.email} | "
                  f"{user.role.value.upper()} | {created}")

        print()
        print("Total :", len(users))

    def display_create_user_form(self):
        self.display_title("Création d'un utilisateur")

        full_name = self.prompt("Nom complet")
        email = self.prompt("Email")
        password = self.prompt_password("Mot de passe")

        print("\nRôles disponibles :")
        print("1 - Commercial")
        print("2 - Support")
        print("3 - Gestion")

        role_choice = self.prompt("Choisissez un rôle (1-3)", "1")

        role_map = {
            "1": "commercial",
            "2": "support",
            "3": "gestion"
        }

        role = role_map.get(role_choice, "commercial")

        return full_name, email, password, role

    def display_user_created(self, user):
        self.display_success("Utilisateur créé")

        print("ID :", user.id)
        print("Nom :", user.full_name)
        print("Email :", user.email)
        print("Rôle :", user.role.value.upper())