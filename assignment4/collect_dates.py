"""
Task 2 (IN4110 only)

parsing dates from wikipedia
"""

from __future__ import annotations

import re

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns() -> tuple[str, str, str]:
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """
    #raise NotImplementedError("remove me to begin task")

    # Regex to capture days, months and years with numbers
    year = r"(?P<year>\d{4})"
    month = r"(?P<month>\d{1,2}|[A-Za-z]{3,9})"
    day = r"(?P<day>\d{1,2})"
    return year, month, day


def convert_month(s: str) -> str:
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    #raise NotImplementedError("remove me to begin task")
    # If already digit do nothing
    if s.isdigit():
        return s

    # Convert to number as string
    return str(month_names.index(s) + 1).zfill(2)


def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    #raise NotImplementedError("remove me to begin task")
    return n.zfill(2)


def find_dates(text: str, output: str | None = None) -> list[str]:
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
        output (str, Optional) : The file to write the output to if wanted
    return:
        results (List): A list with all the dates found
    """
    #raise NotImplementedError("remove me to begin task")
    
    year, month, day = get_date_patterns()

    # Date on format YYYY/MM/DD - ISO
    ISO = fr"\b{year}-{month}-{day}\b"

    # Date on format DD/MM/YYYY
    DMY = fr"\b{day}/{month}/{year}\b"

    # Date on format MM/DD/YYYY
    MDY = fr"\b{month}/{day}/{year}\b"

    # Date on format YYYY/MM/DD
    YMD = fr"\b{year}/{month}/{day}\b"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

# find all dates in any format in text
    if isinstance(text, tuple):
        for component in text:
            dates.extend(re.findall(formats, component))
    else:
        for format in formats:
            dates.extend(re.findall(format, text))

    # Convert dates to YYYY/MM/DD format
    for i in range(len(dates)):
        date = dates[i]

        # Check if the date is a tuple
        if isinstance(date, tuple):
            year, month, day = date
        else:
            year, month, day = date.split("/")

        # Convert the month to a number if it is a string
        if month.isalpha():
            month = convert_month(month, month_names)

        month = zero_pad(month)
        day = zero_pad(day)

        # Reassemble the date in YYYY/MM/DD format
        dates[i] = f"{year}/{month}/{day}"

    # Write to file if wanted
    if output is not None:
        with open(output, "w") as f:
            for date in dates:
                f.write(f"{date}\n")

    return dates