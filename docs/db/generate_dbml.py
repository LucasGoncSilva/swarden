from os import system


def export_db_description():
    with open('./db_description.md', 'r') as f:
        md = f.readlines()

    struct = f'Project SWARDEN {{\n\tdatabase_type: \'PostgreSQL\'\n\tNote: \'\'\'{"".join(md)}\'\'\'}}\n\n'
    
    with open('schema.dbml', 'w') as f:
        f.write('// Use DBML to define your database structure\n// Docs: https://dbml.dbdiagram.io/docs\n\n')

        f.write(struct)


def export_tables():
    with open('_schema.dbml', 'r') as f:
        schema = f.readlines()

    with open('schema.dbml', 'a') as f:
        f.writelines(schema)


def generate_docs():
    system('dbdocs build schema.dbml')


def main():
    export_db_description()
    export_tables()
    generate_docs()


if __name__ == '__main__':
    main()
