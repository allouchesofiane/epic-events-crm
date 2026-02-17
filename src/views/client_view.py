from src.views.base_view import BaseView


class ClientView(BaseView):
    """Vue pour la gestion des clients."""

    def display_clients_list(self, clients, title="Liste des clients"):
        self.display_title(title)

        if not clients:
            print("Aucun client trouvé.")
            return

        print()
        print("ID | Nom | Entreprise | Email | Téléphone")
        print("-" * 70)

        for client in clients:
            company = client.company_name or "-"
            phone = client.phone or "-"

            print(f"{client.id} | {client.full_name} | {company} | "
                  f"{client.email} | {phone}")

        print()
        print("Total :", len(clients), "client(s)")

    def display_create_client_form(self):
        self.display_title("Création d'un client")

        full_name = self.prompt("Nom complet")
        email = self.prompt("Email")
        phone = self.prompt("Téléphone")
        company_name = self.prompt("Nom de l'entreprise (optionnel)", "")

        if company_name == "":
            company_name = None

        return full_name, email, phone, company_name

    def display_update_client_form(self, client):
        self.display_title("Mise à jour du client")

        full_name = self.prompt("Nouveau nom", client.full_name)
        email = self.prompt("Nouveau email", client.email)
        phone = self.prompt("Nouveau téléphone", client.phone or "")
        company_name = self.prompt("Nouvelle entreprise", client.company_name or "")

        if phone == "":
            phone = None

        if company_name == "":
            company_name = None

        return full_name, email, phone, company_name

    def display_client_created(self, client):
        self.display_success("Client créé")

        print("ID :", client.id)
        print("Nom :", client.full_name)
        print("Entreprise :", client.company_name or "-")
        print("Email :", client.email)

    def display_client_updated(self):
        self.display_success("Client mis à jour")