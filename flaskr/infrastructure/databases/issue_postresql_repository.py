from math import ceil
from flask import jsonify
import json
from sqlalchemy import create_engine,extract, func
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ...utils import Logger
from ...domain.models import Issue, IssueAttachment
from ...domain.interfaces import IssueRepository
from ...infrastructure.databases.model_sqlalchemy import Base, IssueModelSqlAlchemy, IssueAttachmentSqlAlchemy, IssueStateSqlAlchemy
log = Logger()
from ...domain.constants import ISSUE_STATUS_SOLVED

class IssuePostgresqlRepository(IssueRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        session = self.Session()
        try:
            issues=session.query(IssueModelSqlAlchemy).filter(
                extract('year', IssueModelSqlAlchemy.created_at) == year,
                extract('month', IssueModelSqlAlchemy.created_at) == month,
                IssueModelSqlAlchemy.status == ISSUE_STATUS_SOLVED,
                IssueModelSqlAlchemy.auth_user_id==user_id).all()
            
            return [self._from_model(issue_model) for issue_model in issues]
        finally:
            session.close()

    def list_issues_filtered(self, user_id, status=None, channel_plan_id=None, created_at=None, closed_at=None):
        session = self.Session()
        try:            
            query = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id)
        
            if status:
                query = query.filter(IssueModelSqlAlchemy.status == status)
            if channel_plan_id:
                query = query.filter(IssueModelSqlAlchemy.channel_plan_id == channel_plan_id)
            if created_at:
                query = query.filter(IssueModelSqlAlchemy.created_at >= created_at)
            if closed_at:
                query = query.filter(IssueModelSqlAlchemy.created_at <= closed_at)

            issues_sqlalchemy = query.all()

            issues = [
                Issue(
                    id=issue_model.id,
                    auth_user_id=issue_model.auth_user_id,
                    auth_user_agent_id=issue_model.auth_user_agent_id,
                    status=issue_model.status,
                    subject=issue_model.subject,
                    description=issue_model.description,
                    created_at=issue_model.created_at,
                    closed_at=issue_model.closed_at,
                    channel_plan_id=issue_model.channel_plan_id
                ).to_dict() for issue_model in issues_sqlalchemy
            ]

            return issues

        finally:
            session.close()

    def create_issue(self, issue:Issue, attachment: IssueAttachment = None):
        try:
            session = self.Session()
            issue_model = self._to_model(issue)
            session.add(issue_model)
            session.commit()  

            if attachment:
                attachment_model = self._to_model_attachment(attachment)
                session.add(attachment_model)
            session.commit()

        except Exception as e:
            if session:
                session.rollback()
            raise e
        finally:
            if session:
                session.close()
    
    def find(self, user_id = None,page=None,limit=None):
        try:
            session = self.Session()
            total_items = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id).count()
            total_pages = ceil(total_items / limit)
            has_next = page < total_pages

            issues = session.query(IssueModelSqlAlchemy).join(IssueStateSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id).order_by(IssueModelSqlAlchemy.created_at).offset((page - 1) * limit).limit(limit).all()

            data = [{
                "id": str(issue.id),
                "auth_user_id": str(issue.auth_user_id),
                "status": str(issue.issue_status.name),
                "subject": issue.subject,
                "description": issue.description,
                "created_at": str(issue.created_at),
                "closed_at": str(issue.closed_at),
                "channel_plan_id": str(issue.channel_plan_id)
                } for issue in issues]
            
            return {
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "has_next": has_next,
                "data": data
            }
        except Exception as ex:
            if session:
                session.rollback()
            raise ex
        finally:
            if session:
                session.close()

    # def _from_model(self, model: Issue) -> IssueModelSqlAlchemy:
    #     return IssueModelSqlAlchemy(
    #         id=model.id,
    #         auth_user_id=model.auth_user_id,
    #         auth_user_agent_id=model.auth_user_agent_id,
    #         status=model.status,
    #         subject=model.subject,
    #         description=model.description,
    #         created_at=model.created_at,
    #         closed_at=model.closed_at,
    #         channel_plan_id=model.channel_plan_id
    #     )
        
    # def _to_model(self,issue:Issue)->IssueModelSqlAlchemy:
    #     issue_entity = IssueModelSqlAlchemy(
    #         id=issue.id,
    #         auth_user_id=issue.auth_user_id,
    #         auth_user_agent_id=issue.auth_user_agent_id,
    #         status=issue.status,
    #         subject=issue.subject,
    #         description=issue.description,
    #         created_at=issue.created_at,
    #         closed_at=issue.closed_at,
    #         channel_plan_id=issue.channel_plan_id
    #     )

    #     return issue_entity    

    def _from_model(self, model: IssueModelSqlAlchemy) -> Issue:
        return Issue(
            id=model.id,
            auth_user_id=model.auth_user_id,
            auth_user_agent_id=model.auth_user_agent_id,
            status=model.status,
            subject=model.subject,
            description=model.description,
            created_at=model.created_at,
            closed_at=model.closed_at,
            channel_plan_id=model.channel_plan_id
        )
    def _to_model(self,issue:Issue)->IssueModelSqlAlchemy:
        return IssueModelSqlAlchemy(
            id=issue.id,
            auth_user_id=issue.auth_user_id,
            auth_user_agent_id=issue.auth_user_agent_id,
            status=issue.status,
            subject=issue.subject,
            description=issue.description,
            created_at=issue.created_at,
            closed_at=issue.closed_at,
            channel_plan_id=issue.channel_plan_id
        )  

    def _to_model_attachment(self,attachment:IssueAttachment)->IssueAttachmentSqlAlchemy:
        attachment_entity = IssueAttachmentSqlAlchemy(
                id=attachment.id,
                issue_id=attachment.issue_id,
                file_path=attachment.file_path
        )

        return attachment_entity  
    

    def list_top_issues_by_user(self,user_id) -> List[Issue]:
        session = self.Session()
        try:
            # issues= (
            #     session.query(IssueModelSqlAlchemy.description)
            #     .filter(IssueModelSqlAlchemy.auth_user_id == user_id)
            #     .distinct(IssueModelSqlAlchemy.description)
            #     .order_by(IssueModelSqlAlchemy.created_at.desc())
            #     .limit(10)
            #     .all()
            # )

            subquery = (
                session.query(
                    IssueModelSqlAlchemy.description,
                    IssueModelSqlAlchemy.created_at
                )
                .filter(IssueModelSqlAlchemy.auth_user_id == user_id)
                .order_by(IssueModelSqlAlchemy.created_at.desc())
                .limit(10)
                .subquery()
            )

            issues = session.query(func.distinct(subquery.c.description)).all()
            return issues
        finally:
            session.close()