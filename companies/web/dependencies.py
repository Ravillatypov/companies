from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jwt import PyJWTError, decode
from settings import setting

auth_token = APIKeyHeader(
    name='Authorization',
    scheme_name='Bearer',
    description='JWT auth as company employee',
)


def _get_payload(token: str) -> dict:
    """Get payload from JWT."""
    token = token.split()[-1]

    try:
        payload = decode(token, setting.auth.jwt_secret, algorithms=['HS256'])
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token or expired',
        )
    if payload.get('type', '') != 'access':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid token type',
        )
    return payload


def get_employee_id(access_token: str = Depends(auth_token)) -> int:
    """Get employee ID from jwt token."""
    payload = _get_payload(access_token)
    return payload.get('employee_id')


def get_company_id(access_token: str = Depends(auth_token)) -> int:
    """Get employee company ID from jwt token."""
    payload = _get_payload(access_token)
    return payload.get('company_id')


def get_role(access_token: str = Depends(auth_token)) -> str:
    """Get employee role from jwt token."""
    payload = _get_payload(access_token)
    return payload.get('role')
