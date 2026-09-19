from schemas import ProjectBlueprint


def main() -> None:
    blueprint = ProjectBlueprint(
        project_name=" ",
        business_outcome=(
            "Automatically classify corporate documents into "
            "appropriate security categories."
        ),
    )

    print(blueprint)
    print(blueprint.model_dump())


if __name__ == "__main__":
    main()