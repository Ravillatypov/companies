from uuid import uuid4

from entities.api.auth import JwtResponse
from helpers.datetime import after
from helpers.email import send_email
from helpers.templates import Templates
from repositories.employees import get_employee_by_email, get_employee_by_reset_code, get_employee_by_email_code, get_employee
from fastapi import HTTPException, status, Response

from services.auth.jwt import get_jwt_tokens


async def reset_password_request(email: str) -> None:  # noqa: WPS217
    """Reset password request."""
    employee = await get_employee_by_email(email)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Employee with email: "{email}" not found',
        )

    minimal_available_dt = after(hours=12)  # noqa: WPS432

    if not (employee.reset_password_code and employee.reset_code_expired_at < minimal_available_dt):
        employee.reset_password_code = uuid4()
        employee.reset_code_expired_at = after(days=1)
        await employee.save()

    await send_email(
        await Templates.build_reset_password_text(employee.reset_password_code),
        'Reset password',
        [employee.email],
        html_text=await Templates.build_reset_password_html(employee.reset_password_code),
    )


async def reset_password_confirm(
        code: str,
        new_password: str,
        response: Response,
) -> JwtResponse:
    """Reset password."""
    employee = await get_employee_by_reset_code(code)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='invalid code or code is expired',
        )

    employee.password_hash = employee.get_pass_hash(new_password)
    await employee.save()

    return await get_jwt_tokens(employee.id, employee.company_id, response)


async def change_password(
        employee_id: int,
        old_password: str,
        new_password: str,
):
    """Change password."""
    employee = await get_employee(employee_id)
    if not employee.is_valid_password(old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid old password',
        )

    employee.password_hash = employee.get_pass_hash(new_password)
    await employee.save()
