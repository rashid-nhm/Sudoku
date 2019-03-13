from collections import Sequence
from typing import List, Optional, Union, Dict


class _Cell:
    __slots__ = ["__candidates", "__value", "__states"]

    def __init__(self) -> None:
        self.__candidates: List[bool] = [True, True, True, True, True, True, True, True, True]
        self.__value: int = 0
        self.__states: List[Dict] = [{"value": self.value, "candidates": self.candidates}]

    @property
    def candidates(self) -> List[int]:
        return [i+1 for i, c in enumerate(self.__candidates) if c]

    @property
    def num_possible_values(self) -> int:
        return len([candidate for candidate in self.candidates if candidate])

    def candidate(self, i: int) -> Optional[bool]:
        return self[i]

    def __getitem__(self, index: int) -> Optional[bool]:
        return self.__candidates[index] if 0 <= index < 9 else None

    def __setitem__(self, index: int, value: bool) -> None:
        if 0 <= index < 9:
            self.__states.append({"value": self.value, "candidates": self.candidates})
            self.__candidates[index] = value

    def __eq__(self, other: '_Cell') -> bool:
        return self.candidates == other.candidates

    @property
    def value(self) -> int:
        return self.__value

    @property
    def states(self) -> List[Dict]:
        return self.__states

    @value.setter
    def value(self, value: int) -> None:
        if not (1 <= value <= 9):
            raise ValueError(f"Value of a cell must be between 1-9 (inclusive). Got {value}")
        self.__states.append({"value": self.value, "candidates": self.candidates})
        self.__value: int = value
        self.__candidates: List[bool] = [False, False, False, False, False, False, False, False, False]
        self.__candidates[value - 1]: bool = True

    def is_solved(self) -> bool:
        return self.value != 0

    def rollback(self) -> None:
        assert len(self.__states), "No further states to roll back to"
        last_state = self.__states.pop()
        self.__value = last_state["value"]
        self.__candidates = [False, False, False, False, False, False, False, False, False]
        for c in last_state["candidates"]:
            self.__candidates[c-1] = True

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
    __slots__ = ["__cells"]

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
    __slots__ = ["__regions", "__rows", "__columns", "__states"]

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
            _Line(self[6][3], self[6][4], self[6][5], self[7][3], self[7][4], self[7][5], self[8][3], self[8][4], self[8][5]),
            _Line(self[6][6], self[6][7], self[6][8], self[7][6], self[7][7], self[7][8], self[8][6], self[8][7], self[8][8]),
        ]

        self.__columns: List[_Line] = [
            _Line(self[0][0], self[0][3], self[0][6], self[3][0], self[3][3], self[3][6], self[6][0], self[6][3], self[6][6]),
            _Line(self[0][1], self[0][4], self[0][7], self[3][1], self[3][4], self[3][7], self[6][1], self[6][4], self[6][7]),
            _Line(self[0][2], self[0][5], self[0][8], self[3][2], self[3][5], self[3][8], self[6][2], self[6][5], self[6][8]),

            _Line(self[1][0], self[1][3], self[1][6], self[4][0], self[4][3], self[4][6], self[7][0], self[7][3], self[7][6]),
            _Line(self[1][1], self[1][4], self[1][7], self[4][1], self[4][4], self[4][7], self[7][1], self[7][4], self[7][7]),
            _Line(self[1][2], self[1][5], self[1][8], self[4][2], self[4][5], self[4][8], self[7][2], self[7][5], self[7][8]),

            _Line(self[2][0], self[2][3], self[2][6], self[5][0], self[5][3], self[5][6], self[8][0], self[8][3], self[8][6]),
            _Line(self[2][1], self[2][4], self[2][7], self[5][1], self[5][4], self[5][7], self[8][1], self[8][4], self[8][7]),
            _Line(self[2][2], self[2][5], self[2][8], self[5][2], self[5][5], self[5][8], self[8][2], self[8][5], self[8][8]),
        ]
        if file:
            self.parse(file=file)

        self.__states = []

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

    @staticmethod
    def __remove_candidates(areas):
        cells_changed = []
        for area in areas:
            if area.is_solved():
                continue
            for i, sub_cell in enumerate(area.cells):
                if sub_cell.value:
                    for j, sub_cell2 in enumerate(area.cells):
                        if i == j:  # Don't compare the same cell to itself
                            continue
                        if not sub_cell2.value and sub_cell2[sub_cell.value-1]:
                            sub_cell2[sub_cell.value-1] = False
                            cells_changed.append(sub_cell2)
        return cells_changed

    @staticmethod
    def __remove_singularity(areas):
        cells_changed = []
        for area in areas:
            if area.is_solved():
                continue
            for i, sub_cell in enumerate(area.cells):
                if not sub_cell.value:
                    for j, candidate in enumerate(sub_cell.candidates):
                        if i == j:  # Don't compare the same cell to itself
                            continue
                        singular = True
                        for sub_cell2 in area.cells:
                            if sub_cell2.value == candidate or not sub_cell2.value and sub_cell2[candidate-1]:
                                singular = False
                                break
                        if singular:
                            sub_cell.value = candidate
                            cells_changed.append(sub_cell)
        return cells_changed

    @staticmethod
    def __validate_areas(areas):
        for area in areas:
            values = [cell.value for cell in area.cells if cell.value != 0]
            if len(values) != len(set(values)):
                return False
        return True

    def update(self) -> None:
        if self.is_solved():  # Nothing to update
            return None

        cells_changed = []

        cells_changed.extend(self.__remove_candidates(self.regions))
        cells_changed.extend(self.__remove_candidates(self.rows))
        cells_changed.extend(self.__remove_candidates(self.columns))

        # Set value if only 1 candidate
        for region in self.regions:
            if region.is_solved():
                continue
            for cell in region.cells:
                if cell.num_possible_values == 1:
                    cell.value = cell.candidates[0]
                    cells_changed.append(cell)

        # Singularity in region
        cells_changed.extend(self.__remove_singularity(self.regions))
        cells_changed.extend(self.__remove_singularity(self.rows))
        cells_changed.extend(self.__remove_singularity(self.columns))

        self.__states.append(cells_changed)

    def validate(self) -> bool:
        return self.__validate_areas(self.regions) \
               and self.__validate_areas(self.rows) \
               and self.__validate_areas(self.columns)

    def solve(self) -> None:
        pass

    def brute_force(self) -> None:
        pass

    def is_solved(self) -> bool:
        return all([region.is_solved() for region in self.regions])

    def undo(self):
        if not self.__states:
            return "Nothing to revert back to"
        last_state = self.__states.pop()
        for cell in last_state:
            cell.rollback()
