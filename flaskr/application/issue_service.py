from typing import List
from ..domain.models import Issue
import requests
from ..domain.interfaces.issue_repository import IssueRepository
from ..infrastructure.mappers import IssueMapper
import uuid
from datetime import datetime
from ..utils import Logger
from  config import Config

class IssueService:
    def __init__(self, issue_repository: IssueRepository=None):
        self.log = Logger()
        self.issue_repository=issue_repository

    