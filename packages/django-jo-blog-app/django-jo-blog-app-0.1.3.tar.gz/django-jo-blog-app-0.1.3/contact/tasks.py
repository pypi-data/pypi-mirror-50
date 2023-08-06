from celery.decorators import task
from celery.utils.log import get_task_logger

from contact.emails import send_contact_email

logger = get_task_logger(__name__)


@task(name="send_contact_email_task")
def send_contact_email_task(email, message):
    """sends an email when contact form is filled successfully"""
    logger.info("Sent contact email")
    return send_contact_email(email, message)


# @periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
# def trigger_emails():
#     send_contact_email()
