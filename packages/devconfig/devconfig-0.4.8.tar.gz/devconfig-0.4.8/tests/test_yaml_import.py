import pytest
import devconfig
import pythonjsonlogger.jsonlogger
import sys
import logging


def test_logging_configured(uncached):
    devconfig_logger = logging.getLogger('devconfig')
    assert isinstance(devconfig_logger.handlers[0].formatter, pythonjsonlogger.jsonlogger.JsonFormatter)
