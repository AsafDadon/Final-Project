import dal


def learn_pattern(matrix, character, model_name):
    pattern = get_pattern(matrix)
    lable = str(character)
    dal.add_to_db(pattern, lable, model_name, False)


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

