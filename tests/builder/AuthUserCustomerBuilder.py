from uuid import UUID
from flaskr.domain.models import AuthUserCustomer

class AuthUserCustomerBuilder:
    def __init__(self):
        self.id = UUID("a257ee3b-c1c6-4139-84bc-f70595a1c773")
        self.auth_user_id = UUID("9ac7bcb5-4158-4e9d-aecf-833609f4e5f6")
        self.customer_id = UUID("22d8c4a0-3ed3-48ca-a9ba-bda265dd18bc")
    
    def with_id(self, id:UUID):
        self.id = id
        return self

    def with_auth_user_id(self, auth_user_id:UUID):
        self.auth_user_id = auth_user_id
        return self

    def with_customer_id(self, customer_id:UUID):
        self.customer_id = customer_id
        return self
    
    def build(self):
        return AuthUserCustomer(id=self.id, auth_user_id=self.auth_user_id, customer_id=self.customer_id)