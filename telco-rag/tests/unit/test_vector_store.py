import pytest

from telco_rag.retrieval import PostgresVectorStore


def make_store(dimensions: int = 3) -> PostgresVectorStore:
    return PostgresVectorStore(
        dsn="postgresql://unused",
        dimensions=dimensions,
        connect=lambda *_args, **_kwargs: None,
    )


def test_vector_store_rejects_invalid_dimensions() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        make_store(0)


def test_validate_vector_accepts_correct_dimensions() -> None:
    store = make_store(3)

    store._validate_vector([0.1, 0.2, 0.3])


def test_validate_vector_rejects_wrong_dimensions() -> None:
    store = make_store(3)

    with pytest.raises(ValueError, match="Expected 3 dimensions"):
        store._validate_vector([0.1, 0.2])


def test_search_rejects_nonpositive_limit() -> None:
    store = make_store(3)

    with pytest.raises(ValueError, match="limit must be greater than zero"):
        store.search_similar([0.1, 0.2, 0.3], limit=0)


def test_store_requires_database_url() -> None:
    with pytest.raises(ValueError, match="DATABASE_URL"):
        PostgresVectorStore(dsn="", dimensions=3)
