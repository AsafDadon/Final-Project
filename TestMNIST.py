import shrinking_model
import extended_model
import multiplication_model
import struct as st
import numpy as np
import mysql.connector as connector
from mysql.connector import errorcode
from collections import Counter
import sys


def test_machine(mat, model_name):
    if 'shrinking' in model_name:
        pattern = shrinking_model.get_pattern(mat)
    elif 'extended' in model_name:
        pattern = extended_model.get_pattern(mat)
    elif 'multiplication' in model_name:
        pattern = multiplication_model.get_pattern(mat)
    elif 'sum_model' in model_name:
        pattern = multiplication_model.get_pattern(mat)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        query = ("SELECT digit FROM {} WHERE pattern = {}".format(model_name, pattern))

        cursor.execute(query)
        digits = []
        for digit in cursor:
            digits.append(digit)

        try:
            return int(Counter(digits).most_common(1).pop(0)[0][0])
        except IndexError:
            print('I could not guess a single number as a first guess.')
            return -1
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


def main():
    for arg in sys.argv[1:]:
        file_name = {'images': 'C:\\Users\\asafm\\PycharmProjects\\Final-Project\\samples\\t10k-images.idx3-ubyte',
                      'labels': 'C:\\Users\\asafm\\PycharmProjects\\Final-Project\\samples\\t10k-labels.idx1-ubyte'}
        labels_array = np.array([])

        data_types = {
            0x08: ('ubyte', 'B', 1),
            0x09: ('byte', 'b', 1),
            0x0B: ('>i2', 'h', 2),
            0x0C: ('>i4', 'i', 4),
            0x0D: ('>f4', 'f', 4),
            0x0E: ('>f8', 'd', 8)}

        for name in file_name.keys():
            if name == 'images':
                images_file = open(file_name[name], 'rb')
            if name == 'labels':
                labels_file = open(file_name[name], 'rb')

        images_file.seek(0)
        magic = st.unpack('>4B', images_file.read(4))
        if (magic[0] and magic[1]) or (magic[2] not in data_types):
            raise ValueError("File Format not correct")

        nDim = magic[3]
        print("Data is ", nDim, "-D")

        # offset = 0004 for number of images
        # offset = 0008 for number of rows
        # offset = 0012 for number of columns
        # 32-bit integer (32 bits = 4 bytes)
        images_file.seek(4)
        nImg = st.unpack('>I', images_file.read(4))[0]  # num of images/labels
        nR = st.unpack('>I', images_file.read(4))[0]  # num of rows
        nC = st.unpack('>I', images_file.read(4))[0]  # num of columns
        nBytes = nImg * nR * nC
        labels_file.seek(8)  # Since no. of items = no. of images and is already read
        print("no. of images :: ", nImg)
        print("no. of rows :: ", nR)
        print("no. of columns :: ", nC)

        # Read all data bytes at once and then reshape
        images_array = 255 - np.asarray(st.unpack('>' + 'B' * nBytes, images_file.read(nBytes))).reshape((nImg, nR, nC))
        labels_array = np.asarray(st.unpack('>' + 'B' * nImg, labels_file.read(nImg))).reshape((nImg, 1))

        sum = 0
        for i in range(10000):
            lable = labels_array[i][0]
            mat = range(784)
            mat = np.reshape(mat, (28, 28))
            for j in range(28):
                for h in range(28):
                    if images_array[i][j][h] == 255:
                        mat[j][h] = 0
                    else:
                        mat[j][h] = 1
            result = test_machine(mat, arg)
            if result == lable:
                sum += 1
                print('sum = ', sum)
                print('photos = ', i)

        print('===============================================================')
        print('Finish to Test the machine with MNIST dataset on {}'.format(arg))
        print('Accuracy of the machine is: ', (sum / 10000) * 100, '%')
        print('===============================================================')


if __name__ == "__main__":
    main()