import databases
import sqlalchemy
import sqlalchemy_utils as sau

from dms import settings

url = str(settings.DATABASE)
database: databases.Database = databases.Database(settings.DATABASE)
metadata = sqlalchemy.MetaData()


def create() -> None:
    engine = sqlalchemy.create_engine(url)
    if not sau.database_exists(url=url):
        sau.create_database(url=url)
    metadata.create_all(bind=engine)


def destroy() -> None:
    if sau.database_exists(url=url):
        sau.drop_database(url=url)
