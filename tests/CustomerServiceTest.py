import unittest
from unittest.mock import patch, MagicMock
from flaskr.application.customer_service import CustomerService
from flaskr.domain.models.customer import Customer
from flaskr.domain.models.plan import Plan

class TestCustomerService(unittest.TestCase):

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_by_id_success(self, mock_get):
        """
        Test successful scenario for get_customer_by_id when API returns valid response.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': '1234',
            'name': 'John Doe',
            'plan_id': '5678',
            'date_suscription': '2023-01-01'
        }
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_customer_by_id('1234')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Customer)
        self.assertEqual(result.id, '1234')
        self.assertEqual(result.name, 'John Doe')
        self.assertEqual(result.plan_id, '5678')
        self.assertEqual(result.date_suscription, '2023-01-01')

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_by_id_no_customer(self, mock_get):
        """
        Test scenario when get_customer_by_id returns no customer.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_customer_by_id('1234')

        self.assertIsNone(result)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_by_id_api_error(self, mock_get):
        """
        Test scenario when get_customer_by_id API returns an error.
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_customer_by_id('1234')

        self.assertIsNone(result)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_customer_by_id_exception(self, mock_get):
        """
        Test scenario when an exception is raised in get_customer_by_id.
        """
        mock_get.side_effect = Exception('API is down')

        customer_service = CustomerService()
        result = customer_service.get_customer_by_id('1234')

        self.assertIsNone(result)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_plan_by_id_success(self, mock_get):
        """
        Test successful scenario for get_plan_by_id when API returns valid response.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': '5678',
            'name': 'Basic Plan',
            'basic_monthly_rate': '100.00',
            'issue_fee': '10.00'
        }
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_plan_by_id('5678')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, Plan)
        self.assertEqual(result.id, '5678')
        self.assertEqual(result.name, 'Basic Plan')
        self.assertEqual(result.basic_monthly_rate, '100.00')
        self.assertEqual(result.issue_fee, '10.00')

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_plan_by_id_no_plan(self, mock_get):
        """
        Test scenario when get_plan_by_id returns no plan.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_plan_by_id('5678')

        self.assertIsNone(result)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_plan_by_id_api_error(self, mock_get):
        """
        Test scenario when get_plan_by_id API returns an error.
        """
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        customer_service = CustomerService()
        result = customer_service.get_plan_by_id('5678')

        self.assertIsNone(result)

    @patch('flaskr.application.customer_service.requests.get')
    def test_get_plan_by_id_exception(self, mock_get):
        """
        Test scenario when an exception is raised in get_plan_by_id.
        """
        mock_get.side_effect = Exception('API is down')

        customer_service = CustomerService()
        result = customer_service.get_plan_by_id('5678')

        self.assertIsNone(result)

