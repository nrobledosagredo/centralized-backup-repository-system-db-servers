import json
import sys
import os
from faker import Faker
import psycopg2

def generate_fake_data(config_file):
    config_file_path = os.path.join("config", config_file)
    with open(config_file_path) as f:
        config = json.load(f)

    fake = Faker()
    db_name = config["db_name"]
    num_records = config["num_records"]
    tables = config["tables"]

    connection = psycopg2.connect(
        host=config["db_host"],
        user=config["db_user"],
        password=config["db_password"],
        dbname=db_name,
    )

    for table in tables:
        table_name = table["name"]
        columns = table["columns"]
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY"

        for column in columns:
            create_table_query += f", {column['name']} VARCHAR(255)"

        create_table_query += ");"

        with connection.cursor() as cursor:
            cursor.execute(create_table_query)

        for _ in range(num_records):
            insert_query = f"INSERT INTO {table_name} ("
            insert_query += ", ".join(column["name"] for column in columns)
            insert_query += ") VALUES ("
            insert_query += ", ".join(
                "'" + str(getattr(fake, column["type"])()) + "'" for column in columns
            )
            insert_query += ");"

            with connection.cursor() as cursor:
                cursor.execute(insert_query)

        connection.commit()

    connection.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_fake_data.py <config_file>")
    else:
        config_file = sys.argv[1]
        generate_fake_data(config_file)