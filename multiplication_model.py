import shrinking_model
import dal
from numpy import *


def learn_pattern(matrix, character, model_name):
    pattern = get_pattern(matrix)
    lable = str(character)
    dal.add_to_db(pattern, lable, model_name, False)


def get_pattern(matrix):
    matrix_transpose = matrix.transpose()
    arr1 = shrinking_model.dense_matrix(matrix)
    arr2 = shrinking_model.dense_matrix(matrix_transpose)
    arr = append(arr1, arr2)

    pattern = shrinking_model.dense_arr(arr)

    return ''.join(str(x) for x in pattern)
