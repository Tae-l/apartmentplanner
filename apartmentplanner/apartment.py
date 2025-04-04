import copy
import json
import logging
import re
from dataclasses import dataclass, field
from os import PathLike
from pathlib import Path
from typing import Dict, List, Optional, Union

from apartmentplanner.errors import InputFileError
from apartmentplanner.tools import read_plan

LOGGER = logging.getLogger(__name__)

DEFAULT_CHAIRS_DICT = {"C": 0, "P": 0, "S": 0, "W": 0}
CHAIRS = ["C", "P", "S", "W"]
WALL_CHAR = ["/", "\\", "|", "+", "-"]


@dataclass
class Bloc:
    """
    Class to describe any kind of bloc of character inside the plan with:
    Args:
        row (int): its row placement
        start (int): beginning of its column placement
        end (int): end of its column placement
    """

    row: int
    start: int
    end: int

    def __repr__(self):
        return f"{self.row}: ({self.start}, {self.end})"


@dataclass
class Walls:
    """
    Class to describe the placement of walls inside the plan.
    An instance Walls is defined by:
    Args:
        row (int): its row placements
        cols (List[Bloc]): a list of `Bloc` describing the placement of different walls inside this row
    """

    row: int
    cols: List[Bloc] = field(default_factory=list)

    def empty_spaces(self) -> List[Bloc]:
        """
        Return a list of `Bloc` describing the placement of empty spaces between the walls of its own row
        """
        if len(self.cols) == 1:
            return []

        empty_spaces = []
        for wall, next_wall in zip(self.cols[0:-1], self.cols[1:]):
            empty_spaces.append(Bloc(row=self.row, start=wall.end, end=next_wall.start))
        return empty_spaces

    def __repr__(self):
        return f"{self.row}: {[(col.start, col.end) for col in self.cols]}"


@dataclass
class Room:
    """
    Class to describe the placement of room inside the plan.
    A Room is defined by
    Args:
        name (str): its name,
        spaces (List[Bloc]): a list of `Bloc` describing the empty spaces occupied by the room inside the plan,
        chairs (Dict): a dictionary describing the number of each type of chair present in the room,
        is_closed (bool): a boolean describing if the room has been closed or not during its construction

    """

    name: Optional = None
    chairs: Dict[str, int] = field(default_factory=dict)
    spaces: list[Bloc] = field(default_factory=list)
    is_closed: bool = False

    def __repr__(self):
        return f"{self.name}: {self.chairs}"


class Apartment:
    def __init__(self, plan: List[str]) -> None:
        """
        Main class of ApartmentPlanner project.
        Stores the plan of the apartment from old txt format and :
            walls: list of Walls describing the placement of walls inside the plan
            rooms: list of Room describing the empty spaces occupied by the room inside the plan and their chairs
            chairs: dictionary describing the number of each type of chair present in the whole apartment

        Args:
            plan (List[str]): Apartment plan from old txt format stored as list of strings
        """
        self.plan = plan
        self.rooms: List[Room] = []
        self.walls: List[Walls] = []
        self.chairs: dict[str, int] = copy.deepcopy(DEFAULT_CHAIRS_DICT)

    def find_walls(self) -> None:
        """
        Parse the plan of the apartment row by row and create an instance of `Walls` for each row, describing the
        placement of walls inside this row. Each instances of `Walls` is added to `Apartment`
        Wall type characters are defined in global variable WALL_CHAR
        """
        for i, _row in enumerate(self.plan):
            walls = list(re.finditer(rf"[{''.join(WALL_CHAR)}]+", _row))
            if walls:
                walls_cols = [Bloc(row=i, start=wall.start(), end=wall.end()) for wall in walls]
                new_walls = Walls(row=i, cols=walls_cols)
                self.walls.append(new_walls)

    def find_rooms(self) -> None:
        """
        Parse the different `Walls` of the apartment row by row and assign the empty spaces between them to a list of
        `Room`.
        A new empty space is either the continuity of a previous one and part of an opened room or define the beginning
        of a new room
        A room is closed when we encounter a wall larger than it's previous empty space
        """

        temp_rooms = []

        for walls in self.walls:
            # if new wall is longer than previous empty space -> close room
            for room in temp_rooms:
                for col in walls.cols:
                    if col.start < room.spaces[-1].start and col.end > room.spaces[-1].end:
                        room.is_closed = True
                        self.rooms.append(room)
            # remove closed rooms
            temp_rooms = [room for room in temp_rooms if not room.is_closed]
            # try to assign empty space to current rooms
            for space in walls.empty_spaces():
                for room in temp_rooms:
                    if max(room.spaces[-1].start, space.start) < min(room.spaces[-1].end, space.end):
                        room.spaces.append(space)
                        break
                # create new room
                else:
                    new_room = Room()
                    new_room.spaces.append(space)
                    temp_rooms.append(new_room)

    def populate_rooms(self) -> None:
        """
        Base on each room placement information, analyse character in each room empty space to find its name and the
        number of each type of chair present in the room
        """
        for room in self.rooms:
            room.chairs = copy.deepcopy(DEFAULT_CHAIRS_DICT)
            for space in room.spaces:
                text = self.plan[space.row][space.start : space.end]
                # looking for up to two words in parentheses, should be generalized if other structure is to be expected
                name = re.search(r"\(\w+.\w+\)", text)
                if name:
                    room.name = name[0][1:-1]
                for chair_type in CHAIRS:
                    room.chairs[chair_type] += text.count(chair_type)

    def compute_chairs(self) -> None:
        """
        Compute total amount of chairs in the apartment based on the detail for each room
        """
        for chair_type in CHAIRS:
            for room in self.rooms:
                self.chairs[chair_type] += room.chairs[chair_type]

    def save_output(self, output_path: [str, PathLike]) -> None:
        """
        Save detail of the number of chair in the apartment
        Two format available:
            .json : classic dict like format
            .txt : specific text format required for old system
        Args:
            output_path ([str, PathLike]): path to save the output file
        """

        LOGGER.info(f"Saving output to: {output_path}")
        output_path = Path(output_path)

        if not output_path.parent.exists():
            output_path.parent.mkdir(parents=True)

        extension = output_path.suffix

        if extension.lower() == ".json":
            output = {
                "apartment": self.chairs,
            }
            for room in self.rooms:
                output.update({room.name: room.chairs})

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=4)

        elif extension.lower() == ".txt":
            output = (
                f"total:\n"
                f"W: {self.chairs['W']}, P: {self.chairs['P']}, S: {self.chairs['S']}, C: {self.chairs['C']}\n"
            )
            for room in self.rooms:
                output += (
                    f"{room.name}\n"
                    f"W: {room.chairs['W']}, P: {room.chairs['P']}, S: {room.chairs['S']}, C: {room.chairs['C']}\n"
                )

                with open(
                    output_path,
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(output)

        else:
            raise NotImplementedError("Output format not supported, please choose between .json and .txt")

    def run(self, output_path: Union[str, PathLike]) -> None:
        """
        Main run for new `Apartment` instance
        Compute wall and room placement information
        Compute chairs information
        Save output file
        Args:
            output_path ([str, PathLike]): path to save the output file
        """
        LOGGER.info("Run Apartment ...")

        self.find_walls()
        self.find_rooms()
        self.populate_rooms()
        self.compute_chairs()
        self.save_output(output_path=output_path)

    @classmethod
    def from_plan(
        cls,
        plan_path: Union[str, PathLike],
    ) -> "Apartment":
        """
        Init an ApartmentPlanner instance from a plan file in txt format.

        Args:
            plan_path: Plan file in txt format.
        """

        if not isinstance(plan_path, (str, PathLike)):
            msg = f"Unable to read plan from {type(plan_path).__name__} object: {plan_path}"
            LOGGER.error(msg)
            LOGGER.error("Use str or Path")
            raise InputFileError(msg)

        if not Path(plan_path).exists():
            msg = f"plan path not found : {plan_path}"
            LOGGER.error(msg)
            raise FileNotFoundError(msg)

        LOGGER.info("Initializing Apartment from plan...")
        plan = read_plan(plan_path)

        return cls(plan=plan)
