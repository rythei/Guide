import sys
sys.path.append('/home/rythei/guide/House3D')
import cv2
import numpy as np
from House3D import objrender, Environment, load_config, create_default_config
import pygame
from pygame.locals import *
import time
import matplotlib.pyplot as plt
from keyboard_listen import waitKey, waitJoystick
import h5py
from haptics import Cuffs
from collections import deque


HOUSES = ["00a42e8f3cb11489501cfeba86d6a297", "09160de615ffdd69d8a9662a46021d29", "0a96348d9c8acf673d3da07b6316e671", "0635535a9980bcd4a311464cad45fda5", "02f594bb5d8c5871bde0d8c8db20125b", "b5bd72478fce2a2dbd1beb1baca48abd", "02d83f79d7c3311ccc3395bbf2ea4ae4", "0762f81764e4fdd31a3410ebb89f59bc", "08f65a7829871e9399c38a261cdd8be0", "04667f43ca426693515b7da9befed6a0", "0a725e073c3a0fd0b0f5a4d126990fda", "04a6f8d6f031d39cd8f52743c08b5fb9", "09d26570eeb14c0976a32be3b243e40e", "08e89905e0a41614aa4f85109d362c1d", "0bda523d58df2ce52d0a1d90ba21f95c", "0b8755a7f00f2d47e246a6384b6c9b8e", "04af8d2c8883e26e9227e169f9a383f2", "0acf79836db830174c202d3a93a6b14a", "01a00a54b07c67729af0c4f5bdb91ccf", "0257400a5ae18e68196835f1e005740c", "03620d135a491a635c198e188e927ba0", "06840849cabbdc4bb9f3069242e1f587", "0b6d4fe900eaddd80aecf4bc79248dd9", "0017aeff679f53cd65edf72ef2349ff1", "0c05dbdef4ee21dc770e5be2f471dc35", "0642bcc7bd4c964830446b700ed4b5d5", "00cdcd4541a2145d004bbd45ee658f66", "09f8b9e6f42002c30d061c3f592d9685", "0acbb6234652a949f52e5b468289226c", "0a578e53e06ac0178bac608e74e51218", "066807814a14cf68d58a92792f162a9c", "03353fe273b81f93a11285c759e8a98b", "0c1f9e71298200e948bbee2d67faf578", "05e17d97e1be878ef08d963b5344b969", "09e46cb7bc972db216e7e5ba0ee4250f", "0b3ee5eefc0a664a153600f321a7b276", "023e21673caa7ac3f2808b498ab4cde8", "047dbcc70a693132ae860b9c73741483", "06f7826572be27f205e701783960416e", "072d8bce0ebe90d5c757ca280b633bd5", "09c1b600e4942ef3ba3ca6d940fa7a36", "034e4c22e506f89d668771831080b291", "0375e18d4664786745786988af6cfbf7", "09390811c51225aaced1ae50c6e6cecc", "035323ee3330e84be752322e598a24cc", "0267d23f3a3888693a11f33506e7f2d4", "092862153228f7466b1f911160e68c41", "09338eb45a9b1b09caeb317bb2b18baa", "0c13c5a3cee7ddc40201ab2e765c8dc7", "0a417c6459befd8a9fa4a5428f2de1e9"]
TEST_HOUSE = np.random.choice(HOUSES,1)[0]

def get_current_pos(map2d):
    ## this function gets the position of the user on the 2d-map
    #aaaaddddmap2d = np.ndarray(map2d)
    ix = np.where((map2d[:,:,0] == 255) & (map2d[:,:,1] == 50))# & (map2d[:,:,2] == 255))
    i = np.mean(ix[0])
    j = np.mean(ix[1])
    current_pos = (i,j)

    return current_pos

# get (x,y) point from pixel location (i,j)
def get_xy_from_pos(i,j,n_col):
    return j, n_col- i- 1


def load_field(field_file):
     h5f = h5py.File(field_file,'r')
     Xdir = h5f['Xdir'][:]
     Ydir = h5f['Ydir'][:]
     h5f.close()
     return Xdir, Ydir


def get_movement_vector(current_pos, Xdir, Ydir):
     ## this function needs to take the users current location and the pre-defined field
     ## and return the corresponding xdir and ydir vector values
     i,j = int(current_pos[0]),int(current_pos[1])
     print(Xdir[i,j])
     x = Xdir[i,j]
     y = Ydir[i,j]
     return x,y

def buzz_back(cuffs):
    cuffs.write_usb(7)
    time.sleep(.08)
    cuffs.write_usb(-1)

def buzz_rs(cuffs):
    cuffs.write_usb(2)
    time.sleep(.05)
    cuffs.write_usb(-1)

def buzz_ls(cuffs):
    cuffs.write_usb(5)
    time.sleep(.05)
    cuffs.write_usb(-1)

def excited_buzz(cuffs, success):
    if not success:
        cuffs.write_usb(7)
        time.sleep(10)
        cuffs.write_usb(-1)


def give_feedback(curr_vec, movement_vec, cuffs):
    ## given a vector output from the above functions, this needs to give a haptic feedback to the user
    ## maybe will need to take in additional arguments
    xm,ym = movement_vec[0],movement_vec[1]
    xc,yc = curr_vec[0],curr_vec[1]

    action = None
    if yc-ym > 0.8: #just set this as an arbitrary threshold.. should improve this
        if xc < 0:
            action = 'left'
        else:
            action = 'right'
    elif yc-ym < -0.8:
        if xc < 0:
            action = 'right'
        else:
            action = 'left'

    if action == 'left':
        print('MOVE LEFT!')
        cuffs.write_usb(2)
        time.sleep(.05)
        cuffs.write_usb(-1)
    elif action == 'right':
        print('MOVE RIGHT!')
        cuffs.write_usb(5)
        time.sleep(.05)
        cuffs.write_usb(-1)
    else:
        print('no feedback given')


def action_to_key(action):  ## convert a joystick action into a key action that we can pass to env.keyboard_control
    if action[0] <= -.8:
        return ord('m') #ord('a')
    elif action[0] >= .8:
        return ord('m') #ord('d')
    elif action[1] <= -.8:
        return ord('w')
    elif action[1] >= .8:
        return ord('s')
    elif action[2] <= -.8:
        return ord('h')
    elif action[2] >= .8:
        return ord('l')
    else:
        return ord('m') #nothing

def run_demo(env, field_file="02f594bb5d8c5871bde0d8c8db20125b-field_v2.h5"):
    Xdir, Ydir = load_field(field_file)
    cuffs = Cuffs()
    cuffs.connect_usb()
    t = 0
    needs_reset=True
    pygame.init()
    jstick = pygame.joystick.Joystick(0)
    pos_past = deque([])
    success = False
    curr_vec = (0,0)
    current_pos = (45.7,39.3)
    curr_yaw = 90 #always start at 90
    while True:
        if t%1000 == 0 and needs_reset:
            env.reset(x=45.3,y=39.3, yaw=90)
            needs_reset=False

        giveFeedback = True
        img = env.debug_render()

        map2d = env.gen_2dmap()

        n_col = map2d.shape[1]
        print('yaw:', env.get_yaw() % 360)

        try:
            prev_pos = current_pos
            current_pos = get_current_pos(map2d)

            if current_pos == prev_pos: #this means we've just rotated, haven't moved at all
                theta_d = env.get_yaw() - curr_yaw
                print('theta_d', theta_d)
                curr_yaw = env.get_yaw()
                ## need to use negate angle because left on coordinate system is
                xn = curr_vec[0]*np.cos(-theta_d) - curr_vec[1]*np.sin(-theta_d)
                yn = curr_vec[0]*np.sin(-theta_d) + curr_vec[1]*np.cos(-theta_d)
                curr_vec = (xn,yn)
            else:   #we've moved
                curr_yaw = env.get_yaw()  #360
                pos_past.append(current_pos)
                print('pos_past', pos_past)
                if len(pos_past)>4:
                    i0,j0 = pos_past[0][0], pos_past[0][1]
                    print('i0,j0',i0,j0)
                    i1,j1 = current_pos[0], current_pos[1]
                    pos_past.popleft()
                    #convert) to cartesian
                    x0,y0 = get_xy_from_pos(i0,j0,n_col)#j0, n_col- i0- 1
                    x1,y1 = get_xy_from_pos(i1,j1,n_col)#j1, n_col- i1- 1
                    dx,dy = x1-x0, y1-y0
                    if dx<0:
                        giveFeedback = False
                    #print('dx,dy',dx,dy)
                    norm = np.linalg.norm(np.array([dx,dy]),2)
                    if norm != 0:
                        curr_vec=(dx/norm,dy/norm)
                    else:
                        curr_vec = (dx,dy)
                #print('current_pos', current_pos)
            print('curr_vec', curr_vec)
            print('norm of curr_vec', np.linalg.norm([curr_vec[0],curr_vec[1]],2))
            print('current_pos', current_pos)
                #current_pos = get_current_pos(map2d)
            x,y = get_movement_vector(current_pos, Xdir, Ydir)
            movement_vec = (x,y)
                #print('movement vector',movement_vec)

            ### handle specific areas ###
            if giveFeedback:
                if current_pos[1] > 480 and current_pos[0] < 88:#made it to the kitchen for the first time this round
                    excited_buzz(cuffs, success)
                    success=True

                elif current_pos[1] > 469 and current_pos[0] > 126 and current_pos[0] < 153: #table
                    buzz_back(cuffs)

                elif current_pos[1] > 458 and current_pos[1] < 473 and current_pos[0] >92 and current_pos[0] < 102:#area just below the kitchen
                    buzz_ls(cuffs)

                elif current_pos[1] > 477 and current_pos[1] < 528 and current_pos[0] < 123:#area just below the kitchen
                    buzz_rs(cuffs)

                elif current_pos[0] > 122 and current_pos[1] > 455:
                    buzz_rs(cuffs)#give_feedback(curr_vec, (0,1), cuffs=cuffs)

                elif current_pos[1] > 343 and current_pos[1] < 437 and current_pos[0] > 94 and current_pos[0] < 107:#left hallway room
                    buzz_back(cuffs)

                elif current_pos[0] > 94 and current_pos[0] < 107 and current_pos[1] > 528 and current_pos[1]< 536:#weird corner
                    buzz_back(cuffs)


                else:
                    give_feedback(curr_vec, movement_vec, cuffs=cuffs)
        except:
            print('couldnt issue haptics')

        ret, jpeg = cv2.imencode('.jpg',img)
        frame = jpeg.tobytes()
        #rgb, depth, map2d = env.get_data()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        action, reset = waitJoystick(jstick)
        #print('action',action)
        key = action_to_key(action)

        if reset:
            env.reset(x=45.3,y=39.3, yaw=90)
            success = False
        #key = waitKey()
        #if key == 110: #pressing 'n' will reset the environment
        #    env.reset()

        if not env.keyboard_control(key):
            break

        t+=1

def practice_run(env):
        t = 0
        needs_reset=True
        pygame.init()
        jstick = pygame.joystick.Joystick(0)
        while True:
            if t%1000 == 0 and needs_reset:
                env.reset()
                needs_reset=False

            try:
                img = env.debug_render()
            except:
                print('render error')

            ret, jpeg = cv2.imencode('.jpg',img)
            frame = jpeg.tobytes()
            #rgb, depth, map2d = env.get_data()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            action, reset = waitJoystick(jstick)
            #print('action',action)
            key = action_to_key(action)

            if reset:
                env.reset()
            #key = waitKey()
            #if key == 110: #pressing 'n' will reset the environment
            #    env.reset()

            if not env.keyboard_control(key):
                break

            t+=1

def create_env(house="02f594bb5d8c5871bde0d8c8db20125b"):
    api = objrender.RenderAPI(w=600, h=450, device=0)
    cfg = create_default_config('/home/rythei/guide/SUNCG/house')

    if house is None:
        env = Environment(api, TEST_HOUSE, cfg)
    else:
        env = Environment(api, house, cfg)
    env.reset()

    return env


if __name__ == '__main__':
    pass
    #env=create_env()
    #run_demo(env, in_web=False)
    #house= "04a6f8d6f031d39cd8f52743c08b5fb9"
    #run_demo(house=TEST_HOUSE)
