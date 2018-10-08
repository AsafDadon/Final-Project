import dal


def learn_pattern(matrix, character, model_name):
    pattern = get_pattern(matrix)
    lable = str(character)
    dal.add_to_db(pattern, lable, model_name, False)


def dense_matrix(matrix):
    consecutive_number = 0
    arr = []
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1):
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

    if pattern.__len__() == 0:
        pattern.append(arr[0])
        return pattern

    if pattern[pattern.__len__() - 1] != arr[i+1]:
        pattern.append(arr[i+1])
    return pattern


def get_pattern(matrix):
    arr = dense_matrix(matrix)
    arr = dense_arr(arr)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

