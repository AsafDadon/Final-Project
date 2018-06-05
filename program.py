import pygame
from numpy import *
import numpy as np
import scipy.io as sio
from pygame.locals import *
from collections import Counter
import mysql.connector as connector
from mysql.connector import errorcode
import pygame.font, pygame.event, pygame.draw

changed = False
screen = None


def convert_image_to_matrix(image, screen):
    # Draw 30x30 image of input
    a = image.ravel()
    a = (255 - a * 255).transpose()
    size = 30
    mat = range(900)
    mat = np.reshape(mat, (30, 30))
    for x in range(size):
        for y in range(size):
            z = x * 30 + y
            c = int(a[z])
            pygame.draw.rect(screen, (c, c, c), (x * 11 + 385, 15 + y * 11, 11, 11))
            if c == 255:
                mat[x][y] = 0
            else:
                mat[x][y] = 1
    return mat.transpose()


def draw_pixelated(image, screen):
    # Draw 30x30 image of input
    a = image.ravel()
    a = (255 - a * 255).transpose()
    size = 30
    for x in range(size):
        for y in range(size):
            z = x * 30 + y
            c = int(a[z])
            pygame.draw.rect(screen, (c, c, c), (x * 11 + 385, 15 + y * 11, 11, 11))


def calculate_image(background, screen, theta1, theta2, line_width):
    # Crop and resize the input
    global changed
    focus_surface = pygame.surfarray.array3d(background)
    focus = abs(1 - focus_surface / 255)
    focus = np.mean(focus, 2)
    x = []
    x_axis = np.sum(focus, axis=1)
    for i, v in enumerate(x_axis):
        if v > 0:
            x.append(i)
            break
    for i, v in enumerate(x_axis[::-1]):
        if v > 0:
            x.append(len(x_axis) - i)
            break

    y = []
    y_axis = np.sum(focus, axis=0)
    for i, v in enumerate(y_axis):
        if v > 0:
            y.append(i)
            break
    for i, v in enumerate(y_axis[::-1]):
        if v > 0:
            y.append(len(y_axis) - i)
            break

    try:
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        bound = focus.shape[0]
        if dx > dy:
            d = dx - dy
            y0t = y[0] - d // 2
            y1t = y[1] + d // 2 + d % 2
            if y0t < 0: y0t = y[0]; y1t = y[1] + d
            if y1t > bound: y0t = y[0] - d; y1t = y[1]
            y[0], y[1] = y0t, y1t
        else:
            d = dy - dx
            x0t = x[0] - d // 2
            x1t = x[1] + d // 2 + d % 2
            if x0t < 0: x0t = x[0]; x1t = x[1] + d
            if x1t > bound: x0t = x[0] - d; x1t = x[1]
            x[0], x[1] = x0t, x1t
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        changed = True
        crop_surf = pygame.Surface((dx, dy))
        crop_surf.blit(background, (0, 0), (x[0], y[0], x[1], y[1]), special_flags=BLEND_RGBA_MAX)
        scaled_background = pygame.transform.smoothscale(crop_surf, (30, 30))

        image = pygame.surfarray.array3d(scaled_background)
        image = abs(1 - image / 253)
        image = np.mean(image, 2)
        image = np.matrix(image.ravel())

        mat = convert_image_to_matrix(image, screen)

        (x, y) = screen.get_size()

    except:
        image = np.zeros((30, 30))

    return mat


def get_key():
    # Get key event
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message):
    # Print a message in a box on the screen
    font_object = pygame.font.Font(None, 120)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height()) - 170,
                      70, 90), 0)
    if len(message) != 0:
        screen.blit(font_object.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 110, (screen.get_height()) - 168))
        pygame.display.flip()


def ask(screen, question):
    # create input box for entering correct value of y
    pygame.font.init()
    current_string = str()
    display_box(screen, question + " " + current_string + "")

    while 1:
        in_key = get_key()

        if in_key == K_BACKSPACE:
            current_string = current_string[0:-1]

        elif in_key == K_RETURN:
            break

        elif in_key == K_MINUS:
            current_string.append("_")

        elif in_key <= 127:
            current_string += (chr(in_key))

        display_box(screen, question + " " + current_string + "")

    return current_string


def check_keys(my_data):
    # test for various keyboard inputs
    (event, background, draw_color, line_width, keep_going, screen, mat) = my_data

    if event.key == pygame.K_q:
        keep_going = False

    elif event.key == pygame.K_c:
        background.fill((255, 255, 255))
        draw_pixelated(np.zeros((30, 30)), screen)

    elif event.key == pygame.K_s:
        answer = int(ask(screen, ""))
        learn_pattern(mat, answer)

    elif event.key == pygame.K_t:
        user_test(my_data)

    background.fill((255, 255, 255))
    draw_pixelated(np.zeros((30, 30)), screen)

    my_data = (event, background, draw_color, line_width, keep_going)
    return my_data


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


def learn_pattern(matrix, character):
    arr = dense_matrix(matrix)
    arr = dense_arr(arr)
    x = ''.join(str(x) for x in arr)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO patterns"
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


def get_pattern(matrix):
    arr = dense_matrix(matrix)
    arr = dense_arr(arr)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern


def user_test(my_data):
    (event, background, draw_color, line_width, keep_going, screen, mat) = my_data
    pattern = get_pattern(mat)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        query = ("SELECT digit FROM patterns WHERE pattern = {}".format(pattern))

        cursor.execute(query)
        digits = []
        for digit in cursor:
            digits.append(digit)

        guess1mount = guess2mount = 0
        try:
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


def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((730, 450))
    pygame.display.set_caption("Handwriting recognition By Patterns")

    background = pygame.Surface((360 ,360))
    background.fill((255, 255, 255))
    background2 = pygame.Surface((360 ,360))
    background2.fill((255, 255, 255))

    clock = pygame.time.Clock()
    keep_going = True
    line_start = (0, 0)
    draw_color = (0, 200, 0)
    line_width = 10

    input_theta = sio.loadmat('scaledTheta.mat')
    theta = input_theta['t']
    num_hidden = 25
    num_input = 900
    num_labels = 10

    theta1 = np.reshape(theta[:num_hidden * (num_input + 1)], (num_hidden, -1))
    theta2 = np.reshape(theta[num_hidden * (num_input + 1):], (num_labels, -1))

    pygame.display.update()
    image = None

    while keep_going:

        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keep_going = False

            elif event.type == pygame.MOUSEMOTION:
                line_end = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(background, draw_color, line_start, line_end, line_width)
                line_start = line_end

            elif event.type == pygame.MOUSEBUTTONUP:
                screen.fill((0, 0, 0))
                screen.blit(background2, (370, 0))
                mat = calculate_image(background, screen, theta1, theta2, line_width)

            elif event.type == pygame.KEYDOWN:
                my_data = (event, background, draw_color, line_width, keep_going, screen, mat)
                my_data = check_keys(my_data)
                (event, background, draw_color, line_width, keep_going) = my_data

        screen.blit(background, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
