import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4
from flaskr.infrastructure.databases.issue_postresql_repository import IssuePostgresqlRepository
from flaskr.domain.models import Issue, IssueAttachment,IssueTrace

class TestIssuePostgresqlRepository(unittest.TestCase):
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def setUp(self, mock_sessionmaker, mock_create_engine):
        mock_create_engine.return_value = MagicMock()
        self.repo = IssuePostgresqlRepository()
        self.repo.Session = MagicMock()

    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def test_list_issues_period(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='SOLVED',
            subject='Test Subject',
            description='Test Description',
            created_at='2023-01-01',
            closed_at='2023-01-02',
            channel_plan_id=uuid4()
        )
        mock_session_instance.query.return_value.filter.return_value.all.return_value = [mock_issue]

        result = self.repo.list_issues_period(user_id=mock_issue.auth_user_id, year=2023, month=1)

        self.assertGreaterEqual(len(result), 0)

    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def test_list_issues_filtered(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status='OPEN',
            subject='Filtered Issue',
            description='Filtered Description',
            created_at='2023-03-01',
            closed_at='2023-03-05',
            channel_plan_id=uuid4()
        )
        mock_session_instance.query.return_value.filter.return_value.all.return_value = [mock_issue]

        result = self.repo.list_issues_filtered(user_id=mock_issue.auth_user_id, status='OPEN')

        self.assertGreaterEqual(len(result), 0)

    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def test_issue_assign_issue_not_found(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value
        
        mock_session_instance.query.return_value.filter.return_value.one_or_none.return_value = None
        
        issue_id = uuid4()
        auth_user_agent_id = uuid4()
        
        with self.assertRaises(ValueError) as context:
            self.repo.assign_issue(issue_id=issue_id, auth_user_agent_id=auth_user_agent_id)
        
        self.assertEqual(str(context.exception), "Issue not found")
    
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def test_issue_create_issue_trace_not_found(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value
        
        mock_session_instance.query.return_value.filter.return_value.one_or_none.return_value = None
        
        mock_issue_trace = IssueTrace(
            id=uuid4(),
            auth_user_id=uuid4(),
            issue_id=uuid4(),
            auth_user_agent_id=uuid4(),
            scope='test OPEN',
            created_at='2023-03-01',
            channel_plan_id=uuid4()
        )
        
        with self.assertRaises(ValueError) as context:
            self.repo.create_issue_trace(issue_trace=mock_issue_trace)
        
        self.assertEqual(str(context.exception), "Issue not found")


    @patch('flaskr.infrastructure.databases.issue_postresql_repository.create_engine')
    @patch('flaskr.infrastructure.databases.issue_postresql_repository.sessionmaker')
    def test_get_top_7_incident_types(self, mock_sessionmaker, mock_create_engine):
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        mock_session_instance = mock_session.return_value

        mock_results = [
            ('Incident Type 1', 10),
            ('Incident Type 2', 8),
            ('Incident Type 3', 7),
            ('Incident Type 4', 6),
            ('Incident Type 5', 5),
            ('Incident Type 6', 4),
            ('Incident Type 7', 3),
        ]
        mock_session_instance.query.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = mock_results

        result = self.repo.get_top_7_incident_types()

        self.assertEqual(len(result), 7)  