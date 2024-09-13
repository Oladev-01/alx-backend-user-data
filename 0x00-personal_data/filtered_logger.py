#!/usr/bin/env python3
"""masking pii"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str):  # noqa
    if fields is None or redaction is None:
        return message
    pattern = f"({'|'.join(fields)})=[^{separator}]+"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
