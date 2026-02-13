from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from src.database.config import Base
from sqlalchemy.orm import relationship

# les roles 
class Role(enum.Enum):
    COMMERCIAL = "commercial"
    SUPPORT = "support"
    GESTION = "gestion"

# la classe User
class User(Base):
    """Modèle pour les collaborateurs Epic Events."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    # Relations
    clients_as_commercial = relationship("Client", back_populates="commercial_contact")
    contracts_as_commercial = relationship("Contract", back_populates="commercial_contact")
    events_as_support = relationship("Event", back_populates="support_contact")
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
