import logging
from typing import Dict, Union
from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task # так помечаются отложенные задачи Celery
def send_feedback_mail(message_form: Dict[str, Union[int, str]]) -> None: # обьявляется функция с параметром через анатирование типов
    logger.info(f"Send message: '{message_form}'") # сообщение в лог
    model_user = get_user_model() # достаем модель User
    user_obj = model_user.objects.get(pk=message_form["user_id"]) # создаем обьект модели User
    send_mail( # отправляем сообщение
        "TechSupport Help",  # subject (title)
        message_form["message"],  # message
        user_obj.email,  # send from
        ["kurashevmichael@gmail.com"],  # send to
        fail_silently=False,
    )
    return None
