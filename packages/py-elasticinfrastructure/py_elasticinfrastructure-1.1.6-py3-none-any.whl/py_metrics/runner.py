import threading
import time
import py_metrics.metrics as module_metric


class Runner:
    def __init__(self, config, elastic, metrics=None):
        self.config = config
        self.es = elastic

        if metrics is None:
            self.metrics = [config.initialize(module_metric, met)
                            for met in config["metrics"]]
        else:
            self.metrics = metrics

    def loop(self, *args, **kwargs):
        while True:
            time.sleep(self.config["time"])
            self.run(*args, **kwargs)

    def run(self, index=True):
        bulk_results = [met.measure() for met in self.metrics]
        print(bulk_results)
        if index is True:
            return self.es.index_bulk(bulk_results)
        else:
            return bulk_results

    def run_background(self, index=True):
        return threading.Thread(name="background",
                                target=self.loop,
                                kwargs={"index": index})
