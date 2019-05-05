import mysql.connector


def create_database(db_host="localhost", db_user="username", db_pass="password", db_name="database"):
    my_db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        auth_plugin='caching_sha2_password'
    )
    db_cursor = my_db.cursor()
    db_cursor.execute("CREATE DATABASE `%s`" % (db_name))


def create_tables(db_host="localhost", db_user="username", db_pass="password", db_name="database"):
    my_db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        passwd=db_pass,
        database=db_name,
        auth_plugin='caching_sha2_password'
    )
    db_cursor = my_db.cursor()

    db_cursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")
    db_cursor.execute(
        "CREATE TABLE exercises (id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL, grade INT,  date_begin DATE NOT NULL, date_end DATE)")


if __name__ == "__main__":
    # create_database()
    # create_tables()
