"""
This is a Tetris game I created myself using python and pygame/simpleaudio modules.
The goal was to create a tetris game WITHOUT object-oriented programming.
Game music is from original Tetris game, and I DO NOT OWN THE MUSIC.
The game uses data from data folder. Boxes were created using Windows Paint.
Also, the game uses config.dat file in order to store the game options and high score.
The game uses 2 fixed resolutions, 525x675 and 600x900.
I used simpleaudio for playing sound because i had some compile errors with pygame
Game was finished on October 2020.
"""
import pygame
import random
import time
import simpleaudio as sa

# initialize the pygame
pygame.init()

# create the screen (weight,height) Coordinate system start from top left corner
config_file = open("data/config.dat", "r+")
config_file.seek(27)
resize_factor_file = config_file.read(1)
if resize_factor_file == "1":
    resize_factor = 1
else:
    resize_factor = 0.75
resize_factor_changed = False
screen = pygame.display.set_mode((int(resize_factor * 700), int(resize_factor * 900)))

# Title and Icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load("data/icon.png")
pygame.display.set_icon(icon)

# Music
music_track = sa.WaveObject.from_wave_file('data/music.wav')

# Import box colors
red_box = pygame.image.load("data/red40.png")
green_box = pygame.image.load("data/green40.png")
blue_box = pygame.image.load("data/blue40.png")
yellow_box = pygame.image.load("data/yellow40.png")
orange_box = pygame.image.load("data/orange40.png")
wall = pygame.image.load("data/wall40.png")
background = pygame.image.load("data/background40.png")
if resize_factor == 0.75:
    red_box = pygame.image.load("data/red30.png")
    green_box = pygame.image.load("data/green30.png")
    blue_box = pygame.image.load("data/blue30.png")
    yellow_box = pygame.image.load("data/yellow30.png")
    orange_box = pygame.image.load("data/orange30.png")
    wall = pygame.image.load("data/wall30.png")
    background = pygame.image.load("data/background30.png")

# Put the box objects in a dictionary with key numbers
color_dict = {1: red_box,
              2: green_box,
              3: blue_box,
              4: yellow_box,
              5: orange_box}

# Every box of the game matrix has a place in the bellow list.
# 0 means that not a colored box will be displayed.
# 1-5 means that a colored box will be displayed
game_matrix = [[0 for i in range(10)] for j in range(20)]


# In this function the shape of the spawned blocks is formed
# The shape of the block is given by the number 1 in the following matrix
# Every shape if identified by the number_of_shape and number_of_rotation
def shape_format(number_of_shape, number_of_rotation):
    shape_to_return = [[0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 0, 0]]

    if number_of_shape == 1:
        if number_of_rotation == 1:
            shape_to_return = [[0, 0, 0, 0],
                               [1, 1, 1, 1],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 0, 1, 0],
                               [0, 0, 1, 0],
                               [0, 0, 1, 0],
                               [0, 0, 1, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [1, 1, 1, 1],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 1, 0, 0]]
    elif number_of_shape == 2:
        if number_of_rotation == 1:
            shape_to_return = [[1, 0, 0, 0],
                               [1, 1, 1, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 1, 1, 0],
                               [0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [1, 1, 1, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [1, 1, 0, 0],
                               [0, 0, 0, 0]]
    elif number_of_shape == 3:
        if number_of_rotation == 1:
            shape_to_return = [[0, 0, 1, 0],
                               [1, 1, 1, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [1, 1, 1, 0],
                               [1, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[1, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
    elif number_of_shape == 4:
        if number_of_rotation == 1:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 1, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 1, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 1, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 1, 0]]
    elif number_of_shape == 5:
        if number_of_rotation == 1:
            shape_to_return = [[0, 1, 1, 0],
                               [1, 1, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [0, 1, 1, 0],
                               [1, 1, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[1, 0, 0, 0],
                               [1, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
    elif number_of_shape == 6:
        if number_of_rotation == 1:
            shape_to_return = [[0, 1, 0, 0],
                               [1, 1, 1, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [1, 1, 1, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[0, 1, 0, 0],
                               [1, 1, 0, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
    elif number_of_shape == 7:
        if number_of_rotation == 1:
            shape_to_return = [[1, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 2:
            shape_to_return = [[0, 0, 1, 0],
                               [0, 1, 1, 0],
                               [0, 1, 0, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 3:
            shape_to_return = [[0, 0, 0, 0],
                               [1, 1, 0, 0],
                               [0, 1, 1, 0],
                               [0, 0, 0, 0]]
        elif number_of_rotation == 4:
            shape_to_return = [[0, 1, 0, 0],
                               [1, 1, 0, 0],
                               [1, 0, 0, 0],
                               [0, 0, 0, 0]]
    return shape_to_return


def initial_Y_position_calc(number_of_shape, number_of_rotation):
    # In this function we calculate the initial Y position of the piece
    if number_of_shape == 1:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -3
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -3
    elif number_of_shape == 2:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -2
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -2
    elif number_of_shape == 3:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -2
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -2
    elif number_of_shape == 4:
        if number_of_rotation == 1:
            initial_Y_pos = -3
        elif number_of_rotation == 2:
            initial_Y_pos = -3
        elif number_of_rotation == 3:
            initial_Y_pos = -3
        elif number_of_rotation == 4:
            initial_Y_pos = -3
    elif number_of_shape == 5:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -2
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -2
    elif number_of_shape == 6:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -2
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -2
    elif number_of_shape == 7:
        if number_of_rotation == 1:
            initial_Y_pos = -1
        elif number_of_rotation == 2:
            initial_Y_pos = -2
        elif number_of_rotation == 3:
            initial_Y_pos = -2
        elif number_of_rotation == 4:
            initial_Y_pos = -2
    return initial_Y_pos


def erase_last_image():
    # Erases the last image of piece in game matrix
    shape_to_erase = shape_format(last_shape_number, last_rotation_number)
    for i in range(last_position_Y, last_position_Y + 4):
        for j in range(last_position_X, last_position_X + 4):
            # if i > 0:
            if 0 <= j - last_position_X <= 9 and 0 <= i - last_position_Y <= 19:
                if shape_to_erase[i - last_position_Y][j - last_position_X] == 1:
                    if 0 <= i <= 19 and 0 <= j <= 9:
                        game_matrix[i][j] = 0
    return


def erase_shape_in_matrix(position_x, position_y, shape_number_to_erase, rotation_number_to_erase):
    # Erases the given piece from matrix
    shape_to_erase = shape_format(shape_number_to_erase, rotation_number_to_erase)
    for i in range(4):
        for j in range(4):
            if 0 <= position_x + j <= 9 and 0 <= position_y + i <= 19:
                if shape_to_erase[i][j] == 1:
                    game_matrix[position_Y + i][position_X + j] = 0
    return


def shape_in_matrix():
    # This function draws the piece in the game matrix
    global position_X, position_Y, last_position_Y
    erase_last_image()
    shape = shape_format(shape_number, rotation_number)

    for i in range(position_Y, position_Y + 4):
        for j in range(position_X, position_X + 4):
            if 0 <= i <= 19:
                if shape[i - position_Y][j - position_X] == 1 and game_matrix[i][j] == 0:
                    game_matrix[i][j] = color_number
    return


def check_X_motion_negative():
    # Checks whether left move is permitted
    erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
    check = True
    shape = shape_format(shape_number, rotation_number)
    if shape[0][0] == 0 and shape[1][0] == 0 and shape[2][0] == 0 and shape[3][0] == 0:
        if shape[0][1] == 0 and shape[1][1] == 0 and shape[2][1] == 0 and shape[3][1] == 0:
            if shape[0][2] == 0 and shape[1][2] == 0 and shape[2][2] == 0 and shape[3][2] == 0:
                if position_X == -3:
                    check = False
                else:
                    for i in range(4):
                        if (19 >= position_Y + i) >= 0 and (0 <= position_X + 2 <= 9):
                            if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][3] == 1:
                                check = False
            else:
                if position_X == -2:
                    check = False
                else:
                    for i in range(4):
                        if 19 >= position_Y + i >= 0:
                            if 0 <= position_X + 2 <= 9:
                                if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][3] == 1:
                                    if shape[i][2] == 0:
                                        check = False
                            if 0 <= position_X + 1 <= 9:
                                if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][2] == 1:
                                    check = False
        else:
            if position_X == -1:
                check = False
            else:
                for i in range(4):
                    if 19 >= position_Y + i >= 0:
                        if 0 <= position_X + 2 <= 9:
                            if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][3] == 1:
                                if shape[i][2] == 0:
                                    check = False
                        if 0 <= position_X + 1 <= 9:
                            if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][2] == 1:
                                if shape[i][1] == 0:
                                    check = False
                        if 0 <= position_X <= 9:
                            if game_matrix[position_Y + i][position_X] != 0 and shape[i][1] == 1:
                                if shape[i][0] == 0:
                                    check = False
    else:
        if position_X == 0:
            check = False
        else:
            for i in range(4):
                if 19 >= position_Y + i >= 0:
                    if 0 <= position_X + 2 <= 9:
                        if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][3] == 1:
                            if shape[i][2] == 0:
                                check = False
                    if 0 <= position_X + 1 <= 9:
                        if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][2] == 1:
                            if shape[i][1] == 0:
                                check = False
                    if 0 <= position_X <= 9:
                        if (0 <= position_X <= 9) and (
                                game_matrix[position_Y + i][position_X] != 0 and shape[i][1] == 1):
                            if shape[i][0] == 0:
                                check = False
                    if 0 <= position_X - 1 <= 9:
                        if game_matrix[position_Y + i][position_X - 1] != 0 and shape[i][0] == 1:
                            check = False
    return check


def check_X_motion_positive():
    # Checks whether right move is permitted
    erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
    check = True
    shape = shape_format(shape_number, rotation_number)
    if shape[0][3] == 0 and shape[1][3] == 0 and shape[2][3] == 0 and shape[3][3] == 0:
        if shape[0][2] == 0 and shape[1][2] == 0 and shape[2][2] == 0 and shape[3][2] == 0:
            if shape[0][1] == 0 and shape[1][1] == 0 and shape[2][1] == 0 and shape[3][1] == 0:
                if position_X == 9:
                    check = False
                else:
                    for i in range(4):
                        if 19 >= position_Y + i >= 0 and (0 <= position_X + 2 <= 9):
                            if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][0] == 1:
                                check = False
            else:
                if position_X == 8:
                    check = False
                else:
                    for i in range(4):
                        if 19 >= position_Y + i >= 0:
                            if 0 <= position_X + 1 <= 9:
                                if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][0] == 1:
                                    if shape[i][1] == 0:
                                        check = False
                            if 0 <= position_X + 2 <= 9:
                                if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][1] == 1:
                                    check = False
        else:
            if position_X == 7:
                check = False
            else:
                for i in range(4):
                    if 19 >= position_Y + i >= 0:
                        if 0 <= position_X + 1 <= 9:
                            if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][0] == 1:
                                if shape[i][1] == 0:
                                    check = False
                        if 0 <= position_X + 2 <= 9:
                            if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][1] == 1:
                                if shape[i][2] == 0:
                                    check = False
                        if 0 <= position_X + 3 <= 9:
                            if game_matrix[position_Y + i][position_X + 3] != 0 and shape[i][2] == 1:
                                check = False
    else:
        if position_X == 6:
            check = False
        else:
            for i in range(4):
                if 19 >= position_Y + i >= 0:
                    if 0 <= position_X + 1 <= 9:
                        if game_matrix[position_Y + i][position_X + 1] != 0 and shape[i][0] == 1:
                            if shape[i][1] == 0:
                                check = False
                    if 0 <= position_X + 2 <= 9:
                        if game_matrix[position_Y + i][position_X + 2] != 0 and shape[i][1] == 1:
                            if shape[i][2] == 0:
                                check = False
                    if 0 <= position_X + 3 <= 9:
                        if game_matrix[position_Y + i][position_X + 3] != 0 and shape[i][2] == 1:
                            if shape[i][3] == 0:
                                check = False
                    if 0 <= position_X + 4 <= 9:
                        if game_matrix[position_Y + i][position_X + 4] != 0 and shape[i][3] == 1:
                            check = False
    return check


def check_Y_motion_down():
    # Checks whether the piece can go one step down
    check = True
    shape = shape_format(shape_number, rotation_number)
    if shape[3][0] == 0 and shape[3][1] == 0 and shape[3][2] == 0 and shape[3][3] == 0:
        if shape[2][0] == 0 and shape[2][1] == 0 and shape[2][2] == 0 and shape[2][3] == 0:
            if shape[1][0] == 0 and shape[1][1] == 0 and shape[1][2] == 0 and shape[1][3] == 0:
                if position_Y == 19:
                    check = False
                else:
                    for j in range(4):
                        if 0 <= position_X + j <= 9:
                            if game_matrix[position_Y + 1][position_X + j] != 0 and shape[0][j] == 1:
                                check = False
            else:
                if position_Y == 18:
                    check = False
                else:
                    for j in range(4):
                        if 0 <= position_X + j <= 9:
                            if game_matrix[position_Y + 2][position_X + j] != 0 and shape[1][j] == 1:
                                check = False
                            if position_Y > -1:
                                if game_matrix[position_Y + 1][position_X + j] != 0 and shape[0][j] == 1:
                                    if shape[1][j] == 0:
                                        check = False
        else:
            if position_Y == 17:
                check = False
            else:
                for j in range(4):
                    if 0 <= position_X + j <= 9:
                        if game_matrix[position_Y + 3][position_X + j] != 0 and shape[2][j] == 1:
                            check = False
                        if position_Y > -1:
                            if game_matrix[position_Y + 2][position_X + j] != 0 and shape[1][j] == 1:
                                if shape[2][j] == 0:
                                    check = False
                        if position_Y > -2:
                            if game_matrix[position_Y + 1][position_X + j] != 0 and shape[0][j] == 1:
                                if shape[1][j] == 0:
                                    check = False
    else:
        if position_Y == 16:
            check = False
        else:
            for j in range(4):
                if 0 <= position_X + j <= 9:
                    if game_matrix[position_Y + 4][position_X + j] != 0 and shape[3][j] == 1:
                        check = False
                    if position_Y > 0:
                        if game_matrix[position_Y + 3][position_X + j] != 0 and shape[2][j] == 1:
                            if shape[3][j] == 0:
                                check = False
                    if position_Y > -1:
                        if game_matrix[position_Y + 2][position_X + j] != 0 and shape[1][j] == 1:
                            if shape[2][j] == 0:
                                check = False
                    if position_Y > 0:
                        if game_matrix[position_Y + 1][position_X + j] != 0 and shape[0][j] == 1:
                            if shape[1][j] == 0:
                                check = False
    return check


def check_rotation(position_x, position_y, number_of_shape, current_rotation_number, next_rotation_number):
    # Checks whether the rotation is permitted
    global game_matrix
    check = True
    current_shape = shape_format(number_of_shape, current_rotation_number)
    next_shape = shape_format(number_of_shape, next_rotation_number)

    for i in range(4):
        for j in range(4):
            if 0 <= position_x + j <= 9:
                if 0 <= position_y + i <= 19:
                    if next_shape[i][j] == 1 and game_matrix[position_y + i][position_x + j] != 0:
                        if current_shape[i][j] != 1:
                            check = False
                else:
                    if next_shape[i][j] == 1 and 0 <= position_y + i:
                        check = False
            else:
                if next_shape[i][j] == 1:
                    check = False
    return check


def calculate_level():
    # Calculated the game level
    global level
    level = total_lines_cleared // 10
    return level


def clear_rows():
    # Checks, clears full rows, and calculates score
    global score, total_lines_cleared, level
    level = calculate_level()
    temp1 = []
    temp2 = []
    return_is_full = False
    number_of_rows_cleared = 0
    for i in range(10):
        temp1.append(0)
        temp2.append(0)

    for i in range(20):
        is_full = True
        n = 0
        for j in range(10):
            if game_matrix[i][j] == 0:
                is_full = False
                break
            else:
                n += 1
        if n == 10:
            number_of_rows_cleared += 1

        if is_full:
            for k in range(i + 1):
                for j in range(10):
                    if k == 0:
                        temp1[j] = game_matrix[k][j]
                        game_matrix[k][j] = 0
                    elif k != i:
                        temp2[j] = game_matrix[k][j]
                        game_matrix[k][j] = temp1[j]
                        temp1[j] = temp2[j]
                    else:
                        game_matrix[k][j] = temp1[j]
        if is_full:
            return_is_full = True

    if number_of_rows_cleared == 1:
        score = score + 40 + level * 40
        total_lines_cleared += number_of_rows_cleared
    elif number_of_rows_cleared == 2:
        score = score + 100 + level * 100
        total_lines_cleared += number_of_rows_cleared
    elif number_of_rows_cleared == 3:
        score = score + 300 + level * 300
        total_lines_cleared += number_of_rows_cleared
    elif number_of_rows_cleared >= 4:
        score = score + 1200 + level * 1200
        total_lines_cleared += number_of_rows_cleared

    return return_is_full


# Function to display all boxes
def display_matrix():
    # Game matrix position
    game_matrix_X = resize_factor * 50
    game_matrix_Y = resize_factor * 50
    box_size = resize_factor * 40
    for i in range(20):
        screen.blit(wall, (int(game_matrix_X - box_size), int(game_matrix_Y + i * box_size)))
        screen.blit(wall, (int(game_matrix_X + box_size * 10), int(game_matrix_Y + i * box_size)))
        for j in range(10):
            if game_matrix[i][j] != 0:
                screen.blit(color_dict[game_matrix[i][j]],
                            (int(game_matrix_X + j * box_size), int(game_matrix_Y + i * box_size)))
            else:
                screen.blit(background, (int(game_matrix_X + j * box_size), int(game_matrix_Y + i * box_size)))
            screen.blit(wall, (int(game_matrix_X + j * box_size), int(game_matrix_Y + 20 * box_size)))

    screen.blit(wall, (int(game_matrix_X - box_size), int(game_matrix_Y + 20 * box_size)))
    screen.blit(wall, (int(game_matrix_X + box_size * 10), int(game_matrix_Y + 20 * box_size)))
    return


def display_next():
    # Displays the next piece
    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 60))
    text = font.render("Next", True, (255, 255, 255), (20, 20, 20))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 600), int(resize_factor * 100))
    screen.blit(text, textRect)
    game_matrix_X = resize_factor * 50
    game_matrix_Y = resize_factor * 50
    box_size = resize_factor * 40
    gapX = resize_factor * 70
    gapY = resize_factor * 90
    shape = shape_format(shape_number_next, rotation_number_next)

    if shape_number_next == 1:
        if rotation_number_next == 1:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 2:
            gapX = gapX - 0.5 * box_size
        elif rotation_number_next == 3:
            gapY = gapY - 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + 0.5 * box_size
    elif shape_number_next == 2:
        if rotation_number_next == 1:
            gapX = gapX + 0.5 * box_size
            gapY = gapY + box_size
        elif rotation_number_next == 2:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 3:
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + 0.5 * box_size
            gapY = gapY + 0.5 * box_size
    elif shape_number_next == 3:
        if rotation_number_next == 1:
            gapX = gapX + 0.5 * box_size
            gapY = gapY + box_size
        elif rotation_number_next == 2:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 3:
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + box_size
            gapY = gapY + 0.5 * box_size
    elif shape_number_next == 4:
        if rotation_number_next == 1:
            gapY = gapY - box_size
        elif rotation_number_next == 2:
            gapY = gapY - box_size
        elif rotation_number_next == 3:
            gapY = gapY - box_size
        elif rotation_number_next == 4:
            gapY = gapY - box_size
    elif shape_number_next == 5:
        if rotation_number_next == 1:
            gapY = gapY + box_size
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 2:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 3:
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + box_size
            gapY = gapY + 0.5 * box_size
    elif shape_number_next == 6:
        if rotation_number_next == 1:
            gapX = gapX + 0.5 * box_size
            gapY = gapY + box_size
        elif rotation_number_next == 2:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 3:
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + box_size
            gapY = gapY + 0.5 * box_size
    elif shape_number_next == 7:
        if rotation_number_next == 1:
            gapY = gapY + box_size
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 2:
            gapY = gapY + 0.5 * box_size
        elif rotation_number_next == 3:
            gapX = gapX + 0.5 * box_size
        elif rotation_number_next == 4:
            gapX = gapX + box_size
            gapY = gapY + 0.5 * box_size

    for i in range(4):
        for j in range(4):
            if shape[i][j] == 1:
                screen.blit(color_dict[color_number_next],
                            (int(game_matrix_X + (10 + j) * box_size + gapX), int(game_matrix_Y + i * box_size + gapY)))
    return


def display_score():
    # Displays the score
    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 60))
    text = font.render("Score", True, (255, 255, 255), (20, 20, 20))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 600), int(resize_factor * 350))
    screen.blit(text, textRect)
    score_text = font.render(str(score), True, (255, 255, 255), (20, 20, 20))
    scoreTextRect = text.get_rect()

    if score // 10 == 0:
        gap = resize_factor * 60
    elif score // 100 == 0:
        gap = resize_factor * 45
    elif score // 1000 == 0:
        gap = resize_factor * 30
    elif score // 10000 == 0:
        gap = resize_factor * 15
    elif score // 100000 == 0:
        gap = resize_factor * 0
    else:
        gap = resize_factor * (-15)

    scoreTextRect.center = (int(resize_factor * 600) + int(gap), int(resize_factor * 430))
    screen.blit(score_text, scoreTextRect)
    return


def level_time(current_level):
    # Calculate the time for each step, for each level
    speed_factor = 60  # fps number for a smooth running pc
    if current_level == 0:
        time_of_level = 1 / (0.01667 * speed_factor)
    elif current_level == 1:
        time_of_level = 1 / (0.021017 * speed_factor)
    elif current_level == 2:
        time_of_level = 1 / (0.026977 * speed_factor)
    elif current_level == 3:
        time_of_level = 1 / (0.035256 * speed_factor)
    elif current_level == 4:
        time_of_level = 1 / (0.04693 * speed_factor)
    elif current_level == 5:
        time_of_level = 1 / (0.06361 * speed_factor)
    elif current_level == 6:
        time_of_level = 1 / (0.0879 * speed_factor)
    elif current_level == 7:
        time_of_level = 1 / (0.1236 * speed_factor)
    elif current_level == 8:
        time_of_level = 1 / (0.1775 * speed_factor)
    elif current_level == 9:
        time_of_level = 1 / (0.2598 * speed_factor)
    elif current_level == 10:
        time_of_level = 1 / (0.388 * speed_factor)
    elif current_level == 11:
        time_of_level = 1 / (0.59 * speed_factor)
    elif current_level == 12:
        time_of_level = 1 / (0.92 * speed_factor)
    elif current_level == 13:
        time_of_level = 1 / (1.46 * speed_factor)
    else:
        time_of_level = 1 / (2.36 * speed_factor)

    return time_of_level


def check_game_over():
    # Checks if game is over
    global shape_number, rotation_number, game_matrix, position_X
    check = False
    shape = shape_format(shape_number, rotation_number)

    if shape[3][0] == 0 and shape[3][1] == 0 and shape[3][2] == 0 and shape[3][3] == 0:
        if shape[2][0] == 0 and shape[2][1] == 0 and shape[2][2] == 0 and shape[2][3] == 0:
            if shape[1][0] == 0 and shape[1][1] == 0 and shape[1][2] == 0 and shape[1][3] == 0:
                for j in range(4):
                    if game_matrix[0][position_X + j] != 0 and shape[0][j] == 1:
                        check = True
            else:
                for j in range(4):
                    if game_matrix[0][position_X + j] != 0 and shape[1][j] == 1:
                        check = True
        else:
            for j in range(4):
                if game_matrix[0][position_X + j] != 0 and shape[2][j] == 1:
                    check = True
    else:
        for j in range(4):
            if game_matrix[0][position_X + j] != 0 and shape[3][j] == 1:
                check = True

    return check


def game_over_screen():
    # Shows the game over texts and also resets the game
    global score, high_score, final_selection, game_over, spawn_new_shape, cleared, hard_drop, level, score, \
        total_lines_cleared, time_start, time_passed, position_X, last_position_X, position_Y, position_Y, \
        last_position_Y, last_rotation_number, rotation_number_next, shape_number, last_shape_number, \
        shape_number_next, color_number, color_number_next, rotation_number, game_matrix

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 90))
    text = font.render("Game Over", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 250), int(resize_factor * 300))
    screen.blit(text, textRect)

    if score > int(high_score):
        high_score = str(score)

    if time_passed > 3:
        final_selection = 0
        game_over = False
        spawn_new_shape = True
        cleared = False
        hard_drop = False
        level = 0
        score = 0
        total_lines_cleared = 0
        time_start = time.time()
        time_passed = 0
        position_X = 0
        last_position_X = 0
        position_Y = 0
        last_position_Y = 0
        rotation_number = 1
        last_rotation_number = rotation_number
        rotation_number_next = random.randint(1, 4)
        shape_number = 1
        last_shape_number = 0
        shape_number_next = random.randint(1, 7)
        color_number = 0
        color_number_next = random.randint(1, 5)
        for i in range(20):
            for j in range(10):
                game_matrix[i][j] = 0

    return


def game():
    # The function of the game
    global running, spawn_new_shape, cleared, hard_drop, level, score, total_lines_cleared, position_X, game_over, \
           last_position_X, position_Y, last_position_Y, rotation_number, last_rotation_number, rotation_number_next, \
           shape_number, last_shape_number, shape_number_next, color_number, color_number_next, time_passed, time_start

    time_passed = time.time() - time_start

    for event in pygame.event.get():  # All event are handled inside this loop
        if event.type == pygame.QUIT:  # QUIT() means that X button is pressed
            config_file_update()
            running = False

        if not game_over:
            if not hard_drop:
                if event.type == pygame.KEYDOWN:  # Check if any key has been pressed
                    if event.key == pygame.K_LEFT:  # If left key
                        last_position_X = position_X
                        last_position_Y = position_Y
                        if check_X_motion_negative():
                            erase_last_image()
                            position_X -= 1

                    if event.key == pygame.K_RIGHT:
                        last_position_X = position_X
                        last_position_Y = position_Y
                        if check_X_motion_positive():
                            # erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                            erase_last_image()
                            position_X += 1

                    if event.key == pygame.K_DOWN:
                        last_position_Y = position_Y
                        last_position_X = position_X
                        if check_Y_motion_down():
                            # erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                            erase_last_image()
                            position_Y += 1
                            time_start = time.time()
                            time_passed = 0
                        else:
                            spawn_new_shape = True
                            cleared = clear_rows()

                    if event.key == pygame.K_SPACE:
                        hard_drop = True

                    if event.key == pygame.K_x:
                        if rotation_number < 4:
                            if check_rotation(position_X, position_Y, shape_number, rotation_number,
                                              rotation_number + 1):
                                erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                                rotation_number += 1
                        else:
                            if check_rotation(position_X, position_Y, shape_number, rotation_number, 1):
                                erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                                rotation_number = 1
                        last_rotation_number = rotation_number

                    if event.key == pygame.K_z:
                        if rotation_number > 1:
                            if check_rotation(position_X, position_Y, shape_number, rotation_number,
                                              rotation_number - 1):
                                erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                                rotation_number -= 1
                        else:
                            if check_rotation(position_X, position_Y, shape_number, rotation_number, 4):
                                erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                                rotation_number = 4
                        last_rotation_number = rotation_number

    if not game_over:
        if cleared:
            cleared = False

        if spawn_new_shape:
            color_number = color_number_next
            shape_number = shape_number_next
            rotation_number = rotation_number_next
            last_shape_number = shape_number
            last_rotation_number = rotation_number
            color_number_next = random.randint(1, 5)
            shape_number_next = random.randint(1, 7)
            rotation_number_next = random.randint(1, 4)
            position_X = 3
            last_position_X = position_X
            position_Y = initial_Y_position_calc(shape_number, rotation_number)
            last_position_Y = position_Y
            spawn_new_shape = False
            if check_game_over():
                game_over = True
                time_start = time.time()
                time_passed = 0

        if hard_drop or time_passed > level_time(level):
            last_position_Y = position_Y
            last_position_X = position_X
            if check_Y_motion_down():
                erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                position_Y += 1
                time_start = time.time()
                time_passed = 0
            else:
                # erase_shape_in_matrix(position_X, position_Y, shape_number, rotation_number)
                # erase_last_image()
                hard_drop = False
                spawn_new_shape = True
                cleared = clear_rows()
                time_start = time.time()
                time_passed = 0

        if not cleared:
            shape_in_matrix()

    display_score()
    display_next()
    display_matrix()

    if game_over:
        game_over_screen()

    return


def main_menu():
    # Main menu
    global running, temp_selection, final_selection, high_score, time_start

    for i in range(int(resize_factor * 10), int(resize_factor * 700), int(resize_factor * 40)):
        for j in range(int(resize_factor * 10), int(resize_factor * 900), int(resize_factor * 40)):
            screen.blit(background, (i, j))

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 100))
    text = font.render("T E T R I S", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 200))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 70))
    if temp_selection == 1:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("PLAY", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 400))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 70))
    if temp_selection == 2:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("OPTIONS", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 525))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 70))
    if temp_selection == 3:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("EXIT", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 650))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 50))
    text = font.render(f"HIGH SCORE: {high_score}", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 750))
    screen.blit(text, textRect)

    for event in pygame.event.get():  # All event are handled inside this loop
        if event.type == pygame.QUIT:  # QUIT() means that X button is pressed
            config_file_update()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if temp_selection != 3:
                    temp_selection += 1
                else:
                    temp_selection = 1

            if event.key == pygame.K_UP:
                if temp_selection != 1:
                    temp_selection -= 1
                else:
                    temp_selection = 3

            if event.key == pygame.K_RETURN:
                final_selection = temp_selection
                if final_selection == 1:
                    time_start = time.time()

    return final_selection


def options():
    # Options
    global running, temp_selection, options_temp_selection, final_selection, resize_factor, config_file, music, \
           resize_factor_changed, playing_music

    for i in range(int(resize_factor * 10), int(resize_factor * 700), int(resize_factor * 40)):
        for j in range(int(resize_factor * 10), int(resize_factor * 900), int(resize_factor * 40)):
            screen.blit(background, (i, j))

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 100))
    text = font.render("T E T R I S", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 200))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 50))
    if options_temp_selection == 1:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("Music:", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350 - 4.1 * resize_factor * 50), int(resize_factor * 350))
    screen.blit(text, textRect)
    if music:
        text = font.render("On", True, color)
        textRect = text.get_rect()
        textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 350))
    else:
        text = font.render("Off", True, color)
        textRect = text.get_rect()
        textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 350))
    screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 50))
    if options_temp_selection == 2:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("Resolution:", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350 - 3 * resize_factor * 50), int(resize_factor * 450))
    screen.blit(text, textRect)
    if resize_factor_changed:
        if resize_factor == 1:
            text = font.render("525x675", True, color)
            textRect = text.get_rect()
            textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 450))
        else:
            text = font.render("600x900", True, color)
            textRect = text.get_rect()
            textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 450))
    else:
        if resize_factor == 1:
            text = font.render("600x900", True, color)
            textRect = text.get_rect()
            textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 450))
        else:
            text = font.render("525x675", True, color)
            textRect = text.get_rect()
            textRect.center = (int(resize_factor * 350 + 4 * resize_factor * 50), int(resize_factor * 450))
    screen.blit(text, textRect)

    if resize_factor_changed:
        font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 35))
        text = font.render("Restart game to activate changes", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (int(resize_factor * 350), int(resize_factor * 50))
        screen.blit(text, textRect)

    font = pygame.font.Font('data/FreeSansBold.ttf', int(resize_factor * 50))
    if options_temp_selection == 3:
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    text = font.render("TO MAIN MENU", True, color)
    textRect = text.get_rect()
    textRect.center = (int(resize_factor * 350), int(resize_factor * 550))
    screen.blit(text, textRect)

    for event in pygame.event.get():  # All event are handled inside this loop
        if event.type == pygame.QUIT:  # QUIT() means that X button is pressed
            config_file_update()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if options_temp_selection != 3:
                    options_temp_selection += 1
                else:
                    options_temp_selection = 1

            if event.key == pygame.K_UP:
                if options_temp_selection != 1:
                    options_temp_selection -= 1
                else:
                    options_temp_selection = 3

            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                if options_temp_selection == 1:
                    music = not music
                    if music:
                        playing_music = music_track.play()
                    else:
                        playing_music.stop()

                if options_temp_selection == 2:
                    resize_factor_changed = not resize_factor_changed

            if event.key == pygame.K_RETURN and options_temp_selection == 3:
                final_selection = 0
                temp_selection = 1
                options_temp_selection = 1

    return


def config_file_update():
    # Updated the config.dat file
    global music, resize_factor_changed, resize_factor, config_file, high_score

    if music:
        music_value_in_file = "1"
    else:
        music_value_in_file = "0"

    if resize_factor_changed:
        if resize_factor == 1:
            resize_factor_in_file = "0"
        else:
            resize_factor_in_file = "1"
    else:
        if resize_factor == 1:
            resize_factor_in_file = "1"
        else:
            resize_factor_in_file = "0"

    output = f"music:\n{music_value_in_file}\nresize factor:\n"f"{resize_factor_in_file}\nhigh score:\n{high_score}"

    config_file.seek(0)
    config_file.truncate(0)
    config_file.write(output)
    config_file.close()

    return


# Loop Variables
config_file.seek(8)
music_config_file = config_file.read(1)
if music_config_file == "1":
    music = True
else:
    music = False

running = True
temp_selection = 1
options_temp_selection = 1
final_selection = 0

config_file.seek(43)
high_score = config_file.read(10)

# Game Variables. Are declared as global in order to be accessible easily from all game functions
game_over = False
spawn_new_shape = True
cleared = False
hard_drop = False
level = 0
score = 0
total_lines_cleared = 0
time_start = time.time()
time_passed = 0
position_X = 0
last_position_X = 0
position_Y = 0
last_position_Y = 0
rotation_number = 1
last_rotation_number = rotation_number
rotation_number_next = random.randint(1, 4)
shape_number = 1
last_shape_number = 0
shape_number_next = random.randint(1, 7)
color_number = 0
color_number_next = random.randint(1, 5)

if music:
    playing_music = music_track.play()


def main():
    global running, temp_selection, playing_music
    while running:
        # RGB Background Color
        screen.fill((20, 20, 20))

        if music and (not playing_music.is_playing()):
            playing_music = music_track.play()

        if final_selection == 0:
            main_menu()
        elif final_selection == 1:
            game()
        elif final_selection == 2:
            options()
        else:
            config_file_update()
            running = False

        pygame.display.update()
    return


main()
