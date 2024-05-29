from sqlalchemy import create_engine, MetaData, Table

# Create engine
engine = create_engine('sqlite:///books.db')

# Initialize the metadata object
meta = MetaData()

# Reflect the existing database into a new model
meta.reflect(bind=engine)

to_be_delete_table = 'Authors'

# Drop the Ratings table if it exists
if to_be_delete_table in meta.tables:
    ratings_table = Table(to_be_delete_table, meta)
    ratings_table.drop(engine)
    print(f"{to_be_delete_table} table dropped.")
else:
    print(f"{to_be_delete_table} table does not exist.")