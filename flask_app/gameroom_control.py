from flask import Flask, request, session, g, url_for, \
render_template, flash
import RPi.GPIO as GPIO
import pigpio
import numpy as np
from light_control.transmitRF import transmit_outlet

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
pi1 = pigpio.pi()

@app.route('/outlet',methods=['POST'])
def outlet():
    for i in request.form.items():
        trans_code = '{}_{}'.format(i[0],i[1].lower())
        transmit_outlet(trans_code)
    return render_template('light_adjust.html',outlet_vals = 'outlet_two')

@app.route('/', methods=['GET','POST'])
def light_controls():
    r = 0
    g = 0
    b = 0
    if request.method == 'POST':
        try:
            new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
            new_colors = new_colors.astype('int')
            assert (np.all(new_colors<256) and np.all(new_colors>=0))
            radio = request.form['mode']
            if (radio=='ceiling') or (radio=='both'):
                pi1.set_PWM_dutycycle(5,new_colors[0])
                pi1.set_PWM_dutycycle(13,new_colors[1])
                pi1.set_PWM_dutycycle(26,new_colors[2])
                r = pi1.get_PWM_dutycycle(5)
                g = pi1.get_PWM_dutycycle(13)
                b = pi1.get_PWM_dutycycle(26)
            if (radio=='table') or (radio=='both'):
                pi1.set_PWM_dutycycle(17,new_colors[0])
                pi1.set_PWM_dutycycle(22,new_colors[1])
                pi1.set_PWM_dutycycle(18,new_colors[2])
                r = pi1.get_PWM_dutycycle(17)
                g = pi1.get_PWM_dutycycle(22)
                b = pi1.get_PWM_dutycycle(26)
        except (ValueError,AssertionError):
            flash('You need to type a value between 0 and 255 for all boxes')
    return render_template('light_adjust.html',r_value=r,g_value=g,b_value=b)
