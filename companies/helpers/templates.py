from os.path import abspath
from pathlib import Path
from uuid import UUID

from aiofile import async_open


class Templates:  # noqa: WPS306
    """Templates for email."""

    root = Path(abspath(__file__)).parent.parent / 'templates'

    email_confirm_html: str = ''
    email_confirm_text: str = """Confirm Your Email Address


Open the link __CONFIRM_URL to confirm your email address. 
If you didn`t create an account, you can safely delete this email.
    """
    reset_password_html: str = ''
    reset_password_text: str = """Reset Your password


Open the link __RESET_PASSWORD_URL to reset your password. 
If you didn`t create an account, you can safely delete this email.
    """

    @classmethod
    async def build_email_confirm_html(cls, code: UUID | str) -> str:
        """Build html for email confirm."""
        if not cls.email_confirm_html:
            async with async_open(cls.root / 'confirm_code.html') as af:
                cls.email_confirm_html = await af.read()

        return cls.email_confirm_html.replace(
            '__SITE_URL',
            'https://vhosty.com/',
        ).replace(
            '__LOGO_URL',
            'https://vhosty.com/logo192.png',
        ).replace(
            '__CONFIRM_URL',
            f'https://vhosty.com/confirmed/{code}',
        )

    @classmethod
    async def build_email_confirm_text(cls, code: UUID | str) -> str:
        """Build text for email confirm."""
        return cls.email_confirm_text.replace(
            '__CONFIRM_URL',
            f'https://vhosty.com/confirmed/{code}',
        )

    @classmethod
    async def build_reset_password_html(cls, code: UUID | str) -> str:
        """Build html for reset password."""
        if not cls.reset_password_html:
            async with async_open(cls.root / 'reset_password.html') as af:
                cls.email_confirm_html = await af.read()

        return cls.email_confirm_html.replace(
            '__SITE_URL',
            'https://vhosty.com/',
        ).replace(
            '__LOGO_URL',
            'https://vhosty.com/logo192.png',
        ).replace(
            '__RESET_PASSWORD_URL',
            f'https://vhosty.com/password-recovery/{code}',
        )

    @classmethod
    async def build_reset_password_text(cls, code: UUID | str) -> str:
        """Build text for reset password."""
        return cls.reset_password_text.replace(
            '__RESET_PASSWORD_URL',
            f'https://vhosty.com/password-recovery/{code}',
        )
