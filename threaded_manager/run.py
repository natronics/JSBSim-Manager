#!/usr/bin/env python
import manager
import rocket
from openrocketdoc import document

def gen():
    r = rocket.Rocket(200, 1200, 15000, [0.6])
    return r.rocket

thread = manager.JSBSimRunner(0, 1, gen)

try:
    thread.start()
    thread.join()
except (KeyboardInterrupt, SystemExit):
    thread.stop()
