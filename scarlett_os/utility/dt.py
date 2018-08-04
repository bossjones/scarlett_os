"""Provides helper methods to handle the time in HA."""
import datetime as dt
import re

# pylint: disable=unused-import
from typing import Any, Union, Optional, Tuple  # noqa

import pytz

from functools import reduce

DATE_STR_FORMAT = "%Y-%m-%d"
UTC = DEFAULT_TIME_ZONE = pytz.utc  # type: dt.tzinfo


# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
DATETIME_RE = re.compile(
    r"(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    r"[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
    r"(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?"
    r"(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$"
)


def set_default_time_zone(time_zone: dt.tzinfo) -> None:
    """Set a default time zone to be used when none is specified.

    Async friendly.
    """
    global DEFAULT_TIME_ZONE  # pylint: disable=global-statement

    # NOTE: Remove in the future in favour of typing
    assert isinstance(time_zone, dt.tzinfo)

    DEFAULT_TIME_ZONE = time_zone


def get_time_zone(time_zone_str: str) -> Optional[dt.tzinfo]:
    """Get time zone from string. Return None if unable to determine.

    Async friendly.
    """
    try:
        return pytz.timezone(time_zone_str)
    except pytz.exceptions.UnknownTimeZoneError:
        return None


def utcnow() -> dt.datetime:
    """Get now in UTC time."""
    return dt.datetime.now(UTC)


def now(time_zone: dt.tzinfo = None) -> dt.datetime:
    """Get now in specified time zone."""
    return dt.datetime.now(time_zone or DEFAULT_TIME_ZONE)


def as_utc(dattim: dt.datetime) -> dt.datetime:
    """Return a datetime as UTC time.

    Assumes datetime without tzinfo to be in the DEFAULT_TIME_ZONE.
    """
    if dattim.tzinfo == UTC:
        return dattim
    elif dattim.tzinfo is None:
        dattim = DEFAULT_TIME_ZONE.localize(dattim)

    return dattim.astimezone(UTC)


def as_timestamp(dt_value):
    """Convert a date/time into a unix time (seconds since 1970)."""
    if hasattr(dt_value, "timestamp"):
        parsed_dt = dt_value
    else:
        parsed_dt = parse_datetime(str(dt_value))
        if not parsed_dt:
            raise ValueError("not a valid date/time.")
    return parsed_dt.timestamp()


def as_local(dattim: dt.datetime) -> dt.datetime:
    """Convert a UTC datetime object to local time zone."""
    if dattim.tzinfo == DEFAULT_TIME_ZONE:
        return dattim
    elif dattim.tzinfo is None:
        dattim = UTC.localize(dattim)

    return dattim.astimezone(DEFAULT_TIME_ZONE)


def utc_from_timestamp(timestamp: float) -> dt.datetime:
    """Return a UTC time from a timestamp."""
    return dt.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)


def start_of_local_day(dt_or_d: Union[dt.date, dt.datetime] = None) -> dt.datetime:
    """Return local datetime object of start of day from date or datetime."""
    if dt_or_d is None:
        date = now().date()  # type: dt.date
    elif isinstance(dt_or_d, dt.datetime):
        date = dt_or_d.date()
    return DEFAULT_TIME_ZONE.localize(dt.datetime.combine(date, dt.time()))


# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
# https://github.com/django/django/blob/master/LICENSE
def parse_datetime(dt_str: str) -> dt.datetime:
    """Parse a string and return a datetime.datetime.

    This function supports time zone offsets. When the input contains one,
    the output uses a timezone with a fixed offset from UTC.
    Raises ValueError if the input is well formatted but not a valid datetime.
    Returns None if the input isn't well formatted.
    """
    match = DATETIME_RE.match(dt_str)
    if not match:
        return None
    kws = match.groupdict()  # type: Dict[str, Any]
    if kws["microsecond"]:
        kws["microsecond"] = kws["microsecond"].ljust(6, "0")
    tzinfo_str = kws.pop("tzinfo")

    tzinfo = None  # type: Optional[dt.tzinfo]
    if tzinfo_str == "Z":
        tzinfo = UTC
    elif tzinfo_str is not None:
        offset_mins = int(tzinfo_str[-2:]) if len(tzinfo_str) > 3 else 0
        offset_hours = int(tzinfo_str[1:3])
        offset = dt.timedelta(hours=offset_hours, minutes=offset_mins)
        if tzinfo_str[0] == "-":
            offset = -offset
        tzinfo = dt.timezone(offset)
    else:
        tzinfo = None
    kws = {k: int(v) for k, v in kws.items() if v is not None}
    kws["tzinfo"] = tzinfo
    return dt.datetime(**kws)


def parse_date(dt_str: str) -> dt.date:
    """Convert a date string to a date object."""
    try:
        return dt.datetime.strptime(dt_str, DATE_STR_FORMAT).date()
    except ValueError:  # If dt_str did not match our format
        return None


def parse_time(time_str):
    """Parse a time string (00:20:00) into Time object.

    Return None if invalid.
    """
    parts = str(time_str).split(":")
    if len(parts) < 2:
        return None
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        second = int(parts[2]) if len(parts) > 2 else 0
        return dt.time(hour, minute, second)
    except ValueError:
        # ValueError if value cannot be converted to an int or not in range
        return None


# Found in this gist: https://gist.github.com/zhangsen/1199964
def get_age(date: dt.datetime) -> str:
    # pylint: disable=too-many-return-statements
    """
    Take a datetime and return its "age" as a string.

    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it won't work.
    """

    def formatn(number: int, unit: str) -> str:
        """Add "unit" if it's plural."""
        if number == 1:
            return "1 %s" % unit
        elif number > 1:
            return "%d %ss" % (number, unit)

    def q_n_r(first: int, second: int) -> Tuple[int, int]:
        """Return quotient and remaining."""
        return first // second, first % second

    delta = now() - date
    day = delta.days
    second = delta.seconds

    year, day = q_n_r(day, 365)
    if year > 0:
        return formatn(year, "year")

    month, day = q_n_r(day, 30)
    if month > 0:
        return formatn(month, "month")
    if day > 0:
        return formatn(day, "day")

    hour, second = q_n_r(second, 3600)
    if hour > 0:
        return formatn(hour, "hour")

    minute, second = q_n_r(second, 60)
    if minute > 0:
        return formatn(minute, "minute")

    return formatn(second, "second") if second > 0 else "0 seconds"


def parse_time_i(timestr, err=(ValueError, re.error)):
    """Parse a time string in hh:mm:ss, mm:ss, or ss format."""
    if timestr[0:1] == "-":
        m = -1
        timestr = timestr[1:]
    else:
        m = 1
    try:
        return m * reduce(lambda s, a: s * 60 + int(a), re.split(r":|\.", timestr), 0)
    except err:
        return 0


def validate_query_date(datestr):  # noqa
    """Validates a user provided date that can be compared using date_key().

    Returns True id the date is valid.
    """

    parts = datestr.split("-")
    if len(parts) > 3:
        return False

    if len(parts) > 2:
        try:
            v = int(parts[2])
        except ValueError:
            return False
        else:
            if not 1 <= v <= 31:
                return False

    if len(parts) > 1:
        try:
            v = int(parts[1])
        except ValueError:
            return False
        else:
            if not 1 <= v <= 12:
                return False

    try:
        int(parts[0])
    except ValueError:
        return False

    return True


def date_key(datestr):  # noqa
    """Parse a date format y-m-d and returns an undefined integer that
    can only be used to compare dates.

    In case the date string is invalid the returned value is undefined.
    """

    # this basically does "2001-02-03" -> 20010203

    default = [0, 1, 1]
    parts = datestr.split("-")
    parts += default[len(parts) :]

    value = 0
    for d, p, m in zip(default, parts, (10000, 100, 1)):
        try:
            value += int(p) * m
        except ValueError:
            # so that "2003-01-" is equal to "2003-01" ..
            value += d * m
    return value


# NOTE: Duplicate function
# def parse_date(datestr):  # noqa
#     """Parses yyyy-mm-dd date format and returns unix time.

#     Raises ValueError in case the input couldn't be parsed.
#     """

#     import time

#     try:
#         frmt = ["%Y", "%Y-%m", "%Y-%m-%d"][datestr.count("-")]
#     except IndexError:
#         raise ValueError

#     return time.mktime(time.strptime(datestr, frmt))


def format_time(time):
    """Turn a time value in seconds into hh:mm:ss or mm:ss."""

    if time < 0:
        time = abs(time)
        prefix = "-"
    else:
        prefix = ""
    if time >= 3600:  # 1 hour
        # time, in hours:minutes:seconds
        return "%s%d:%02d:%02d" % (prefix, time // 3600, (time % 3600) // 60, time % 60)
    else:
        # time, in minutes:seconds
        return "%s%d:%02d" % (prefix, time // 60, time % 60)


def format_time_display(time):
    """Like format_time, but will use RATIO instead of a colon to separate"""

    return format_time(time).replace(":", u"\u2236")
