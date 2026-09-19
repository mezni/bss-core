import sys

from application import create_application
from exceptions import ProjectGenerationError
from logging_config import configure_logging


def main() -> None:
    configure_logging()

    if len(sys.argv) < 2:
        raise SystemExit(
            'Usage: uv run python app.py "<project idea>"'
        )

    project_idea = sys.argv[1]

    application = create_application()

    try:
        result = application.generate_blueprint(project_idea)

    except ValueError as exc:
        raise SystemExit(f"Input error: {exc}") from exc

    except ProjectGenerationError as exc:
        raise SystemExit(f"Generation error: {exc}") from exc

    print()
    print(f"Project Name: {result.blueprint.project_name}")
    print()
    print(f"Business Outcome: {result.blueprint.business_outcome}")
    print()
    print(f"Request ID: {result.telemetry.request_id}")
    print(f"Latency: {result.telemetry.latency_seconds:.3f}s")


if __name__ == "__main__":
    main()