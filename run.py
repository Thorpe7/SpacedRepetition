""" Running Spaced Repetition script & terminal user input. """

import logging

from pathlib import Path
from src.main import SpacedRepetitionManager

log = logging.basicConfig(level=logging.INFO)


def main() -> None:

    prob_name, url, date_completed = input(
        "Please Enter: \nProblem Name, URL, and date completed:"
    ).split(", ")
    MyReviewManager = SpacedRepetitionManager(Path("data/spaced_repetition.json"))
    MyReviewManager.save_entry(
        problem_name=prob_name, problem_url=url, date_completed=date_completed
    )


if __name__ == "__main__":
    main()
