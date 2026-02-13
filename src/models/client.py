from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.config import Base

# La classe client
class Client(Base):
    """Modèle pour les clients."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(30))
    company_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    
    # Clé étrangère vers l'utilisateur (commercial)
    commercial_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relations
    commercial_contact = relationship("User", back_populates="clients_as_commercial")
    contracts = relationship("Contract", back_populates="client", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="client")
    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "company_name": self.company_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
