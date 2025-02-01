"""add default chat and user

Revision ID: 287817bca837
Revises: 681f09ccb375
Create Date: 2025-01-31 18:45:59.485998

"""

import sqlmodel
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlmodel import Session, select

from src.dal.models import User, Chat
from src.core.settings import settings

# revision identifiers, used by Alembic.
revision: str = "287817bca837"
down_revision: Union[str, None] = "681f09ccb375"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    default_user = User(id=settings.server.default_user_uuid, username="system_default_user")
    session.add(default_user)
    default_chat = Chat(
        id=settings.server.default_chat_uuid, name="general_chat", owner_id=default_user.id, is_private=False
    )
    session.add(default_chat)

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    chat = select(Chat).where(Chat.id == settings.server.default_chat_uuid)
    user = select(User).where(User.id == settings.server.default_user_uuid)

    session.delete(chat)
    session.delete(user)

    session.commit()
