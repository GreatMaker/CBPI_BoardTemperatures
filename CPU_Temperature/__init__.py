from modules import cbpi
from modules.core.hardware import  SensorActive
from modules.core.props import Property

cpu_temperature = '/sys/class/thermal/thermal_zone0/temp'

@cbpi.sensor
class CPUTempSensor(SensorPassive):
    offset = Property.Number("Offset", True, 0, description="Offset which is added to the received sensor data. Positive and negative values are both allowed.")
    temp = 0

    def init(self):
        return

    def stop(self):
        return

    def read(self):
        value = open(cpu_temperature, 'r').read().strip()

        if self.get_config_parameter("unit", "C") == "C":
            self.data_received(round((value + self.offset_value()) / 1000, 2))
        else:
            self.data_received(round(9.0 / 5.0 * ((value + self.offset_value()) / 1000) + 32, 2))

    @cbpi.try_catch(0)
    def offset_value(self):
        return float(self.offset)

    @classmethod
    def init_global(self):
        try:
            with open(cpu_temperature) as fp:
                print("CPU temperature readable")
        except IOError as err:
            print("Error reading CPU temperature {}".format(err))
        pass
