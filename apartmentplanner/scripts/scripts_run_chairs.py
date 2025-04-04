from pathlib import Path

from apartmentplanner.tools import setup_logs

from apartmentplanner import Apartment

IS_CONSOLE_LOG_DEBUG = False

PLAN_PATH = Path(__file__).parent.resolve() / "config" / "rooms.txt"
OUTPUT_PATH = Path(__file__).parent.resolve() / "results" / "result.txt"


def apartment_run():

    setup_logs(IS_CONSOLE_LOG_DEBUG)

    apartment = Apartment.from_plan(PLAN_PATH)
    apartment.run(OUTPUT_PATH)


if __name__ == "__main__":
    apartment_run()
