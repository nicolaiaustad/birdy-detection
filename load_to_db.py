import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_postgres(csv_file, db_name, user, password, host, port, table_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Print the DataFrame to verify its content
    print(df.head())

    # Create the connection string
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    # Create a SQLAlchemy engine
    engine = create_engine(connection_string)

    # Write the DataFrame to the PostgreSQL table
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"Data loaded successfully into {table_name} table in {db_name} database.")

