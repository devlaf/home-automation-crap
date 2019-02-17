#!/usr/bin/env python

import sys
import os
from crontab import CronTab
from twisted.internet.defer import succeed
from twisted.web.static import File
from klein import run, route

cron = CronTab(user='devin')

def set_alarm(hour, minute):
    remove_existing()
    
    job = cron.new(command=os.path.dirname(os.path.realpath(__file__)) + '/alarm.sh')
    job.hour.on(hour)
    job.minute.on(minute)
    job.enable()
    cron.write()

def remove_existing():
    for entry in cron.find_command('alarm.sh'):
        cron.remove(entry)

@route('/alarm', methods=['POST'])
def setname(request):
    hour = request.args.get(b'hour', [b''])[0].decode("utf8")
    minute = request.args.get(b'minute', [b''])[0].decode("utf8")
    set_alarm(hour, minute)
    return succeed(None)

@route('/', branch=True)
def home(request):
  return File('./')

run('0.0.0.0', 80)
