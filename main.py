from multiprocessing import Process, Value
import ctypes
from snake_game import run_snake_game
from minesweeper import run_minesweeper  # must match the updated file

if __name__ == "__main__":
    shared_game_over = Value(ctypes.c_bool, False)

    p1 = Process(target=run_snake_game, args=(shared_game_over,))
    p2 = Process(target=run_minesweeper, args=(shared_game_over,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
