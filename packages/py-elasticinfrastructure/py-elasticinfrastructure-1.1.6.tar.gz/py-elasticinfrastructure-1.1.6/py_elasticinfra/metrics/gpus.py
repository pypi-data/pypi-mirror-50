from .base import BaseMetric
import GPUtil


class GPUs(BaseMetric):
    def __init__(self):
        pass

    def measure(self):
        all = []
        gpus = GPUtil.getGPUs()
        for g in gpus:
            all.append(g.__dict__)

        return {
            "gpus_data": all,
            "gpus_averages": self._get_gpus_metadata(gpus)}

    def get_type(self):
        return 'gpu'

    def _get_gpus_metadata(self, gpus):
        labels = ["load", "memoryUsed", "memoryFree", "temperature"]
        metadata = {}
        for l in labels:
            d = 0
            for g in gpus:
                d += g.__dict__[l]
            metadata[l] = d / len(gpus)
        return metadata
