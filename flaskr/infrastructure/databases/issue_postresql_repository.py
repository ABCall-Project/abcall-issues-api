from math import ceil
from flask import jsonify
import json
from sqlalchemy import create_engine,extract, func, desc
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ...utils import Logger
from ...domain.models import Issue, IssueAttachment
from ...domain.interfaces import IssueRepository
from ...infrastructure.databases.model_sqlalchemy import Base, IssueModelSqlAlchemy, IssueAttachmentSqlAlchemy, IssueStateSqlAlchemy
log = Logger()
from ...domain.constants import ISSUE_STATUS_SOLVED
from .postgres.db import Session, engine

class IssuePostgresqlRepository(IssueRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def list_issues_period (self,user_id,year, month) -> List[Issue]:
        with self.session() as session:
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
        with self.session() as session:
            try:            
                query = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id)
            
                if status:
                    query = query.filter(IssueModelSqlAlchemy.issue_status.has(name=status))
                if channel_plan_id:
                    query = query.filter(IssueModelSqlAlchemy.channel_plan_id == channel_plan_id)
                if created_at:
                    query = query.filter(IssueModelSqlAlchemy.created_at >= created_at)
                if closed_at:
                    query = query.filter(IssueModelSqlAlchemy.closed_at <= closed_at)

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
            except Exception as ex:
                log.error(f'Error retrieving issues by user_id {user_id}: {ex}')
                raise ex
            finally:
                session.close()         

    def create_issue(self, issue:Issue, attachment: IssueAttachment = None):
        with self.session() as session:
            try:
                issue_model = self._to_model(issue)
                session.add(issue_model)
                session.commit()
                session.refresh(issue_model)

                if attachment:
                    attachment_model = self._to_model_attachment(attachment)
                    session.add(attachment_model)
                session.commit()
                session.refresh(attachment_model)

            except Exception as e:
                if session:
                    session.rollback()
                raise e
            finally:
                if session:
                    session.close()
    
    def find(self, user_id = None,page=None,limit=None):
        with self.session() as session:
            try:
                total_items = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id).count()
                total_pages = ceil(total_items / limit)
                has_next = page < total_pages

                issues = session.query(IssueModelSqlAlchemy).join(IssueStateSqlAlchemy).filter(IssueModelSqlAlchemy.auth_user_id == user_id).order_by(desc(IssueModelSqlAlchemy.created_at)).offset((page - 1) * limit).limit(limit).all()

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

    def get_issue_by_id(self, issue_id: str) -> Optional[dict]:
        with self.session() as session:
            try:
                issue = (
                    session.query(IssueModelSqlAlchemy, IssueStateSqlAlchemy.name.label("status_name"))
                    .join(IssueStateSqlAlchemy, IssueModelSqlAlchemy.status == IssueStateSqlAlchemy.id)
                    .filter(IssueModelSqlAlchemy.id == issue_id)
                    .first()
                )

                if not issue:
                    return issue

                issue_data = {
                    "created_at": issue.IssueModelSqlAlchemy.created_at.isoformat() if issue.IssueModelSqlAlchemy.created_at else None,
                    "id": str(issue.IssueModelSqlAlchemy.id),  # Convertir UUID a cadena
                    "subject": issue.IssueModelSqlAlchemy.subject,
                    "description": issue.IssueModelSqlAlchemy.description,
                    "status": issue.status_name,
                    "closed_at": issue.IssueModelSqlAlchemy.closed_at.isoformat() if issue.IssueModelSqlAlchemy.closed_at else None
                }
                return issue_data

            except Exception as ex:
                log.error(f"Error retrieving issue by issue_id {issue_id}: {ex}")
                return None
            finally:
                session.close()         

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
        with self.session() as session:
            try:
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