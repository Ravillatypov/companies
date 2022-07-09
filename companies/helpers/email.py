from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from logging import getLogger
from typing import List

import aiosmtplib
from settings import setting

logger = getLogger(__name__)


async def send_email(
        text: str,
        subject: str,
        emails: List[str] = None,
        html_text: str = None,
        attachments=None,
):
    """Send email if enabled."""
    if not setting.smtp.is_enabled:
        logger.info(
            'email is disabled',
            extra={'text': text, 'subject': subject, 'emails': emails},
        )
        return

    message = MIMEMultipart()
    message['From'] = setting.smtp.from_email
    message['Subject'] = subject
    message['To'] = ', '.join(emails)

    message_body = MIMEMultipart('alternative')
    message_body.attach(MIMEText(text, 'plain', 'utf-8'))

    if html_text:
        message_body.attach(MIMEText(html_text, 'html', 'utf-8'))

    message.attach(message_body)
    for attach in attachments or []:
        message.attach(attach)

    try:
        await aiosmtplib.send(
            message,
            setting.smtp.from_email,
            recipients=emails,
            hostname=setting.smtp.host,
            port=setting.smtp.port,
            username=setting.smtp.login,
            password=setting.smtp.password,
            use_tls=setting.smtp.ssl,
        )
    except Exception as err:
        logger.warning(f'Error on send email to {emails}. Error: {err}')
