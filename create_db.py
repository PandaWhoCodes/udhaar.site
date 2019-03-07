from db_secrets import DB_NAME, USER_NAME, PASSWORD, HOST
import pymysql


def create_connection(DB_NAME):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = pymysql.connect(host=HOST,
                               user=USER_NAME,
                               password=PASSWORD,
                               db=DB_NAME,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)

        return conn
    except Exception as e:
        print("Connection to the database could not be created: ", e)
        return None


def create_tables(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        conn.commit()
    except Exception as e:
        print("Tables could not be created:", e)


def create_db():
    """
    A function used to create a database file to store all the data
    """
    connection = create_connection(DB_NAME)
    sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                  user_id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                  user_name text,
                                  name text,
                                  email text
                                ); """
    sql_create_user_input_table = """ CREATE TABLE IF NOT EXISTS udhaars (
                                  id INTEGER PRIMARY KEY AUTO_INCREMENT,
                                  user_name text NOT NULL,
                                  name text,
                                  email text,
                                  amount FLOAT
                                ); """

    create_tables(conn=connection, create_table_sql=sql_create_users_table)
    create_tables(conn=connection, create_table_sql=sql_create_user_input_table)


if __name__ == '__main__':
    create_connection(DB_NAME)
    create_db()
