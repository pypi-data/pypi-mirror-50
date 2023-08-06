def ini(row_size: int, column_size: int, value_ject):
    return [[
        value_ject(x, y)
        for x in range(column_size)
    ] for y in range(row_size)
    ]


def transpose(mx):
    return [*zip(*mx)]


def row(mx, x):
    return mx[x]


def col(mx, y):
    return [mx[x][y] for x in range(len(mx))]


def veho(mx, ject):
    return [[
        ject(mx[x][y])
        for y in range(len(mx[0]))
    ] for x in range(len(mx))
    ]


def veho_col(mx, column_ject):
    tsp = transpose(mx)
    return [column_ject(c) for c in tsp]
