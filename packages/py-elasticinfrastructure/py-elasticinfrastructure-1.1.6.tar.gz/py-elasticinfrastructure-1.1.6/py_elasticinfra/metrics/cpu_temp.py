import numpy as np
import psutil
from .base import BaseMetric


class CpuTemp(BaseMetric):
    def __init__(self, *args, **kwargs):
        if "tmp_key" in kwargs:
            self.tmp_key = kwargs["tmp_key"]
        else:
            raise "Temperature requires a key from psutil."

    def measure(self):
        temps = self._get_temps()
        return {"cpu_temperatures": temps,
                "cpu_temperature_average": self._get_temp_averages(temps)}

    def get_type(self):
        return 'cpu'

    def _get_temps(self):
        temp = psutil.sensors_temperatures()
        temps = []
        for t in temp[self.tmp_key]:
            temps.append({
                "label": t.label,
                "current": t.current,
                "high": t.high,
                "critical": t.critical
            })
        return temps

    def _get_temp_averages(self, temps):
        labels = set([t["label"] for t in temps])
        metadata = {}
        for label in labels:
            res = [t["current"] for t in temps if t["label"] == label]
            res = np.array(res)
            metadata[label] = np.average(res)
        return metadata
