from pico2d import *
from g_platform import Platform
from meso import Meso
from lupin import Lupin
from potion import Potion

import gfw
import gobj

UNIT_PER_LINE = 100
SCREEN_LINES = 10
BLOCK_SIZE = 60

lines = []
my_row = 0


def load(file: str):
    global lines, current_x, create_at, map_index
    with open(file, 'r') as f:
        lines = f.readlines()
    current_x = 0
    map_index = 0
    create_at = get_canvas_width() + 2 * BLOCK_SIZE


def count():
    return len(lines) // SCREEN_LINES * UNIT_PER_LINE


def update(dx):
    global current_x, create_at
    current_x += dx
    while current_x < create_at:
        create_column()


def create_column():
    global current_x, map_index
    y = BLOCK_SIZE // 2
    for row in range(SCREEN_LINES):
        global my_row
        my_row = row
        ch = get(map_index, row)
        create_object(ch, current_x, y)
        y += BLOCK_SIZE

    current_x += BLOCK_SIZE
    map_index += 1


def create_object(ch, x, y):
    if ch in ['1', '2', '3', '4']:
        obj = Meso(ord(ch) - ord('1'), x, y)
        gfw.world.add(gfw.layer.meso, obj)
    elif ch in ['O', 'P', 'Q']:
        dy = 3.8 if ch == 'O' else 1
        y -= int(dy * BLOCK_SIZE) // 2
        x -= BLOCK_SIZE // 2
        obj = Platform(ord(ch) - ord('O'), x, y)
        gfw.world.add(gfw.layer.platform, obj)
    # 루팡이 1 행에서 생성될 때와 나머지 행에서 생성될 때 y위치 값이 다르다
    elif ch in ['X']:
        if my_row == 2:
            y -= int(BLOCK_SIZE) // 2
        else:
            y -= 8
        obj = Lupin(x, y)
        gfw.world.add(gfw.layer.enemy, obj)
    elif ch in ['A', 'B']:
        obj = Potion(ord(ch) - ord('A'), x, y)
        gfw.world.add(gfw.layer.item, obj)


def get(x, y):
    col = x % UNIT_PER_LINE
    row = x // UNIT_PER_LINE * SCREEN_LINES + SCREEN_LINES - 1 - y
    return lines[row][col]


def test_gen():
    load(gobj.res('stage_01.txt'))
    print('count=', count())
    line = 0
    for x in range(200):
        s = ''
        for y in range(10):
            s += get(x, y)
        line += 1


def test_gen_2():
    open_canvas()
    gfw.world.init(['item', 'platform'])
    load(gobj.res('stage_01.txt'))
    for i in range(100):
        update(0.1)
    close_canvas()


if __name__ == '__main__':
    test_gen()
