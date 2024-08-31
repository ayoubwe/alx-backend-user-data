#!/usr/bin/env python3
"""
contains a function that Obfusicates a log message
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfusicate fields separeted bt separator in message by redaction
    and returns the obfusicated log
    """
    ans = ''
    for field in re.split(separator, message)[0:-1]:
        field = re.sub(r'=.*$', '=' + redaction, field) if \
            field.split('=')[0] in fields else field
        ans += field + ';'
    return ans
