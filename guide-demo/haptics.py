import serial
import socket
import time
import os.path
import sys
sys.path.append('/home/luminosity/guide/House3D')

BAUD_RATE = 9600

class Cuffs:

    def __init__(self,usb_port_l = '/dev/ttyUSB0',usb_port_r = '/dev/ttyUSB1'):

        self.usb_port_l = usb_port_l
        self.usb_port_r = usb_port_r

    def connect_usb(self):

        while True:
            try:
                print("Attempting to connect left usb to {} and right usb to {}".format(self.usb_port_l,self.usb_port_r))
                self.usb_l = serial.Serial(self.usb_port_l, BAUD_RATE)
                self.usb_r = serial.Serial(self.usb_port_r, BAUD_RATE)
                self.usb_l.close()
                self.usb_r.close()
                time.sleep(2)
                self.usb_l.open()
                self.usb_r.open()
                time.sleep(2)
                print("Connected!")
                break
            except serial.SerialException:
                print("[ERROR] Could not connect to requested port.")
                time.sleep(1)

    def write_usb(self,c):

        l = -1
        r = -1
        if (c < 4):
            l = c
            r = -1
        else:
            r = c-3
            l = -1
        if (c == 7):
            l = 1
            r = 1

        left_message = ';'+str(l)+':'
        right_message = ';'+str(r)+':'
        # Send information over USB.
        self.usb_l.flush()
        self.usb_l.write(left_message)
        print("left Message   ", left_message)
        self.usb_l.flush()

        self.usb_r.flush()
        self.usb_r.write(right_message)
        print("Right Message   ", right_message)
        self.usb_r.flush()



if __name__ == '__main__':

    # Establish USB connection
    a = Cuffs()
    a.connect_usb()


    while True:
        # messag = ';HI:'
        a.write_usb(7)
        print("Wrote")
        time.sleep(10)
        a.write_usb(1)
        print("Wrote")
        time.sleep(10)
        a.write_usb(2)
        print("Wrote")
        time.sleep(10)
        a.write_usb(3)
        print("Wrote")
        time.sleep(10)
        a.write_usb(4)
        print("Wrote")
        time.sleep(10)
        a.write_usb(5)
        print("Wrote")
        time.sleep(10)
        a.write_usb(6)
        print("Wrote")
        time.sleep(10)
        a.write_usb(-1)
        print("Wrote Final")
        time.sleep(10)
