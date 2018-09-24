import RPi.GPIO as GPIO
import time

RCLK  = 11
SRCLK = 12
SDI   = 13

tab = [0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f]

data = [
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, #NULL
		0x00,0x00,0x3C,0x42,0x42,0x3C,0x00,0x00, #0
		0x00,0x00,0x00,0x44,0x7E,0x40,0x00,0x00, #1
		0x00,0x00,0x44,0x62,0x52,0x4C,0x00,0x00, #2
		0x00,0x00,0x78,0x14,0x12,0x14,0x78,0x00, #A
		0x00,0x00,0x60,0x90,0x90,0xFE,0x00,0x00, #d
		0x00,0x00,0x1C,0x2A,0x2A,0x2A,0x24,0x00, #e
		0x00,0x00,0x1C,0x2A,0x2A,0x2A,0x24,0x00, #e
		0x00,0x00,0x7E,0x12,0x12,0x0C,0x00,0x00, #p
		0x00,0x00,0x08,0x7E,0x88,0x40,0x00,0x00, #t
		0x3C,0x42,0x95,0xB1,0xB1,0x95,0x42,0x3C, #:)
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00  #NULL
		]

def print_msg():
	print ('Program is running...')
	print ('Press Ctrl+C to end the program...')

def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def hc595_in(dat):
	for bit in range(0, 8):	
		GPIO.output(SDI, 0x80 & (dat << bit))
		GPIO.output(SRCLK, GPIO.HIGH)
		GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
	GPIO.output(RCLK, GPIO.HIGH)
	GPIO.output(RCLK, GPIO.LOW)

def loop():
	for i in range(0, 96-8):
		for k in range(0, 15):
			for j in range(0, 8):
				hc595_in(data[i+j])
				hc595_in(tab[j])
				hc595_out()
				time.sleep(0.002)
	

def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == ('__main__'):   # Program starting from here 
	print_msg()
	setup() 
	try:
		loop()  
	except KeyboardInterrupt:  
		destroy()  
