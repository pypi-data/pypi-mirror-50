import json
from typing import List, Any

from veho import mat, vec
from xbrief import strx, vecx


class CrosTab:
    side: list
    banner: list
    matrix: list
    title: strx

    def __init__(self, side, banner, matrix, title=None):
        self.side = side
        self.banner = banner
        self.matrix = matrix
        if title:
            self.title = title
        else:
            self.title = ''  # f'{side.__name__} * {banner.__name__}'

    @staticmethod
    def ini(side, banner, ject, title):
        matrix = mat.ini(len(side), len(banner), ject)
        return CrosTab(side, banner, matrix, title)

    def to_dict(self):
        return {'side': self.side,
                'banner': self.banner,
                'matrix': self.matrix,
                'title': self.title}

    def to_json(self):
        return json.dumps(self.to_dict())

    def map(self, ject):
        matrix = mat.veho(self.matrix, ject)
        return CrosTab(self.side, self.banner, matrix, self.title)

    def cell(self, x, y):
        return self.matrix[x][y]

    def query_cell(self, side_name, banner_name):
        x, y = self.side.index(side_name), self.banner.index(banner_name)
        if x < 0 and y < 0:
            return None
        else:
            return self.matrix[x][y]

    def ht(self):
        return len(self.matrix)

    def wd(self):
        return len(self.matrix[0])

    def row(self, row_name):
        if isinstance(row_name, int):
            x = row_name
        else:
            x = self.side.index(row_name)
        return self.matrix[x]

    def column(self, column_name):
        if isinstance(column_name, int):
            y = column_name
        else:
            y = self.side.index(column_name)
        return mat.col(self.matrix, y)

    def set_row(self, row_name, new_row):
        if isinstance(row_name, int):
            x = row_name
        else:
            x = self.side.index(row_name)
        self.matrix[x] = new_row
        return self

    def set_column(self, column_name, new_column):
        if isinstance(column_name, int):
            y = column_name
        else:
            y = self.side.index(column_name)
        for i, row in enumerate(self.matrix):
            row[y] = new_column[i]
        return self

    def transpose(self, new_title=None):
        return CrosTab(
            self.banner,
            self.side,
            mat.transpose(self.matrix),
            new_title if new_title else self.title)

    def _brief2(self, abstract=lambda x: f'{x}'):
        matrix = mat.veho(self.matrix, abstract)
        stb_w = max([len(x) for x in [self.title] + self.side])
        col_ws = mat.veho_col(matrix, lambda col: max([len(x) for x in col]))
        bnr_ws = [max(tup) for tup in zip(col_ws, [len(str(x)) for x in self.banner])]
        side = [strx.pad_start(str(x), stb_w) for x in self.side]
        banner = \
            strx.pad_end(self.title, stb_w) \
            + ' | ' \
            + vecx.hbrief(vec.zips(
                self.banner, bnr_ws, zipper=lambda x, l: strx.pad_end(str(x), l)
            ), ' : ')
        rows = [vecx.hbrief(
            vec.zips(row, bnr_ws, zipper=lambda x, l: strx.pad_start(x, l))
        ) for row in matrix]
        line = '-' * stb_w + '-+-' + vecx.hbrief(bnr_ws, '-+-', lambda x: '-' * x)
        rows = vec.zips(side, rows, zipper=lambda x, row: f'{x} | {row}')
        return '\r\n'.join([banner, line] + rows)

    def brief(self, abstract: callable = lambda x: f'{x}') -> strx:
        matrix: List[List[Any]] = mat.veho(self.matrix, abstract)
        stb_w: int = max([len(x) for x in [self.title] + self.side])
        col_ws: List[int] = [max([len(x) for x in col]) for col in mat.transpose(matrix)]
        bnr_ws: List[int] = [max(a, b) for a, b in zip(col_ws, [len(str(x)) for x in self.banner])]
        side: List[strx] = [f'{x: <{stb_w}}' for x in self.side]
        banner: strx = \
            f'{self.title: >{stb_w}}' \
            + ' | ' \
            + vecx.hbrief([f'{x: <{l}}' for x, l in zip(self.banner, bnr_ws)], ' : ')
        rows: List[strx] = [vecx.hbrief([f'{x: >{l}}' for x, l in zip(row, bnr_ws)], ' : ') for row in matrix]
        line: strx = '-' * stb_w + '-+-' + vecx.hbrief(bnr_ws, '-+-', lambda x: '-' * x)
        rows = [f'{x} | {row}' for x, row in zip(side, rows)]
        return '\r\n'.join([banner, line] + rows)
