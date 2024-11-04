import unittest
from uuid import uuid4
from datetime import datetime
from flaskr.domain.models import Issue
from datetime import datetime, timezone


class TestIssueModel(unittest.TestCase):

    def setUp(self):
        
        self.issue = Issue(
            id=uuid4(),
            auth_user_id=uuid4(),
            auth_user_agent_id=uuid4(),
            status=uuid4(),
            subject="Test Issue",
            description="This is a test issue description",
            created_at=datetime.now(timezone.utc),
            closed_at=None,
            channel_plan_id=uuid4()
        )

    def test_issue_instance(self):
        
        self.assertIsInstance(self.issue, Issue)
        self.assertEqual(self.issue.subject, "Test Issue")
        self.assertEqual(self.issue.description, "This is a test issue description")
        self.assertIsNotNone(self.issue.created_at)
        self.assertIsNone(self.issue.closed_at)

    def test_issue_to_dict(self):
        
        issue_dict = self.issue.to_dict()
        
        self.assertEqual(issue_dict['subject'], "Test Issue")
        self.assertEqual(issue_dict['description'], "This is a test issue description")
        self.assertIsNotNone(issue_dict['created_at'])
        self.assertIsNone(issue_dict['closed_at'])

        
        self.assertIn('id', issue_dict)
        self.assertIn('auth_user_id', issue_dict)
        self.assertIn('auth_user_agent_id', issue_dict)
        self.assertIn('status', issue_dict)
        self.assertIn('subject', issue_dict)
        self.assertIn('description', issue_dict)
        self.assertIn('created_at', issue_dict)
        self.assertIn('closed_at', issue_dict)
        self.assertIn('channel_plan_id', issue_dict)

if __name__ == '__main__':
    unittest.main()
