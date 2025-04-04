import logging
import os
import sys
from os import PathLike
from pathlib import Path
from typing import List, Union

from apartmentplanner.errors import InputFileError

LOGGER = logging.getLogger(__name__)


def read_plan(plan_path: Union[str, Path, PathLike]) -> List[str]:
    """
    Reads an apartment plan file and returns it as a list of strings containing plan information for each row.

    Args:
        plan_path: path to apartment plan file (txt)

    Returns:
        List if string with the loaded plan
    """

    if not isinstance(plan_path, (str, PathLike)):
        msg = f"Unable to read conf from {type(plan_path).__name__} object: {plan_path}"
        LOGGER.error(msg)
        LOGGER.error("Use str or Path instead")
        raise InputFileError(msg)

    if not os.path.isfile(plan_path):
        msg = f"plan file not found : {plan_path}"
        LOGGER.error(msg)
        raise FileNotFoundError(msg)

    extension = Path(plan_path).suffix

    # txt file
    if extension.lower() in [".txt"]:
        try:
            with open(
                plan_path,
                "r",
                encoding="utf-8",
            ) as f:
                plan = f.read().splitlines()

        except Exception as e:
            msg = f"There was an issue while reading the plan in txt format: {e}"
            raise InputFileError(msg=msg, logger=LOGGER) from e

    else:
        msg = f"Unable to read extension {extension}"
        raise InputFileError(msg=msg, logger=LOGGER)

    return plan


def setup_logs(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    log_format = "%(asctime)s UTC [%(levelname)s] (%(module)s) - %(message)s"
    date_format = "%Y-%m-%dT%H:%M:%S%z"

    stdout_handler = logging.StreamHandler(sys.stdout)

    handlers: List[logging.Handler] = [stdout_handler]

    logging.basicConfig(format=log_format, datefmt=date_format, level=level, handlers=handlers)
