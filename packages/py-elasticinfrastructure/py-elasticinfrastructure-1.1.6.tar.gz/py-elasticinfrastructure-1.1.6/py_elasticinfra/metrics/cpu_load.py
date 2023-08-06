import psutil
from .base import BaseMetric


class CpuLoad(BaseMetric):
    def __init__(self):
        pass

    def measure(self):
        load = psutil.cpu_percent()
        cpu_threads = psutil.cpu_percent(percpu=True)
        return {'cpu_load_average': load,
                'cpu_load_threads': cpu_threads}

    def get_type(self):
        return 'cpu'
