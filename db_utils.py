"""
functions for interaction with the database.
"""
from db_secrets import DB_NAME, USER_NAME, PASSWORD, HOST
import pymysql


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or Noneinsert_into_user_input
    """
    try:
        conn = pymysql.connect(host=HOST,
                               user=USER_NAME,
                               password=PASSWORD,
                               db=DB_NAME,
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except:
        return None


def run_query(query, args=[], conn=None):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param query: a SQL query
    :return:
    """
    if conn == None:
        conn = create_connection()

    with conn.cursor() as cursor:
        if query.lower().startswith("select"):
            cursor.execute(query=query, args=args)
            return cursor.fetchall()
        else:
            cursor.execute(query=query, args=args)
    try:
        conn.commit()
    except Exception as e:
        print("ERROR OCCURED WHILE DB COMMIT --- DB_UTILS", e)


def insert_into_users(user_name, name, email):
    """
    :return:
    """
    sql_query = """insert into users (user_name,name,email) VALUES (%s,%s,%s)"""
    run_query(sql_query, [user_name, name, email])


def insert_into_udhaar(user_name, name, email, amount):
    sql_query = """insert into udhaars (user_name,name,email,amount) VALUES (%s,%s,%s,%s)"""
    run_query(sql_query, [user_name, name, email, amount])


def get_udhaars(user_name):
    sql_query = """select * from udhaars where user_name = "%s" """ % user_name
    return run_query(sql_query)

def get_udhaar(id):
    sql_query = """select * from udhaars where id = %s """ % id
    return run_query(sql_query)

def get_user_mail_and_name(user_name):
    sql_query = """select email,name from users where user_name = "%s" """ % user_name
    return run_query(sql_query)

def delete_udhaar(udhaar_id):
    sql_query = """DELETE from udhaars where id = %s""" % udhaar_id
    run_query(sql_query)


def get_user(user_name):
    sql_query = """SELECT * from users where user_name = "%s" """ % user_name
    return run_query(sql_query)
