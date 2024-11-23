from sqlalchemy import Column, String, Numeric, DateTime,Text,ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class IssueStateSqlAlchemy(Base):
    __tablename__ = 'issue_state'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(10), nullable=False)

class IssueModelSqlAlchemy(Base):
    __tablename__ = 'issue'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_user_id = Column(PG_UUID(as_uuid=True), nullable=True)
    auth_user_agent_id = Column(PG_UUID(as_uuid=True), nullable=True)
    status = Column(PG_UUID(as_uuid=True),ForeignKey('issue_state.id'), nullable=True)
    subject = Column(String(255), nullable=False)
    description=Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())
    closed_at = Column(DateTime(timezone=True), default=func.now())
    channel_plan_id = Column(PG_UUID(as_uuid=True), nullable=True)
    issue_status = relationship("IssueStateSqlAlchemy")



class IssueAttachmentSqlAlchemy(Base):
    __tablename__ = 'issue_attachment'
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(PG_UUID(as_uuid=True), ForeignKey('issue.id'), nullable=False)
    file_path = Column(String(255), nullable=False) 

    issue = relationship("IssueModelSqlAlchemy", backref="attachments")

class IssueTraceSqlAlchemy(Base):
    __tablename__ = 'issue_trace'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    issue_id = Column(PG_UUID(as_uuid=True), ForeignKey('issue.id'), nullable=False)
    auth_user_id = Column(PG_UUID(as_uuid=True), nullable=True)
    auth_user_agent_id = Column(PG_UUID(as_uuid=True), nullable=True)
    scope = Column(String(255), nullable=True)
    channel_plan_id = Column(PG_UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now()) 
    