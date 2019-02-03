from panel.beacon import XPlaneBeaconListener
from panel.xplane import XPlaneReceiver
from panel.max7219 import Lcd
from panel.display import Display
from panel.encoder import Encoder
from panel.keyboard import Keyboard




def onEncoderLeft():
	global freq
	freq = freq - 0.125
	if freq < 108.0:
		freq = 122.0
	print ("Left turn: New stby freq: %3.3f" % freq)

def onEncoderRight():
	global freq
	freq = freq + 0.125
	if freq > 122.0:
		freq = 108.0
	print ("Right turn: New stby freq: %3.3f" % freq)




print ("Setup display")
display = Display()

print ("Setup Keyboard")
keyboard = Keyboard( [0,5,6,13], [4,3,2,19])
keyboard.start()

print ("Setup encoder system")
freq = 108.0
encoder = Encoder(17, 27, 22)
encoder.registerLeftEvent(onEncoderLeft)
encoder.registerRightEvent(onEncoderRight)

print ("Staring Beacon-finder")
x = XPlaneBeaconListener()
(host, port) = x.listen()
print ("X-Plane deteced on %s" % host)

receiver = XPlaneReceiver(xp_host=host, xp_port=port, local_port=port)
receiver.start()
cont = True

while cont:
    try:
        cont = True
    except KeyboardInterrupt:
        print ("quitting...")
        cont = False

keyboard.stop()
x.stop()
receiver.stop()
print ("Waiting for thread termination")
#receiver.join()
print ("Thread terminated !")


