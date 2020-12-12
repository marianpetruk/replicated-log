import gc
import threading

from gevent import killall, Greenlet
from greenlet import GreenletExit


class CountDownLatch:
    def __init__(self, count=1):
        self.set_count(count)
        self.lock = threading.Condition()

    def set_count(self, count):
        self.count = count

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count == 0:
            print("start NotifyAll")
            self.lock.notifyAll()
            print("finish NotifyAll")
        self.lock.release()

    def await_(self):
        print("AWAIT LOCKED")
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        print("AWAIT UNLOCKED")
        self.lock.release()


class Notifier:
    def __init__(self, w, result, num_of_nodes):
        self.notified = False
        self.results = []
        self.counter = w
        self.result = result
        self.num_of_nodes = num_of_nodes

    def notify(self, res):
        if not self.notified:
            self.result.append(res)
            killall(
                [obj for obj in gc.get_objects() if isinstance(obj, Greenlet)]
            )
            self.notified = True

    def accept_result(self, result):
        if isinstance(result, GreenletExit):
            return
        self.results.append(result)
        if sum(self.results) >= self.counter:
            self.notify(True)
        if len(self.results) == self.num_of_nodes:
            self.notify(False)
