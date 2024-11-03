from flask_restful import Resource
from flask import jsonify, request
import os
from config import Config
from http import HTTPStatus
from flaskr.application.issue_service import IssueService
from flaskr.infrastructure.databases.issue_postresql_repository import IssuePostgresqlRepository
from ...utils import Logger


log = Logger()

class Issue(Resource):

    def __init__(self):
        config = Config()
        self.issue_repository = IssuePostgresqlRepository(config.DATABASE_URI)
        self.service = IssueService(self.issue_repository)

    def post(self,action=None):
        try:
            file_path = None
            file = request.files.get('file')

            if request.is_json:  
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            auth_user_id = data.get("auth_user_id") 
            auth_user_agent_id = data.get('auth_user_agent_id')  
            subject = data.get("subject")  
            description = data.get("description")  
            log.info(f"auth_user_id at {auth_user_id}")
           
            if file:
                upload_directory = os.path.join(os.getcwd(), 'uploads')
                os.makedirs(upload_directory, exist_ok=True)
                file_path = os.path.join(upload_directory, file.filename)
                file.save(file_path)
                log.info(f"File uploaded successfully at {file_path}")

            self.service.create_issue(
                auth_user_id=auth_user_id,
                auth_user_agent_id=auth_user_agent_id,
                subject=subject,
                description=description,
                file_path=file_path
            )

            return {"message": f"Issue created successfully with ID"}, HTTPStatus.CREATED

        except Exception as ex:
            log.error(f"Error while creating issue: {ex}")
            return {"message": "Error creating issue"}, HTTPStatus.INTERNAL_SERVER_ERROR

    def get(self, action=None):
        if action == 'getIssuesByCustomer':
            return self.getIssuesByCustomer()
        elif action == 'getIssuesDasboard':
            return self.getIssuesDasboard()
        elif action == 'getIAResponse':
            return self.getIAResponse()
        elif action== 'find':
            return self.get_issues_by_user()
        elif action=='getIAPredictiveAnswer':
            return self.get_ia_predictive_answer()
        if action == 'get_issue_by_id':
            return self.getIssueDetail()
        else:
            return {"message": "Action not found"}, HTTPStatus.NOT_FOUND
        
    def getIssuesByCustomer(self):
        try:

            log.info(f'Receive request to get issues by customer')
            customer_id = request.args.get('customer_id')
            year = request.args.get('year')
            month = request.args.get('month')
            issue_list = self.service.list_issues_period(customer_id=customer_id,year=year,month=month)
            list_issues=[]
            if issue_list:
                list_issues = [issue.to_dict() for issue in issue_list]

            
            return list_issues, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue list: {ex}')
            return {'message': 'Something was wrong trying to get issue list'}, HTTPStatus.INTERNAL_SERVER_ERROR    
    
    def listIssuesFiltered(self, user_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        query = self.session.query(Issue).filter(Issue.user_id == user_id)

        if status:
            query = query.filter(Issue.status == status)
        if channel_plan_id:
            query = query.filter(Issue.channel_plan_id == channel_plan_id)
        if created_at and closed_at:
            query = query.filter(Issue.created_at.between(created_at, closed_at))
        elif created_at:
            query = query.filter(Issue.created_at >= created_at)

        return query.all()

    def getIssuesDasboard(self):
        try:
            customer_id = request.args.get('customer_id')
            status = request.args.get('status')
            channel_plan_id = request.args.get('channel_plan_id')
            created_at = request.args.get('created_at')
            closed_at = request.args.get('closed_at')

            log.info(f'Receive request to getIssuesDashboard {customer_id}  {status} {channel_plan_id} {created_at} {closed_at}')

            issue_list = self.service.list_issues_filtered(
                customer_id=customer_id,
                status=status,
                channel_plan_id=channel_plan_id,
                created_at=created_at,
                closed_at=closed_at
            )
            log.info(f'issue list {issue_list}')

            list_issues = []
            if issue_list:
                list_issues = [
                    {
                        "status": issue.get("status"),
                        "channel_plan_id": issue.get("channel_plan_id"),
                        "created_at": issue.get("created_at")
                    } for issue in issue_list
                ]

            log.info(f'list issue {list_issues}')

            return list_issues, HTTPStatus.OK

        except Exception as ex:
            log.error(f'Error trying to get issue list: {ex}')
            return {'message': 'Something went wrong trying to get the issue dashboard'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    def getIssueDetail(self):
        try:
            customer_id = request.args.get('customer_id')
            issue_id = request.args.get('issue_id')

            issue = self.service.get_issue_by_id(customer_id=customer_id, issue_id=issue_id)
            log.info(f'Issue retrieved: {issue}')
            
            if issue:
                issue_detail = {
                    "created_at": issue.get("created_at"),
                    "id": issue.get("id"),
                    "subject": issue.get("subject"),
                    "description": issue.get("description"),
                    "status": issue.get("status")                  
                }
                return issue_detail, HTTPStatus.OK
            else:
                return {'message': 'Issue not found'}, HTTPStatus.NOT_FOUND

        except Exception as ex:
            log.error(f'Error trying to get issue detail: {ex}')
            return {'message': 'Something went wrong trying to get the issue detail'}, HTTPStatus.INTERNAL_SERVER_ERROR


    def getIAResponse(self):
        try:
            log.info(f'Receive request to ask to open ai')
            question = request.args.get('question')
            answer=self.service.ask_generative_ai(question)
            return {
                'answer': answer
            }, HTTPStatus.OK
            
        except Exception as ex:
            log.error(f'Some error occurred trying ask open ai: {ex}')
            return {'message': 'Something was wrong trying ask open ai'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
    def get_ia_predictive_answer(self):
        try:

            log.info(f'Receive request ai predictive')
            user_id = request.args.get('user_id')
            answer=self.service.ask_predictive_analitic(user_id)
            return {
                'answer': answer
            }, HTTPStatus.OK
            
        except Exception as ex:
            log.error(f'Some error occurred trying query ai predictive: {ex}')
            return {'message': 'Something was wrong trying query ai predictive'}, HTTPStatus.INTERNAL_SERVER_ERROR

class Issues(Resource):
    def __init__(self):
        config = Config()
        self.issue_repository = IssuePostgresqlRepository(config.DATABASE_URI)
        self.service = IssueService(self.issue_repository)

    def get(self, action=None, user_id=None):
        if action== 'find':
            return self.find(user_id)
        else:
            return {"message": "Action not found"}, HTTPStatus.NOT_FOUND
        

    def find(self, user_id:str):
        try:
            log.info(f'Receive request to get issues by user')
            page = int(request.args.get('page'))
            limit = int(request.args.get('limit'))
            issue_list = self.service.find_issues(user_id=user_id,page=page,limit=limit)

            return issue_list, HTTPStatus.OK
        except ValueError as ex:
            log.error(f'There was an error validate the values {ex}')
            return {'message': 'There was an error validate the values'}, HTTPStatus.BAD_REQUEST
        except Exception as ex:
            log.error(f'Some error occurred trying to get issue list: {ex}')
            return {'message': 'Something was wrong trying to get issue list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
