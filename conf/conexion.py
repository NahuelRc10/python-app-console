import mysql.connector

def get_connection(connector=mysql.connector):
    return connector.connect(host='localhost',
                             database='adminproyectos',
                             user='root',
                             password='root')

'''
def read_database_version():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * from roles;")
        db_version = cursor.fetchone()
        print("You are connected to MySQL version: ", db_version)
    except (Exception, mysql.connector.Error) as error:
        print("Error while getting data", error)

print("Question 1: Print Database version")
'''
