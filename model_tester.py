import shrinking_model
import extended_model
import multiplication_model
import sum_model
import mysql.connector as connector
from mysql.connector import errorcode
from collections import Counter


def test_model(my_data, model_name):
    (event, background, draw_color, line_width, keep_going, screen, mat) = my_data
    if 'shrinking' in model_name:
        pattern = shrinking_model.get_pattern(mat)
    elif 'extended' in model_name:
        pattern = extended_model.get_pattern(mat)
    elif 'multiplication' in model_name:
        pattern = multiplication_model.get_pattern(mat)
    elif 'sum' in model_name:
        pattern = sum_model.get_pattern(mat)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        query = ("SELECT digit FROM {} WHERE pattern = {}".format(model_name, pattern))

        cursor.execute(query)
        digits = []
        for digit in cursor:
                digits.append(digit)

        guess1mount = guess2mount = 0
        try:
            print('*** TEST FOR {} ***'.format(model_name))
            guess1is = Counter(digits).most_common(2).pop(0)[0][0]
            guess1mount = Counter(digits).most_common(2).pop(0)[1]
            print('Guess 1 is :', guess1is)
        except IndexError:
            print('I could not guess a single number as a first guess.')

        try:
            guess2is = Counter(digits).most_common(2).pop(1)[0][0]
            guess2mount = Counter(digits).most_common(2).pop(1)[1]
            print('Guess 2 is :', guess2is)
        except IndexError:
            print('I could not guess a single number as a second guess.')

        sum = guess1mount + guess2mount
        try:
            print('Accuracy of :', guess1is, ': ', (guess1mount / sum) * 100, '%')
            print('Accuracy of :', guess2is, ': ', (guess2mount / sum) * 100, '%')
        except UnboundLocalError:
            print('I could not calculate the accuracy')

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
