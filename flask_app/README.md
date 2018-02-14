# Making a Flask Light Control Web App

### First of all, don't get discouraged!

I'm about to go through the process of making a Flask app in just a page or so. If you're new to this, don't get discouraged! It took me a while to work my way to this solution. I used a lot of different resources, including some how-to guides I have listed in the works cited section at the end. Flask looked like gibberish the first time I went through the documentation, so you aren't alone. Remember: in programming you can do anything as long as you're willing to fail a lot, fight your way through the documentation, and you're not too proud to consult very basic-level resources if you need them.

### File Structure

<p align="center">
  <img src="images/file_structure.png" alt="Screenshot of Directories">
</p>

First some bookkeeping. If we want to make a Flask application, we're going to want a particular file structure. The application here is called 'light_controls,' so we have a directory called 'light_controls' which contains two subdirectories called 'templates' and 'static.' Templates contains the html templates for the webpages we're going to be displaying, and static will contain the 'Cascading Style Sheet' or CSS. I'll go into what that means in more detail later. The MANIFEST.in, setup.py, and __init__.py files are there so that we can install 'light_controls' as a package. I'll also go more in depth on these later.

### light_control.py

I've copied the entire python code for this down below. It's only about 30 lines long, and it could have been shorter if I wasn't focusing on readability. 

So what's going on here? 

'''python
from flask import Flask, request, session, g, url_for, \
render_template, flash
import pigpio
import numpy as np
from light_controls.transmitRF import transmit_outlet

# This is all boilerplate 
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) 
app.config.from_envvar('LIGHT_CONTROLS_SETTINGS', silent=True) # have the name of your app here, if different

pi1 = pigpio.pi() # This gives us access to the local GPIO
red_pin = 5       # <- the GPIO pins we're using. 
green_pin = 13    # replace with yours if different.
blue_pin = 26

@app.route('/', methods=['GET','POST']) # '/' is going to appear at the end of the url - so this is our
                                        # default landing page. 'GET' means we're letting it retrieve and 
                                        # display the page, 'POST' means we're letting the page update
                                        # information - i.e., the user tells us what color they want
def light_controls():
    if request.method == 'POST':  # this only executes if we're 'POST'ing something. This is the case
                                  # the user submits the form in our html document (chooses a color and
                                  # hits 'submit'). Otherwise it skips to the end.
        
        # This try/except clause shouldn't be necessary. I built it in while I was piecing this web
        # app together - using a manual, 'type in three numbers' mode of color entry. I decided to leave
        # it in, in case you're tinkering as well.
        try:
            # This is using the 'request' function from Flask to retrieve the values the user
            # selected. We then make sure they're the right type, check to see that they fall into the 
            # acceptable range (0-255), and - if everything checks out - the GPIO pins are told to 
            # take on the PWM values the user submitted. 
            new_colors = np.array([request.form['red'],request.form['green'],request.form['blue']])
            new_colors = new_colors.astype('int') # make the values all ints
            assert (np.all(new_colors<256) and np.all(new_colors>=0)) # Are all the values 0-255?
            pi1.set_PWM_dutycycle(red_pin,new_colors[0])  # set new PWM dutycycles
            pi1.set_PWM_dutycycle(green_pin,new_colors[1])
            pi1.set_PWM_dutycycle(blue_pin,new_colors[2])
        except (ValueError,AssertionError):
            flash('Invalid Input')
    return render_template('light_adjust.html') # This tells Flask to take the light_adjust.html document
                                                # from our templates folder and render it. 

'''

To summarize:

This is a VERY basic web app. It's going to have one page, with the option to adjust the red, green, and blue value of one set of LEDs. When the webpage is called with a GET request, light_controls() skips to the end and renders the page from an HTML document. When it's called with a POST request, which happens when the user submits a form, light_controls() will adjust the LEDs and then render the page.

### layout.html

Oh boy. HTML isn't my strongest suit, but I'll try to explain the important parts. 
First of all:

[Here is a link to w3schools](https://www.w3schools.com/html/default.asp) excellent HTML tuturials. They do a much better job of explaining what's going on than I will. An absolute lifesaver.

[A link to the 'Flaskr' app](http://flask.pocoo.org/docs/0.12/tutorial/introduction/) which is a simple twitter clone implimented in Flask. I consulted this a LOT as I was working my way through the basics of FLASK and HTML. 


