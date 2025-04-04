import logging

LOGGER = logging.getLogger(__name__)


class ApartmentPlannerSystemExit(SystemExit):
    code: int = -1
    prefix_text: str = ""

    def __init__(self, msg: str, logger: logging.Logger = LOGGER):
        super().__init__(self.code, self.prefix_text + msg)
        logger.error(self.args[1])


class InputFileError(ApartmentPlannerSystemExit):
    code = 10
    prefix_text = "Error with input file: "
