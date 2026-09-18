from pydantic import BaseModel


class ProjectIdea(BaseModel):
    """A high-level AI project idea provided by the user."""

    idea: str


class Blueprint(BaseModel):
    """Structured architecture blueprint placeholder."""

    name: str
    business_outcome: str