from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), 
        server_default=func.timezone('UTC', func.now())
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), 
        server_default=func.timezone('UTC', func.now()), 
        onupdate=func.timezone('UTC', func.now())
    )