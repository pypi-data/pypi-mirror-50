import threading
import time


class LoopThread(threading.Thread):
    """Thread class with a stop() method, which
      runs a loop
    """

    def __init__(self, run_method,
                 run_kwargs,
                 thread_kwargs={},
                 sleep=False):
        """
        :param run_method: method to run in the loop
        :param run_kwargs: arguments for method in the loop
        :thread_kwargs: arguments for threading.Thread class
        :sleep: time to sleep in the loop
        """
        super(LoopThread, self).__init__(**thread_kwargs)
        self._stop_event = threading.Event()
        self.run_method = run_method
        self.run_kwargs = run_kwargs
        self.sleep = sleep

    def run(self):
        while not self.stopped():
            if self.sleep is not False:
                time.sleep(self.sleep)
            self.run_method(**self.run_kwargs)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
