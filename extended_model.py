import shrinking_model
import mysql.connector as connector
from mysql.connector import errorcode


def learn_pattern(matrix, character):
    x = get_pattern(matrix)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO one_zero_extended"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")

        """add_pattern = ("INSERT INTO extended_model"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")"""
        data_pattern = (x, y)

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


def get_pattern(matrix):
    arr = shrinking_model.dense_matrix(matrix)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

