import os
import getpass
from crontab import CronTab, CronItem


def schedule_cron(command, interval, crontab=None):
    if not os.path.exists(crontab):
        with open(crontab, 'w'):
            pass

    if crontab:
        c = CronTab(tabfile=crontab)
    else:
        c = CronTab(user=getpass.getuser())

    job = CronItem.from_line(interval + ' ' + command, cron=c)

    c.append(job)
    c.write()
    return c, job


def unschedule_cron(command, crontab=None):
    if crontab:
        c = CronTab(tabfile=crontab)
    else:
        c = CronTab(user=getpass.getuser())

    for line in c.lines:
        if str(line) == command:
            line.delete()
            c.write()
            return True
    return False
