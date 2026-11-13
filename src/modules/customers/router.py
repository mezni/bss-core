# src/modules/customers/router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.modules.auth.dependencies import get_current_user
from src.modules.auth.models import User
from src.modules.customers.repository import CustomerRepository
from src.modules.customers.schemas import CustomerCreate, CustomerResponse

router = APIRouter(tags=["Customers"])


@router.post(
    "/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer_in: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  repo = CustomerRepository(db)
  return repo.create(customer_in, owner_id=current_user.id)


@router.get("/", response_model=list[CustomerResponse])
def list_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  repo = CustomerRepository(db)
  return repo.get_all(owner_id=current_user.id, skip=skip, limit=limit)
