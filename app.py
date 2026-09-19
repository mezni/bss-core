import sys

from exceptions import ProjectGenerationError
from generator import ProjectGenerator


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            'Usage: uv run python app.py "<project idea>"'
        )

    project_idea = sys.argv[1]

    try:
        generator = ProjectGenerator()
        blueprint = generator.generate(project_idea)

    except ValueError as exc:
        raise SystemExit(f"Input error: {exc}") from exc

    except ProjectGenerationError as exc:
        raise SystemExit(f"Generation error: {exc}") from exc

    print()
    print(f"Project Name: {blueprint.project_name}")
    print()
    print(f"Business Outcome: {blueprint.business_outcome}")


if __name__ == "__main__":
    main()