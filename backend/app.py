from flask import Flask, request
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from LampTrigger import LampTrigger
from Scheduler import Scheduler, scheduleIds
import json

app = Flask(__name__)

PIN = 5

lamp = LampTrigger(PIN)
scheduler = Scheduler(lamp)

@app.route('/')
def status():
    return json.dumps(scheduler.getStatuses())

@app.route('/stop')
def stop():
    id = request.args.get('id')
    scheduler.removeJob(id)
    return '{} stopped'.format(id)

@app.route('/toggle')
def toggle():
    lamp.toggle()
    return json.dumps({'relayStatus': bool(lamp.getStatus())})

@app.route('/customTime', methods=['POST'])
def customTime():
    res = request.get_json()
    scheduler.scheduleAtTime(res['date'], scheduleIds['custom-time'])
    return 'timer set up'

@app.route('/sunset')
def sunset():
    return json.dumps({'sunset': bool(scheduler.toggleSunsetMode())})