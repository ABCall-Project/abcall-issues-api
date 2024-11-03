from typing import List
from flaskr.domain.interfaces import IssueRepository
from flaskr.domain.models import Issue
from math import ceil


class IssueMockRepository(IssueRepository):
    def __init__(self, issuesMock: list[Issue] = []):
        super().__init__()
        self.issues = issuesMock
        self.issues_attachment = []

    def list_issues_period(self, user_id, year, month) -> List[Issue]:
        return self.issues

    def list_issues_filtered(self, user_id, status, channel_plan_id, created_at, closed_at) -> List[Issue]:
        return self.issues

    def create_issue(self, issue_data, new_attachment):
        self.issues.append(issue_data)
        if new_attachment:
            self.issues_attachment.append(new_attachment)

        return issue_data

    def find(self, user_id=None, page=1, limit=10):
        total_pages = ceil(len(self.issues)/limit)
        has_next = page < total_pages

        data = [{
            "id": str(issue.id),
            "auth_user_id": str(issue.auth_user_id),
            "status": "CREATED",
            "subject": issue.subject,
            "description": issue.description,
            "created_at": str(issue.created_at),
            "closed_at": str(issue.closed_at),
            "cnnel_plan_id": str(issue.channel_plan_id)
        } for issue in self.issues]

        return {
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "has_next": has_next,
            "data": data
        }
