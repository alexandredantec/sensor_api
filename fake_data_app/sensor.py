import sys
from datetime import date, timedelta

import numpy as np


class VisitSensor:
    """
    Simulates a sensor at the entrance of a mall.
    Takes a mean and a standard deviation
    and returns the number of visitors that passed through
    a particular door on a given date.
    """
    def __init__(
            self,
            avg_visit: int,
            std_visit: int,
            perc_break: float = 0.015,
            perc_malfunction: float = 0.035,
    ) -> None:
        """Initialize Sensor"""
        self.avg_visit = avg_visit
        self.std_visit = std_visit
        self.perc_malfunction = perc_malfunction
        self.perc_break = perc_break

    def simulate_visit_count(self, business_date: date) -> int:
        """Simulate the number of people detected by the sensor
        during the day"""

        # ensure measurements can be reproduced
        np.random.seed(seed=business_date.toordinal())

        # Find out the day of the business date: Monday = 0, Sunday = 6
        week_day = business_date.weekday()

        visit = np.random.normal(self.avg_visit, self.std_visit)
        # More traffic on Wednesdays (2), Fridays (4), and Saturdays (5)
        if week_day == 2:
            visit *= 1.10
        if week_day == 4:
            visit *= 1.25
        if week_day == 5:
            visit *= 1.35

        # if the business day is a Sunday the store is closed
        if week_day == 6:
            visit = -1

        # return an integer
        return np.floor(visit)

    def get_visit_count(self, business_date: date) -> int:
        """return the number of visitors detected by the sensor during the day"""

        np.random.seed(seed=business_date.toordinal())
        proba_malfunction = np.random.random()

        # the sensor can break sometimes
        if proba_malfunction < self.perc_break:
            print("break")
            return 0

        visit = self.simulate_visit_count(business_date)

        # the sensor can also malfunction
        if proba_malfunction < self.perc_malfunction:
            print("malfunction")
            visit = np.floor(visit * 0.2)  # make it so bad we can detect it

        return visit


if __name__ == "__main__":
    if len(sys.argv) > 1:
        year, month, day = [int(v) for v in sys.argv[1].split("-")]
    else:
        year, month, day = 2023, 10, 25
    queried_date = date(year, month, day)

    captor = VisitSensor(avg_visit=1500, std_visit=150)

    # ad hoc test to quickly verify malfunction and break
    # init_date = date(year=2022, month=1, day=1)
    # while init_date < date(year=2024, month=1, day=1):
    #     init_date += timedelta(days=1)
    #     visit_count = captor.get_visit_count(init_date)
    #     print(init_date, visit_count)
    print(captor.simulate_visit_count(queried_date))
