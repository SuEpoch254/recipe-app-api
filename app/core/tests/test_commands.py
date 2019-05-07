from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Note: Use path to mock the connection handler to just return True
            # every time it's called.
            gi.return_value = True
            # Note: So during test, we're rewriting connection handler
            # Now we can test our call command.
            call_command('wait_for_db')
            # Check the mock object gi (the connection handler) was called once
            self.assertEqual(gi.call_count, 1)

    # Now we want to check that wait_of_db command will check for connection
    # five times. On the sixth time it will be successful and continue.

    # We use patch as a decorator to mock the time.sleep, which would make it
    # wait a second before testing again the connection. We want to patch that
    # to speed up the test.

    # Even though we don't use ts we need to add it as an argument othetwise it
    # will show an error.

    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # We use again the contect manager patch to pass the handler as gi
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Instead of changing the value we change the side_effect
            # We want to make it raise the operational error 5 times. On the
            # 6th it will proceed. This is what the construction below means.
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)