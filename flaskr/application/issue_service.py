from typing import List, Optional
import requests
from uuid import UUID
import uuid
from datetime import datetime
from typing import TypedDict
from ..domain.interfaces.issue_repository import IssueRepository
from ..domain.models import Issue, IssueAttachment
from ..utils import Logger
from  config import Config
from .auth_service import AuthService
from .openAiService import OpenAIService
from .customer_service import CustomerService
from ..utils import Logger
log = Logger()
class Status(TypedDict):
    id: UUID
    name: str
   
class IssueStatus:
    NEW = {"id": UUID("574408a7-3aa0-4eab-b279-62ed10e6107e"), "name": "New"}
    IN_PROGRESS = {"id": UUID("18e7d7dd-247b-4e27-aa0e-4f15e8ba5930"), "name": "In Progress"}
    RESOLVED = {"id": UUID("791353c6-3899-4d35-bcd9-af8775e240bf"), "name": "Resolved"}
    CLOSED = {"id": UUID("00000000-0000-0000-0000-000000000004"), "name": "Closed"}

    ALL_STATUSES = [NEW, IN_PROGRESS, RESOLVED, CLOSED]
class IssueService:
    def __init__(self, issue_repository: IssueRepository=None):
        self.log = Logger()
        self.issue_repository=issue_repository
        self.config=Config()

    def list_issues_period(self, customer_id, year, month):
        auth_service=AuthService()
        list_user_customer=auth_service.get_users_by_customer_list(customer_id)
        self.log.info(f'list user customer {list_user_customer}')
        issues=[]
        if list_user_customer:
            for item in list_user_customer:
                issues.extend(self.issue_repository.list_issues_period(item.auth_user_id,year,month))
            return issues
        else:
            return None
        
    def list_issues_filtered(self, customer_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        auth_service = AuthService()
        list_user_customer = auth_service.get_users_by_customer_list(customer_id)
        self.log.info(f'list user customer {list_user_customer}')
        issues = []
        
        if list_user_customer:
            for item in list_user_customer:
                self.log.info(f'for each user {item}')
                user_issues = self.issue_repository.list_issues_filtered(
                    user_id=item.auth_user_id, 
                    status=status, 
                    channel_plan_id=channel_plan_id, 
                    created_at=created_at, 
                    closed_at=closed_at
                )
                issues.extend(user_issues)
                
            return issues
        else:
            return None
        
    def get_issue_by_id(self, issue_id: str) -> Optional[dict]:
        auth_service = AuthService()

        try:
            issue = self.issue_repository.get_issue_by_id(issue_id=issue_id)
            if issue:
                return issue
            else:
                return None

        except Exception as ex:
            self.log.error(f"Error retrieving issue by issue_id {issue_id}: {ex}")
            return None

    def create_issue(self, auth_user_id: uuid, auth_user_agent_id: uuid, subject: str, description: str, file_path: str = None) -> uuid:
        if not auth_user_id or not subject or not description or not auth_user_agent_id:
            raise ValueError("All fields are required to create an issue.")
        new_issue = Issue(
            id=uuid.uuid4(),
            auth_user_id=auth_user_id,
            auth_user_agent_id=auth_user_agent_id,
            status=IssueStatus.NEW["id"],
            subject=subject,
            description=description,
            created_at=datetime.utcnow(),
            closed_at=None,
            channel_plan_id=None
        )

        new_attachment = None
        if file_path:
            new_attachment = IssueAttachment(
                id=uuid.uuid4(),
                issue_id=new_issue.id,
                file_path=file_path,
            )
        self.issue_repository.create_issue(new_issue, new_attachment)
        return new_issue
    
    def find_issues(self, user_id: UUID, page: int, limit: int):
        if not user_id:
            raise ValueError("All fields are required to create an issue.")

        issue_response = self.issue_repository.find(
                    user_id=user_id,
                    page=page,
                    limit=limit
                )
        
        return issue_response

    def ask_generative_ai(self,question):
        """
        method to ask question to chat gpt
        Args:
            question (str): question to ask
        Return:
            answer (str): answer about ask
        """
        ia_service=OpenAIService()
        return ia_service.ask_chatgpt(question)
    

    def ask_predictive_analitic(self,user_id:UUID) -> str :
        """
        method to ask predictive analitic
        Args:
            user_id (str): id user to build de context
        Return:
            answer (str): answer about ask
        """
        self.log.info('entró en el predictive analitic')
        self.log.info('leyendo el promp')
        promp_to_ask=''
        with open('openaipromp.txt', 'r', encoding='utf-8') as promp_file:
            promp_to_ask = promp_file.read()


        auth_service=AuthService()

        #1. obtener compañia del usuario
        customer_user=auth_service.get_customer_by_user_id(user_id)
        self.log.info(f'obteniendo el customer_user {customer_user}')
        if customer_user:

            #1. obtener el nombre compañia
            customer_service=CustomerService()
            customer=customer_service.get_customer_by_id(customer_user.customer_id)
            company_name=customer.name
            promp_to_ask=promp_to_ask.replace('{NOMBRECLIENTE}', customer.name)
            self.log.info(f'obteniendo el nombre del cliente {customer} {company_name}')
            #2. obtener el nombre del plan
            plan=customer_service.get_plan_by_id(customer.plan_id)
            plan_name=plan.name
            promp_to_ask=promp_to_ask.replace('{PLAN}', plan_name)
            self.log.info(f'obteniendo el nombre del plan {plan} {plan_name}')
            #3. obtener un distinct de los ultimos incidentes reportados por el cliente distintos
            list_top_issues=self.issue_repository.list_top_issues_by_user(user_id)
            if list_top_issues:
                top_issues_descriptions =' - '.join(row[0] for row in list_top_issues)
                self.log.info(f'top de issues {top_issues_descriptions}')
                promp_to_ask=promp_to_ask.replace('{INCIDENTES}', top_issues_descriptions)


            self.log.info(f'el promp {promp_to_ask}')


            if promp_to_ask:
                ia_service=OpenAIService()
                return ia_service.ask_predictive_ai_chatgpt(promp_to_ask)
            else:
                return 'No se puede dar sugerencias en este momento'
        else:
            return 'No se pudo identificar al cliente para dar sugerencias'
