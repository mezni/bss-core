# src/modules/customers/models.py
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    owner_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )  # Links customer to a user

    # Optional relationship back to User
    owner = relationship("User", backref="customers")
