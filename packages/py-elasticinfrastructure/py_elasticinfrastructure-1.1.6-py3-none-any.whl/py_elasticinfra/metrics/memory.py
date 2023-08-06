import psutil
from .base import BaseMetric


class Memory(BaseMetric):
    def __init__(self):
        pass

    def measure(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "virtual_memory": {
                "total": mem.total,
                "available": mem.available,
                "percent": mem.percent,
                "used": mem.used,
                "free": mem.free
            },
            "swap_memory": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        }

    def get_type(self):
        return 'memory'
