from math import pi
from openrocketdoc import document


class Rocket(object):

    # Fixed parameters:
    prop_density = 1750  # kg/m3  Roughtly HTPB composite solid density
    LD = 10              # Motor length to width ratio
    Nose_LD = 5          # Nosecone length to width ratio

    def __init__(self, Isp, thrust, impulse, CD):
        """Take variables as input, build a rocket"""

        # Create an engine document
        engine = document.Engine('Motor')

        # Set our design
        engine.Isp = Isp
        engine.thrust_avg = thrust
        engine.I_total = impulse

        # volume of propellent needed
        prop_volume = engine.m_prop/self.prop_density

        # Solve for the radius/length of the fuel grain (assume solid, end burning)
        engine.diameter = 2 * (prop_volume / (2*self.LD*pi))**(1/3.0)
        engine.length = engine.diameter * self.LD

        # Add a nose
        nose = document.Nosecone(
            document.Noseshape.TANGENT_OGIVE,  # Shape
            1.0,  # shape_parameter
            3.5,  # mass
            engine.diameter * self.Nose_LD,  # Length
            diameter=engine.diameter,
        )

        # Payload section
        payload = document.Bodytube(
            "Payload",  # Name
            3.5,        # mass
            0.33,       # length, fixed
            diameter=engine.diameter,
        )

        # Body section the size of the engine
        body = document.Bodytube(
            "Body",  # Name
            20.0,     # mass
            engine.length,
            diameter=engine.diameter,
        )

        body.components = [engine]

        # Rocket:
        rocket = document.Rocket("Rocket")
        rocket.aero_properties['CD'] = CD
        stage0 = document.Stage("Sustainer")
        stage0.components = [nose, payload, body]
        rocket.stages = [stage0]

        self.rocket = rocket
