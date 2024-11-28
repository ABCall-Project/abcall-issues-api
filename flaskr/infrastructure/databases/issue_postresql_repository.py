from math import ceil
from flask import jsonify
import json
from sqlalchemy import create_engine,extract, func, desc
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ...utils import Logger
from ...domain.models import Issue, IssueAttachment,IssueTrace
from ...domain.interfaces import IssueRepository
from ...infrastructure.databases.model_sqlalchemy import Base, IssueModelSqlAlchemy, IssueAttachmentSqlAlchemy, IssueStateSqlAlchemy,IssueTraceSqlAlchemy
from ...domain.constants import ISSUE_STATUS_SOLVED, ISSUE_STATUS_OPEN,ISSUE_STATUS_INPROGRESS
from .postgres.db import Session, engine

log = Logger()


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
                
                issue = self._from_model(issue_model)
                return issue

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

    def all(self):
            with self.session() as session:
                try:
                    issues = (session.query(IssueModelSqlAlchemy)
                            .join(IssueStateSqlAlchemy)
                            .filter(IssueModelSqlAlchemy.status ==ISSUE_STATUS_OPEN)
                            .order_by(desc(IssueModelSqlAlchemy.created_at))
                            .all()
                    )

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
                    
                    return data
                except Exception as ex:
                    if session:
                        session.rollback()
                    raise ex
                finally:
                    if session:
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
    
    def assign_issue(self, issue_id, auth_user_agent_id) -> dict:
            with self.session() as session:
                try:
                    
                    issue = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.id == issue_id).one_or_none()
                    log.info(f"The issue: ${issue}")
                    if not issue:
                        raise ValueError("Issue not found")
                    issue.auth_user_agent_id = auth_user_agent_id
                    issue.status = ISSUE_STATUS_INPROGRESS
                    session.commit()
                except Exception as ex:
                    session.rollback()
                    raise ex
    def get_open_issues(self,page=None,limit=None):
        with self.session() as session:
            log.info('Receive request IssuePostgresqlRepository --->')
            try:
                total_items = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.status == ISSUE_STATUS_OPEN).count()
                total_pages = ceil(total_items / limit)
                has_next = page < total_pages
                issues = (session.query(IssueModelSqlAlchemy)
                            .join(IssueStateSqlAlchemy)
                            .filter(IssueModelSqlAlchemy.status == ISSUE_STATUS_OPEN)
                            .order_by(desc(IssueModelSqlAlchemy.created_at))
                            .offset((page - 1) * limit)
                            .limit(limit)
                            .all()
                    )
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
            finally:
                session.close()
    
    def create_issue_trace(self, issue_trace: IssueTrace):
        with self.session() as session:
            try:
                log.info(f'Receive request Postgres to create_issue_trace')

                issue = session.query(IssueModelSqlAlchemy).filter(IssueModelSqlAlchemy.id == issue_trace.issue_id).one_or_none()

                if issue is None:
                    raise ValueError("Issue not found")

                issue_trace.channel_plan_id = issue.channel_plan_id
                issue_trace_model = self._to_model_issue_trace(issue_trace)
                session.add(issue_trace_model)
                session.commit()
                session.refresh(issue_trace_model)

            except Exception as e:
                if session:
                    session.rollback()
                raise e
            finally:
                if session:
                    session.close()

    def _to_model_issue_trace(self,issueTrace:IssueTraceSqlAlchemy)->IssueTraceSqlAlchemy:
        trace = IssueTraceSqlAlchemy(
                id=issueTrace.id,
                issue_id=issueTrace.issue_id,
                auth_user_id = issueTrace.auth_user_id,
                auth_user_agent_id = issueTrace.auth_user_agent_id,
                scope = issueTrace.scope,
                channel_plan_id = issueTrace.channel_plan_id
        )

        return trace  
    

    def get_top_7_incident_types(self) -> List[Issue]:
        """
        Get the 7 most reported types of incidents as Issue objects.

        Returns:
            List[Issue]: A list of Issue objects representing the top 7 incident types.
        """
        with self.session() as session:
            try:
                results = (
                    session.query(IssueModelSqlAlchemy.subject, func.count(IssueModelSqlAlchemy.id).label('count'))
                    .group_by(IssueModelSqlAlchemy.subject)
                    .order_by(desc('count'))
                    .limit(7)
                    .all()
                )
                
                top_issues = [
                    self._from_model(IssueModelSqlAlchemy(subject=result[0]))
                    for result in results
                ]
                return top_issues
            finally:
                session.close()