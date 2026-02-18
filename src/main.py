import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database.config import SessionLocal, init_db
from src.controllers.auth_controller import AuthController
from src.controllers.user_controller import UserController
from src.controllers.client_controller import ClientController
from src.controllers.contract_controller import ContractController
from src.controllers.event_controller import EventController
from src.views.auth_view import AuthView
from src.views.user_view import UserView
from src.views.client_view import ClientView
from src.views.contract_view import ContractView
from src.views.event_view import EventView
from src.views.base_view import BaseView
from src.utils.validators import (
    validate_email_format,
    validate_phone,
    validate_password_strength,
    validate_amount,
    validate_attendees
)
from src.utils.auth import hash_password


TOKEN_FILE = ".current_token"


class EpicEventsCRM:

    def __init__(self):
        self.current_user = None
        self.token = None

        self.base_view = BaseView()
        self.auth_view = AuthView()
        self.user_view = UserView()
        self.client_view = ClientView()
        self.contract_view = ContractView()
        self.event_view = EventView()

    # TOKEN 

    def save_token(self, token):
        with open(TOKEN_FILE, "w") as f:
            f.write(token)

    def load_token(self):
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r") as f:
                return f.read().strip()
        return None

    def clear_token(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.current_user = None
        self.token = None

    def verify_authentication(self):
        if self.current_user is None:
            self.base_view.display_error("Vous devez être connecté.")
            return False
        return True

    # INITIALISATION 

    def initialize_database(self):
        init_db()
        self.base_view.display_success("Base de données initialisée")

    # AUTH

    def login(self):
        email, password = self.auth_view.display_login_form()

        db = SessionLocal()
        controller = AuthController(db)

        try:
            result = controller.login(email, password)
            self.current_user = result["user"]
            self.token = result["token"]
            self.save_token(self.token)

            self.auth_view.display_login_success(self.current_user)

        except Exception as e:
            self.auth_view.display_login_error(e)

        finally:
            db.close()

    def logout(self):
        self.clear_token()
        self.base_view.display_success("Déconnexion réussie")

    # USERS 

    def list_users(self):
        if not self.verify_authentication():
            return

        db = SessionLocal()
        controller = UserController(db, self.current_user)

        try:
            users = controller.get_all_users()
            self.user_view.display_users_list(users)
        except Exception as e:
            self.base_view.display_error(str(e))
        finally:
            db.close()

    # CLIENTS

    def list_clients(self):
        if not self.verify_authentication():
            return

        db = SessionLocal()
        controller = ClientController(db, self.current_user)

        try:
            clients = controller.get_all_clients()
            self.client_view.display_clients_list(clients)
        except Exception as e:
            self.base_view.display_error(str(e))
        finally:
            db.close()

    # CONTRATS 

    def list_contracts(self):
        if not self.verify_authentication():
            return

        db = SessionLocal()
        controller = ContractController(db, self.current_user)

        try:
            contracts = controller.get_all_contracts()
            self.contract_view.display_contracts_list(contracts)
        except Exception as e:
            self.base_view.display_error(str(e))
        finally:
            db.close()

    # EVENTS 

    def list_events(self):
        if not self.verify_authentication():
            return

        db = SessionLocal()
        controller = EventController(db, self.current_user)

        try:
            events = controller.get_all_events()
            self.event_view.display_events_list(events)
        except Exception as e:
            self.base_view.display_error(str(e))
        finally:
            db.close()

    # MENU

    def main_menu(self):
        while True:

            if self.current_user:
                info = f"Connecté : {self.current_user.full_name}"
            else:
                info = "Non connecté"

            options = {
                "1": "Se connecter",
                "2": "Lister utilisateurs",
                "3": "Lister clients",
                "4": "Lister contrats",
                "5": "Lister événements",
                "6": "Se déconnecter",
                "0": "Quitter"
            }

            choice = self.base_view.display_menu(f"EPIC EVENTS CRM - {info}", options)

            if choice == "1":
                self.login()
            elif choice == "2":
                self.list_users()
            elif choice == "3":
                self.list_clients()
            elif choice == "4":
                self.list_contracts()
            elif choice == "5":
                self.list_events()
            elif choice == "6":
                self.logout()
            elif choice == "0":
                break
            else:
                self.base_view.display_error("Choix invalide")

            input("\nAppuyez sur Entrée pour continuer...")

    def run(self):
        token = self.load_token()

        if token:
            db = SessionLocal()
            controller = AuthController(db)
            try:
                self.current_user = controller.verify_token(token)
                self.token = token
            except:
                self.clear_token()
            finally:
                db.close()

        self.main_menu()


def main():
    app = EpicEventsCRM()

    if len(sys.argv) > 1:
        if sys.argv[1] == "init":
            app.initialize_database()
        else:
            print("Commande inconnue")
    else:
        app.run()


if __name__ == "__main__":
    main()