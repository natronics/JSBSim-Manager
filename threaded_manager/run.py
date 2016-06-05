#!/usr/bin/env python
import manager
import rocket


def gen():
    r = rocket.Rocket(200, 1200, 15000, [0.6])
    return r.rocket


number_of_sims = 30
number_of_threads = 3

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
