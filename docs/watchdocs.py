import argparse
import os
import subprocess
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class TouchFileEventHandler(PatternMatchingEventHandler):
    """Event handler """
    def __init__(self, *args, **kwargs):
        self.touch_file = kwargs.pop('touch_file', None)
        super(TouchFileEventHandler, self).__init__(*args, **kwargs)

    def on_any_event(self, event):
        with open(self.touch_file, 'a') as fp:
            os.utime(fp.name, None)


class MakeEventHandler(PatternMatchingEventHandler):
    def __init__(self, *args, **kwargs):
        self.make_target = kwargs.pop('make_target', None)
        self.after = kwargs.pop('after', None)
        super(MakeEventHandler, self).__init__(*args, **kwargs)

    def on_any_event(self, event):
        subprocess.call(['make', self.make_target])

        if self.after:
            subprocess.call(self.after, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--after', help="a command to run after")
    args = parser.parse_args()

    py_event_handler = TouchFileEventHandler(
        patterns=['*.py'],
        touch_file='index.rst'
    )
    rst_event_handler = MakeEventHandler(
        patterns=['*.rst'],
        make_target='html',
        after=args.after)

    observer = Observer()
    observer.schedule(py_event_handler, path='..', recursive=True)
    observer.schedule(rst_event_handler, path='.', recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
