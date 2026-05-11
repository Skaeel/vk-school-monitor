from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.user import User
    from src.db.models.alert import Alert

class Post(Base):
    __tablename__ = "posts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    link: Mapped[str] = mapped_column(String(255), unique=True)
    text: Mapped[Optional[str]] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(DateTime, index=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("post_statuses.id"))

    user: Mapped["User"] = relationship("User", back_populates="posts")
    alert: Mapped["Alert"] = relationship("Alert", back_populates="post", uselist=False, cascade="all, delete-orphan")
        

class PostStatus(Base):
    __tablename__ = "post_statuses"

    status: Mapped[str] = mapped_column(String(30), unique=True)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="status")