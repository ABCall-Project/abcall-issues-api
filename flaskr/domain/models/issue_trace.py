from uuid import UUID
from datetime import datetime

class IssueTrace:
    def __init__(self, id:UUID,issue_id:UUID,auth_user_id:UUID,auth_user_agent_id:UUID,scope:str,created_at:datetime,channel_plan_id:UUID):
        self.id=id
        self.issue_id=issue_id,
        self.auth_user_id=auth_user_id
        self.auth_user_agent_id=auth_user_agent_id
        self.scope=scope
        self.created_at=created_at
        self.channel_plan_id=channel_plan_id


    def to_dict(self):
        return {
            'id': str(self.id),
            'issue_id': str(self.issue_id),
            'auth_user_id': str(self.auth_user_id),
            'auth_user_agent_id': str(self.auth_user_agent_id),
            'scope': str(self.scope),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'channel_plan_id': str(self.channel_plan_id)
        }