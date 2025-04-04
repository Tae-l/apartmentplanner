import argparse
import logging

from apartmentplanner.tools import setup_logs

from apartmentplanner import Apartment

LOGGER = logging.getLogger(__file__)


def run() -> None:
    # define parser and its arguments
    parser = argparse.ArgumentParser()

    help_plan = "path to load the plan file in .txt format"
    parser.add_argument("--plan", help=help_plan, required=True)

    help_output = "path to save the results in txt"
    parser.add_argument("--output", help=help_output, default=None)

    parser.add_argument("--verbose", action="store_true", help="set verbose mode")

    args = parser.parse_args()

    setup_logs(args.verbose)

    # run simulation
    LOGGER.info("Launching ApartmentPlanner with args:")
    LOGGER.info("* plan_path = %s", args.plan)
    LOGGER.info("* output = %s", args.output)

    apartment = Apartment.from_plan(args.plan)
    apartment.run(args.output)


if __name__ == "__main__":
    run()
