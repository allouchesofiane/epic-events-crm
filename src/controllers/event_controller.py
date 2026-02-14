from src.models.user import User, Role
from src.models.event import Event
from src.models.contract import Contract
from src.permissions.decorators import (
    check_is_authenticated,
    check_is_commercial,
    check_is_gestion,
    check_is_owner_or_gestion
)


class EventController:

    def __init__(self, db, current_user=None):
        self.db = db
        self.current_user = current_user

    def get_all_events(self):
        check_is_authenticated(self.current_user)
        return self.db.query(Event).all()

    def get_my_events(self):
        check_is_authenticated(self.current_user)

        if self.current_user.role != Role.SUPPORT:
            raise PermissionError("Réservé au SUPPORT")

        return self.db.query(Event).filter(
            Event.support_contact_id == self.current_user.id
        ).all()

    def get_unassigned_events(self):
        check_is_authenticated(self.current_user)

        return self.db.query(Event).filter(
            Event.support_contact_id == None
        ).all()

    def create_event(self, contract_id, event_date_start,
                     event_date_end, location, attendees, notes=None):

        check_is_commercial(self.current_user)

        contract = self.db.query(Contract).filter(
            Contract.id == contract_id
        ).first()

        if contract is None:
            raise ValueError("Contrat non trouvé")

        if contract.commercial_contact_id != self.current_user.id:
            raise PermissionError("Vous ne pouvez créer que pour vos contrats")

        if not contract.is_signed:
            raise ValueError("Le contrat doit être signé")

        if contract.event:
            raise ValueError("Un événement existe déjà pour ce contrat")

        new_event = Event(
            contract_id=contract_id,
            client_id=contract.client_id,
            event_date_start=event_date_start,
            event_date_end=event_date_end,
            location=location,
            attendees=attendees,
            notes=notes
        )

        self.db.add(new_event)
        self.db.commit()

        return new_event

    def assign_event(self, event_id, support_user_id):
        check_is_gestion(self.current_user)

        event = self.db.query(Event).filter(
            Event.id == event_id
        ).first()

        if event is None:
            raise ValueError("Événement non trouvé")

        support_user = self.db.query(User).filter(
            User.id == support_user_id
        ).first()

        if support_user is None or support_user.role != Role.SUPPORT:
            raise ValueError("L'utilisateur doit être SUPPORT")

        event.support_contact_id = support_user_id
        self.db.commit()

        return event

    def update_event(self, event_id, location=None,
                     attendees=None, notes=None):

        event = self.db.query(Event).filter(
            Event.id == event_id
        ).first()

        if event is None:
            raise ValueError("Événement non trouvé")

        if self.current_user.role == Role.COMMERCIAL:
            raise PermissionError("Les COMMERCIAUX ne peuvent pas modifier")

        if self.current_user.role == Role.SUPPORT:
            if not event.support_contact_id:
                raise PermissionError("Non assigné")

            check_is_owner_or_gestion(
                self.current_user,
                event,
                "support_contact_id"
            )
        if location:
            event.location = location
        if attendees is not None:
            event.attendees = attendees
        if notes is not None:
            event.notes = notes
        self.db.commit()
        return event

    def get_event_by_id(self, event_id):
        return self.db.query(Event).filter(
            Event.id == event_id
        ).first()
