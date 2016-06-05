#!/usr/bin/env python
import manager
import rocket
import random

def gen():

    # starting values, real numbers for an N2501 motor
    isp     =   179    # s
    thrust  =  2510    # N
    impulse = 15280    # N*s
    CD      =     0.6

    # Randomize
    isp = random.gauss(isp, isp*0.03)                       # 3% spread
    thrust = random.gauss(thrust, thrust*0.10)              # 10% spread
    impulse = random.uniform(impulse - 200, impulse + 200)  # +/- 200 N*s
    cd_avg = random.gauss(0.6, 0.1)                         # ~16% spread

    r = rocket.Rocket(isp, thrust, impulse, [cd_avg])
    return r.rocket


number_of_sims = 4000
number_of_threads = 4

threads = []

for i in range(number_of_threads):
    thread = manager.JSBSimRunner(i, number_of_threads, gen)
    thread.run_times = int(number_of_sims / number_of_threads)
    threads.append(thread)

try:
    for thread in threads:
        print("Started Thread ", thread)
        thread.start()

    # Wait for everything to finish:
    for thread in threads:
        thread.join()
except (KeyboardInterrupt, SystemExit):
    for thread in threads:
        thread.stop()
