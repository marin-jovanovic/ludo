class Tile:

    def __init__(self, row, column):
        self.row = row
        self.column = column

        # self.visitors = set()

    # def add_visitor(self, visitor):
    #     if visitor in self.visitors:
    #         print("visitor already in this")
    #         sys.exit(-1)
    #
    #     self.visitors.add(visitor)

    def __str__(self):
        return f"row: {self.row}, column: {self.column}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Tile):
            return self.row == other.row and self.column == other.column
        return False

        # def __eq__(self, other):
        #     if isinstance(other, self.__class__):
        #         return self.__dict__ == other.__dict__
        #     else:
        #         return False
        # return NotImplemented

    def __hash__(self):
        """Overrides the default implementation"""
        return hash(tuple(sorted(self.__dict__.items())))
