from os import system


def export_db_description() -> None:
    with open('./db_description.md') as f:
        _md: list[str] = f.readlines()

    proj: str = 'Project SWARDEN'
    db: str = "database_type: 'PostgreSQL'"
    md: str = ''.join(_md)
    struct: str = f"{proj} {{\n\t{db}\n\tNote: '''{md}'''}}\n\n"

    with open('schema.dbml', 'w') as f:
        f.write(
            '// Use DBML to define your database structure\n// Docs: https://dbml.dbdiagram.io/docs\n\n'
        )

        f.write(struct)


def export_tables() -> None:
    with open('_schema.dbml') as f:
        schema: list[str] = f.readlines()

    with open('schema.dbml', 'a') as f:
        f.writelines(schema)


def generate_docs() -> None:
    system('dbdocs build schema.dbml')


def main() -> None:
    export_db_description()
    export_tables()
    generate_docs()


if __name__ == '__main__':
    main()
