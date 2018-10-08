import mysql.connector as connector
from mysql.connector import errorcode


def add_to_db(pattern, lable, choose_model, one_zero):
    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()
        insert_into = "INSERT INTO " + choose_model + " (pattern, digit)" + " VALUES (%s, %s)"
        if one_zero is True:
            add_pattern = insert_into
        else:
            add_pattern = insert_into

        data_pattern = (pattern, lable)

        cursor.execute(add_pattern, data_pattern)
        cnx.commit()

        cursor.close()

    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    else:
        cnx.close()