from datetime import datetime
from src.views.base_view import BaseView


class EventView(BaseView):
    """Vue pour la gestion des événements."""

    def display_events_list(self, events, title="Liste des événements"):
        self.display_title(title)

        if not events:
            print("Aucun événement trouvé.")
            return

        print()
        print("ID | Client | Lieu | Date | Support")
        print("-" * 80)

        for event in events:
            client_name = event.client.full_name if event.client else "-"
            date_str = event.event_date_start.strftime("%d/%m/%Y %H:%M")
            support_name = event.support_contact.full_name if event.support_contact else "Non assigné"

            print(f"{event.id} | {client_name} | "
                  f"{event.location} | {date_str} | {support_name}")

        print()
        print("Total :", len(events), "événement(s)")

    def display_create_event_form(self):
        self.display_title("Création d'un événement")

        location = self.prompt("Lieu de l'événement")
        attendees = int(self.prompt("Nombre de participants"))

        print("\nFormat attendu : AAAA-MM-JJ HH:MM")
        start_str = self.prompt("Date de début")
        end_str = self.prompt("Date de fin")

        start_date = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        end_date = datetime.strptime(end_str, "%Y-%m-%d %H:%M")

        notes = self.prompt("Notes (optionnel)", "")
        if notes == "":
            notes = None

        return start_date, end_date, location, attendees, notes

    def display_update_event_form(self, event):
        self.display_title("Mise à jour de l'événement")

        location = self.prompt("Nouveau lieu", event.location)
        attendees = int(self.prompt("Nouveau nombre de participants", str(event.attendees)))
        notes = self.prompt("Nouvelles notes", event.notes or "")

        if notes == "":
            notes = None

        return location, attendees, notes

    def display_event_created(self, event):
        self.display_success("Événement créé")

        print("ID :", event.id)
        print("Client :", event.client.full_name)
        print("Lieu :", event.location)
        print("Date :", event.event_date_start.strftime("%d/%m/%Y %H:%M"))

    def display_event_assigned(self, event, support):
        self.display_success(
            f"Événement {event.id} assigné à {support.full_name}"
        )

    def display_event_updated(self):
        self.display_success("Événement mis à jour")