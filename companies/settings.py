from os import environ
from typing import Tuple

from pydantic import BaseModel, Field
from pydantic.env_settings import BaseSettings, SettingsSourceCallable
from urllib3.util import Url, parse_url


class AuthSetting(BaseModel):
    """Authorization config."""

    jwt_secret: str = '3$gfOmGl'
    access_timeout_minutes: int = 15
    refresh_timeout_hours: int = 15
    email_activation_timeout_hours: int = 24
    phone_activation_timeout_seconds: int = 300


class SMTP(BaseModel):
    """Email configuration."""

    is_enabled: bool = False
    from_email: str = ''
    host: str = ''
    port: int = 25
    ssl: bool = False
    login: str = ''
    password: str = ''


class Setting(BaseSettings):
    """Main application settings."""

    env: str = 'local'
    debug: bool = False
    version: str = '0.1.0'
    sentry_dsn: str = ''

    db_url: str = 'sqlite://db.sqlite3'
    allow_origins: list[str] = [
        'http://localhost:8000',
        'http://localhost:3000',
        'http://dev.vhosty.com',
        'https://dev.vhosty.com',
    ]
    allow_domains: list[str] = []

    auth: AuthSetting = Field(default_factory=AuthSetting)
    smtp: SMTP = Field(default_factory=SMTP)

    def calc_allow_domains(self):
        """Calc allow domains by allow origins."""
        if not self.allow_domains and self.allow_origins:
            urls: list[Url] = [parse_url(url) for url in self.allow_origins]
            self.allow_domains.extend(list({url.hostname for url in urls if url.hostname}))

    class Config:  # noqa: WPS431, WPS306
        """Setting configuration."""

        env_nested_delimiter = '__'
        secrets_dir = environ.get('SECRET_DIR', '/tmp')  # noqa: S108
        env_file = environ.get('ENV_FILE', '.env')

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            """Priority load setting."""
            return (file_secret_settings, env_settings, init_settings)


setting = Setting()
setting.calc_allow_domains()
