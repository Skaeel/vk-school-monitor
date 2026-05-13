from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.mixins import CreatedAtMixin
from src.db.models.base import Base

if TYPE_CHECKING:
    from src.db.models.user import User
    from src.db.models.post import Post

class Alert(Base, CreatedAtMixin):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), unique=True)
    reason: Mapped[str] = mapped_column(Text)

    user: Mapped["User"] = relationship("User", back_populates="alerts")
    post: Mapped["Post"] = relationship("Post", back_populates="alert")


