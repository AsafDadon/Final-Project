import numpy as np
import pygame


def convert_image_to_matrix(image, screen):
    # Draw 28x28 image of input
    a = image.ravel()
    a = (255 - a * 255).transpose()
    size = 28
    mat = range(784)
    mat = np.reshape(mat, (28, 28))
    for x in range(size):
        for y in range(size):
            z = x * 28 + y
            c = int(a[z])
            pygame.draw.rect(screen, (c, c, c), (x * 11 + 385, 15 + y * 11, 11, 11))
            if c == 255:
                mat[x][y] = 0
            else:
                mat[x][y] = 1
    return mat.transpose()


def focus_mat(matrix):
    up_row = down_row = left_col = right_col = None
    for i in range(matrix.__len__()):
        for j in range(matrix.__len__()):
            if matrix[i][j] == 1:
                up_row = i
                break
        if up_row is not None:
            break

    for i in range(matrix.__len__()):
        for j in range(matrix.__len__()):
            if matrix[j][i] == 1:
                left_col = i
                break
        if left_col is not None:
            break

    for i in range(matrix.__len__() - 1, 0, -1):
        for j in range(matrix.__len__() - 1, 0, -1):
            if matrix[i][j] == 1:
                down_row = i
                break
        if down_row is not None:
            break

    for i in range(matrix.__len__() - 1, 0, -1):
        for j in range(matrix.__len__() - 1, 0, -1):
            if matrix[j][i] == 1:
                right_col = i
                break
        if right_col is not None:
            break

    r = (down_row - up_row) + 1
    c = (right_col - left_col) + 1
    mat = range(r * c)
    mat = np.reshape(mat, (r, c))
    for i in range(up_row, down_row + 1):
        for j in range(left_col, right_col + 1):
            mat[i - up_row][j - left_col] = matrix[i][j]

    #print(mat)
    return mat
