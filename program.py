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

#Draw 30x30 image of input
def ConvertImageToMatrix(image, screen):
    A = image.ravel()
    A = (255 - A * 255).transpose()
    size = 30
    mat = range(900)
    mat = np.reshape(mat, (30, 30))
    for x in range(size):
        for y in range(size):
            z = x * 30 + y
            c = int(A[z])
            pygame.draw.rect(screen, (c, c, c), (x * 11 + 385, 15 + y * 11, 11, 11))
            if c == 255:
                mat[x][y] = 0
            else:
                mat[x][y] = 1
    #print(mat.transpose())
    return mat.transpose()

#Draw 30x30 image of input
def drawPixelated(image, screen):
    A = image.ravel()
    A = (255 - A * 255).transpose()
    size = 30
    for x in range(size):
        for y in range(size):
            z = x * 30 + y
            c = int(A[z])
            pygame.draw.rect(screen, (c, c, c), (x * 11 + 385, 15 + y * 11, 11, 11))

#Crop and resize the input
def calculateImage(background, screen, Theta1, Theta2, lineWidth):
    global changed
    focusSurface = pygame.surfarray.array3d(background)
    focus = abs(1 - focusSurface / 255)
    focus = np.mean(focus, 2)
    x = []
    xaxis = np.sum(focus, axis=1)
    for i, v in enumerate(xaxis):
        if v > 0:
            x.append(i)
            break
    for i, v in enumerate(xaxis[::-1]):
        if v > 0:
            x.append(len(xaxis) - i)
            break

    y = []
    yaxis = np.sum(focus, axis=0)
    for i, v in enumerate(yaxis):
        if v > 0:
            y.append(i)
            break
    for i, v in enumerate(yaxis[::-1]):
        if v > 0:
            y.append(len(yaxis) - i)
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
        scaledBackground = pygame.transform.smoothscale(crop_surf, (30, 30))

        image = pygame.surfarray.array3d(scaledBackground)
        image = abs(1 - image / 253)
        image = np.mean(image, 2)
        image = np.matrix(image.ravel())

        mat = ConvertImageToMatrix(image, screen)

        (x, y) = screen.get_size()

    except:
        image = np.zeros((30, 30))

    return mat

#Get key event
def get_key():

    while 1:
        event = pygame.event.poll()

        if event.type == KEYDOWN:
            return event.key

        else:
            pass

#Print a message in a box on the screen
def display_box(screen, message):

    fontobject = pygame.font.Font(None, 120)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height()) - 170,
                      70, 90), 0)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 110, (screen.get_height()) - 168))
        pygame.display.flip()

#create input box for entering correct value of y
def ask(screen, question):

    pygame.font.init()
    current_string = str()
    display_box(screen, question + " " + current_string + "")

    while 1:
        inkey = get_key()

        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]

        elif inkey == K_RETURN:
            break

        elif inkey == K_MINUS:
            current_string.append("_")

        elif inkey <= 127:
            current_string += (chr(inkey))

        display_box(screen, question + " " + current_string + "")

    return current_string

#test for various keyboard inputs
def checkKeys(myData):

    (event, background, drawColor, lineWidth, keepGoing, screen, mat) = myData

    if event.key == pygame.K_q:
        keepGoing = False

    elif event.key == pygame.K_c:
        background.fill((255, 255, 255))
        drawPixelated(np.zeros((30, 30)), screen)

    elif event.key == pygame.K_s:
        answer = int(ask(screen, ""))
        learnPattern(mat, answer)

    elif event.key == pygame.K_t:
        userTest(myData)

    background.fill((255, 255, 255))
    drawPixelated(np.zeros((30, 30)), screen)

    myData = (event, background, drawColor, lineWidth, keepGoing)
    return myData

def denseMatrix(matrix):

    consecutiveNumber = 0
    i = 0
    arr = []

    for j in range(matrix.__len__()):
        for i in range(matrix.__len__() - 1):
            if matrix[i][j] == 1 and matrix[i+1][j] == 0:
                consecutiveNumber = consecutiveNumber + 1
        if matrix[i+1][j] == 1:
            consecutiveNumber = consecutiveNumber + 1
        arr.append(consecutiveNumber)
        consecutiveNumber = 0

    #print(arr)
    return arr

def denseArr(arr):
    pattern = []

    for i in range(arr.__len__() - 1):
        if arr[i] != arr[i+1]:
            pattern.append(arr[i])

    if pattern[pattern.__len__() - 1] != arr[i+1]:
        pattern.append(arr[i+1])

    #print(str(pattern))
    return pattern

def learnPattern(matrix, character):
    arr = denseMatrix(matrix)
    arr = denseArr(arr)
    x = ''.join(str(x) for x in arr)
    y = str(character)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        add_pattern = ("INSERT INTO patterns"
                       "(pattern, digit)"
                       "VALUES (%s, %s)")
        data_pattern= (x, y)

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

def getPattern(matrix):
    arr = denseMatrix(matrix)
    arr = denseArr(arr)
    pattern = "{x}".format(x=''.join(str(x) for x in arr))
    return pattern

def userTest(myData):
    (event, background, drawColor, lineWidth, keepGoing, screen, mat) = myData
    flag = False
    pattern = getPattern(mat)

    try:
        cnx = connector.connect(user='admin', password='123456', database='hand_write_recognition')
        cursor = cnx.cursor()

        query = ("SELECT digit FROM patterns WHERE pattern = {}".format(pattern))

        cursor.execute(query)
        digits = []
        for digit in cursor:
            digits.append(digit)

        print("=========================")
        print("guess 1     |     guess 2")
        print("=========================")
        print(Counter(digits).most_common(2))
        print("=========================")

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
    keepGoing = True
    lineStart = (0, 0)
    drawColor = (0, 200, 0)
    lineWidth = 10

    inputTheta = sio.loadmat('scaledTheta.mat')
    theta = inputTheta['t']
    num_hidden = 25
    num_input = 900
    num_lables = 10

    Theta1 = np.reshape(theta[:num_hidden * (num_input + 1)], (num_hidden, -1))
    Theta2 = np.reshape(theta[num_hidden * (num_input + 1):], (num_lables, -1))

    pygame.display.update()
    image = None

    while keepGoing:

        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.MOUSEMOTION:
                lineEnd = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    pygame.draw.line(background, drawColor, lineStart, lineEnd, lineWidth)
                lineStart = lineEnd

            elif event.type == pygame.MOUSEBUTTONUP:
                screen.fill((0, 0, 0))
                screen.blit(background2, (370, 0))
                mat = calculateImage(background, screen, Theta1, Theta2, lineWidth)

            elif event.type == pygame.KEYDOWN:
                myData = (event, background, drawColor, lineWidth, keepGoing, screen, mat)
                myData = checkKeys(myData)
                (event, background, drawColor, lineWidth, keepGoing) = myData

        screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()