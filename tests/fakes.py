from schemas import ProjectBlueprint


class FakeLLM:

    @property
    def model_name(self) -> str:
        return "fake-model"

    def generate(self, messages):
        return ProjectBlueprint(
            project_name="Test Project",
            business_outcome="Test business outcome.",
        )