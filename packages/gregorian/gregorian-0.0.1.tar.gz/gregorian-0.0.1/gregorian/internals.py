import datetime
import pandas as pd

def isdatelike(value):
    """
    Returns whether a given value has a date-like interface
    """
    if isinstance(value, (datetime.date, datetime.datetime, pd.Timestamp)):
        return True
    return False