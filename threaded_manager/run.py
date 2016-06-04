#!/usr/bin/env python
import manager
import rocket


def gen():
    r = rocket.Rocket(200, 1200, 15000, [0.6])
    return r.rocket

thread = manager.JSBSimRunner(0, 1, gen)
thread.run_times = 10

try:
    thread.start()
    thread.join()
except (KeyboardInterrupt, SystemExit):
    thread.stop()
