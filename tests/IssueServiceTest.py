import unittest
from unittest.mock import patch
from builder import AuthUserCustomerBuilder, IssueBuilder, IssueAttachmentBuilder
from flaskr.application.issue_service import IssueService
from flaskr.domain.models import Issue, AuthUserCustomer
from mocks.repositories import IssueMockRepository
from utils.testHelper import dict_to_obj


class TestIssueService(unittest.TestCase):

    @patch('flaskr.application.openAiService.OpenAIService.ask_chatgpt')
    def test_ask_generative_ai(self, mock_ask_chatgpt):
        """
        Test ask_generative_ai method which uses OpenAIService.
        """

        mock_ask_chatgpt.return_value = "This is an AI response"


        issue_service = IssueService()


        result = issue_service.ask_generative_ai("What is AI?")


        self.assertEqual(result, "This is an AI response")
  
    @patch('flaskr.application.issue_service.AuthService')
    def test_return_list_issues_period(self, AuthServiceMock):
        customers_mocked: list[AuthUserCustomer] = []
        issues_mocked: list[Issue] = []
        customers_mocked.append(AuthUserCustomerBuilder().build())
        issues_mocked.append(IssueBuilder()
                             .with_auth_user_id(customers_mocked[0].auth_user_id)
                             .build()
                            )
        auth_instance = AuthServiceMock.return_value
        auth_instance.get_users_by_customer_list.return_value = customers_mocked

        issue_service = IssueService(issue_repository=IssueMockRepository(issues_mocked))
        issues = issue_service.list_issues_period(customer_id="fake_id", year="fake_year", month="fake_month")

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].auth_user_id, customers_mocked[0].auth_user_id)
    
    @patch('flaskr.application.issue_service.AuthService')
    def test_return_none_if_there_are_not_customers(self, AuthServiceMock):
        customers_mocked = []
        instance = AuthServiceMock.return_value
        instance.get_users_by_customer_list.return_value = customers_mocked

        issue_service = IssueService()
        issues = issue_service.list_issues_period(customer_id="fake_id", year="fake_year", month="fake_month")

        self.assertIsNone(issues)

    @patch('flaskr.application.issue_service.AuthService')
    def test_return_in_filtered_none_if_there_are_not_customers(self, AuthServiceMock):
        customers_mocked = []
        instance = AuthServiceMock.return_value
        instance.get_users_by_customer_list.return_value = customers_mocked

        issue_service = IssueService()
        issues = issue_service.list_issues_filtered(customer_id="fake_id", status="fake_status", channel_plan_id="fake_channel", created_at="fake_created_at", closed_at="fake_closed_at")

        self.assertIsNone(issues)

    @patch('flaskr.application.issue_service.AuthService')
    def test_return_in_issues_with_filters(self, AuthServiceMock):
        customers_mocked:list[AuthUserCustomer] = []
        issues_mocked: list[Issue] = []
        customers_mocked.append(AuthUserCustomerBuilder().build())
        issues_mocked.append(IssueBuilder()
                             .with_auth_user_id(customers_mocked[0].auth_user_id)
                             .build()
                            )
        instance = AuthServiceMock.return_value
        instance.get_users_by_customer_list.return_value = customers_mocked

        issue_service = IssueService(issue_repository=IssueMockRepository(issues_mocked))
        issues = issue_service.list_issues_filtered(customer_id="fake_id", status="fake_status", channel_plan_id="fake_channel", created_at="fake_created_at", closed_at="fake_closed_at")

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].auth_user_id, customers_mocked[0].auth_user_id)

    
    def test_error_create_issue_with_missed_params(self):
        with self.assertRaises(ValueError) as context:
            issue_service = IssueService()
            self.assertRaises(issue_service.create_issue(auth_user_id=None,auth_user_agent_id=None,subject=None,description=None,file_path=None))
        error_expected = "All fields are required to create an issue."

        self.assertEqual(str(context.exception), error_expected)

    @patch('flaskr.application.issue_service.IssueStatus')
    @patch('uuid.uuid4', return_value="e3a54f43-3e8d-4c16-b340-9aba07dfb1ec")
    def test_should_create_an_issue(self, uuid4Mock, IssueStatusMock):
        issue_mock = IssueBuilder() \
                    .with_id('e3a54f43-3e8d-4c16-b340-9aba07dfb1ec') \
                    .build()
        instance = IssueStatusMock.return_value
        instance.NEW.return_value = {"id": issue_mock.status, "name": "New"}

        issue_service = IssueService(issue_repository=IssueMockRepository([]))
        issue = issue_service.create_issue(
            auth_user_id=issue_mock.auth_user_id,
            auth_user_agent_id=issue_mock.auth_user_agent_id,
            subject=issue_mock.subject,
            description=issue_mock.description
        )


        self.assertEqual(issue.id, issue_mock.id)

    @patch('flaskr.application.issue_service.IssueStatus')
    @patch('uuid.uuid4', return_value="e3a54f43-3e8d-4c16-b340-9aba07dfb1ec")
    def test_should_create_an_issue_with_attachment(self, uuid4Mock, IssueStatusMock):
        uuid_mock = "e3a54f43-3e8d-4c16-b340-9aba07dfb1ec"
        issue_mock = IssueBuilder() \
                    .with_id(uuid_mock) \
                    .build()
        attachment_mock = IssueAttachmentBuilder() \
                          .with_id(uuid_mock) \
                          .with_issue_id(uuid_mock) \
                          .build()
        instance = IssueStatusMock.return_value
        instance.NEW.return_value = {"id": issue_mock.status, "name": "New"}

        issue_service = IssueService(issue_repository=IssueMockRepository([]))
        issue = issue_service.create_issue(
            auth_user_id=issue_mock.auth_user_id,
            auth_user_agent_id=issue_mock.auth_user_agent_id,
            subject=issue_mock.subject,
            description=issue_mock.description,
            file_path=attachment_mock.file_path
        )


        self.assertEqual(issue.id, issue_mock.id)

    def test_error_in_issue_finder_without_a_user(self):
        with self.assertRaises(ValueError) as context:
            issue_service = IssueService()
            self.assertRaises(issue_service.find_issues(user_id=None, page=1, limit=10))
        error_expected = "All fields are required to create an issue."

        self.assertEqual(str(context.exception), error_expected)

    def test_should_get_issues_by_user(self):
        issues_mocked: list[Issue] = []
        issues_mocked.append(IssueBuilder().build())

        issue_service = IssueService(issue_repository=IssueMockRepository(issues_mocked))
        issues = issue_service.find_issues(issue_service,1,10)
        issue_obj = dict_to_obj(issues)


        self.assertEqual(len(issue_obj.data), 1)
        self.assertEqual(issue_obj.page, 1)
        self.assertEqual(issue_obj.limit, 10)
        self.assertEqual(issue_obj.total_pages, 1)
        self.assertFalse(issue_obj.has_next)

        





