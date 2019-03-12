from collections import Sequence
from typing import List, Optional, Union


class _Cell:
    __slots__ = ["__candidates", "__value"]

    def __init__(self) -> None:
        self.__candidates: List[bool] = [True, True, True, True, True, True, True, True, True]
        self.__value: int = 0

    @property
    def candidates(self) -> List[bool]:
        return self.__candidates

    def candidate(self, i: int) -> Optional[bool]:
        return self[i]

    def __getitem__(self, index: int) -> Optional[bool]:
        return self.__candidates[index] if 0 <= index < 9 else None

    def __setitem__(self, index: int, value: bool) -> None:
        if 0 <= index < 9:
            self.__candidates[index] = value

    def __eq__(self, other: '_Cell') -> bool:
        return self.candidates == other.candidates

    @property
    def value(self) -> int:
        return self.__value

    @value.setter
    def value(self, value: int) -> None:
        if not (1 <= value <= 9):
            raise ValueError(f"Value of a cell must be between 1-9 (inclusive). Got {value}")
        self.__value: int = value
        self.__candidates: List[bool] = [False, False, False, False, False, False, False, False, False]
        self.__candidates[value - 1]: bool = True

    def is_solved(self) -> bool:
        return self.value != 0

    def __str__(self) -> str:
        return str(self.value) if self.value else "-"

    def __repr__(self) -> str:
        return f"Cell({self.value})"


class _Region:
    __slots__ = ["__cells"]

    def __init__(self) -> None:
        self.__cells: List[Optional[_Cell]] = [
                                               _Cell(), _Cell(), _Cell(),
                                               _Cell(), _Cell(), _Cell(),
                                               _Cell(), _Cell(), _Cell(),
                                               ]

    @property
    def cells(self) -> List[_Cell]:
        return self.__cells

    def cell(self, i: int) -> Optional[_Cell]:
        return self[i]

    def __getitem__(self, index: int) -> Optional[_Cell]:
        return self.__cells[index] if 0 <= index < 9 else None

    def is_solved(self) -> bool:
        return all([cell.is_solved() for cell in self.cells])


class _Line(Sequence):
    def __init__(self,  *cells: _Cell):
        assert len(cells) == 9, "9 cells must be passed to create a full line"
        assert all(isinstance(cell, _Cell) for cell in cells), "All cells passed to a line must be of instance Cell"

        self.__cells: List[_Cell] = [*cells]

    @property
    def cells(self) -> List[_Cell]:
        return self.__cells

    def cell(self, i: int) -> Optional[_Cell]:
        return self.__cells[i] if 0 <= i < 9 else None

    def __len__(self) -> int:  # Required to be implemented by Sequence parent class
        return 9

    def __getitem__(self, splice: int) -> Union[_Cell, List[_Cell]]:
        return self.cells[splice]

    def __setitem__(self, i: int, value: int):
        self.__cells[i].value = value

    def is_solved(self) -> bool:
        return all([cell.is_solved() for cell in self.cells])


class Board:
    def __init__(self, file: str = None) -> None:
        self.__regions = [
                          _Region(), _Region(), _Region(),
                          _Region(), _Region(), _Region(),
                          _Region(), _Region(), _Region(),
                          ]

        self.__rows: List[_Line] = [
            _Line(self[0][0], self[0][1], self[0][2], self[1][0], self[1][1], self[1][2], self[2][0], self[2][1], self[2][2]),
            _Line(self[0][3], self[0][4], self[0][5], self[1][3], self[1][4], self[1][5], self[2][3], self[2][4], self[2][5]),
            _Line(self[0][6], self[0][7], self[0][8], self[1][6], self[1][7], self[1][8], self[2][6], self[2][7], self[2][8]),

            _Line(self[3][0], self[3][1], self[3][2], self[4][0], self[4][1], self[4][2], self[5][0], self[5][1], self[5][2]),
            _Line(self[3][3], self[3][4], self[3][5], self[4][3], self[4][4], self[4][5], self[5][3], self[5][4], self[5][5]),
            _Line(self[3][6], self[3][7], self[3][8], self[4][6], self[4][7], self[4][8], self[5][6], self[5][7], self[5][8]),

            _Line(self[6][0], self[6][1], self[6][2], self[7][0], self[7][1], self[7][2], self[8][0], self[8][1], self[8][2]),
            _Line(self[6][3], self[6][4], self[6][5], self[7][3], self[7][4], self[7][7], self[8][3], self[8][4], self[8][5]),
            _Line(self[6][6], self[6][7], self[6][8], self[7][6], self[7][7], self[7][8], self[8][6], self[8][7], self[8][8]),
        ]

        self.__columns: List[_Line] = [
            _Line(self[0][0], self[0][3], self[0][6], self[3][0], self[3][3], self[3][6], self[6][0], self[6][3], self[6][6]),
            _Line(self[0][1], self[0][4], self[0][7], self[3][1], self[3][4], self[3][7], self[6][1], self[6][4], self[6][7]),
            _Line(self[0][2], self[0][5], self[0][8], self[3][2], self[3][5], self[3][8], self[6][2], self[6][5], self[6][8]),

            _Line(self[1][0], self[1][3], self[1][6], self[4][0], self[4][3], self[4][6], self[7][0], self[7][3], self[7][6]),
            _Line(self[1][1], self[1][4], self[1][7], self[4][1], self[4][4], self[4][7], self[7][1], self[7][4], self[7][7]),
            _Line(self[1][2], self[1][5], self[1][8], self[4][2], self[4][6], self[4][8], self[7][2], self[7][5], self[7][8]),

            _Line(self[2][0], self[2][3], self[2][6], self[5][0], self[5][3], self[5][6], self[8][0], self[8][3], self[8][6]),
            _Line(self[2][1], self[2][4], self[2][7], self[5][1], self[5][4], self[5][7], self[8][1], self[8][4], self[8][7]),
            _Line(self[2][2], self[2][5], self[2][8], self[5][2], self[5][5], self[5][8], self[8][2], self[8][5], self[8][8]),
        ]
        if file:
            self.parse(file=file)

    def __getitem__(self, i: int) -> Optional[_Region]:
        return self.__regions[i] if 0 <= i < 9 else None

    @property
    def regions(self) -> List[_Region]:
        return self.__regions

    def region(self, i: int) -> Optional[_Region]:
        return self[i]

    @property
    def rows(self) -> List[_Line]:
        return self.__rows

    def row(self, i: int) -> _Line:
        return self.__rows[i]

    @property
    def columns(self) -> List[_Line]:
        return self.__columns

    def column(self, i: int) -> _Line:
        return self.__columns[i]

    def parse(self, file: str = None) -> None:
        with open(file) as sudoku_challenge:
            for i, row in enumerate(sudoku_challenge):
                row = row.strip()
                for j, value in enumerate(row):
                    value = int(value)
                    if value:
                        self.row(i).cell(j).value = value

    def __str__(self) -> str:
        ret: str = ""
        for i, row in enumerate(self.rows):
            if i and not i % 3:
                ret += '-' * 21
                ret += "\n"
            ret += " ".join(map(str, row[:3]))
            ret += " | "
            ret += " ".join(map(str, row[3:6]))
            ret += " | "
            ret += " ".join(map(str, row[6:9]))
            ret += "\n"
        return ret

    def draw(self) -> None:
        print(str(self))

    def update(self) -> None:
        # Remove candidates from regions
        for region in self.regions:
            if region.is_solved():
                continue
            for cell1 in region.cells:
                if cell1.value:
                    for cell2 in region.cells:
                        if not cell2.value and cell2[cell1.value]:
                            cell2[cell1.value] = False

        # Remove candidates from same row
        for row in self.rows:
            if row.is_solved():
                continue
            for cell1 in row:
                if cell1.value:
                    for cell2 in row:
                        if not cell2.value and cell2[cell1.value]:
                            cell2[cell1.value] = False

        # Remove candidates from same column
        for column in self.columns:
            if column.is_solved():
                continue
            for cell1 in column:
                if cell1.value:
                    for cell2 in column:
                        if not cell2.value and cell2[cell1.value]:
                            cell2[cell1.value] = False

        # Set value if only 1 candidate
        for region in self.regions:
            if region.is_solved():
                continue
            for cell in region.cells:
                if not cell.value and len(cell.candidates) == 1:
                    cell.value = cell.candidates[0]

        # Singularity in region
        for region in self.regions:
            if region.is_solved():
                continue
            for cell1 in region:
                if not cell1.value:
                    for candidate in cell1.candidates:
                        singularity = True
                        for cell2 in region:
                            if cell1 != cell2 and not cell2.value and cell2[candidate]:
                                singularity = False
                                break
                        if singularity:
                            cell1.value = candidate

        # Singularity in rows
        for row in self.rows:
            if all([cell.is_solved() for cell in row]):  # row.is_solved()
                continue
            for cell1 in row:
                if not cell1.value:
                    for candidate in cell1.candidates:
                        singularity = True
                        for cell2 in row:
                            if cell1 != cell2 and not cell2.value and cell2[candidate]:
                                singularity = False
                                break
                        if singularity:
                            cell1.value = candidate

        # Singularity in columns
        for column in self.columns:
            if all([cell.is_solved() for cell in column]):  # column.is_solved()
                continue
            for cell1 in column:
                if not cell1.value:
                    for candidate in cell1.candidates:
                        singularity = True
                        for cell2 in column:
                            if cell1 != cell2 and not cell2.value and cell2[candidate]:
                                singularity = False
                                break
                        if singularity:
                            cell1.value = candidate

    def solve(self) -> None:
        pass

    def is_solved(self) -> bool:
        return all([region.is_solved() for region in self.regions])

    def undo(self):
        pass
