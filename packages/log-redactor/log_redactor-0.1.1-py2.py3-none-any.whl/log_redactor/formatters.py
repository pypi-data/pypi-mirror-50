# -*- coding: utf-8 -*-

"""Main module."""
from logging import Formatter, LogRecord


class RedactingFormatter(object):
    def __init__(self, orig_formatter: Formatter, patterns: list):
        self.orig_formatter = orig_formatter
        self._patterns = patterns

    def format(self, record: LogRecord):
        for pattern in self._patterns:
            record.msg = record.msg.replace(pattern, "YEET")
        new_record = self.orig_formatter.format(record)
        return new_record

    def __getattr__(self, attr):
        return getattr(self.orig_formatter, attr)
