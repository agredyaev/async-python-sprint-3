import secrets

from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import settings
from src.dal import ChatInviteRepository, UserChatRepository
from src.schemas.api import Body, Path, Response, StatusCode
from src.schemas.services import ChatInviteCreate


class InviteService:
    """Invite service."""

    __slots__ = ("invite_repo", "user_chat_repo")

    def __init__(self, session: AsyncSession):
        self.invite_repo = ChatInviteRepository(session)
        self.user_chat_repo = UserChatRepository(session)

    async def generate_invite_link(self, data: ChatInviteCreate) -> Response:
        """Generate invite link for chat."""
        token = secrets.token_urlsafe(settings.server.token_size)
        await self.invite_repo.create(data)
        return Response(
            status_code=StatusCode.OK,
            body=Body(details=f"{Path.CHAT_GENERATE_INVITE}?token={token}&user_id={data.inviter.id}"),
        )

    async def accept_invite(self, token: str, user_id: UUID) -> Response:
        """Accept invite to chat."""
        invite = await self.invite_repo.get_by_token(token)
        if not invite:
            return Response(status_code=StatusCode.NOT_FOUND, body=Body(details="Invite not found"))

        if invite.is_accepted:
            return Response(status_code=StatusCode.BAD_REQUEST, body=Body(details="Invite already accepted"))

        if await self.user_chat_repo.exists(primary_keys=(user_id, invite.chat_id)):
            return Response(
                status_code=StatusCode.BAD_REQUEST, body=Body(details="User is already a member of the chat")
            )

        await self.user_chat_repo.create(user_id=user_id, chat_id=invite.chat_id)
        invite.is_accepted = True
        await self.invite_repo.upsert(invite)

        return Response(status_code=StatusCode.OK, body=Body(details=f"chat_id: {invite.chat_id}"))
