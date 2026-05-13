from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixins import CreatedAtMixin, UpdatedAtMixin
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.post import Post
    from src.db.models.alert import Alert


class User(Base, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(30))
    surname: Mapped[Optional[str]] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(15))
    link: Mapped[str] = mapped_column(String(255), unique=True)
    status_id: Mapped[int] = mapped_column(ForeignKey("user_statuses.id"), default=0)

    status: Mapped["UserStatus"] = relationship("UserStatus")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship("Alert", back_populates="user", cascade="all, delete-orphan")


class UserStatus(Base):
    __tablename__ = "user_statuses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    status: Mapped[str] = mapped_column(String(30), unique=True)
    
    users: Mapped[list["User"]] = relationship("User", back_populates="status")