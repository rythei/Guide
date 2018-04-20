from pynput import keyboard
import pygame
import numpy as np
import time

def get(j):
    j.init()
    out = [0]*j.get_numaxes()#,0,0,0,0,0,0,0,0,0,0,0,0]
    reset = False
    it = 0 #iterator
    pygame.event.pump()
    #Read input from the two joysticks

    for i in range(0, j.get_numaxes()):
        out[i] = j.get_axis(i)

    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
         if j.get_button(i) != 0:
             reset = True
    #    it+=1
    return out, reset

def waitJoystick(j):
    j.init()
    caught = False
    while not caught:
        time.sleep(.01)
        out,reset = get(j)
        if np.sum(out) != 0 or reset:
            caught=True
            return out, reset


def waitKey():
    a = []
    def on_press(key):
        a.append(key)
        return False

    def on_release(key):
        pass

    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()

    try:
        return ord(a[0].char)
    except:
        return 0


if __name__=='__main__':
    pygame.init()
    j = pygame.joystick.Joystick(0)

    out = waitJoystick(j)
    print(out)
