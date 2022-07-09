from entities.api.auth import EmailLoginRequest, RegistrationRequest, JwtResponse, ResetPasswordRequest, \
    RefreshTokenRequest, ChangePasswordRequest, ResetPasswordConfirm
from fastapi import APIRouter, Response, Cookie, Depends
from repositories.tokens import remove_token
from services.auth.register import register_employee
from services.auth.jwt import auth_by_email, refresh_tokens
from services.auth.password import reset_password_confirm, reset_password_request, change_password
from web.dependencies import get_employee_id
router = APIRouter(prefix='/api/companies', tags=['companies'])


@router.post(
    '/employees/register',
    response_model=JwtResponse,
)
async def register_company_url(
        request_model: RegistrationRequest,
        response: Response,
) -> JwtResponse:
    """Register employee url."""
    return await register_employee(request_model, response)


@router.post(
    '/employees/login',
    response_model=JwtResponse,
)
async def login_url(
        request_model: EmailLoginRequest,
        response: Response,
) -> JwtResponse:
    """Login url."""
    return await auth_by_email(
        request_model.email,
        request_model.password,
        response,
    )


@router.post(
    '/token/refresh',
    response_model=JwtResponse,
)
async def refresh_token_url(
        request_model: RefreshTokenRequest | None,
        response: Response,
        refresh_token: str | None = Cookie(default='', alias='refresh_companies'),
) -> JwtResponse:
    """Refresh tokens."""
    token = refresh_token
    if not token and request_model:
        token = request_model.refresh_token

    return await refresh_tokens(token, response)


@router.post(
    '/token/revoke'
)
async def revoke_token_url(
        request_model: RefreshTokenRequest | None,
        response: Response,
        refresh_token: str | None = Cookie(default='', alias='refresh_companies'),
):
    """Revoke tokens."""
    token = refresh_token
    if not token and request_model:
        token = request_model.refresh_token

    if token:
        await remove_token(token)

    response.delete_cookie('refresh_companies')


@router.post(
    '/password/reset-request'
)
async def reset_password_request_url(request_model: ResetPasswordRequest):
    """Reset password request."""
    await reset_password_request(request_model.email)


@router.post(
    '/password/reset-confirm',
    response_model=JwtResponse,
)
async def reset_password_request_url(
        request_model: ResetPasswordConfirm,
        response: Response,
):
    """Reset password request."""
    await reset_password_confirm(request_model.code, request_model.new_password, response)


@router.post(
    '/password/change'
)
async def change_password_url(
        request_model: ChangePasswordRequest,
        employee_id: int = Depends(get_employee_id),
):
    """Change password request."""
    await change_password(
        employee_id,
        request_model.old_password,
        request_model.new_password,
    )


@router.get(
    '/my-company',
)
async def get_my_company_url():
    """Get about my company."""


@router.post(
    '/my-company',
)
async def get_my_company_url():
    """Get about my company."""
