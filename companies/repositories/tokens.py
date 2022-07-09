from datetime import datetime

from tortoise.expressions import Q

from helpers.datetime import utcnow
from repositories.pg_models import PGRefreshToken, PGEmployee


async def create_token(
        refresh_token: str,
        expired_at: datetime,
        employee_id: int,
) -> None:
    """Save new refresh token."""
    await PGRefreshToken.filter(expired_at__lte=utcnow()).delete()
    await PGRefreshToken.create(
        employee_id=employee_id,
        refresh_token=refresh_token,
        expired_at=expired_at,
    )


async def get_employee_by_token(refresh_token: str) -> PGEmployee | None:
    """Get user id by refresh token."""
    token = await PGRefreshToken.filter(
        refresh_token=refresh_token,
        expired_at__gte=utcnow(),
    ).first()
    if token:
        employee = await token.employee.get()
        await token.delete()
        return await employee


async def remove_token(token: str) -> None:
    """Remove token from DB."""
    await PGRefreshToken.filter(
        Q(join_type=Q.OR, refresh_token=token, expired_at__lte=utcnow()),
    ).delete()
