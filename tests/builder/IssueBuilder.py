from uuid import UUID
from datetime import datetime
from flaskr.domain.models import Issue

class IssueBuilder:
    def __init__(self):
        self.id=UUID('17be4b3e-3b6d-44e2-9721-229d6a746f15')
        self.auth_user_id=UUID('c91b20d5-a104-427e-af4f-5d32e3fa2182')
        self.auth_user_agent_id=UUID('d5f445e8-9151-42d9-8ddc-19f5fc343f66')
        self.status=UUID('f009ac23-104e-49ff-82ef-de25d3b15d15')
        self.subject='subject'
        self.description='Lorem ipsum'
        self.created_at=datetime.fromisoformat('2024-10-12T11:34:43')
        self.closed_at=datetime.fromisoformat('2024-10-25T18:56:34')
        self.channel_plan_id=UUID('c71ef779-cd17-4263-acc2-ecdb5d423793')
    
    def with_id(self, id: UUID):
        self.id = id
        return self
    
    def with_auth_user_id(self, auth_user_id: UUID):
        self.auth_user_id = auth_user_id
        return self
    
    def with_auth_user_agent_id(self, auth_user_agent_id: UUID):
        self.auth_user_agent_id = auth_user_agent_id
        return self
    
    def with_status(self, status: UUID):
        self.status = status
        return self
    
    def with_subject(self, subject: str):
        self.subject = subject
        return self
    
    def with_description(self, description: str):
        self.description = description
        return self
    
    def with_created_at(self, created_at: datetime):
        self.created_at = created_at
        return self
    
    def with_closed_at(self, closed_at: datetime):
        self.closed_at = closed_at
        return self
    
    def with_channel_plan_id(self, channel_plan_id: UUID):
        self.channel_plan_id = channel_plan_id
        return self
    
    def build(self):
        return Issue(
            id = self.id,
            auth_user_id =self.auth_user_id,
            auth_user_agent_id =self.auth_user_agent_id,
            status = self.status,
            subject = self.subject,
            description = self.description,
            created_at = self.created_at,
            closed_at = self.closed_at,
            channel_plan_id = self.channel_plan_id
        )