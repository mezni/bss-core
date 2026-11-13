#!/usr/bin/env python3
"""Synthetic data generator for bss-core.

Creates 5 users with valid passwords and 50 customers linked to those users.
Uses direct SQLAlchemy DB access with Faker (bypasses API for speed).
"""
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base, SQLALCHEMY_DATABASE_URL
from src.modules.auth.models import User
from src.modules.customers.models import Customer
from src.core.security import SECRET_KEY, ALGORITHM, get_password_hash, create_access_token
from src.core.security import SECRET_KEY, ALGORITHM


# Use in-memory SQLite for generation (don't affect the app.db)
_gen_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

# Create all tables defined in the app's Base metadata
Base.metadata.create_all(bind=_gen_engine)

_gen_session = sessionmaker(autocommit=False, autoflush=False, bind=_gen_engine)
_gen_session = sessionmaker(autocommit=False, autoflush=False, bind=_gen_engine)


def _get_gen_session():
    return _gen_session()


def _valid_password():
    """Return a password meeting complexity requirements."""
    return "ValidPass1!"


def _rand_string(length=8):
    """Generate a random lowercase string."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _rand_email(prefix="user"):
    """Generate a unique email."""
    suffix = "".join(random.choices(string.digits, k=4))
    return f"{prefix}_{suffix}@test.com"


def _rand_phone():
    """Generate a random phone number."""
    return f"+1-555-{random.randint(100, 9999)}"


def _generate_users(n=5):
    """Register n users in the generator DB and return their emails + sessions."""
    session = _get_gen_session()
    users = []
    for i in range(n):
        email = _rand_email(f"user{i}")
        user = User(
            email=email,
            hashed_password=get_password_hash("ValidPass1!"),
            role="user",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access token for this user
        access_token = create_access_token({"sub": user.email})
        users.append({"email": email, "token": access_token, "id": user.id})
    session.close()
    return users


def _generate_customers(user_data, customers_per_user=10):
    """Create customers for each user in the generator DB.

    Args:
        user_data: list of dicts with 'email', 'token', 'id' keys
        customers_per_user: how many customers per user (default 10)
    """
    session = _get_gen_session()
    for u in user_data:
        for i in range(customers_per_user):
            customer = Customer(
                name=f"Customer {u['email'].split('@')[0]} {i}",
                email=_rand_email(f"c{i}") + "@test.com",
                phone=_rand_phone(),
                owner_id=u["id"],
            )
            session.add(customer)
        session.commit()
    session.close()


def main():
    """Run the full synthetic data generation."""
    print("Generating 5 users in memory DB...")
    user_data = _generate_users(5)
    for u in user_data:
        print(f"  - {u['email']} (id={u['id']})")

    print("Generating 50 customers (10 per user)...")
    _generate_customers(user_data, customers_per_user=10)

    print("Synthetic data generation complete!")


if __name__ == "__main__":
    main()