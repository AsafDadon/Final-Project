import mysql.connector as connector
from mysql.connector import errorcode


def learn_pattern(matrix, character):
    x = get_pattern(matrix)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO shrinking_model"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")
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


def dense_matrix(matrix):
    consecutive_number = 0
    i = 0
    arr = []

    for j in range(matrix.__len__()):
        for i in range(matrix.__len__() - 1):
            if matrix[i][j] == 1 and matrix[i+1][j] == 0:
                consecutive_number = consecutive_number + 1
        if matrix[i+1][j] == 1:
            consecutive_number = consecutive_number + 1
        arr.append(consecutive_number)
        consecutive_number = 0
    return arr


def dense_arr(arr):
    pattern = []
    for i in range(arr.__len__() - 1):
        if arr[i] != arr[i+1]:
            pattern.append(arr[i])

    if pattern[pattern.__len__() - 1] != arr[i+1]:
        pattern.append(arr[i+1])
    return pattern


def get_pattern(matrix):
    arr = dense_matrix(matrix)
    arr = dense_arr(arr)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

