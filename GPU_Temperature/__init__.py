from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property

import os


@cbpi.sensor
class GPUTempSensor(SensorPassive):
    offset = Property.Number("Offset", True, 0,
                             description="Offset which is added to the received sensor data. Positive and negative values are both allowed.")
    temp = 0

    def init(self):
        return

    def stop(self):
        return

    def read(self):
        value = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
        value.replace("temp=", "").replace("'C\n", "")

        if self.get_config_parameter("unit", "C") == "C":
            self.data_received(round(value + self.offset_value(), 2))
        else:
            self.data_received(round(9.0 / 5.0 * (value + self.offset_value()) + 32, 2))

    @cbpi.try_catch(0)
    def offset_value(self):
        return float(self.offset)

    @classmethod
    def init_global(self):
        try:
            with open('/opt/vc/bin/vcgencmd') as fp:
                print("GPU temperature readable")
        except IOError as err:
            print("Error reading GPU temperature {}".format(err))
        pass
