from typing import List, Optional
from uuid import UUID
from ..models.issue import Issue
from ..models.issue_attachment import IssueAttachment

class IssueRepository:
    def list(self) -> List[Issue]:
        raise NotImplementedError
    
    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        raise NotImplementedError
    
    def list_issues_filtered (self, user_id, status, channel_plan_id, created_at, closed_at) -> List[Issue]:
        raise NotImplementedError
    
    def get_users_by_customer_list (self, user_id, status, channel_plan_id, created_at, closed_at) -> List[Issue]:
        raise NotImplementedError
    
    def create_issue(self, issue_data: dict, new_attachment:dict) -> Issue:
        raise NotImplementedError
    
    def create_issue_attachment(self, issue_attachment: dict)-> IssueAttachment:
        raise NotImplementedError
    
    def find(self, user_id = None,page=None,limit=None):
        raise NotImplementedError
    
    def get_issue_by_id(self, issue_id) -> Optional[Issue]:
        raise NotImplementedError    