"""
Connect 4 Game

Developer: Stan Ermokhin
Version: 0.0.0

"""

import re
import warnings

import numpy as np
from scipy.signal import convolve2d
from tabulate import tabulate

# These can be reasonably changed
CONNECT_X_FACTOR: int = 4
FIELD_WIDTH: int = 6
FIELD_HEIGHT: int = 7
PLAYER_RED: str = "R"
PLAYER_YELLOW: str = "Y"
EMPTY: str = "o"
# -------------------------------

FIELD_INDEXES: list[str] = [str(i) for i in range(FIELD_WIDTH)]

# Kernels to check for game over
HORIZONTAL_KERNEL: np.ndarray = np.array([[1 for _ in range(CONNECT_X_FACTOR)]])
VERTICAL_KERNEL: np.ndarray = np.transpose(HORIZONTAL_KERNEL)
DIAGONAL_KERNEL_1: np.ndarray = np.eye(CONNECT_X_FACTOR, dtype=np.uint8)
DIAGONAL_KERNEL_2: np.ndarray = np.fliplr(DIAGONAL_KERNEL_1)
DETECTION_KERNELS: list[np.ndarray] = [HORIZONTAL_KERNEL,
                                       VERTICAL_KERNEL,
                                       DIAGONAL_KERNEL_1,
                                       DIAGONAL_KERNEL_2]

MOVE_REGEX: str = r"^[0-9];[0-9]$"
EXPLANATION_MESSAGE: str = "Make move by typing: X;Y\n(X is left to right, Y is up to bottom)"
PROMPT_REQUEST: str = "Make your move, player"
OUT: str = "Wins: Player"


def check_regex(_input: str) -> bool:
    return bool(re.fullmatch(pattern=MOVE_REGEX, string=_input)[0])


def check_bounds(x: int, y: int) -> bool:
    return 0 <= x <= FIELD_WIDTH and 0 <= y <= FIELD_HEIGHT


def check_input(_input: str,
                field: list[list[str | None]]) -> bool:
    """

    :param field:
    :param _input:
    :return: True if _input is acceptable
    """

    regex_passed_check: bool = check_regex(_input=_input)
    if regex_passed_check:
        move: list = _input.split(";")
        input_x: int = int(move[0])
        input_y: int = int(move[1])

        if check_bounds(x=input_x, y=input_y) and field[input_y][input_x] == EMPTY:
            return True

    return False


def check_game_over(player_tag: str,
                    field: list[list[str | None]]) -> bool:
    _numpy_field: np.ndarray = np.array(field)

    _numpy_field = np.where(
        (_numpy_field == player_tag),
        1,
        0
    )
    _numpy_field = _numpy_field.astype(np.uint8)

    for kernel in DETECTION_KERNELS:
        if CONNECT_X_FACTOR in convolve2d(_numpy_field == 1, kernel, mode="valid"):
            return True

    return False


def request_move_and_change_field(player_tag: str,
                                  field: list[list[str | None]]) -> list[list[str | None]]:
    """
    Request player to make a move

    :param player_tag: "R" or "Y"
    :param field: old field
    :return: new field
    """

    _input_move = input(f"{PROMPT_REQUEST} {player_tag}: ")

    while not check_input(_input=_input_move, field=field):
        print("ERROR")
        _input_move = input(f"{PROMPT_REQUEST} {player_tag}: ")

    move: list = _input_move.split(";")
    input_x: int = int(move[0])
    input_y: int = int(move[1])

    if input_y != FIELD_HEIGHT:

        for height_index in range(input_y, FIELD_HEIGHT - 1):
            if field[height_index + 1][input_x] == EMPTY:
                input_y += 1

    field[input_y][input_x] = player_tag

    return field


def print_field(field: list[list[str | None]]) -> None:
    to_print: str = tabulate(tabular_data=field,
                             headers=FIELD_INDEXES,
                             showindex=True)
    print(to_print)


def main(field_width: int, field_height: int) -> None:
    game_over: bool = False
    current_player_has_won: bool = False
    field: list[list[str]] = [[EMPTY for _ in range(field_width)]
                              for _ in range(field_height)]

    current_player: str = PLAYER_RED
    other_player: str = PLAYER_YELLOW

    print(EXPLANATION_MESSAGE)
    print_field(field=field)

    while not game_over:
        request_move_and_change_field(player_tag=current_player,
                                      field=field)
        print_field(field=field)

        current_player_has_won: bool = check_game_over(player_tag=current_player, field=field)
        other_player_has_won: bool = check_game_over(player_tag=other_player, field=field)
        game_over = current_player_has_won or other_player_has_won

        current_player, other_player = other_player, current_player

    current_player, other_player = other_player, current_player
    print(f"{OUT} {current_player if current_player_has_won else other_player}")


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    main(field_width=FIELD_WIDTH, field_height=FIELD_HEIGHT)
