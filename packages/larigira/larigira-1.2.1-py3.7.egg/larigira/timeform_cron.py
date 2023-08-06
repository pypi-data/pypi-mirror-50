import logging

from flask_wtf import Form
from wtforms import StringField, validators, SubmitField, ValidationError
from croniter import croniter

log = logging.getLogger(__name__)


class CronAlarmForm(Form):
    nick = StringField(
        "Alarm nick",
        validators=[validators.required()],
        description="A simple name to recognize this alarm",
    )
    cron_format = StringField(
        "cron-like format",
        validators=[validators.required()],
        description="the frequency specification, as in the <tt>cron</tt> command; "
        'see <a href="https://crontab.guru/">crontab.guru</a> for a hepl with cron format',
    )
    submit = SubmitField("Submit")

    def populate_from_timespec(self, timespec):
        if "nick" in timespec:
            self.nick.data = timespec["nick"]
        if "cron_format" in timespec:
            self.cron_format.data = timespec["cron_format"]

    def validate_cron_format(self, field):
        if not croniter.is_valid(field.data):
            raise ValidationError("formato di cron non valido")


def cronalarm_receive(form):
    return {
        "kind": "cron",
        "nick": form.nick.data,
        "cron_format": form.cron_format.data,
    }
