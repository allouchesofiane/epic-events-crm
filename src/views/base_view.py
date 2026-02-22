class BaseView:
    """Classe de base pour toutes les vues."""

    @staticmethod
    def display_title(title):
        print("\n" + "=" * 50)
        print(title)
        print("=" * 50)

    @staticmethod
    def display_success(message):
        print(message)

    @staticmethod
    def display_error(message):
        print(message)

    @staticmethod
    def display_info(message):
        print(message)

    @staticmethod
    def display_separator():
        print("-" * 50)

    @staticmethod
    def prompt(message, default=None):
        if default is not None:
            value = input(f"{message} [{default}] : ")
            if value == "":
                return default
            return value
        return input(f"{message} : ")

    @staticmethod
    def prompt_password(message="Mot de passe"):
        import getpass
        return getpass.getpass(message + " : ")

    @staticmethod
    def prompt_confirm(message):
        response = input(message + " (o/n) : ").lower()
        return response in ["o", "oui"]

    @staticmethod
    def display_menu(title, options):
        BaseView.display_title(title)

        for key in options:
            print(f"{key} - {options[key]}")

        return input("Votre choix : ")