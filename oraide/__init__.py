from contextlib import contextmanager
import logging
import random
import subprocess
import time

from . import keys as keyboard


logger = logging.getLogger(__name__)


class ConnectionFailedError(Exception):
    """The tmux server connection failed (often because the server was not
    running at the time the command was sent).
    """
    def __str__(self):
        return 'Connection to tmux server failed.'


class SessionNotFoundError(Exception):
    """The tmux session was not found (but a connection to tmux server was
    established).
    """
    def __init__(self, session):
        self.session = session

    def __str__(self):
        return 'tmux session {} not found.'.format(repr(self.session))


def send_keys(session, keys, literal=True):
    """Send keys to a tmux session.
    This function is a wrapper around tmux's ``send-keys`` command.

    If ``literal`` is ``False``, tmux will attempt to convert keynames such as
    ``Escape`` or ``Space`` to their single-key equivalents.

    :param session: name of a tmux session
    :param keys: keystrokes to send to the tmux session
    :param literal: whether to prevent tmux from looking up keynames
    """

    args = ["tmux", "send-keys"]

    if literal:
        args.append('-l')

    args.append("-t{}".format(session))
    args.append(keys)

    logger.info('Sending keys with command: {}'.format(' '.join(args)))
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        if 'session not found' in exc.output:
            raise SessionNotFoundError(session)
        elif 'failed to connect to server' in exc.output:
            raise ConnectionFailedError
        else:
            raise


def prompt(keys, verb="send"):
    raw_input("Press enter to {}: {}".format(verb, keys))


class Session(object):
    """A session to which to send keys. This function allows for the
    deduplication of session names when repeatedly sending keystrokes the same
    session.

    :param session: the name of a tmux session
    :param enable_auto_advance: whether to send keystrokes to the session
        immediately, or wait for confirmation
    """

    def __init__(self, session, enable_auto_advance=False):
        self.session = session
        self.auto_advancing = enable_auto_advance

    def send_keys(self, keys, literal=True, after=None):
        """Send each literal character in ``keys`` to the session.

        :param keys: literal keystrokes to send to the session
        :param literal: whether to prevent tmux from looking up keynames
        """
        send_keys(self.session, keys, literal=literal)

    def teletype(self, keys, delay=90):
        """Type ``keys`` character-by-character, as if you were actually typing
        them by hand.

        The ``delay`` parameter adds time between each keystroke for
        verisimilitude. The actual time between keystrokes varies up to ten
        percent more or less than the nominal value. The default, 90
        milliseconds, approximates a fast typist.

        :param keys: the literal keys to be typed
        :param int delay: the nominal time between keystrokes in milliseconds.
        """
        delay_variation = delay / 10

        with self.auto_advance():
            for key in keys:
                self.send_keys(key)

                current_delay = random.randint(delay - delay_variation,
                                               delay + delay_variation)
                time.sleep(current_delay / 1000.0)

    def enter(self, keys=None, teletype=True, after=keyboard.enter):
        """Type ``keys``, then press :kbd:`Enter`.

        By default, typing character-by-character is enabled with the
        ``teletype`` parameter.

        :param keys: the keystroke to be sent to the to the session. These keys
            may only be literal keystrokes, not keynames to be looked up by
            tmux.
        :param after: additional keystrokes to send to the session with
            ``literal`` set to ``False`` (typically for appending a special keys
            from :mod:`oraide.keys`, like the default, :kbd:`Enter`)
        """
        if not self.auto_advancing:
            prompt(keys)

        if teletype:
            self.teletype(keys)
        else:
            self.send_keys(keys)

        with self.auto_advance():
            self.send_keys(after, literal=False)

    @contextmanager
    def auto_advance(self):
        """Return a context manager that disables prompts before sending
        keystrokes to the session. For example:

        .. code-block:: python

           session.enter('vim some_file.txt')    # prompt first
           with session.auto_advance():          # disables prompts
               session.teletype('jjji')
               session.enter('Hello, World!')
               session.press_key(keys.escape)
           session.enter(':x')                   # prompt first
        """
        initial_auto_state = self.auto_advancing
        self.auto_advancing = True
        yield
        self.auto_advancing = initial_auto_state


__all__ = [send_keys, Session]
