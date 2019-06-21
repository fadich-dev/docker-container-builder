import sys

from time import sleep
from threading import Thread


class Spinner:

    def __init__(self, speed: float = 3.0, stdout = None):
        self._speed = speed
        self._started = False
        self._thread = None  # type: Thread
        self.stdout = stdout or sys.stdout

    def start(self, label: str = ''):
        if self._started:
            self.stop()
            raise RuntimeError(f'{self} is already started')

        self._started = True

        self._thread = Thread(target=self._run, args=(label, ))
        self._thread.start()

    def stop(self):
        if not self._started:
            raise RuntimeError(f'{self} is not started')

        self._started = False
        self._thread.join()
        self._thread = None
        self.stdout.write('\n')

    def _run(self, label: str = ''):
        i = 0
        while self._started:
            self.stdout.write('\r{}{:<5}'.format(label, '.' * i))
            self.stdout.flush()
            i = i + 1 if i < 5 else 0
            sleep(1 / self._speed)


if __name__ == '__main__':
    spinner = Spinner()
    spinner.start('Hello')

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        spinner.stop()
