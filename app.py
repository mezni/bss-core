from generator import ProjectGenerator


def main() -> None:
    generator = ProjectGenerator()

    blueprint = generator.generate(
        "Build an AI system that classifies corporate documents."
    )

    print(f"Project Name: {blueprint.project_name}")
    print(f"Business Outcome: {blueprint.business_outcome}")

    print(blueprint.model_dump())


if __name__ == "__main__":
    main()