class Tile:

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __str__(self):
        return f"row: {self.row}, column: {self.column}"

    def __eq__(self, other):
        # if isinstance(other, Tile):
        if isinstance(other, self.__class__):
            return self.row == other.row and self.column == other.column
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
