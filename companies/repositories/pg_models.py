from bcrypt import hashpw, checkpw, gensalt
from tortoise import Model, fields

# flake8: noqa


class PGCompany(Model):
    """Company model."""

    name = fields.CharField(max_length=120, null=True)
    email = fields.CharField(max_length=100, null=True)
    is_verified = fields.BooleanField(default=False)
    phone = fields.CharField(max_length=13, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    main_employee: fields.ForeignKeyRelation['PGEmployee'] = fields.ForeignKeyField(
        'models.PGEmployee',
        on_delete=fields.SET_NULL,
        null=True,
    )

    extra = fields.JSONField(null=True)

    class Meta:
        table = 'companies'


class PGEmployee(Model):
    """Employee model."""

    email = fields.CharField(max_length=100, index=True, null=True)
    email_is_verified = fields.BooleanField(default=False)
    email_activate_code = fields.UUIDField(null=True)
    email_code_expired_at = fields.DatetimeField(null=True)

    reset_code_expired_at = fields.DatetimeField(null=True)
    reset_password_code = fields.UUIDField(null=True)

    password_hash = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=13, null=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    extra = fields.JSONField(null=True)

    company: fields.ForeignKeyRelation[PGCompany] = fields.ForeignKeyField(
        'models.PGCompany',
        related_name='employees',
        on_delete=fields.SET_NULL,
        null=True,
    )

    class Meta:
        table = 'employees'

    @classmethod
    def get_pass_hash(cls, password: str) -> str:
        """Generate password hash."""
        return hashpw(password.encode(), gensalt()).decode()

    def is_valid_password(self, password: str) -> bool:
        """Check password."""
        return checkpw(password.encode(), self.password_hash.encode())


class PGRefreshToken(Model):
    """Tokens store model."""

    refresh_token = fields.CharField(max_length=255, index=True)
    employee: fields.ForeignKeyRelation[PGEmployee] = fields.ForeignKeyField(
        'models.PGEmployee',
        related_name='tokens',
    )
    expired_at = fields.DatetimeField()

    class Meta:
        table = 'refresh_tokens'
