import random
import pygame as pg
import sys
import argparse
import os
import colour
import math

from PIL import Image
from typing import Optional, Callable

directory_now = os.path.dirname(os.path.realpath(__file__)) + r'\temp'
frame_counter = 0


def my_sort(array: list, reverse: bool = False,
            key: Optional[Callable] = None,
            cmp: Optional[Callable] = None) -> list:
    """
    Realization of quicksort

    :param array: Array for sorting
    :param reverse: Flag for reverse sorting
    :param key: Key for sorting
    :param cmp: Comparator for equal values
    :return: Sorted array
    """

    key = key if key else lambda x: x
    cmp = cmp if cmp else lambda x, y: x <= y

    def _partition(_array: list, begin: int, end: int):
        pivot = begin
        for i in range(begin + 1, end + 1):
            if cmp(key(_array[begin]), key(_array[i])) if reverse else cmp(
                    key(_array[i]), key(_array[begin])):
                pivot += 1
                _array[i], _array[pivot] = _array[pivot], _array[i]
        _array[pivot], _array[begin] = _array[begin], _array[pivot]
        return pivot

    def _qsort(_array: list, begin: int, end: int, deep):
        if deep + 1 == sys.getrecursionlimit():
            _array = sorted(_array)
            return
        if begin >= end:
            return
        print(deep)
        pivot = _partition(_array, begin, end)
        _qsort(_array, begin, pivot - 1, deep + 1)
        _qsort(_array, pivot + 1, end, deep + 1)

    _qsort(array, 0, len(array) - 1, 0)
    return array


def float_rgb_to_byte(color):
    return [max(0, min(255, math.floor(_color * 256.0))) for _color in
            color.get_rgb()]


def draw_array_col(array: list, width: int, height: int, current_index: int,
                   screen: pg.Surface, color: tuple, tick: int,
                   color_array: list, filename_list: list, save: bool):
    """
    Draw column by element value

    :param array: Array with values
    :param width: Width of screen
    :param height: Height of screen
    :param current_index: Current indexes were we change
    :param screen: Main pygame surface
    :param color: Color
    :param tick: Tick update (in millisecond)
    :return:
    """
    len_col = len(array)
    norm_x = width / len_col
    norm_w = width / len_col - 1

    screen.fill((0, 0, 0))
    for j, v in enumerate(array):
        if norm_w <= 1:
            norm_w = 1
        norm_h = (v - 1) / len_col * height
        norm_y = height - norm_h
        if color == (0, 255, 0):
            norm_c = float_rgb_to_byte(color_array[j])
            _color = norm_c if j <= current_index else (255, 255, 255)
        else:
            _color = color if j == current_index else (255, 255, 255)
        pg.draw.rect(screen,
                     _color,
                     (norm_x * j, norm_y, norm_w, norm_h))

    pg.display.update()

    if save:
        global frame_counter
        filename_list.append(
            os.path.join(directory_now, 'temp' + str(frame_counter) + '.png'))
        pg.image.save(screen, filename_list[frame_counter])
        frame_counter += 1

    pg.time.wait(tick)


def color_constructor(color):
    _color = color if '.' not in color else [c for c in
                                             map(float, color.split(sep=' '))]
    if _color == color:
        return colour.Color(_color)
    else:
        return colour.Color(rgb=_color)


def draw_sort(args_array: list, reverse: bool, colors, filename_list: list,
              save: bool):
    """
    Draw visualisation of sort

    :param filename_list: List of pygame frames
    :param colors: List of two colors for gradient
    :param args_array: Array with values
    :param reverse: Reverse massive
    """
    pg.init()

    width, height = 800, 600

    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Qsort visualize")

    color_1 = color_constructor(colors[0])
    color_2 = color_constructor(colors[1])
    color_array = list(color_1.range_to(color_2, len(args_array)))

    def my_sort(array: list, reverse: bool = False,
                key: Optional[Callable] = None,
                cmp: Optional[Callable] = None) -> list:
        key = key if key else lambda x: x
        cmp = cmp if cmp else lambda x, y: x <= y

        def _partition(_array: list, begin: int, end: int):
            pivot = begin
            for i in range(begin + 1, end + 1):
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
                    pg.event.clear()

                if cmp(key(_array[begin]), key(_array[i])) if reverse else cmp(
                        key(_array[i]), key(_array[begin])):
                    pivot += 1
                    _array[i], _array[pivot] = _array[pivot], _array[i]
                    draw_array_col(_array, width, height, i, screen,
                                   (255, 0, 0), 1, color_array, filename_list,
                                   save)

            _array[pivot], _array[begin] = _array[begin], _array[pivot]

            return pivot

        def _qsort(_array: list, begin: int, end: int):

            if begin >= end:
                return
            pivot = _partition(_array, begin, end)
            _qsort(_array, begin, pivot - 1)
            _qsort(_array, pivot + 1, end)

        _qsort(array, 0, len(array) - 1)

        for i in range(len(array)):
            draw_array_col(array, width, height, i, screen, (0, 255, 0), 1,
                           color_array, filename_list, save)

        return array

    run = True
    while run:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    my_sort(args_array, reverse)


def validate_path(path: str) -> str:
    if not os.path.isabs(path):
        return os.path.abspath(path)

    return os.path.normpath(path)


def main():
    parser = argparse.ArgumentParser(description="Simple CLI for qsort")

    parser.add_argument("--array", "-a", dest="array", type=int, nargs="+",
                        help="Array of integers (example: 1 3 4 5 2 4 2)")
    parser.add_argument("--array_path", "-ap", dest="array_path",
                        type=validate_path,
                        help="Name of file (absolute or not)")
    parser.add_argument("--random_array", "-ra", dest="random_array",
                        nargs=2, type=int,
                        help="Generate random array, first int - max value "
                             "(from 1 to max) and second int - count of "
                             "elements")

    group_file = parser.add_mutually_exclusive_group()
    group_file.add_argument('--sort_read', "-sr", dest="sort_read",
                            action=argparse.BooleanOptionalAction,
                            help="Read array from file and sort")
    group_file.add_argument('--sort_write', "-sw", dest="sort_write",
                            action=argparse.BooleanOptionalAction,
                            help="Sort array in file")

    parser.add_argument("--visualize", "-v", dest="visualize",
                        action=argparse.BooleanOptionalAction,
                        help="Visualize array sorting")
    parser.add_argument("--reverse", "-r", dest="reverse", default=False,
                        action=argparse.BooleanOptionalAction,
                        help="Sorting array in reverse")

    parser.add_argument("--colors", "-c", dest="colors", type=str,
                        nargs=2, default=("red", "blue"),
                        help="Colors for coloring sorted array. "
                             "Gradient from first color and last. "
                             "(values must be in '', and supports rgb, 3hex "
                             "6hex)\nRgb example: '0.2 0.1 0.5'\n"
                             "Hex example: #ff0000)")

    parser.add_argument("--gif", "-g", dest="gif", type=str)

    args = parser.parse_args()

    if args.random_array:
        args.array = [random.randint(1, args.random_array[0]) for _ in
                      range(args.random_array[1])]

    if args.array_path and args.sort_read:
        with open(args.array_path) as file:
            args.array = list(map(int, file.read().split(sep=" ")))
            print(my_sort(args.array[:]))
    if args.array_path and args.sort_write:
        with open(args.array_path, "w") as file:
            if args.array:
                file.write(' '.join(map(str, my_sort(args.array[:]))))
            else:
                parser.error("Array is empty!")

    if args.visualize and args.array:
        filename_list = []

        if not args.gif:
            draw_sort(args.array, args.reverse, args.colors, filename_list,
                      args.gif)
            return

        draw_sort(args.array, args.reverse, args.colors, filename_list,
                  args.gif)

        print("Save gif, please wait 0_0")
        frames = [Image.open(i) for i in filename_list]

        frames[0].save(
            f'{args.gif}.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=20,
            loop=0,
        )
        print("Gif successfully save ;)")

        if True:
            for filename in filename_list:
                os.remove(filename)


if __name__ == '__main__':
    main()
