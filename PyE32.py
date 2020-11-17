import serial
import RPi.GPIO as GPIO

DEFAULT_INTERFACE = "/dev/serial0"
DEFAULT_M0_PIN = 23
DEFAULT_M1_PIN = 24
DEFAULT_AUX_PIN = 18
MODE_NORMAL = 1
MODE_WAKE_UP = 2
MODE_POWERSAVE = 3
MODE_PROG_SLEEP = 4

class   e32ttl(object):
    interface = DEFAULT_INTERFACE
    m0_pin = DEFAULT_M0_PIN
    m1_pin = DEFAULT_M1_PIN
    aux_pin = DEFAULT_AUX_PIN
    baudrate = 9600
    bytesize = serial.EIGHTBITS
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    serial_object = None

    def __init__(self, interface, m0_pin, m1_pin, aux_pin, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE):
        self.interface = interface
        self.m0_pin = m0_pin
        self.m1_pin = m1_pin
        self.aux_pin = aux_pin
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.m0_pin, GPIO.OUT)
        GPIO.setup(self.m1_pin, GPIO.OUT)
        GPIO.setup(self.aux_pin, GPIO.IN)

        try:
            self.serial_object = serial.Serial(
                interface=self.interface,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                parity=self.parity,
                stopbits=self.stopbits
            )
        except:
            print("Error in opening serial interface, check parameters.")
        
        self.setMode(MODE_NORMAL)
        
    def setMode(self, mode):
        if self.serial_object == None:
            print("Interface is not initialised.")
            return 1
        if mode == MODE_NORMAL:
            GPIO.output(self.m0_pin, GPIO.LOW)
            GPIO.output(self.m1_pin, GPIO.LOW)
            return 0
        elif mode == MODE_WAKE_UP:
            GPIO.output(self.m0_pin, GPIO.HIGH)
            GPIO.output(self.m1_pin, GPIO.LOW)
            return 0
        elif mode == MODE_POWERSAVE:
            GPIO.output(self.m0_pin, GPIO.LOW)
            GPIO.output(self.m1_pin, GPIO.HIGH)
            return 0
        elif mode == MODE_PROG_SLEEP:
            GPIO.output(self.m0_pin, GPIO.HIGH)
            GPIO.output(self.m1_pin, GPIO.HIGH)
            return 0

    def receiveMessage(self):
        if self.serial_object == None:
            print("Interface is not initialised.")
            return 1
        recv = self.serial_object.read()
        recv += self.serial_object.read(self.serial_object.in_waiting)
        return recv.decode('utf-8')

    def sendMessage(self, msg):
        if self.serial_object == None:
            print("Interface is not initialised.")
            return 1
        print('todo')

