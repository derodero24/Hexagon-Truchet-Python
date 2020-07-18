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


class Mover:
    def __init__(self, pos):
        self.pos = pos

    def move(self, path):
        p = path.split()
        p[1] = self.pos[0] + int(p[1])
        p[2] = self.pos[1] + int(p[2])
        p[-2] = self.pos[0] + int(p[-2])
        p[-1] = self.pos[1] + int(p[-1])
        if len(p) == 14:
            p[4] = self.pos[0] + int(p[4])
            p[5] = self.pos[1] + int(p[5])
        return ' '.join(map(str, p))


def add_tile(dwg, tile_type, pos, rotate):
    pos = (pos[0] * 4, pos[1] * 4)
    m = Mover(pos)

    # 回転角度・中心
    deg, cx, cy = 90 * rotate, pos[0] + 2, pos[1] + 2

    base = dwg.g(transform=f'rotate({deg},{cx},{cy})')

    g = dwg.g(class_='line')
    if tile_type == 0:
        g.add(dwg.path(d=m.move('M 2 0 A 2 2 0 0 0 4 2')))
        g.add(dwg.path(d=m.move('M 1 0 A 3 3 0 0 0 4 3')))
        g.add(dwg.path(class_='background',
                       d=m.move('M 0 4 L 0 1 A 3 3 0 0 1 3 4')))
        g.add(dwg.path(d=m.move('M 0 2 A 2 2 0 0 1 2 4')))
        g.add(dwg.path(d=m.move('M 3 4 A 3 3 0 0 0 0 1')))

    elif tile_type in (1, 2):
        g.add(dwg.path(d=m.move('M 4 2 A 0.5 0.5 0 0 0 4 3')))
        g.add(dwg.path(d=m.move('M 2 4 A 0.5 0.5 0 0 1 3 4')))
        if tile_type == 2:
            g.add(dwg.path(d=m.move('M 4 3 A 1 1 0 0 0 3 4')))

    elif tile_type == 3:
        g.add(dwg.path(d=m.move('M 4 2 A 2 2 0 0 0 2 4')))
        g.add(dwg.path(d=m.move('M 4 3 A 1 1 0 0 0 3 4')))
    base.add(g)

    base.add(dwg.path(class_='background',
                      d=m.move('M 0 0 L 3 0 A 3 3 0 0 1 0 3')))

    g = dwg.g(class_='line')
    g.add(dwg.path(d=m.move('M 1 0 A 1 1 0 0 1 0 1')))
    g.add(dwg.path(d=m.move('M 2 0 A 2 2 0 0 1 0 2')))
    g.add(dwg.path(d=m.move('M 3 0 A 3 3 0 0 1 0 3')))
    g.add(dwg.path(d=m.move('M 3 0 A 1 1 0 0 0 4 1')))
    g.add(dwg.path(d=m.move('M 0 3 A 1 1 0 0 1 1 4')))
    base.add(g)

    dwg.add(base)


def main(width, height):
    dwg = svgwrite.Drawing()
    dwg.add(dwg.rect(class_='background',
                     insert=(0, 0), size=('100%', '100%')))

    for w in range(width):
        for h in range(height):
            add_tile(dwg, rnd.randrange(4), (w, h), rnd.randrange(4))

    # define style
    dwg.add(dwg.style(f'''
        .background {{
            fill: black;
            stroke: none;
        }}
        .line {{
            stroke: white;
            stroke-width: {0.3};
            stroke-linecap: round;
            fill: none;
        }}
    '''))

    dwg['width'] = width * 4
    dwg['height'] = height * 4
    cairosvg.svg2png(dwg.tostring().encode('utf-8'),
                     write_to='swirl_truchet.png',
                     scale=2000 / dwg['width'])


if __name__ == '__main__':
    main(width=10, height=10)
