#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Send SMS via PanaceaMobile API"""
#
# @author: Jacek Smit<info@jaceksmit.nl>
#

from contextlib import suppress
import random
import string
import requests

from PanaceaMobile.const import VERSION, \
    CONFIG_FILE_CONTENT

_API_URL = "http://api.panaceamobile.com/json"

PANACEA_LOGIN = None  # normally your phone number
PANACEA_PASSWORD = None  # your password

# alternatively import passwd and number from external file
with suppress(ImportError):
    # pylint: disable-msg=E0611
    from .secrets import PANACEA_LOGIN, PANACEA_PASSWORD


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class PanaceaMobile:
    """PanaceaMobile class for sending SMS"""

    class NoRecipientError(ValueError):
        """empty recipient."""

        pass

    class EmptyMessageError(ValueError):
        """empty message."""

        pass

    class LoginError(ValueError):
        """login credentials not accepted."""

        pass

    class SMSSendingError(RuntimeError):
        """error during sending."""

        pass

    def __init__(self, panacea_login=PANACEA_LOGIN, panacea_password=PANACEA_PASSWORD):
        """Initialize PanaceaMobile member variables."""
        self._version = VERSION
        self._api_url = _API_URL
        self.panacea_login = panacea_login
        self.panacea_password = panacea_password
        self._suspended = False

    def send(self, recipient, message, sender=False):
        """Send an SMS."""
        if self.panacea_login is None or \
                self.panacea_password is None:
            err_mess = "Login data required"
            raise self.LoginError(err_mess)
        if not recipient:
            raise self.NoRecipientError("Recipient number missing")
        if not isinstance(recipient, str):
            raise ValueError("str expected as recipient number")
        if not message:
            raise self.EmptyMessageError("Message is empty")
        if not sender:
            sender = 'panacea-' + random_string(8)
        request_content = [
            ('action', 'message_send'),
            ('username', self.panacea_login),
            ('password', self.panacea_password),
            ('to', recipient),
            ('text', message),
            ('from', sender),
            ('report_mask', '19'),
            ('report_url', None),
            ('charset', None),
            ('data_coding', None),
            ('message_class', -1),
            ('auto_detect_encoding', None)
        ]

        result = requests.get(self._api_url, request_content)
        result_json = result.json()
        if result_json.get('status') == 1:
            return True
        else:
            raise self.SMSSendingError(result_json.get('message'), "Unknown error occured!")

    def version(self):
        """Get version of PanaceaMobile package."""
        return self._version


def version_info():
    """Display version information"""
    print("panaceamobile {}".format(PanaceaMobile().version()))


def print_config_file():
    """Print a sample config file, to pipe into a file"""
    print(CONFIG_FILE_CONTENT, end="")


if __name__ == "__main__":
    pm = PanaceaMobile(panacea_login='username', panacea_password='password-or-api-key')
    pm.send(recipient='', message='Example message from Python!')
