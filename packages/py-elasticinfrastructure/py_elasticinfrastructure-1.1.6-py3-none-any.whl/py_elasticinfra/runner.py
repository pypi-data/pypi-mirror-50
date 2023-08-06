import threading
import time
import py_elasticinfra.metrics as module_metric
from py_elasticinfra.utils.loop_thread import LoopThread


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
        if index is True:
            return self.es.index_bulk(self.metrics)
        else:
            return [met.measure() for met in self.metrics]

    def run_background(self, index=True):
        self.loop_thread = LoopThread(
            run_method=self.run,
            run_kwargs={"index": index},
            thread_kwargs={"name": "background-loop"},
            sleep=self.config["time"]
        )
        self.loop_thread.start()

    def stop_background(self):
        if self.loop_thread:
            self.loop_thread.stop()
