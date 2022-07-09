from entities.enums import LegalTypeEnum
from pydantic import BaseModel, EmailStr, validator


class EmailLoginRequest(BaseModel):
    """Request model for login via email."""

    email: EmailStr
    password: str


class RegistrationRequest(EmailLoginRequest):
    """Request model for register Company via email."""

    email: EmailStr
    password: str
    password2: str
    first_name: str
    last_name: str
    phone: str
    legal_type: LegalTypeEnum

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):  # noqa: WPS110, WPS111, N805
        """Compare passwords."""
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str | None = None


class ResetPasswordRequest(BaseModel):
    """Reset password request model."""

    email: EmailStr


class ResetPasswordConfirm(BaseModel):
    """Reset password confirm model."""

    code: str
    new_password: str
    new_password2: str

    @validator('new_password2')
    def passwords_match(cls, v, values, **kwargs):  # noqa: WPS110, WPS111, N805
        """Compare passwords."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('passwords do not match')
        return v


class ChangePasswordRequest(BaseModel):
    """Change password request."""

    old_password: str
    new_password: str
    new_password2: str

    @validator('new_password2')
    def passwords_match(cls, v, values, **kwargs):  # noqa: WPS110, WPS111, N805
        """Compare passwords."""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('passwords do not match')
        return v


class JwtResponse(BaseModel):
    """JWT response schema."""

    access_token: str
    refresh_token: str
