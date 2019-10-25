from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json

scheduleIds = {
    'cron-watcher': 'cron-watcher',
    'sunset-time': 'sunset-time',
    'custom-time': 'custom-time'
}

class Scheduler:
    def __init__(self, lampTrigger):
        self.url = 'https://api.sunrise-sunset.org/json?lat=51.751822&lng=19.425888&formatted=0'
        self.lamp = lampTrigger
        self.scheduler = BackgroundScheduler()
        self.sunsetModeActive = False
        self.customTimeActive = False
        self.sunsetTime = ""
        self.customTime = ""
        self.scheduler.add_job(self.setSunsetTime, 'cron', hour=23, minute=18, id=scheduleIds['cron-watcher'])
        self.scheduler.start()

    def setSunsetTime(self):
        date = requests.get(self.url).json()['results']['sunset']
        self.sunsetTime = date

    def scheduleAtTime(self, iso, id):
        date = None
        if id == scheduleIds['custom-time']:
            self.customTimeActive = True
            self.customTime = iso
            date = datetime.fromisoformat(iso)
        elif id == scheduleIds['sunset-time']:
            date = datetime.fromisoformat(iso[:-6]) + timedelta(hours=2)
        self.scheduler.add_job(self.lamp.on, 'date', run_date=date, id=id)

    def getStatuses(self):
        status = {
            'sunset': {
                'active': self.sunsetModeActive,
                'date': self.sunsetTime
            },
            'custom': {
                'active': self.customTimeActive,
                'date': self.customTime
            }
        }
        return status

    def toggleSunsetMode(self):
        self.sunsetModeActive = not self.sunsetModeActive
        if self.sunsetModeActive:
            self.scheduleAtTime(self.sunsetTime, scheduleIds['sunset-time'])
        else:
            self.removeJob(scheduleIds['sunset-time'])
        return self.sunsetModeActive

    def removeJob(self, id):
        if id == scheduleIds['custom-time']:
            self.customTimeActive = False
        try:
            self.scheduler.remove_job(id)
        except:
            return 'Error: no job'