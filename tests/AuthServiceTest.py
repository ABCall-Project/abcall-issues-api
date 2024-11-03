import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.auth_service import AuthService
from flaskr.domain.models.auth_user_customer import AuthUserCustomer


class TestAuthService(unittest.TestCase):
    
    @patch('flaskr.application.auth_service.requests.get')
    def test_get_users_by_customer_list_success(self, mock_get):
        """
        Test the successful scenario when API returns a valid response with users.
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'auth_user_id': 10,
                'customer_id': 100
            },
            {
                'id': 2,
                'auth_user_id': 20,
                'customer_id': 100
            }
        ]
        mock_get.return_value = mock_response

        auth_service = AuthService()

        result = auth_service.get_users_by_customer_list(100)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], AuthUserCustomer)
        self.assertEqual(result[0].auth_user_id, 10)
        self.assertEqual(result[1].auth_user_id, 20)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_users_by_customer_list_no_users(self, mock_get):
        """
        Test the scenario when API returns no users (empty list).
        """

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

    
        auth_service = AuthService()

        result = auth_service.get_users_by_customer_list(100)

        self.assertIsNone(result)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_users_by_customer_list_api_error(self, mock_get):
        """
        Test the scenario when the API returns an error (status code 500).
        """

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response


        auth_service = AuthService()

   
        result = auth_service.get_users_by_customer_list(100)

        self.assertIsNone(result)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_users_by_customer_list_exception(self, mock_get):
        """
        Test the scenario when an exception is raised during the API call.
        """

        mock_get.side_effect = Exception('API is down')

        auth_service = AuthService()

        result = auth_service.get_users_by_customer_list(100)

        self.assertIsNone(result)

    
    @patch('flaskr.application.auth_service.requests.get')
    def test_get_customer_by_user_id_success(self, mock_get):
        """
        Test the successful scenario when API returns a valid response for a customer by user ID.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1, 'auth_user_id': 10, 'customer_id': 100
        }
        mock_get.return_value = mock_response

        auth_service = AuthService()
        result = auth_service.get_customer_by_user_id(10)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, AuthUserCustomer)
        self.assertEqual(result.auth_user_id, 10)
        self.assertEqual(result.customer_id, 100)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_customer_by_user_id_no_user(self, mock_get):
        """
        Test the scenario when the API returns no customer data.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        auth_service = AuthService()
        result = auth_service.get_customer_by_user_id(10)

        self.assertIsNone(result)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_customer_by_user_id_api_error(self, mock_get):
        """
        Test the scenario when the API returns an error (status code 500).
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        auth_service = AuthService()
        result = auth_service.get_customer_by_user_id(10)

        self.assertIsNone(result)

    @patch('flaskr.application.auth_service.requests.get')
    def test_get_customer_by_user_id_exception(self, mock_get):
        """
        Test the scenario when an exception is raised during the API call.
        """
        mock_get.side_effect = Exception('API is down')

        auth_service = AuthService()
        result = auth_service.get_customer_by_user_id(10)

        self.assertIsNone(result)
