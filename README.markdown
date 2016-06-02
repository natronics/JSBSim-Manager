
# Build A Rocket And Launch It

Proceduarlly build and sim a flight. This is my attempt to use the [open aerospace rocket documentation tool](https://open-aerospace.github.io/openrocketdoc/) to describe a rocket and generate JSBSim configuration to simulate its flight.

## Design Engine

Pick an engine design. Well define it based on a desired Isp, thrust, and burn time.



Design parameters:

      Input     |   Number  | Units 
 -------------- | --------: | :---- 
            Isp |     214.0 | s
         Thrust |   1,255.0 | N
      Burn Time |      12.0 | s





Our computed engine will need 7.2 kg of propellent.
It has a total impulse of 15,060 Ns. That would make it a ''(%) class motor.

Generated JSBSim engine document:

```
<?xml version="1.0" ?>
<rocket_engine name="Engine">
  <isp>214.0</isp>
  <builduptime>0.1</builduptime>
  <thrust_table name="propulsion/thrust_prop_remain" type="internal">
    <tableData>
 0.000 282.135
 5.274 282.135
 10.547 282.135
    </tableData>
  </thrust_table>
</rocket_engine>
 ```


## Build Rocket

Now we know how much propellent, guess the density and come up with some parametric rocket design.



Generated JSBSim 'Aircraft' document:

```
<?xml version="1.0" ?>
<fdm_config name="Rocket" release="ALPHA" version="2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://jsbsim.sourceforge.net/JSBSim.xsd">
  <fileheader/>
  <metrics>
    <wingarea unit="M2">0.0</wingarea>
    <wingspan unit="M">0.0</wingspan>
    <chord unit="M">0.0</chord>
    <htailarea unit="M2">0.0</htailarea>
    <htailarm unit="M">0.0</htailarm>
    <vtailarea unit="M2">0.0</vtailarea>
    <vtailarm unit="M">0.0</vtailarm>
    <location name="AERORP" unit="M">
      <x>0.0</x>
      <y>0.0</y>
      <z>0.0</z>
    </location>
  </metrics>
  <mass_balance>
    <pointmass name="Body">
      <form shape="tube">
        <radius unit="M">0.0000</radius>
        <length unit="M">0.8052</length>
      </form>
      <weight unit="KG">1.5000</weight>
      <location unit="M">
        <x>0.4026</x>
        <y>0.0</y>
        <z>0.0</z>
      </location>
    </pointmass>
  </mass_balance>
  <propulsion/>
  <aerodynamics/>
  <ground_reactions/>
  <system/>
</fdm_config>

```



