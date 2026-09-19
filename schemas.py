from pydantic import BaseModel


class ProjectBlueprint(BaseModel):
    project_name: str
    business_outcome: str