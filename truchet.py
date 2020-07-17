import math
import random as rnd
from itertools import permutations

import cairosvg
import svgwrite

ROOT3 = math.sqrt(3)
VERTICES = [(2, 0), (1, ROOT3), (-1, ROOT3),
            (-2, 0), (-1, -ROOT3), (1, -ROOT3)]
MIDPOINTS = [(0, -ROOT3), (1.5, -ROOT3 / 2), (1.5, ROOT3 / 2),
             (0, ROOT3), (-1.5, ROOT3 / 2), (-1.5, -ROOT3 / 2)]
CONNECT_LIST = list(permutations(range(6)))


def connect_points(dwg, midpoints, idx1, idx2):
    """Connect two point
    Args:
        midpoints (list): point list
        idx1 (int): index of 1st point
        idx2 (int): index of 2nd point
    """
    # 使用する座標
    idx1, idx2 = min(idx1, idx2), max(idx1, idx2)
    if (idx1, idx2) == (0, 5):  # 例外
        idx1, idx2 = idx2, idx1
    (x1, y1), (x2, y2) = midpoints[idx1], midpoints[idx2]

    if abs(idx1 - idx2) in (1, 5):  # 隣り合った点
        dwg.add(dwg.path(
            class_='outer-line',
            d=f'M {x1} {y1} A 1 1 0 0 0 {x2} {y2}'
        ))
        dwg.add(dwg.path(
            class_='inner-line',
            d=f'M {x1} {y1} A 1 1 0 0 0 {x2} {y2}'
        ))

    elif abs(idx1 - idx2) == 2:  # 2個隣りの点
        dwg.add(dwg.path(
            class_='outer-line',
            d=f'M {x1} {y1} A 3 3 0 0 0 {x2} {y2}'
        ))
        dwg.add(dwg.path(
            class_='inner-line',
            d=f'M {x1} {y1} A 3 3 0 0 0 {x2} {y2}'
        ))

    elif abs(idx1 - idx2) == 3:  # 向かい合った点
        dwg.add(dwg.line(class_='outer-line',
                         start=(x1, y1), end=(x2, y2)))
        dwg.add(dwg.line(class_='inner-line',
                         start=(x1, y1), end=(x2, y2)))

    elif abs(idx1 - idx2) == 4:  # 2個隣りの点
        dwg.add(dwg.path(
            class_='outer-line',
            d=f'M {x1} {y1} A 3 3 0 0 1 {x2} {y2}'
        ))
        dwg.add(dwg.path(
            class_='inner-line',
            d=f'M {x1} {y1} A 3 3 0 0 1 {x2} {y2}'
        ))


def add_tile(dwg, tile_type, pos=(0, 0)):
    pos = (pos[0] * 3 - 1, pos[1] * ROOT3)
    vertices = [(c[0] + pos[0], c[1] + pos[1]) for c in VERTICES]
    midpoints = [(c[0] + pos[0], c[1] + pos[1]) for c in MIDPOINTS]

    # Hexagon
    dwg.add(dwg.polygon(class_='background', points=vertices))

    # How to connect
    li = CONNECT_LIST[tile_type]
    connect_list = [li[0:2], li[2:4], li[4:6]]

    # Connect
    for idx1, idx2 in connect_list:
        connect_points(dwg, midpoints, idx1, idx2)


def main(width, height, stroke_width):
    dwg = svgwrite.Drawing()

    for w in range(width + 2):
        for h in range(w % 2, height + 2, 2):
            tile_type = rnd.randrange(720)
            add_tile(dwg, tile_type, (w, h))

    # define style
    dwg.add(dwg.style(f'''
        .background {{
            fill: #000;
        }}
        .outer-line {{
            stroke: #000;
            stroke-width: {stroke_width};
            fill: none;
        }}
        .inner-line {{
            stroke: white;
            stroke-width: {stroke_width - 0.2};
            fill: none;
        }}
    '''))

    dwg['width'] = 3 * width + 1
    dwg['height'] = ROOT3 * (height + 1)
    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='truchet.png', scale=2000 / dwg['width'])


if __name__ == '__main__':
    main(width=12, height=20, stroke_width=1.5)
