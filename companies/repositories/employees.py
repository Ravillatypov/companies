from datetime import datetime
from uuid import UUID

from tortoise.expressions import Q

from helpers.datetime import utcnow
from repositories.pg_models import PGEmployee


async def email_is_exist(email: str) -> bool:
    """Check email is used or not."""
    return await PGEmployee.filter(email=email).exists()


async def create_employee(
        email: str,
        code: str | UUID,
        code_expired_at: datetime,
        first_name: str,
        last_name: str,
        password: str,
) -> PGEmployee:
    """Create employee."""
    return await PGEmployee.create(
        email=email,
        email_activate_code=code,
        email_code_expired_at=code_expired_at,
        first_name=first_name,
        last_name=last_name,
        password_hash=PGEmployee.get_pass_hash(password),
    )


async def get_employee_by_email(email: str) -> PGEmployee | None:
    """Get employee by email."""
    return await PGEmployee.filter(email=email).order_by('-email_is_verified').first()


async def get_employee_by_email_code(code: str) -> PGEmployee | None:
    """Get matched employee or None."""
    return await PGEmployee.filter(
        email_activate_code=code,
    ).first()


async def get_employee_by_reset_code(code: str | UUID) -> PGEmployee | None:
    """Get employee by reset code."""
    return await PGEmployee.filter(
        reset_password_code=code,
        reset_code_expired_at__gte=utcnow(),
    ).first()


async def get_employee(id_: int) -> PGEmployee:
    """Get employee model from DB."""
    return await PGEmployee.get(id=id_)


async def clear_inactive_employees_by_email(email: str):
    """Delete not verified employees."""
    await PGEmployee.filter(
        Q(join_type=Q.OR, email=email, email_code_expired_at__lte=utcnow()),
        email_is_verified=False,
        phone_is_verified=False,
    ).delete()

    await PGEmployee.filter(
        email=email,
        email_is_verified=False,
    ).update(
        email=None,
        email_code_expired_at=None,
        email_activate_code=None,
    )

