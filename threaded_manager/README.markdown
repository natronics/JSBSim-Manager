
# Monte Carlo

Another attempt at a monte carlo analysis, this time with LV2-like numbers.

This directory has an attempt at a managing JSBSim sessions that can spin up multiple threads to run simulations in parallel. It also kills the sim at apogee, whenever that may be. The upshot is that I can run many more simulations per minute than the naive approach.

This setup:

```python
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
```




Ran 4000 indapendent simulations in 12.8 miuntes.
That's about 0.18 seconds per simulation.




Highest sim went to:          10.3 km

Lowest sim went to:            6.8 km

The mean sim altitude was:     8.1 km

The median sim altitude was:   8.1 km






![](analysis_files/analysis_3_0.png)





![](analysis_files/analysis_4_0.png)





![](analysis_files/analysis_5_0.png)





![](analysis_files/analysis_6_0.png)



