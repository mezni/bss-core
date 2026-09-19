from schemas import ProjectBlueprint


class FakeLLM:
    model_name = "test-model"

    def invoke(self, messages):
        return ProjectBlueprint(
            project_name="Test Project",
            business_outcome="Test business outcome.",
        )