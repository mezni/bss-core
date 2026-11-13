# src/modules/customers/repository.py
from sqlalchemy.orm import Session
from src.modules.customers.models import Customer
from src.modules.customers.schemas import CustomerCreate


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: int, owner_id: int) -> Customer | None:
        return (
            self.db.query(Customer)
            .filter(Customer.id == customer_id, Customer.owner_id == owner_id)
            .first()
        )

    def get_all(self, owner_id: int, skip: int = 0, limit: int = 100) -> list[Customer]:
        return (
            self.db.query(Customer)
            .filter(Customer.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, obj_in: CustomerCreate, owner_id: int) -> Customer:
        db_obj = Customer(
            name=obj_in.name,
            email=obj_in.email,
            phone=obj_in.phone,
            owner_id=owner_id,
        )
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
