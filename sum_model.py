import mysql.connector as connector
from mysql.connector import errorcode


def learn_pattern(matrix, character):
    x = get_pattern(matrix)
    print(x)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO one_zero_sum"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")

        """add_pattern = ("INSERT INTO sum_model"
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


def sum_matrix(matrix):
    row_counter = 0
    col_counter = 0
    row = []
    col = []

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                row_counter = row_counter + 1
        row.append(row_counter)
        row_counter = 0

    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            if matrix[i][j] == 1:
                col_counter = col_counter + 1
        col.append(col_counter)
        col_counter = 0

    row.extend(col)
    return row


def dense_arr(arr):
    pattern = []
    for i in range(arr.__len__() - 1):
        if arr[i] != arr[i+1]:
            pattern.append(arr[i])

    if pattern[pattern.__len__() - 1] != arr[i+1]:
        pattern.append(arr[i+1])
    return pattern


def get_pattern(matrix):
    arr = sum_matrix(matrix)
    arr = dense_arr(arr)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

