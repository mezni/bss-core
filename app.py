from generator import ProjectGenerator


def main() -> None:
    generator = ProjectGenerator()

    result = generator.generate(
        "Build an AI system that classifies corporate documents."
    )

    print(result)


if __name__ == "__main__":
    main()