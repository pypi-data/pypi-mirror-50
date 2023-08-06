#!/usr/bin/python

import curses
import argparse

import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import laplace
from scipy.ndimage.interpolation import rotate


def average_rotate(array, degree):
    '''Generates an n-fold symmetrical array'''

    array = np.mean(
        [
            rotate(array, (360 / degree) * i, reshape=False, mode='wrap')
            for i in range(degree)
        ],
        axis=0,
    )

    return array


def update_bz(array, coefficients):
    '''Apply reaction equations to an array'''

    alpha, beta, gamma = coefficients
    # Count the average amount of each species in the 9 cells around each cell
    local_avg = np.zeros(array.shape)
    for k in range(3):
        local_avg[k] = convolve2d(
            array[k], np.ones((3, 3)) / 9, mode="same", boundary="wrap"
        )
    # Apply the reaction equations
    array[0] = local_avg[0] * (1 + alpha * local_avg[1] - gamma * local_avg[2])
    array[1] = local_avg[1] * (1 + beta * local_avg[2] - alpha * local_avg[0])
    array[2] = local_avg[2] * (1 + gamma * local_avg[0] - beta * local_avg[1])
    # Ensure the species concentrations are kept within [0,1]
    np.clip(array, 0, 0.99, array)

    return array


def update_turing(array, coefficients):
    '''Apply reaction equations to an array'''

    DT, DA, DB = 0.001, 1, 100
    alpha, beta, _ = coefficients
    # Apply the reaction equations
    array[0] = array[0] + DT * (
        DA * laplace(array[0], mode='wrap')
        + array[0]
        - array[0] ** 3
        - array[1]
        + alpha
    )
    array[1] = array[1] + DT * (
        DB * laplace(array[1], mode='wrap') + (array[0] - array[1]) * beta
    )
    # Ensure the species concentrations are kept within [0,1].
    np.clip(array, 0, 0.99, array)

    return array


def render(args):
    '''Initializes array then updates and renders it ad infinitum'''

    # Nicer syntax
    args.ascii = np.array(args.ascii)

    screen = curses.initscr()
    height, width = screen.getmaxyx()

    # Color pairs setup
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, 1, args.background)
    curses.init_pair(2, 2, args.background)
    curses.init_pair(3, 3, args.background)
    curses.init_pair(4, 4, args.background)
    curses.init_pair(5, 5, args.background)
    curses.init_pair(6, 6, args.background)
    curses.init_pair(7, 7, args.background)
    screen.clear()

    # Initialize the array and apply rotation
    array = np.array(
        [
            average_rotate(np.random.random(size=(height, width)), args.symmetry)
            for _ in range(3)
        ]
    )

    while True:
        # Apply reaction equations and update array
        if not args.turing:
            array = update_bz(array, args.coefficients)
        else:
            # Turing is too slow to be rendered each time step
            for _ in range(20):
                array = update_turing(array, args.coefficients)
        # Map array values to an args.ascii index
        idxs = (array[0] * 10).astype("int8")
        # Render array
        if not args.fast:
            for line in range(height - 1):
                for column in range(width - 1):
                    idx = idxs[line, column]
                    screen.addstr(
                        line,
                        column,
                        args.ascii[idx],
                        curses.color_pair(args.color[idx]) | curses.A_BOLD,
                    )
        else:
            for line in range(height - 1):
                screen.addstr(
                    line,
                    0,
                    ''.join(args.ascii[idxs[line]]),
                    curses.color_pair(7) | curses.A_BOLD,
                )
        screen.refresh()
        screen.timeout(30)
        # Ends rendering
        if screen.getch() != -1:
            curses.endwin()
            break


def main():
    '''Parse command line arguments and calls render function'''

    # Default parameters
    COEFFICIENT = 1.0, 1.0, 1.0
    ASCII = (" ", ".", " ", ":", "*", "*", "#", "#", "@", "@")
    COLOR = (1, 1, 2, 2, 2, 3, 3, 3, 7, 1)

    parser = argparse.ArgumentParser(
        prog='belousov-zhabotinsky',
        description='''The python package you never knew you needed! Now you
        can appreciate all the glory of the Belousov-Zhabotinsky reaction and
        Turing Patterns from the comfort of your console window in a state of
        the art ASCII art rendering. Your life will never be the same!''',
        epilog='''You can exit the program by pressing any key, but using the
        Ctrl key can cause the terminal to bug. For bug report or more
        information: https://github.com/neumann-mlucas/belousov-zhabotinsky''',
    )
    parser.add_argument(
        '-a',
        '--ascii',
        action='store',
        default=ASCII,
        nargs=10,
        help='''10 ASCII characters to be use in the rendering. Each point in the
        screen has a value between 0 and 1, and each ASCII character used as an
        input represents a range of values (e.g. 0.0-0.1, 0.1-0.2 etc)''',
    )
    parser.add_argument(
        '-b',
        '--background',
        action='store',
        default=0,
        type=int,
        help='''Background color [int 0-7]. 0:black, 1:red, 2:green, 3:yellow,
        4:blue, 5:magenta, 6:cyan, and 7:white''',
    )
    parser.add_argument(
        '-c',
        '--color',
        action='store',
        default=COLOR,
        nargs=10,
        type=int,
        help='''10 numbers in the [0-7] range for mapping colors to the ASCII
        characters. 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta,
        6:cyan, and 7:white''',
    )
    parser.add_argument(
        '-coef',
        '--coefficients',
        action='store',
        default=COEFFICIENT,
        nargs=3,
        type=float,
        help='''Values for alpha, beta and gamma -- changes the reaction's
        behavior. Default is alpha=1.0, beta=1.0, gamma=1.0''',
    )
    parser.add_argument(
        '-f',
        '--fast',
        action='store_true',
        default=False,
        help='''One color mode. Recommended for faster rendering in big terminal
        windows''',
    )
    parser.add_argument(
        '-n', '--number', action='store_true', default=False, help='Show grid values'
    )
    parser.add_argument(
        '-s',
        '--symmetry',
        action='store',
        default=1,
        type=int,
        help='''Symmetric mode, generates a n-fold symmetric grid''',
    )
    parser.add_argument(
        '-t',
        '--turing',
        action='store_true',
        default=False,
        help='''Turing
        patterns mode''',
    )
    args = parser.parse_args()

    # Default Turing args
    if args.turing:
        if args.coefficients == COEFFICIENT:
            args.coefficients = -0.005, 10, 0
        if args.ascii == ASCII:
            args.ascii = np.array((".", "*", "#", ":", "*", "#", "*", ";", "*", "#"))
        if args.color == COLOR:
            args.color = (1, 2, 4, 1, 2, 4, 1, 2, 4, 1)
    if args.number:
        args.ascii = np.array(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))

    render(args)


if __name__ == "__main__":
    main()
