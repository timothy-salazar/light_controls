# Light Controls with a Raspberry Pi

My roommate and I have a game room, where we will play board games or tabletop roleplaying games when we have friends over. Especially in the context of tabletop RPGs it's nice to be able to control the atmosphere, and lighting is one of the most powerful tools you can use to create mood. I had recently bought a Raspberry Pi, and I was looking for a project, so I decided that it would be an interesting idea to set up a light control system using the Raspberry Pi. 

I purchased 10 meters worth of RGB LED strips to run along the ceiling, and another 5 meters to run underneath the table. They required 12V DC current at 72W per 5 meter length maximum. The power supply provided with the 10 meter length would output 12V at 5A:
```
Watts = Amps x Voltage 
Watts = 5A x 12V
60W
```
That's less than optimal - even for one LED strip - and that was reflected in the product reviews. But at $20 for 10 meters, the price was definitely right, so I purchased a separate 12V 10A power supply.
![alt-text](../images/light_control_setup.jpg,"Components for Light Control Project")
