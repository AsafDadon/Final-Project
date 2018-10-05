import shrinking_model
import extended_model
import multiplication_model
import sum_model
import struct as st
import numpy as np


def main():
    file_name = {'images': 'C:\\Users\\asafm\\PycharmProjects\\Final-Project\\samples\\train-images.idx3-ubyte',
                 'labels': 'C:\\Users\\asafm\\PycharmProjects\\Final-Project\\samples\\train-labels.idx1-ubyte'}
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

    for i in range(5000):
        lable = labels_array[i][0]
        mat = range(784)
        mat = np.reshape(mat, (28, 28))
        for j in range(28):
            for h in range(28):
                if images_array[i][j][h] == 255:
                    mat[j][h] = 0
                else:
                    mat[j][h] = 1
        print(mat)
        sum_model.learn_pattern(mat, lable)
        #shrinking_model.learn_pattern(mat, lable)
        #extended_model.learn_pattern(mat, lable)
        #multiplication_model.learn_pattern(mat, lable)
    print('Finish to load MNIST dataset')


if __name__ == "__main__":
    main()