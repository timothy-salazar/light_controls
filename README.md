# Light Controls with a Raspberry Pi

My roommate and I have a game room, where we will play board games or tabletop roleplaying games when we have friends over. Especially in the context of tabletop RPGs it's nice to be able to control the atmosphere, and lighting is one of the most powerful tools you can use to create mood. I had recently bought a Raspberry Pi, and I was looking for a project, so I decided to set up a light control system using the Raspberry Pi. 

## Materials
### Preliminary Work
I purchased 10 meters worth of RGB LED strips in two 5 meter rolls to run along the ceiling. They required 12V DC current at 72W per 5 meter length (maximum). The power supply provided with the 10 meter length would output 12V at 5A:
```
Watts = Amps x Voltage 
Watts = 5A x 12V
60W
```
That's less than optimal - even for one LED strip - and that was reflected in the product reviews. But at $20 for 10 meters, the price was definitely right. I purchased a separate 12V 10A power supply and used it to power the LEDs instead.

![alt-text](../master/images/led_strip_ceiling.jpg "Running the LED strips along the ceiling")

I ran the LED strips along the edge of the ceiling. To go around corners I cut them and used flexible strip connectors to link the segments together. Because of the way the LED strips are designed, the LEDs at the end of the strip would be less bright if I connected power to one end and ran it through the entire length of the strip, so I powered both 5 meter long sections in parallel.
### Connecting the Raspberry Pi
![alt-text](../master/images/light_control_setup.jpg "Components for Light Control Project")

Now to connect the LEDs to the Raspberry Pi. Our Raspberry Pi can interact with other devices through GPIO pins - or General Purpose In/Out pins. However, the voltage we're running through the LED strips is 12V 10A, whereas the Raspberry Pi GPIO voltage is 3.3V. That's more than enough to fry our Pi, so we need some way to let our Pi control the flow of current through the LEDs without ever being exposed to that voltage. 

The obvious choice is to use MOSFETs. Each MOSFET has a gate, source, and drain pin. To oversimplify a little, think of it as a faucet. Water (current) flows in through the source pin and out through the drain pin. The gate pin is the tap - by connecting one of our GPIO pins and applying a voltage we can turn the faucet on or off. It's not quite that simple, because when the faucet is 'half on' what we're actually doing is flipping the switch on and off very quickly - but it gets across the basic idea. 

![alt-text](../master/images/leds_with_mosfets.jpg "Hardware Setup")

The LED strip is attached to the 12V power supply, and the red, green, and blue wires - which correspond to the red, green, and blue ground connections - are each attached to the source pin of a MOSFET. Then the GPIO we have designated to control each color is attached to the respective gate pin, and the drain pins are then connected to ground. Now we have the hardware in place to control the flow of current from our power supply, through the LED strips, and down to ground for each color.

## Controlling GPIO with Raspberry Pi
![alt-text](../master/images/light_control_webpage.png "Light Control Webpage")
I chose to use the [Pigpio library for the Raspberry Pi](http://abyz.me.uk/rpi/pigpio/). This gives us the tools to control whether a pin is on or off, as well as PWM (pulse width modulation), which lets us control the 'amount' of red, green, and blue. It also has the pigpiod daemon, which lets us check that everything is working before we go any further. The daeomon can be started with:
```
sudo pigpiod
```

I assigned the blue LED to GPIO 26, so if at this point we wanted to check that it was functional, we could type:

```
pigs p 26 255
```
Note that PWM operates on a scale of 0-255, so the line above is telling our Raspberry Pi to power the blue LEDs with a 100% duty cycle. By using values between 0 and 255, we can provide more or less power to each color.

<img src="images/ceiling_blue_off.jpg" width=400><img src="images/ceiling_blue_on.jpg" width=400>

Within Python code, it would look something like this:

```python
import pigpio

pi1 = pigpio.pi() # pi1 accesses local GPIO
pi1.set_mode(26,pigpio.OUTPUT)  # sets this GPIO pin as output. Not necessary, but 
                                # used in the documentation, seems like best practices
pi1.set_PWM_dutycycle(26,255) # set pin 26 to 100% duty cycle
```
Once we have those basics down, the rest is pretty straightforward. [Here's a jupyter notebook with some sample code to play around with](../master/src/sample_pigpio.ipynb)


## Works Cited







