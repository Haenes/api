from datetime import datetime

from sqlalchemy import (
    VARCHAR, DateTime, ForeignKey, CheckConstraint, text
    )
from sqlalchemy.orm import Mapped, mapped_column

from models import BaseClass
from .schemas import IssueType, IssueStatus, IssuePriority


class Issue(BaseClass):
    __tablename__ = "issue"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("project.id", ondelete="CASCADE")
        )
    key: Mapped[int] = mapped_column(default=1)
    title: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    type: Mapped[str] = mapped_column(VARCHAR)
    priority: Mapped[str] = mapped_column(VARCHAR)
    status: Mapped[str] = mapped_column(VARCHAR)
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=text("CURRENT_TIMESTAMP"),
        server_default=text("CURRENT_TIMESTAMP")
        )

    __table_args__ = (
        CheckConstraint(
            sqltext=type.in_(
                [
                    IssueType.bug.value,
                    IssueType.feature.value
                    ]
                ),
            name='issue_type_check'
            ),
        CheckConstraint(
            sqltext=priority.in_(
                [
                    IssuePriority.lowest.value,
                    IssuePriority.low.value,
                    IssuePriority.medium.value,
                    IssuePriority.high.value,
                    IssuePriority.highest.value
                    ]
                ),
            name='issue_priority_check'
            ),
        CheckConstraint(
            sqltext=status.in_(
                [
                    IssueStatus.to_do.value,
                    IssueStatus.in_progress.value,
                    IssueStatus.done.value
                    ]
                ),
            name='issue_status_check'
            )
        )
