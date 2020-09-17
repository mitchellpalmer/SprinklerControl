import os
import RPi.GPIO as GPIO
import base64
import json
import pretty_cron
from flask import *
from crontab import CronTab

app = Flask(__name__)

mapIDtoWiringPi = [-1, 4, 5, 6, 27, 0, 2, 3, 21]
mapIDtoBCM = [-1, 23, 24, 25, 16, 17, 27, 22, 5]

my_cron = CronTab(user='pi')

GPIO.setmode(GPIO.BCM)

def find_sprinkler_status(id):
    GPIO.setup(mapIDtoBCM[id], GPIO.OUT)
    return bool(GPIO.input(mapIDtoBCM[id]))

def get_scheduled_runs():
    for i, run in enumerate(my_cron.find_comment('SPRINKLER')):
        yield {
            "id":i,
            "sched":pretty_cron.prettify_cron(str(run).split("python")[0].rstrip()),
            "sprinkler":int(run.command.split(" ")[2]),
            "time":float(run.command.split(" ")[3])
        }

@app.route('/')
def welcome_to_soak():
    return render_template("app.html", sprinkler = [find_sprinkler_status(i) for i in xrange(1,9)], runs = get_scheduled_runs(), skey=['Lawn', 'Lawn', 'Lawn', 'Front Drive', 'Back Drive', 'Road Garden', 'Back Fence', '~'])

@app.route('/create/<schedule>')
def create_run(schedule):
    schedule = json.loads(base64.b64decode(schedule))
    job = my_cron.new(command='python /home/pi/SprinklerApp/sprinkle.py {0} {1}'.format(str(schedule["sprinkler"]), str(schedule["run-time"])), comment='SPRINKLER')
    job.setall(schedule["cron"])
    job.enable()
    my_cron.write()
    return redirect("/")


@app.route('/on/<int:id>')
def turn_on(id):
    os.system("gpio mode {0} out".format(str(mapIDtoWiringPi[id])))  
    os.system("gpio write {0} 1".format(str(mapIDtoWiringPi[id])))  
    return redirect("/")

@app.route('/off/<int:id>')
def turn_off(id):
    os.system("gpio mode {0} out".format(str(mapIDtoWiringPi[id])))  
    os.system("gpio write {0} 0".format(str(mapIDtoWiringPi[id])))  
    return redirect("/")

@app.route('/delete_all/')
def delete_all():
    my_cron.remove_all(comment='SPRINKLER')
    my_cron.write()
    return redirect("/")    

@app.route('/delete/<id>')
def delete(id):
    
    for i, x in enumerate(my_cron.find_comment('SPRINKLER')):
        if i == id:
            toDelete = x
            break
        
    my_cron.remove(x)
    my_cron.write()
    return redirect("/")  

@app.route('/ati.png')
def icon():
    return send_file("templates/SprinklerControl.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
