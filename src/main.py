
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime

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
from src.models.user import Role, User
from src.utils.validators import (
    validate_email_format,
    validate_phone,
    validate_password_strength,
    validate_amount,
    validate_attendees
)
from src.utils.logger import init_sentry
from src.utils.auth import hash_password


# Fichier pour stocker le token de session
TOKEN_FILE = ".current_token"


class EpicEventsCRM:
    """Application principale CRM Epic Events."""
    
    def __init__(self):
        self.db = None
        self.current_user = None
        self.token = None
        
        # Créer les vues
        self.base_view = BaseView()
        self.auth_view = AuthView()
        self.user_view = UserView()
        self.client_view = ClientView()
        self.contract_view = ContractView()
        self.event_view = EventView()
    
    # ========== GESTION DU TOKEN ==========
    
    def save_token(self, token):
        """Sauvegarde le token dans un fichier."""
        with open(TOKEN_FILE, 'w') as f:
            f.write(token)
    
    def load_token(self):
        """Charge le token depuis le fichier."""
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as f:
                return f.read().strip()
        return None
    
    def clear_token(self):
        """Supprime le fichier de token."""
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
        self.token = None
        self.current_user = None
    
    def verify_authentication(self):
        """Vérifie que l'utilisateur est connecté."""
        if not self.current_user:
            self.base_view.display_error("Vous devez être connecté pour accéder à cette fonction")
            return False
        return True
    
    # ========== INITIALISATION ==========
    
    def initialize_database(self):
        """Initialise la base de données."""
        self.base_view.display_title("INITIALISATION DE LA BASE DE DONNÉES")
        try:
            init_db()
            init_sentry()
            self.base_view.display_success("Base de données initialisée avec succès!")
        except Exception as e:
            self.base_view.display_error(f"Erreur lors de l'initialisation: {str(e)}")
    
    def create_first_admin(self):
        """Crée le premier utilisateur administrateur."""
        db = SessionLocal()
        try:
            # Vérifier s'il y a déjà des utilisateurs
            if db.query(User).count() > 0:
                self.base_view.display_error("Des utilisateurs existent déjà. Utilisez le menu pour en créer d'autres.")
                return
            
            self.base_view.display_title("CRÉATION DU PREMIER ADMINISTRATEUR")
            
            full_name = self.base_view.prompt("Nom complet")
            
            email = self.base_view.prompt("Email")
            while not validate_email_format(email):
                self.base_view.display_error("Email invalide")
                email = self.base_view.prompt("Email")
            
            password = self.base_view.prompt_password()
            is_valid, error_msg = validate_password_strength(password)
            
            while not is_valid:
                self.base_view.display_error(error_msg)
                password = self.base_view.prompt_password()
            
            # Créer l'admin
            admin = User(
                full_name=full_name,
                email=email,
                password_hash=hash_password(password),
                role=Role.GESTION
            )
            db.add(admin)
            db.commit()
            
            self.base_view.display_success("Administrateur créé avec succès!")
            print(f"   Email: {email}")
            print(f"   Rôle: GESTION")
            
        except Exception as e:
            db.rollback()
            self.base_view.display_error(str(e))
        finally:
            db.close()
    
    # ========== AUTHENTIFICATION ==========
    
    def login(self):
        """Gère la connexion d'un utilisateur."""
        try:
            email, password = self.auth_view.display_login_form()
            
            db = SessionLocal()
            auth_controller = AuthController(db)
            
            result = auth_controller.login(email, password)
            
            self.token = result["token"]
            self.current_user = result["user"]
            self.save_token(self.token)
            
            self.auth_view.display_login_success(self.current_user)
            
            db.close()
            
        except Exception as e:
            self.auth_view.display_login_error(e)
    
    def logout(self):
        """Déconnecte l'utilisateur."""
        self.clear_token()
        self.base_view.display_success("Déconnexion réussie")
    
    def show_current_user(self):
        """Affiche l'utilisateur connecté."""
        if not self.verify_authentication():
            return
        
        self.auth_view.display_current_user(self.current_user)
    
    # ========== GESTION DES UTILISATEURS ==========
    
    def list_users(self):
        """Liste tous les utilisateurs."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            user_controller = UserController(db, self.current_user)
            users = user_controller.get_all_users()
            self.user_view.display_users_list(users)
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def create_user(self):
        """Crée un nouvel utilisateur."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            user_controller = UserController(db, self.current_user)
            
            full_name, email, password, role = self.user_view.display_create_user_form()
            
            # Validations
            if not validate_email_format(email):
                self.base_view.display_error("Email invalide")
                return
            
            is_valid, error_msg = validate_password_strength(password)
            if not is_valid:
                self.base_view.display_error(error_msg)
                return
            
            new_user = user_controller.create_user(full_name, email, password, role)
            self.user_view.display_user_created(new_user)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    # ========== GESTION DES CLIENTS ==========
    
    def list_clients(self):
        """Liste tous les clients."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            client_controller = ClientController(db, self.current_user)
            
            # Si c'est un commercial, proposer de voir tous ou juste les siens
            if self.current_user.role == Role.COMMERCIAL:
                choice = self.base_view.prompt("Afficher (1) Tous les clients ou (2) Mes clients ?", "2")
                if choice == "2":
                    clients = client_controller.get_my_clients()
                    self.client_view.display_clients_list(clients, "MES CLIENTS")
                else:
                    clients = client_controller.get_all_clients()
                    self.client_view.display_clients_list(clients)
            else:
                clients = client_controller.get_all_clients()
                self.client_view.display_clients_list(clients)
            
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def create_client(self):
        """Crée un nouveau client."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            client_controller = ClientController(db, self.current_user)
            
            full_name, email, phone, company_name = self.client_view.display_create_client_form()
            
            # Validations
            if not validate_email_format(email):
                self.base_view.display_error("Email invalide")
                return
            
            if not validate_phone(phone):
                self.base_view.display_error("Numéro de téléphone invalide")
                return
            
            new_client = client_controller.create_client(full_name, email, phone, company_name)
            self.client_view.display_client_created(new_client)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def update_client(self):
        """Met à jour un client."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            client_id = int(self.base_view.prompt("ID du client à modifier"))
            
            client_controller = ClientController(db, self.current_user)
            client = client_controller.get_client_by_id(client_id)
            
            if not client:
                self.base_view.display_error(f"Client {client_id} non trouvé")
                return
            
            full_name, email, phone, company_name = self.client_view.display_update_client_form(client)
            
            client_controller.update_client(client_id, full_name, email, phone, company_name)
            self.client_view.display_client_updated()
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    # ========== GESTION DES CONTRATS ==========
    
    def list_contracts(self):
        """Liste les contrats."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            contract_controller = ContractController(db, self.current_user)
            
            print("\n1. Tous les contrats")
            print("2. Contrats non signés")
            print("3. Contrats non payés")
            
            choice = self.base_view.prompt("Votre choix", "1")
            
            if choice == "2":
                contracts = contract_controller.get_unsigned_contracts()
                self.contract_view.display_contracts_list(contracts, "CONTRATS NON SIGNÉS")
            elif choice == "3":
                contracts = contract_controller.get_unpaid_contracts()
                self.contract_view.display_contracts_list(contracts, "CONTRATS NON PAYÉS")
            else:
                contracts = contract_controller.get_all_contracts()
                self.contract_view.display_contracts_list(contracts)
            
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def create_contract(self):
        """Crée un nouveau contrat."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            client_id = int(self.base_view.prompt("ID du client"))
            
            from src.models.client import Client
            client = db.query(Client).filter(Client.id == client_id).first()
            
            if not client:
                self.base_view.display_error(f"Client {client_id} non trouvé")
                return
            
            contract_controller = ContractController(db, self.current_user)
            
            total_amount, remaining_amount = self.contract_view.display_create_contract_form(client)
            
            # Validation
            if not validate_amount(total_amount):
                self.base_view.display_error("Le montant total doit être > 0")
                return
            
            new_contract = contract_controller.create_contract(client_id, total_amount, remaining_amount)
            self.contract_view.display_contract_created(new_contract)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def sign_contract(self):
        """Signe un contrat."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            contract_id = int(self.base_view.prompt("ID du contrat à signer"))
            
            contract_controller = ContractController(db, self.current_user)
            
            confirm = self.base_view.prompt_confirm(f"Confirmer la signature du contrat {contract_id} ?")
            if not confirm:
                self.base_view.display_info("Opération annulée")
                return
            
            contract = contract_controller.sign_contract(contract_id)
            self.contract_view.display_contract_signed(contract)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    # ========== GESTION DES ÉVÉNEMENTS ==========
    
    def list_events(self):
        """Liste les événements."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            event_controller = EventController(db, self.current_user)
            
            # Menu spécifique selon le rôle
            if self.current_user.role == Role.SUPPORT:
                print("\n1. Tous les événements")
                print("2. Mes événements")
                choice = self.base_view.prompt("Votre choix", "2")
                
                if choice == "2":
                    events = event_controller.get_my_events()
                    self.event_view.display_events_list(events, "MES ÉVÉNEMENTS")
                else:
                    events = event_controller.get_all_events()
                    self.event_view.display_events_list(events)
            elif self.current_user.role == Role.GESTION:
                print("\n1. Tous les événements")
                print("2. Événements non assignés")
                choice = self.base_view.prompt("Votre choix", "1")
                
                if choice == "2":
                    events = event_controller.get_unassigned_events()
                    self.event_view.display_events_list(events, "ÉVÉNEMENTS NON ASSIGNÉS")
                else:
                    events = event_controller.get_all_events()
                    self.event_view.display_events_list(events)
            else:
                events = event_controller.get_all_events()
                self.event_view.display_events_list(events)
            
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def create_event(self):
        """Crée un nouvel événement."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            contract_id = int(self.base_view.prompt("ID du contrat"))
            
            event_controller = EventController(db, self.current_user)
            
            try:
                start_date, end_date, location, attendees, notes = self.event_view.display_create_event_form()
            except ValueError:
                self.base_view.display_error("Format de date invalide. Utilisez: AAAA-MM-JJ HH:MM")
                return
            
            # Validation
            if not validate_attendees(attendees):
                self.base_view.display_error("Le nombre de participants doit être > 0")
                return
            
            new_event = event_controller.create_event(
                contract_id, start_date, end_date, location, attendees, notes
            )
            self.event_view.display_event_created(new_event)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def assign_event(self):
        """Assigne un événement à un support."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            event_id = int(self.base_view.prompt("ID de l'événement"))
            support_id = int(self.base_view.prompt("ID de l'utilisateur SUPPORT"))
            
            event_controller = EventController(db, self.current_user)
            
            # Récupérer le support pour affichage
            support = db.query(User).filter(User.id == support_id).first()
            
            event = event_controller.assign_event(event_id, support_id)
            self.event_view.display_event_assigned(event, support)
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    def update_event(self):
        """Met à jour un événement."""
        if not self.verify_authentication():
            return
        
        db = SessionLocal()
        try:
            event_id = int(self.base_view.prompt("ID de l'événement à modifier"))
            
            event_controller = EventController(db, self.current_user)
            event = event_controller.get_event_by_id(event_id)
            
            if not event:
                self.base_view.display_error(f"Événement {event_id} non trouvé")
                return
            
            location, attendees, notes = self.event_view.display_update_event_form(event)
            
            event_controller.update_event(event_id, location, attendees, notes)
            self.event_view.display_event_updated()
            
        except PermissionError as e:
            self.base_view.display_error(str(e))
        except ValueError as e:
            self.base_view.display_error(str(e))
        except Exception as e:
            self.base_view.display_error(f"Erreur: {str(e)}")
        finally:
            db.close()
    
    # ========== MENUS ==========
    
    def menu_users(self):
        """Menu de gestion des utilisateurs."""
        while True:
            options = {
                "1": "Lister les utilisateurs",
                "2": "Créer un utilisateur",
                "0": "Retour"
            }
            
            choice = self.base_view.display_menu("GESTION DES UTILISATEURS", options)
            
            if choice == "1":
                self.list_users()
            elif choice == "2":
                self.create_user()
            elif choice == "0":
                break
            else:
                self.base_view.display_error("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_clients(self):
        """Menu de gestion des clients."""
        while True:
            options = {
                "1": "Lister les clients",
                "2": "Créer un client",
                "3": "Modifier un client",
                "0": "Retour"
            }
            
            choice = self.base_view.display_menu("GESTION DES CLIENTS", options)
            
            if choice == "1":
                self.list_clients()
            elif choice == "2":
                self.create_client()
            elif choice == "3":
                self.update_client()
            elif choice == "0":
                break
            else:
                self.base_view.display_error("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_contracts(self):
        """Menu de gestion des contrats."""
        while True:
            options = {
                "1": "Lister les contrats",
                "2": "Créer un contrat",
                "3": "Signer un contrat",
                "0": "Retour"
            }
            
            choice = self.base_view.display_menu("GESTION DES CONTRATS", options)
            
            if choice == "1":
                self.list_contracts()
            elif choice == "2":
                self.create_contract()
            elif choice == "3":
                self.sign_contract()
            elif choice == "0":
                break
            else:
                self.base_view.display_error("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_events(self):
        """Menu de gestion des événements."""
        while True:
            options = {
                "1": "Lister les événements",
                "2": "Créer un événement",
                "3": "Assigner un événement",
                "4": "Modifier un événement",
                "0": "Retour"
            }
            
            choice = self.base_view.display_menu("GESTION DES ÉVÉNEMENTS", options)
            
            if choice == "1":
                self.list_events()
            elif choice == "2":
                self.create_event()
            elif choice == "3":
                self.assign_event()
            elif choice == "4":
                self.update_event()
            elif choice == "0":
                break
            else:
                self.base_view.display_error("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def main_menu(self):
        """Menu principal."""
        while True:
            # Afficher l'utilisateur connecté
            if self.current_user:
                user_info = f" - Connecté: {self.current_user.full_name} ({self.current_user.role.value.upper()})"
            else:
                user_info = " - Non connecté"
            
            options = {
                "1": "Se connecter",
                "2": "Voir mon profil",
                "3": "Gestion des utilisateurs",
                "4": "Gestion des clients",
                "5": "Gestion des contrats",
                "6": "Gestion des événements",
                "7": "Se déconnecter",
                "0": "Quitter"
            }
            
            choice = self.base_view.display_menu(f"EPIC EVENTS CRM{user_info}", options)
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.show_current_user()
            elif choice == "3":
                self.menu_users()
            elif choice == "4":
                self.menu_clients()
            elif choice == "5":
                self.menu_contracts()
            elif choice == "6":
                self.menu_events()
            elif choice == "7":
                self.logout()
            elif choice == "0":
                self.base_view.display_info("Au revoir !")
                sys.exit(0)
            else:
                self.base_view.display_error("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def run(self):
        """Lance l'application."""
        # Essayer de charger un token existant
        token = self.load_token()
        if token:
            try:
                db = SessionLocal()
                auth_controller = AuthController(db)
                self.current_user = auth_controller.verify_token(token)
                self.token = token
                db.close()
            except:
                # Token invalide ou expiré
                self.clear_token()
        
        # Afficher le menu principal
        self.main_menu()


def main():
    """Fonction principale."""
    init_sentry()
    # Vérifier s'il y a des arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        app = EpicEventsCRM()
        
        if command == "init":
            app.initialize_database()
        elif command == "create-admin":
            app.create_first_admin()
        else:
            print(f"Commande inconnue:")
    else:
        # Lancer l'application normale
        app = EpicEventsCRM()
        app.run()


if __name__ == "__main__":
    main()