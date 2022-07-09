from uuid import uuid4

from entities.api.auth import RegistrationRequest, JwtResponse
from helpers.datetime import after
from repositories.employees import email_is_exist, create_employee
from fastapi import HTTPException, status, Response
from services.auth.jwt import get_jwt_tokens


async def register_employee(
        request_model: RegistrationRequest,
        response: Response,
) -> JwtResponse:
    """Register as employee of company."""
    if await email_is_exist(request_model.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Employee with email: "{request_model.email}" already exist',
        )

    employee = await create_employee(
        email=request_model.email,
        code=uuid4(),
        code_expired_at=after(days=1),
        first_name=request_model.first_name,
        last_name=request_model.last_name,
        password=request_model.password,
    )

    return await get_jwt_tokens(employee.id, employee.company_id, response)


async def confirm_email(code: str):
    """Confirm email address."""
