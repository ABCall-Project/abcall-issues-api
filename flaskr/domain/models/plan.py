class Plan:
    """
    This class represent a plan of abcall service
    Attributes:
        id (UUID): plan id
        name (str): plan name
        basic_monthly_rate (UUID): plan rate
        issue_fee (Timestamp): fee by issue
    """
    def __init__(self, id, name,basic_monthly_rate,issue_fee):
        self.id=id
        self.name=name
        self.basic_monthly_rate=basic_monthly_rate
        self.issue_fee=issue_fee


    def to_dict(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            'basic_monthly_rate': str(self.basic_monthly_rate),
            'issue_fee': str(self.issue_fee)
        }




