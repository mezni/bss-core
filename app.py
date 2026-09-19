import sys

from application import create_application
from schemas import GenerateBlueprintRequest


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            'Usage: uv run python app.py "<project idea>"'
        )

    project_idea = sys.argv[1]

    request = GenerateBlueprintRequest(
        project_idea=project_idea
    )

    application = create_application()

    response = application.generate_blueprint(request)

    print()
    print(f"Project Name: {response.blueprint.project_name}")
    print()
    print(
        f"Business Outcome: "
        f"{response.blueprint.business_outcome}"
    )
    print()
    print(f"Request ID: {response.telemetry.request_id}")
    print(
        f"Latency: "
        f"{response.telemetry.latency_seconds:.2f}s"
    )


if __name__ == "__main__":
    main()