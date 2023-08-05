import json
import logging
import sys
from typing import Dict, Optional, Set


class LoggerWithFlexibleArgsAdapter(logging.LoggerAdapter):
    """
        This class just add any keyword argument of the standard logging functions to 'extra' key
        of the extra argument of LogRecord constructor. This is very useful with structured logging
        because extra argument will be passed as is to a formatter. In conjunction with
        JsonFormatter this will result that the keyword arguments will appears in a JSON document
        in "extra" key.
    """

    def process(self, msg, kwargs):
        new_kwargs = {}

        # Cleanup any real argument of Logger._log() except 'extra' from original kwargs
        _log_method_args = {'level', 'msg', 'args', 'exc_info', 'stack_info'}
        for arg in _log_method_args:
            if arg in kwargs:
                new_kwargs[arg] = kwargs[arg]
                del kwargs[arg]

        new_kwargs['extra'] = {'extra': {**self.extra}}
        if 'extra' in kwargs:
            new_kwargs['extra']['extra'].update(kwargs['extra'])
            del kwargs['extra']
        new_kwargs['extra']['extra'].update(kwargs)

        return msg, new_kwargs

    # Unfortunately Python community still don't use Decorator patter for LoggerAdapter class
    # and I should implement this method by hand
    def addHandler(self, hdlr):
        return self.logger.addHandler(hdlr)


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style='%',
        skip_fields_calculation: Optional[Set[str]] = None,
        drop_fields_from_json: Optional[Set[str]] = None,
        simplify_exception_text: bool = True,
        json_dumps_args: Optional[Dict] = None,
    ):
        super().__init__(fmt, datefmt, style)
        self._skip_fields_calculation = set(skip_fields_calculation) if skip_fields_calculation \
            else set()
        self._drop_fields_from_json = set(drop_fields_from_json) if drop_fields_from_json else set()
        self._simplify_exception_text = bool(simplify_exception_text)
        self._json_dumps_args = json_dumps_args if json_dumps_args else {}

    def format(self, record: logging.LogRecord):
        if isinstance(record.msg, dict):
            if hasattr(record, 'extra'):
                record.extra.update(record.msg)
            record.message = None
        else:
            record.message = record.getMessage()

        if record.message is not None and 'messageFormatted' not in self._skip_fields_calculation:
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)
            record.messageFormatted = self.formatMessage(record)

        if record.exc_info:
            record.exceptionClass = record.exc_info[0].__name__
            record.exceptionMessage = str(record.exc_info[1])
            # Cache the traceback text to avoid converting it multiple times (it's constant anyway)
            if not record.exc_text and 'exc_text' not in self._skip_fields_calculation:
                record.exc_text = self.formatException(record.exc_info)

        json_data = record.__dict__

        del json_data['msg'], json_data['args']
        # We can't serialize exc_info to JSON by default thus drop it.
        del json_data['exc_info']

        for field in self._drop_fields_from_json:
            if field in json_data:
                del json_data[field]

        return json.dumps(json_data, **self._json_dumps_args)


def init_flexible_logger(name: str) -> LoggerWithFlexibleArgsAdapter:
    result = logging.getLogger(name)
    # Using logging.LoggerAdapter instead of implementing own Logger subclass solve an issue with
    # multi-threads programs in case of temporary changing of logging.getLoggerClass() to hack
    # the logging.getLogger(name) call
    return LoggerWithFlexibleArgsAdapter(result, {})


def init_json_logger(
    name: str,
    drop_formatted_message: bool = True,
    drop_old_exception_text: bool = True,
    stream=sys.stdout,
    formatter: Optional[JsonFormatter] = None
) -> LoggerWithFlexibleArgsAdapter:
    if not formatter:
        skip_fields = set()
        if drop_formatted_message:
            skip_fields.add('messageFormatted')
        if drop_old_exception_text:
            skip_fields.add('exc_text')
        formatter = JsonFormatter(
            skip_fields_calculation=skip_fields,
            drop_fields_from_json=skip_fields
        )

    result = init_flexible_logger(name)
    handler = logging.StreamHandler(stream)
    handler.setFormatter(formatter)
    result.addHandler(handler)

    return result
