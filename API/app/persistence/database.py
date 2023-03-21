
from databases import Database
import sqlalchemy

DATABASE_URL = "sqlite:///./fabrik.db"


database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
dialect = sqlalchemy.dialects.sqlite.dialect()

async def init_tables():
    print("attempting to create tables")
    # Create tables
    for table in metadata.tables.values():
        # Set `if_not_exists=False` if you want the query to throw an
        # exception when the table already exists
        print("creating table", table)
        schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=dialect))
        await database.execute(query=query)
    print("all tables created!")
