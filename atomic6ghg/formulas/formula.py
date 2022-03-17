""" Base class for all formula classes """
import json
import logging
from io import StringIO

logger = logging.getLogger(__name__)


class Formula:
    """ Base class for all formula classes """
    def __init__(self, wks_data=None):
        self.wks_data = wks_data or {}

        # This variable exists for convenience of calculating totals in child classes
        self._total_emissions = {}

        self._output = {}

    def recalc(self, wks_data):
        """ All child classes must implement this method """
        raise NotImplementedError

    def to_dict(self):
        """ API to expose _output """
        try:
            # Check to ensure that _output is JSON serializable, otherwise TypeError is thrown
            io = StringIO()
            json.dump(self._output, io)
            ret = self._output
        except TypeError as e:
            err_msg = f'{self.__class__.__name__}._output is not a dict. Error message: {e}'
            logger.error(err_msg)
            ret = None
        return ret

    def to_json(self):
        """ API to expose _output as JSON """
        try:
            ret = json.dumps(self._output, indent=2)
        except TypeError as e:
            err_msg = f'{self.__class__.__name__}._output is not a dict. Error message: {e}'
            logger.error(err_msg)
            ret = None
        return ret


def null_replacer(value):
    """ Replaces None with 0. for user input float values to be used in equations """
    if not value:
        value = 0.
    return value
