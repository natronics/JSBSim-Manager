import threading
import subprocess
import time
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from openrocketdoc import document
from openrocketdoc import writers


class JSBSimRunner(threading.Thread):
    """A class to build and run a JSBSim case in a thread. Init as many
    instances of this class as you want threads to run parallel cases.

    :param int thread_id: Which thread this is
    :param int n_treads: Total number of threads expected to run
    :param callback rocket_gen: A callback that returns a rocket document
    """

    def __init__(self, thread_id, n_threads, rocket_gen):
        super(JSBSimRunner, self).__init__()
        self._stop_event = threading.Event()
        self.daemon = True

        self.thread_id = thread_id
        self.n_threads = n_threads
        self.thread_path = "thread_%d" % self.thread_id

        self.make_rocket = rocket_gen

    def run(self):
        # generate first case:
        rocket = self.make_rocket()

        # Build file structure:
        self.setup_case_path(rocket)

        # Go to there
        os.chdir(self.thread_path)

        # Run N number of times
        for i in range(1):

            # kill thread
            if self._stop_event.is_set():
                break

            # Generate a new rocket
            rocket = self.make_rocket()

            # Write the rocket casefiles
            self.write_case(rocket)

            # Setup output file
            self.write_case_output(i)

            # Run!
            p = subprocess.Popen(["JSBSim", "--logdirectivefile=output.xml", "--script=run.xml"])
            time.sleep(5)

    def stop(self):
        self._stop_event.set()

    def write_case_output(self, num):

        output_file = ET.Element('output')
        output_file.attrib['name'] = "../data/sim-%05d.csv" % ((num * self.n_threads) + self.thread_id)
        output_file.attrib['type'] = "CSV"
        output_file.attrib['rate'] = "10"

        alt = ET.SubElement(output_file, 'property')
        alt.attrib['caption'] = "Altitude MSL [m]"
        alt.text = "position/h-sl-meters"
        vel = ET.SubElement(output_file, 'property')
        vel.attrib['caption'] = "Velocity Down [fps]"
        vel.text = "velocities/v-down-fps"
        thrust = ET.SubElement(output_file, 'property')
        thrust.attrib['caption'] = "Thrust [lbf]"
        thrust.text = "forces/fbx-prop-lbs"

        xmldoc = minidom.parseString(ET.tostring(output_file, encoding="UTF-8"))
        with open("output.xml", 'w') as outfile:
            outfile.write(xmldoc.toprettyxml(indent="  "))

    def write_case(self, rocket):

        # Write aircraft
        with open(os.path.join("aircraft", rocket.name_slug, rocket.name_slug + ".xml"), 'w') as airfile:
            airfile.write(writers.JSBSimAircraft.dump(rocket))

        # Write init conditions
        init_file = ET.Element('initialize')
        init_file.attrib['name'] = "Initial Conditions"

        ubody = ET.SubElement(init_file, 'ubody')
        ubody.attrib['unit'] = "M/SEC"
        ubody.text = "0.0"
        vbody = ET.SubElement(init_file, 'vbody')
        vbody.attrib['unit'] = "M/SEC"
        vbody.text = "0.0"
        wbody = ET.SubElement(init_file, 'wbody')
        wbody.attrib['unit'] = "M/SEC"
        wbody.text = "0.0"

        phi = ET.SubElement(init_file, 'phi')
        phi.attrib['unit'] = "DEG"
        phi.text = "0.0"
        theta = ET.SubElement(init_file, 'theta')
        theta.attrib['unit'] = "DEG"
        theta.text = "90.0"
        psi = ET.SubElement(init_file, 'psi')
        psi.attrib['unit'] = "DEG"
        psi.text = "0.0"
        altitude = ET.SubElement(init_file, 'altitude')
        altitude.attrib['unit'] = "M"
        altitude.text = "0.0"

        lat = ET.SubElement(init_file, 'latitude')
        lat.attrib['unit'] = "DEG"
        lat.text = "45.0"
        longitude = ET.SubElement(init_file, 'longitude')
        longitude.attrib['unit'] = "DEG"
        longitude.text = "-122.0"
        elev = ET.SubElement(init_file, 'elevation')
        elev.attrib['unit'] = "M"
        elev.text = "250"

        xmldoc = minidom.parseString(ET.tostring(init_file, encoding="UTF-8"))
        with open(os.path.join("aircraft", rocket.name_slug, "init.xml"), 'w') as initfile:
            initfile.write(xmldoc.toprettyxml(indent="  "))

        # Write engine files
        for stage in rocket.stages:
            for comp in stage.components:
                for subcon in comp.components:
                    if type(subcon) is document.Engine:
                        engine = subcon
                        with open(os.path.join("engine", engine.name_slug + ".xml"), 'w') as enginefile:
                            enginefile.write(writers.JSBSimEngine.dump(engine))
                        with open(os.path.join("engine", engine.name_slug + "_nozzle.xml"), 'w') as nozzlefile:
                            nozzle_file = ET.Element('nozzle')
                            nozzle_file.attrib['name'] = "Nozzle"
                            area = ET.SubElement(nozzle_file, 'area')
                            area.attrib['unit'] = "M2"
                            area.text = "0.001"
                            xmldoc = minidom.parseString(ET.tostring(nozzle_file, encoding="UTF-8"))
                            nozzlefile.write(xmldoc.toprettyxml(indent="  "))

    def setup_case_path(self, rocket):

        if not os.path.exists(self.thread_path):
            os.makedirs(self.thread_path)

        aircraft_path = os.path.join(self.thread_path, "aircraft", rocket.name_slug)
        engine_path = os.path.join(self.thread_path, "engine")

        if not os.path.exists(aircraft_path):
            os.makedirs(aircraft_path)
        if not os.path.exists(engine_path):
            os.makedirs(engine_path)

        with open(os.path.join(self.thread_path, "run.xml"), 'w') as runfile:
            runfile.write(self.runfile(rocket))

    def runfile(self, rocket):
        doc = ET.Element('runscript')
        doc.attrib['name'] = "Thead %d Simulation Runner" % self.thread_id
        doc.attrib['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
        doc.attrib['xsi:noNamespaceSchemaLocation'] = "http://jsbsim.sourceforge.net/JSBSim.xsd"

        use = ET.SubElement(doc, 'use')
        use.attrib['aircraft'] = rocket.name_slug
        use.attrib['initialize'] = "init"

        run = ET.SubElement(doc, 'run')
        run.attrib['start'] = "0.0"
        run.attrib['end'] = "100"
        run.attrib['dt'] = "0.001"

        prop = ET.SubElement(run, 'property')
        prop.attrib['value'] = "1"
        prop.text = "forces/hold-down"

        # set events:
        # Ignite
        event_ignite = ET.SubElement(run, 'event')
        event_ignite.attrib['name'] = "Ignition"
        ET.SubElement(event_ignite, 'condition').text = "simulation/sim-time-sec  ge  0.001"
        event_ignite_set = ET.SubElement(event_ignite, 'set')
        event_ignite_set.attrib['name'] = "fcs/throttle-cmd-norm[0]"
        event_ignite_set.attrib['value'] = "1.0"
        ET.SubElement(event_ignite, 'notify')

        # Liftoff
        event_liftoff = ET.SubElement(run, 'event')
        event_liftoff.attrib['name'] = "Liftoff"
        ET.SubElement(event_liftoff, 'condition').text = "forces/fbx-prop-lbs gt inertia/weight-lbs"
        event_liftoff_set = ET.SubElement(event_liftoff, 'set')
        event_liftoff_set.attrib['name'] = "forces/hold-down"
        event_liftoff_set.attrib['value'] = "0"
        ET.SubElement(event_liftoff_set, 'notify')

        # Ignite
        event_apogee = ET.SubElement(run, 'event')
        event_apogee.attrib['name'] = "APOGEE"
        ET.SubElement(event_apogee, 'condition').text = "velocities/v-down-fps gt 1"
        ET.SubElement(event_ignite, 'notify')

        # pretty print
        xmldoc = minidom.parseString(ET.tostring(doc, encoding="UTF-8"))
        return xmldoc.toprettyxml(indent="  ")

