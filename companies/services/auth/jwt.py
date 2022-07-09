from fastapi import HTTPException, status, Response
from jwt import encode

from entities.api.auth import JwtResponse
from helpers.datetime import after
from repositories.employees import get_employee_by_email
from repositories.tokens import create_token, get_employee_by_token
from settings import setting


async def get_jwt_tokens(
        employee_id: int,
        company_id: int,
        response: Response,
        role: str = 'employee',
) -> JwtResponse:
    """Get jwt tokens."""
    payload = {
        'employee_id': employee_id,
        'company_id': company_id,
        'role': role,
        'type': 'access',
        'exp': after(minutes=setting.auth.access_timeout_minutes),
    }
    access_token = encode(payload, setting.auth.jwt_secret)
    payload['type'] = 'refresh'
    payload['exp'] = after(hours=setting.auth.refresh_timeout_hours)
    refresh_token = encode(payload, setting.auth.jwt_secret)

    await create_token(refresh_token, payload['exp'], employee_id)

    response.set_cookie(
        'refresh_companies',
        refresh_token,
        expires=int(payload['exp'].timestamp()),
        httponly=True,
    )
    for domain in setting.allow_domains:
        response.set_cookie(
            'refresh_companies',
            refresh_token,
            expires=int(payload['exp'].timestamp()),
            httponly=True,
            domain=domain,
        )

    return JwtResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def auth_by_email(
        email: str,
        password: str,
        response: Response,
) -> JwtResponse:
    """Authorize employee by email."""
    employee = await get_employee_by_email(email)
    if employee and employee.is_valid_password(password):
        return await get_jwt_tokens(employee.id, employee.company_id, response)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid password or email.',
    )


async def refresh_tokens(token: str, response: Response) -> JwtResponse:
    """Refresh tokens."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='refresh token required',
        )

    employee = await get_employee_by_token(token)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired or revoked',
        )

    return await get_jwt_tokens(employee.id, employee.company_id, response)
