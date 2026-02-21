from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.config import Base

# Classe Event
class Event(Base):
    """Modèle pour les événements."""
    
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    support_contact_id = Column(Integer, ForeignKey("users.id"))
    event_date_start = Column(DateTime, nullable=False)
    event_date_end = Column(DateTime, nullable=False)
    location = Column(String(500), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    # Relations 
    contract = relationship("Contract", back_populates="event")
    client = relationship("Client", back_populates="events")
    support_contact = relationship("User", back_populates="events_as_support")

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "client_id": self.client_id,
            "support_contact_id": self.support_contact_id,
            "event_date_start": self.event_date_start,
            "event_date_end": self.event_date_end,
            "location": self.location,
            "attendees": self.attendees,
            "notes": self.notes
        }
