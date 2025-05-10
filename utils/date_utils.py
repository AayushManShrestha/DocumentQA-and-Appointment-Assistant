# date_utils.py
import parsedatetime
from datetime import datetime

def parse_natural_date(text: str):
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(text)
    if parse_status == 0:
        return None
    parsed_date = datetime(*time_struct[:6])
    return parsed_date.date().isoformat()
