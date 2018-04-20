from __future__ import division
from flask import Flask
from flask import render_template, request, redirect, url_for, Response, stream_with_context
import os
import time
from run_demo import run_demo, create_env, practice_run
from House3D import objrender, Environment, load_config, create_default_config


TEST_HOUSE = "02f594bb5d8c5871bde0d8c8db20125b"

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def demo_index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    env = create_env(house=TEST_HOUSE)
    return Response(run_demo(env),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
