import json
from typing import Callable

from crostab import CrosTab
from crostab.crit import Crit
from crostab.infer_dp_type import infer_dp_type
from crostab.table_spec import TableSpec
from veho import mat, vec, fun
from xbrief import Curt, Preci


class Table:
    banner: list
    matrix: list
    title: str
    types: list

    def __init__(self, banner: list, matrix: list, title: str = None, types: list = None):
        self.title = title if title is not None else ''
        self.matrix = matrix
        self.banner = banner
        wd_b = len(banner)
        if types:
            self.types = types
        else:
            self.infer_types()

    @staticmethod
    def from_rows(rows, title, types):
        sep = json.loads(rows)
        return Table(sep.banner, sep.samples, title, types)

    def ht(self):
        return len(self.matrix)

    def wd(self):
        return len(self.matrix[0])

    def cell(self, x, y):
        return self.matrix[x][y]

    def column_index(self, col_name):
        if isinstance(col_name, int):
            return col_name
        else:
            return self.banner.index(col_name)

    def column(self, col_name):
        y = self.column_index(col_name)
        return mat.col(self.matrix, y)

    def columns(self, cols):
        matrix = mat.transpose([self.column(c) for c in cols])
        return Table(cols, matrix, self.title, self.types)

    def set_column(self, col_name, new_column):
        y = self.column_index(col_name)
        for i, row in enumerate(self.matrix):
            row[y] = new_column[i]
        return self

    def set_column_by(self, col_name, ject):
        y = self.column_index(col_name)
        for i, row in enumerate(self.matrix):
            row[y] = ject(row[i])
        return self

    def change_type(self, col_name, type_name):
        column = self.column(col_name)
        if type_name == 'str':
            column = [f'{v}' for v in column]
        elif type_name in ('number', 'float'):
            column = [float(v) for v in column]
        elif type_name == 'int':
            column = [int(v) for v in column]
        elif type_name == 'bool':
            column = [bool(v) for v in column]
        self.set_column(col_name, column)
        return self

    def infer_types(self):
        self.types = mat.veho_col(self.matrix, infer_column_type)
        for i, typ in enumerate(self.types):
            if typ == 'str_num':
                self.change_type(i, 'number')
            elif typ == 'misc':
                self.change_type(i, 'str')
            else:
                pass
            self.types[i] = infer_column_type(mat.col(self.matrix, i))
        return self

    def filter(self, col_name, crit: Callable[[object], bool]):
        y = self.column_index(col_name)
        matrix = [row for row in self.matrix if crit(row[y])]
        return Table(self.banner, matrix, self.title, self.types)

    def filters(self, *column_crits: Crit):
        if column_crits:
            table = self
            for crit in column_crits:
                table = table.filter(crit.column, crit.crit)
            return table
        else:
            return self

    def samples(self, side, banner, aggreg_labels):
        x = self.banner.index(side)
        y = self.banner.index(banner)
        vals = [self.banner.index(label) for label in aggreg_labels]
        return [(row[x],
                 row[y],
                 *[row[z] for z in vals])
                for row in self.matrix]

    def cros_tab(self, table_spec: TableSpec):
        table_filtered = self.filters(*table_spec.filters)
        sample_set = table_filtered.samples(table_spec.side, table_spec.banner, table_spec.aggreg_labels)
        crostab_raw = CrosTab.ini(
            side=vec.distinct([x for x, _, *_ in sample_set]),
            banner=vec.distinct([y for _, y, *_ in sample_set]),
            ject=lambda x, y: [[] for _ in range(table_spec.aggregs_count)],
            title=f'{table_spec.side} * {table_spec.banner} · {table_spec.aggreg_labels}')
        for x, y, *values in sample_set:
            accum = crostab_raw.query_cell(x, y)
            for i, v in values:
                accum[i].append(v)
        return crostab_raw.map(lambda acc: table_spec.calc_exec(acc))

    def brief(self, banr: Curt = Curt(None, None, None), matr: Curt = Curt(None, None, None)):
        banr.abstract = fun.chain(banr.abstract, str) if banr.abstract else str
        matr.abstract = fun.chain(matr.abstract, str) if matr.abstract else str
        banner_list = Preci \
            .from_curt(self.banner, banr) \
            .to_list('..')
        matrix_list = Preci.from_arr(self.matrix, matr.head, matr.tail) \
            .map(lambda row: Preci
                 .from_arr(row, banr.head, banr.tail)
                 .map(matr.abstract)
                 .to_list('..')) \
            .to_list(['..' for _ in banner_list])
        pads = mat.veho_col([banner_list] + matrix_list, lambda col: max([len(x) for x in col]))
        banner_line, blank_line, matrix_line = \
            [f'{x: >{pads[i]}}' for i, x in enumerate(banner_list)], \
            ['-' * l for l in pads], \
            [[f'{x: >{l}}' for x, l in zip(row, pads)] for row in matrix_list]
        return '\r\n'.join([
                               f'[{self.title}]',
                               ' | '.join(banner_line),
                               '-+-'.join(blank_line)
                           ] +
                           [
                               ' | '.join(row) for row in matrix_line
                           ])


def infer_column_type(column):
    if column:
        types = [infer_dp_type(x) for x in column]
        types_dist = {*types}
        size = len(types_dist)
        if size == 1:
            return types_dist.pop()
        elif size == 2:
            nums = ['number', 'float', 'int', 'str_num']
            if types_dist.pop() in nums and types_dist.pop() in nums:
                return 'str_num'
            else:
                return 'misc'
        else:
            return 'misc'
    else:
        return 'none'
