
# Build A Rocket And Launch It

Procedurally build and simulate a flight. This is my attempt to use the [open aerospace rocket documentation tool](https://open-aerospace.github.io/openrocketdoc/) to describe a rocket and generate JSBSim configuration to simulate its flight.

View the raw jupyter notebook: [rocket.ipynb](https://github.com/natronics/JSBSim-Manager/blob/master/rocket.ipynb)

You can run it yourself by cloning this repo and install requirements:

    $ pip install -r requirements.txt

Then run jupyter to edit/run the document in your browser:

    $ jupyter notebook

The idea is that you can make up some numbers ("what if I built a rocket with _this_ much thrust?") and this script will parametrically design an entire rocket. Then using openrocketdoc, generate a valid JSBSim case and run JSBSim for you, generating flight simulation output.

Just put in numbers for the engine design and then run the notebook!


## Step 1. Design The Engine

Pick an engine design. Well define it based on a desired Isp, thrust, and burn time.



Engine Design parameters:

      Input     |   Number  | Units 
 -------------- | --------: | :---- 
            Isp |     214.0 | s
         Thrust |   1,555.0 | N
      Burn Time |      10.0 | s


All we need to do is create an openrocketdoc Engine with those basic numbers:

```python
from openrocketdoc import document

engine = document.Engine('My Rocket Motor')
engine.Isp = 214.0
engine.thrust_avg = 1555.0
engine.t_burn = 10.0
```

Everything else can be computed from that engine class:




Our computed engine will need 7.4 kg of propellent.
It has a total impulse of 15,550 Ns. That would make it a 'N'(52%) class motor.

Generated JSBSim engine document:

```xml
<?xml version="1.0" ?>
<rocket_engine name="Python Motor">
  <isp>214.0</isp>
  <builduptime>0.1</builduptime>
  <thrust_table name="propulsion/thrust_prop_remain" type="internal">
    <tableData>
      0.000 349.578
      5.445 349.578
      10.890 349.578
    </tableData>
  </thrust_table>
</rocket_engine>

```


## Step 2. Build The Rocket

Now we know how much propellent, guess the density and come up with some parametric rocket design. If we compute some numbers based on a guess of the density of our propellent, we can build up a full rocket desgin from our `engine`. The only hardcoded magic is a prefered lenght-to-diameter ratio.



Rocket Design parameters:

          Input         |   Number  | Units 
 ---------------------- | --------: | :---- 
     Propellent Density |   1,555.0 | kg/m3
        Motor L/D ratio |      10.0 | 
     Nosecone L/D ratio |       5.0 | 




Computed rocket length: 1.6 meters, diameter: 81.39 mm

Generated diagram of the rocket, with a nosecone, fixed length dummy payload section, and motor:



![](https://rawgit.com/natronics/JSBSim-Manager/master/rocket_files/rocket_6_1.svg)




Generated JSBSim 'Aircraft' document:

```xml
<?xml version="1.0" ?>
<fdm_config name="Rocket" release="ALPHA" version="2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://jsbsim.sourceforge.net/JSBSim.xsd">
  <fileheader/>
  <!--

  Primary Metrics (Ovearall size of vehicle)

  -->
  <metrics>
    <wingarea unit="M2">0.0052</wingarea>
    <wingspan unit="M">0.0814</wingspan>
    <chord unit="M">0.0</chord>
    <htailarea unit="M2">0.0</htailarea>
    <htailarm unit="M">0.0</htailarm>
    <vtailarea unit="M2">0.0</vtailarea>
    <vtailarm unit="M">0.0</vtailarm>
    <location name="AERORP" unit="M">
      <x>1.5508</x>
      <y>0.0</y>
      <z>0.0</z>
    </location>
  </metrics>
  <!--

  Mass Elements: describe dry mass of vehicle

  -->
  <mass_balance>
    <pointmass name="Payload">
      <form shape="tube">
        <radius unit="M">0.0407</radius>
        <length unit="M">0.3300</length>
      </form>
      <weight unit="KG">2.5000</weight>
      <location unit="M">
        <x>0.5719</x>
        <y>0.0</y>
        <z>0.0</z>
      </location>
    </pointmass>
    <pointmass name="Body">
      <form shape="tube">
        <radius unit="M">0.0407</radius>
        <length unit="M">0.8139</length>
      </form>
      <weight unit="KG">1.5000</weight>
      <location unit="M">
        <x>1.1439</x>
        <y>0.0</y>
        <z>0.0</z>
      </location>
    </pointmass>
  </mass_balance>
  <!--

  Propulsion: describe tanks, fuel and link to engine def files

  -->
  <propulsion>
    <tank type="FUEL">
      <location unit="M">
        <x>1.1439</x>
        <y>0.0</y>
        <z>0.0</z>
      </location>
      <radius unit="M">0.0407</radius>
      <grain_config type="CYLINDRICAL">
        <length unit="M">0.8139</length>
        <bore_diameter unit="M">0</bore_diameter>
      </grain_config>
      <capacity unit="KG">7.4096</capacity>
      <contents unit="KG">7.4096</contents>
    </tank>
    <engine file="python-motor">
      <feed>0</feed>
      <location unit="M">
        <x>0.7369</x>
        <y>0.0</y>
        <z>0.0</z>
      </location>
      <thruster file="python-motor_nozzle">
        <location unit="M">
          <x>1.5508</x>
          <y>0.0</y>
          <z>0.0</z>
        </location>
      </thruster>
    </engine>
  </propulsion>
  <!--

  Aerodynamics

  -->
  <aerodynamics>
    <axis name="DRAG">
      <function name="aero/force/drag">
        <description>Coefficient of Drag</description>
        <product>
          <property>aero/qbar-psf</property>
          <property>metrics/Sw-sqft</property>
          <value>0.600000</value>
        </product>
      </function>
    </axis>
  </aerodynamics>
  <!--
  Ground reactions and systems are not auto-generated.
  -->
  <ground_reactions/>
  <system/>
</fdm_config>

```


## Build JSBSim Case

JSBSim needs several files in directories with a particular file structure. We simply write the files above to the filesystem appropriate places. A generic `run.xml` and `init.xml` files are already here. They're almost completely independent from the rocket definitions, the only thing "hard coded" is the name of the rocket (which has to match the filename).



## Run JSBSim

Now we can simulate the flight by invoking JSBSim (assuming you have it installed and in your path). It's as easy as this:

```python
import subprocess
# Run JSBSim using Popen
p = subprocess.Popen(["JSBSim", "--logdirectivefile=output_file.xml", "--script=run.xml"])
```



## Analyze The Simulation Results

Now we should have a datafile from the simulation!



The apogee (maximum altitude) of this flight was 17.8 km above sea level





![](rocket_files/rocket_14_0.png)





![](rocket_files/rocket_15_0.png)



