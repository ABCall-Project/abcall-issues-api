from unittest.mock import patch
import unittest
from config import Config

class ConfigTestCase(unittest.TestCase):

    @patch('os.getenv', return_value='local')
    def test_config_environment_when_it_is_local(self, getenv_mocked):
        environmentExpected = 'local'
        envConfig = Config()

        environment = envConfig.ENVIRONMENT
        
        self.assertEqual(environment, environmentExpected)
    
    @patch('os.getenv', return_value='test')
    def test_config_environment_when_it_is_test(self, getenv_mocked):
        environmentExpected = 'test'
        envConfig = Config()

        environment = envConfig.ENVIRONMENT
        
        self.assertEqual(environment, environmentExpected)

    @patch('os.getenv', return_value='production')
    @patch('dotenv.load_dotenv', return_value="production")
    def test_config_environment_when_it_is_production(self, getenv_mocked, load_dotenv_mocked):
        envConfig = Config()
        environmentExpected = "production"

        environment = envConfig.ENVIRONMENT
        
        self.assertEqual(environment, environmentExpected)
