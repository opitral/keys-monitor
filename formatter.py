class Row:
    def __init__(self, name: str, value: int) -> None:
        if name.startswith("Key."):
            name = name[4:]
        self.name = name.capitalize()
        self.value = int(value)

    def __str__(self) -> str:
        return f'{self.name}: {self.value}'

    def calc_diff(self, other: 'Row') -> int:
        diff = self.value - other.value
        return diff

    def calc_diff_percent(self, other: 'Row') -> float:
        if other.value == 0:
            return 0.0
        diff = self.calc_diff(other)
        percent = diff / other.value * 100
        return percent


class RowDiff(Row):
    def __init__(self, name, count, prev_count):
        super().__init__(name, count)
        self.prev_count = prev_count

    def __str__(self):
        other = Row('other', self.prev_count)
        diff = self.calc_diff(other)
        prefix = "📉" if diff < 0 else "📈"
        diff = "+" + str(diff) if diff >= 0 else "-" + str(diff)
        diff_percent = int(self.calc_diff_percent(other))
        diff_percent = "+" + str(diff_percent) if diff_percent >= 0 else "-" + str(diff_percent)
        return f'{prefix} {self.name}: {diff} ({diff_percent}%)'


class Table:
    def __init__(self, title: str, rows: list[Row | RowDiff] = None):
        if rows is None:
            rows = []
        self.title = title
        self.rows = rows

    def __str__(self):
        return f'{self.title}\n' + '\n'.join(map(str, self.rows))

    def add_row(self, row: Row | RowDiff):
        self.rows.append(row)