import logging
from datetime import datetime

from croniter import croniter

from .timegen_every import Alarm

log = logging.getLogger("time-cron")


class CronAlarm(Alarm):

    description = "Frequency specified by cron-like format. nerds preferred"

    def __init__(self, obj):
        super().__init__()

        self.cron_format = obj["cron_format"]
        if not croniter.is_valid(self.cron_format):
            raise ValueError("Invalid cron_format: %s" % self.cron_format)

    def next_ring(self, current_time=None):
        if current_time is None:
            current_time = datetime.now()

        return croniter(self.cron_format, current_time).get_next(datetime)

    def has_ring(self, current_time=None):
        # cron specification has no possibility of being over
        return True
