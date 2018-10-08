import shrinking_model
import mysql.connector as connector
from mysql.connector import errorcode
from numpy import *


def learn_pattern(matrix, character):
    x = get_pattern(matrix)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO one_zero_multiplication"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")

        """add_pattern = ("INSERT INTO multiplication_model"
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
    matrix_transpose = matrix.transpose()
    arr1 = shrinking_model.dense_matrix(matrix)
    arr2 = shrinking_model.dense_matrix(matrix_transpose)
    arr = append(arr1, arr2)

    pattern = shrinking_model.dense_arr(arr)

    return ''.join(str(x) for x in pattern)
