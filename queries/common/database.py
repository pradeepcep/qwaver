import pandas

from queries.models import Database


def get_column_list(database, user, table):
    engine = database.get_engine_with_user(user=user)
    query = f"select * from {table} where false;"
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
        try:
            df = pandas.read_sql(query, connection)
            return list(df.columns.values)
        except Exception as err:
            print(err)
            return None
