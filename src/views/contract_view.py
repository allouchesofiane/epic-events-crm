from src.views.base_view import BaseView


class ContractView(BaseView):
    """Vue pour la gestion des contrats."""

    def display_contracts_list(self, contracts, title="Liste des contrats"):
        self.display_title(title)

        if not contracts:
            print("Aucun contrat trouvé.")
            return

        print()
        print("ID | Client | Montant | Restant | Signé | Date")
        print("-" * 70)

        for contract in contracts:
            client_name = contract.client.full_name if contract.client else "-"
            signed = "Oui" if contract.is_signed else "Non"
            date = contract.created_at.strftime("%d/%m/%Y")

            print(f"{contract.id} | {client_name} | "
                  f"{float(contract.total_amount):.2f}€ | "
                  f"{float(contract.remaining_amount):.2f}€ | "
                  f"{signed} | {date}")

        print()
        print("Total :", len(contracts), "contrat(s)")

    def display_create_contract_form(self, client):
        self.display_title("Création d'un contrat")

        print("Client :", client.full_name)

        total_amount = float(self.prompt("Montant total (€)"))
        remaining_input = self.prompt("Montant restant (€)", str(total_amount))
        remaining_amount = float(remaining_input)

        return total_amount, remaining_amount

    def display_contract_created(self, contract):
        self.display_success("Contrat créé")

        print("ID :", contract.id)
        print("Client :", contract.client.full_name)
        print("Montant total :", float(contract.total_amount), "€")
        print("Montant restant :", float(contract.remaining_amount), "€")

    def display_contract_signed(self, contract):
        self.display_success(f"Contrat {contract.id} signé")