from sqlalchemy import Column, Integer, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database.config import Base

# Classe contrat
class Contract(Base):
    """Modèle pour les contrats."""
    
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    remaining_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_signed = Column(Boolean, default=False)

    # Relations 
    client = relationship("Client", back_populates="contracts")
    commercial_contact = relationship("User", back_populates="contracts_as_commercial")

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "commercial_contact_id": self.commercial_contact_id,
            "total_amount": float(self.total_amount),
            "remaining_amount": float(self.remaining_amount),
            "created_at": self.created_at,
            "is_signed": self.is_signed
        }
