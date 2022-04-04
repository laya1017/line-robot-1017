from apscheduler.schedulers.blocking import BlockingScheduler
import requests
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    r = requests.get("https://www.google.com/")
    for key in r.headers :
        print(key + ":" + r.headers[key])
sched.start()
