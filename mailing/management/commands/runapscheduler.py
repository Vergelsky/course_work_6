# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
import datetime
import pytz
from django.core.mail import send_mail

from mailing.models import Mailing, Log
from mailinger.settings import TIME_ZONE, EMAIL_HOST_USER

logger = logging.getLogger(__name__)


def send_mailing(mailing):
    try:
        result = send_mail(subject=mailing.letter.title,
                           message=mailing.letter.text,
                           from_email=EMAIL_HOST_USER,
                           recipient_list=[client.email for client in mailing.clients.all()])
        return result
    except Exception as ex:
        return 0


def send_active_mailings():
    for mailing in Mailing.objects.all():  # Для каждой рассылки из всех рассылок
        if mailing.status == 'started':  # Если она запущена
            if datetime.date.today() < mailing.finish_date:  # И если дата окончания находится в будущем
                if mailing.start_date < datetime.date.today():  # А дата начала - в прошлом
                    if datetime.datetime.now().time() > mailing.send_time:  # И время отправки уже настало
                        log = Log.objects.filter(mailing=mailing)  # Ищем логи от этой рассылки
                        if log.filter(result='success').exists():  # Если они есть и не все провальные
                            # То берём логи с успешным результатом, сортируем по убыванию и берем верхний в списке
                            last_success_log = log.filter(result='success').order_by('-last_try_dt').first()
                            # Из него узнаём дату с последней рассылки. Времени с последней рассылки прошло:
                            past_time = datetime.date.today().day - last_success_log.last_try_dt.replace(tzinfo=None).day
                            # И смотрим - если времени прошло больше чем частота рассылки
                            if past_time >= {'day': 1, 'week': 7, 'month': 30}.get(mailing.period):
                                print(111234567890)
                                # То отправляем письмо клиентам и сохраняем логи
                                result = send_mailing(mailing)
                                if result: mailing.sends += 1
                                mailing.save()
                                timezone = pytz.timezone('asia/ho_chi_minh')
                                log_time = datetime.datetime.now()
                                Log.objects.create(last_try_dt=datetime.datetime.now(),
                                                   result=['failed', 'success'][result],  # result может быть 0 или 1
                                                   mailing=mailing
                                                   )
                            else:  # Но по логам отправка в этом периоде уже была
                                continue
                        else:  # Если логов этой рассылки ещё нет - шлём письма и создаём первый лог
                            result = send_mailing(mailing)
                            if result: mailing.sends += 1
                            mailing.save()
                            Log.objects.create(last_try_dt=datetime.date.today(),
                                               result=['failed', 'success'][result],  # result может быть 0 или 1
                                               mailing=mailing)
                    else:  # Еще рано, время отправки не пришло, клиент спит
                        continue
                else:  # Дата начала в будущем - переходим к следующей рассылке
                    continue
            else:  # Если дата окончания рассылки уже прошла - переносим в завершённые
                mailing.status = 'ended'
                mailing.save()
        else:  # Рассылка не активна - переходим к следующей
            continue

            # The `close_old_connections` decorator ensures that database connections, that have become
            # unusable or are obsolete, are closed before and after your job has run. You should use it
            # to wrap any jobs that you schedule that access the Django database in any way.


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_active_mailings,
            trigger=CronTrigger(second="*/50"),  # Every 50 sec
            id="send_active_mailings",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

# Тот же скрипт, но с кучей комментариев, для отладки
# def send_active_mailings():
#     print('Запуск скрипта')
#     for mailing in Mailing.objects.all():  # Для каждой рассылки из всех рассылок
#         print('Проверяем рассылку ', mailing)
#         if mailing.status == 'started':  # Если она запущена
#             print('Рассылка ', mailing, ' имеет статус started')
#             if datetime.date.today() < mailing.finish_date:  # И если дата окончания находится в будущем
#                 print('Рассылка ', mailing, ' ещё не закончилась')
#                 if mailing.start_date < datetime.date.today():  # А дата начала - в прошлом
#                     print('Рассылка ', mailing, ' уже началась')
#                     if datetime.datetime.now().time() > mailing.send_time:  # И время отправки уже настало
#                         print(f'Рассылку {mailing} уже пора отправить: надо в {mailing.send_time}, а сейчас {datetime.datetime.now().time()}')
#                         log = Log.objects.filter(mailing=mailing)  # Ищем логи от этой рассылки
#                         print('Рассылка ', mailing, ' имеет логи:', log)
#                         if log.exists():  # Если они есть
#                             # То берём логи с успешным результатом, сортируем по убыванию и берем верхний в списке
#                             last_success_log = log.filter(result='success').order_by('-last_try_dt').first()
#                             print('Рассылка ', mailing, ' последний успешный лог:', last_success_log, 'его дата', last_success_log.last_try_dt)
#                             # Из него узнаём дату с последней рассылки. Времени с последней рассылки прошло:
#                             past_time = datetime.date.today().day - last_success_log.last_try_dt.replace(tzinfo=None).day
#                             print('Рассылка ', mailing, ' с последней рассылки прошло:', past_time, " из ", {'day': 1, 'week': 7, 'month': 30}.get(mailing.period))
#                             # И смотрим - если времени прошло больше чем частота рассылки
#                             if past_time >= {'day': 1, 'week': 7, 'month': 30}.get(mailing.period):
#                                 print(past_time, 'это больше чем ',
#                                       {'day': 1, 'week': 7, 'month': 30}.get(mailing.period), ' дней')
#                                 # То отправляем письмо клиентам и сохраняем логи
#                                 result = send_mailing(mailing)
#                                 if result: mailing.sends += 1
#                                 mailing.save()
#                                 print('Рассылка ', mailing, ' отправлена с результатом ', ['failed', 'success'][result])
#                                 timezone = pytz.timezone('asia/ho_chi_minh')
#                                 log_time = datetime.datetime.now()
#                                 print("Время лога: ", log_time)
#                                 Log.objects.create(last_try_dt=datetime.datetime.now(),
#                                                    result=['failed', 'success'][result],  # result может быть 0 или 1
#                                                    mailing=mailing
#
#                                                    )
#                                 print("Логи сохранены")
#                             else:  # Но по логам отправка в этом периоде уже была
#                                 print('Рассылка ', mailing, ' в этом периоде уже была')
#                                 continue
#                         else:  # Если логов этой рассылки ещё нет - шлём письма и создаём первый лог
#                             print('Рассылка ', mailing, ' делаем первую отправку')
#                             result = send_mailing(mailing)
#                             if result: mailing.sends += 1
#                             mailing.save()
#                             Log.objects.create(last_try_dt=datetime.date.today(),
#                                                result=['failed', 'success'][result],  # result может быть 0 или 1
#                                                mailing=mailing)
#                     else:  # Еще рано, время отправки не пришло, клиент спит
#                         print('Рассылка ', mailing, ' сегодня, но попозже')
#                         continue
#                 else:  # Дата начала в будущем - переходим к следующей рассылке
#                     print('Рассылка ', mailing, ' ещё не началась')
#                     continue
#             else:  # Если дата окончания рассылки уже прошла - переносим в завершённые
#                 print('Рассылка ', mailing, ' период рассылки закончен')
#                 mailing.status = 'ended'
#                 mailing.save()
#         else:  # Рассылка не активна - переходим к следующей
#             print('Рассылка ', mailing, ' не активна')
#             continue
