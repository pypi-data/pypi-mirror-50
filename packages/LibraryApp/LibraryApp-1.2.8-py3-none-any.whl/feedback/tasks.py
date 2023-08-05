from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from feedback.emails import send_feedback_email
from feedback.emails import send_periodic_email

logger = get_task_logger(__name__)


@task(name="send_feedback_email_task")
def send_feedback_email_task(email, message):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")
    return send_feedback_email(email, message)


@periodic_task(run_every=(
    crontab(minute='*/1')), name="sendperiodic_email", ignore_result=True)
def send_periodic_email_task():
    logger.info("Sent periodic email")
    send_periodic_email()

# testing tasks with flower
# celery flower -A locallibrary --address=127.0.0.1 --port=5555
