from uuid import UUID
from flaskr.domain.models import IssueAttachment

class IssueAttachmentBuilder:
    def __init__(self):
        self.id = UUID('f5141ed4-414e-4da4-b0cb-2db76054367c')
        self.issue_id = UUID('65663352-7501-4bcc-b47a-1193eca352a1')
        self.file_path='my_fake_file'
    
    def with_id(self, id:UUID):
        self.id = id
        return self

    def with_issue_id(self, issue_id:UUID):
        self.issue_id = issue_id
        return self

    def with_file_path(self,file_path:str):
        self.file_path = file_path
        return self
    
    def build(self):
        return IssueAttachment(self.id, self.issue_id, self.file_path)