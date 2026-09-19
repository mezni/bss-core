import sys

from generator import ProjectGenerator


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: uv run python app.py \"<project idea>\""
        )

    project_idea = sys.argv[1]

    generator = ProjectGenerator()
    blueprint = generator.generate(project_idea)

    print()
    print(f"Project Name: {blueprint.project_name}")
    print()
    print(f"Business Outcome: {blueprint.business_outcome}")


if __name__ == "__main__":
    main()