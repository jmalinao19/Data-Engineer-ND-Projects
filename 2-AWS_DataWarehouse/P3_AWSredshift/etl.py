import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    executes staging events and staging songs tables from sql_queries file
    @type cur -- object
    @param cur -- cursor object

    @type conn -- object
    @param conn -- database connection object

    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    inserts data from staging tables to landing tables (facts and dimension tables)
    @type cur -- object
    @param cur -- cursor object

    @type conn -- object
    @param conn -- database connection object
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()