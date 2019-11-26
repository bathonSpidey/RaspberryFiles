from gpiozero import LED
import time

led=LED(18)
#led.on()
#time.sleep(5)
#led.off()
led.blink(1,1,10)