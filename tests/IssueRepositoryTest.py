import unittest
from flaskr.domain.interfaces.issue_repository import IssueRepository


class IssueRepositoryUseCase(unittest.TestCase):

    def setUp(self):
        self.repo = IssueRepository()

    def test_should_return_error_when_list_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.list()

    def test_should_return_error_when_list_issues_period_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.list_issues_period(user_id="", year="", month="")
    
    def test_should_return_error_when_list_issues_filtered_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.list_issues_filtered(user_id="", status="", channel_plan_id="", created_at="", closed_at="")

    def test_should_return_error_when_create_issue_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create_issue(issue_data=None,new_attachment=None)
        
    def test_should_return_error_when_create_issue_attachment_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.create_issue_attachment(issue_attachment=None)

    def test_should_return_error_when_find_method_is_not_implement(self):
        with self.assertRaises(NotImplementedError):
            self.repo.find()
