""" Main script handling json storage. """

import json
import logging

from datetime import datetime, date, timedelta
from typing import Dict, List, Union
from pathlib import PosixPath, Path

log = logging.getLogger(__name__)


class SpacedRepetitionManager:
    def __init__(self, data: PosixPath):
        self.data = data
        self.loaded_json = self._load_json()

    def _load_json(
        self,
    ) -> Dict[str, List[Union[str, datetime]]]:
        """Loads json file for manipulation by user."""
        with open("data/spaced_repetition.json", "r") as fp:
            json_data = json.load(fp)
            return json_data

    def _find_problems_to_repeat(self) -> None:
        pass

    def save_entry(
        self,
        problem_name: str,
        problem_url: str,
        date_completed: datetime = None,
        get_review_qs: bool = True,
    ) -> None:
        """ """
        if not date_completed:
            date_completed = date.today().strftime("%m/%d/%y")

        if problem_name in self.loaded_json.keys():
            times_reviewed = int(self.loaded_json[problem_name][2])
            times_reviewed = str(times_reviewed + 1)
            self.loaded_json[problem_name][2] = times_reviewed
            log.info("Entry (%s) has incremented times reviewed!", problem_name)

        else:
            self.loaded_json[problem_name] = [
                problem_url,
                date_completed,
                "1",
            ]
            log.info("Entry (%s) has been added!", problem_name)

        with open(self.data, "w") as fp:
            json.dump(self.loaded_json, fp)

        if get_review_qs:
            qs_for_review = self._get_review_qs()

            for item in qs_for_review:
                print(item)

    def _get_review_qs(
        self,
    ) -> List[str]:
        needs_review = []
        for prob_name, url_date_seen in self.loaded_json.items():

            url = url_date_seen[0]
            date_completed = url_date_seen[1]
            formatted_date = datetime.strptime(date_completed, "%m/%d/%y")
            times_completed = url_date_seen[2]

            num_days = abs((datetime.now() - formatted_date).days)

            if num_days >= 4 and times_completed == "1":
                needs_review.append(f"4 Day Review: \n{prob_name}: {url}")
            if num_days >= 7 and times_completed == "2":
                needs_review.append(f"One Week Review: \n{prob_name}: {url}")
            if num_days >= 30 and times_completed == "3":
                needs_review.append(f"One Month Review: \n{prob_name}: {url}")

        if not needs_review:
            needs_review.append(f"No problems found that need review.")

        return needs_review


if __name__ == "__main__":
    MyRepetitionManager = SpacedRepetitionManager(Path("data/spaced_repetition.json"))
    MyRepetitionManager.save_entry(
        "83. Remove Duplicates from Sorted List",
        "https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/",
        "12/29/24",
        get_review_qs=True,
    )
