from src.views.base_view import BaseView


class AuthView(BaseView):
    """Vue pour l'authentification."""

    def display_login_form(self):
        self.display_title("Connexion")

        email = self.prompt("Email")
        password = self.prompt_password("Mot de passe")
        return email, password
    
    def display_login_success(self, user):
        self.display_success("Connexion réussie")
        print("Nom :", user.full_name)
        print("Rôle :", user.role.value.upper())

    def display_login_error(self, error):
        self.display_error(error)

    def display_current_user(self, user):
        self.display_title("Utilisateur connecté")

        print("Nom :", user.full_name)
        print("Email :", user.email)
        print("Rôle :", user.role.value.upper())