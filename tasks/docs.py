import os
import time

from invoke import run, task

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

DOCS_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'docs')
)


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
        run('cd {docs_root} && make {target}'.format(docs_root=DOCS_ROOT,
                                                     target=self.make_target))

        if self.after:
            run(self.after)


@task
def watch(after=None):
    py_event_handler = TouchFileEventHandler(
        patterns=['*.py'],
        touch_file='index.rst'
    )
    rst_event_handler = MakeEventHandler(
        patterns=['*.rst'],
        make_target='html',
        after=after)

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
