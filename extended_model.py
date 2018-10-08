import shrinking_model
import dal


def learn_pattern(matrix, character, model_name):
    pattern = get_pattern(matrix)
    lable = str(character)
    dal.add_to_db(pattern, lable, model_name, False)


def get_pattern(matrix):
    arr = shrinking_model.dense_matrix(matrix)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

