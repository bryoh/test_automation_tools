"""
webdriver_factory.py

Factory for supplying webdriver instances configured
from the environment (.env)
"""

import os
from datetime import datetime

from dotenv import find_dotenv, load_dotenv
from seleniumbase import BaseCase


load_dotenv(find_dotenv())


class MyBaseCase(BaseCase):
    """set common values which will be needed to run test cases
        eg the site url is something common across all test cases therefore its
        better to define it here
        Specify new testcases using the following method from the command line

        pytest my_test_suite.py --browser=chrome
    """
    url = os.environ.get('HOST')
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')

    def waitFor(self, condition, timeout=10):
        ''' A quick wait for function.
        Condition needs to be a callable object that return True, otherwise the
        function will act like a snooze until
        the
        '''
        now = datetime.now()
        statement = True if condition() else False
        while (not statement) and (datetime.now() - now).total_seconds() < timeout:
            statement = True if condition() else False

        return statement
