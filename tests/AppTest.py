from unittest.mock import patch
import unittest
import logging
from flaskr.app import before_server_stop

class AppTestCase(unittest.TestCase):
        
    
    @patch('logging.Logger.info', wraps=logging.getLogger('default').info)
    def test_should_calling_log_info_before_server_stop(self, info_mock):
        expectedInfo = 'Closing application ...'
        
        before_server_stop()

        info_mock.assert_called_once_with(expectedInfo)
