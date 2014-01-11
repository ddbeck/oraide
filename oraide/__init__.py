"""'A library to help presenters demonstrate terminal sessions hands-free."""

__version__ = '0.4'

import locale
import logging
import random
import subprocess
import time
import warnings
from contextlib import contextmanager
from functools import wraps

from . import keys as keyboard

logger = logging.getLogger(__name__)

# check for minimum tmux version
VALID_VERSIONS = ['1.7', '1.8', '1.9']
WRONG_VERSION_MESSAGE = ('tmux {ver} or greater not found. '
                         'Oraide requires tmux>={ver}'
                         ).format(ver=VALID_VERSIONS[0])
try:
    output = subprocess.check_output(['tmux', '-V'], stderr=subprocess.STDOUT)
    output = output.decode(locale.getdefaultlocale()[1])
    version_checks = (ver in output for ver in VALID_VERSIONS)
    if not any(version_checks):
        warnings.warn(WRONG_VERSION_MESSAGE, Warning)
except Exception as exc:
    warnings.warn(WRONG_VERSION_MESSAGE, Warning)


class TmuxError(subprocess.CalledProcessError):
    """The command sent to tmux returned a non-zero exit status. This is an
    unrecognized tmux error.

    This exception type inherits from :exc:`subprocess.CalledProcessError`,
    which adds ``returncode``, ``cmd``, and ``output`` attributes.
    """
    pass


class ConnectionFailedError(TmuxError):
    """The tmux server connection failed (often because the server was not
    running at the time the command was sent).
    """
    def __str__(self):
        return 'Connection to tmux server failed.'


class SessionNotFoundError(TmuxError):
    """The tmux session was not found (but a connection to tmux server was
    established).

    This exception type adds another attribute, ``session``, for your debugging
    convenience.
    """
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        super(SessionNotFoundError, self).__init__(*args, **kwargs)

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

    cmd = ' '.join(args)

    logger.debug('Sending keys with command: %s', cmd)
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        output = exc.output.decode(locale.getdefaultlocale()[1])
        if 'session not found' in output:
            raise SessionNotFoundError(exc.returncode, cmd, exc.output,
                                       session=session)
        elif 'failed to connect to server' in output:
            raise ConnectionFailedError(exc.returncode, cmd, exc.output)
        else:
            raise


def prompt(func, input_func=None):
    """Handle prompting for advancement on `Session` methods."""
    if input_func is None:
        try:
            input_func = raw_input
        except NameError:
            input_func = input

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        keys = args[1] if len(args) > 1 else None

        if not args[0].auto_advancing:
            if keys is not None:
                msg = "[{session}] Press enter to send {keys}".format(
                    keys=repr(keys),
                    session=self.session,
                )
            else:
                msg = "[{session}] Press enter to continue".format(
                    session=self.session
                )
            input_func(msg)
        return func(*args, **kwargs)
    return wrapper


class Session(object):
    """A session to which to send keys. This function allows for the
    deduplication of session names when repeatedly sending keystrokes the same
    session.

    :param session: the name of a tmux session
    :param enable_auto_advance: whether to send keystrokes to the session
        immediately, or wait for confirmation, on certain methods
    :param int teletype_delay: the delay between keystrokes for the
        :meth:`teletype` method (for overriding the default of 90 milliseconds)
    """

    def __init__(self, session, enable_auto_advance=False,
                 teletype_delay=None):
        self.session = session
        self.auto_advancing = enable_auto_advance
        self.teletype_delay = teletype_delay

    def send_keys(self, keys, literal=True):
        """Send each literal character in ``keys`` to the session.

        :param keys: literal keystrokes to send to the session
        :param literal: whether to prevent tmux from looking up keynames

        .. seealso:: :func:`send_keys`
        """
        send_keys(self.session, keys, literal=literal)

    @prompt
    def teletype(self, keys, delay=None):
        """teletype(keys, delay=90)
        Type ``keys`` character-by-character, as if you were actually typing
        them by hand.

        The ``delay`` parameter adds time between each keystroke for
        verisimilitude. The actual time between keystrokes varies up to ten
        percent more or less than the nominal value. The default, 90
        milliseconds, approximates a fast typist.

        .. note:: |auto-advancing|

        :param keys: the literal keys to be typed
        :param int delay: the nominal time between keystrokes in milliseconds.
        """
        if delay is None:
            delay = (self.teletype_delay if self.teletype_delay is not None
                     else 90)

        delay_variation = delay / 10

        with self.auto_advance():
            logger.info('[%s] Sending %s', self.session, repr(keys))
            for key in keys:
                self.send_keys(key)

                current_delay = random.randint(delay - delay_variation,
                                               delay + delay_variation)
                time.sleep(current_delay / 1000.0)

    @prompt
    def enter(self, keys=None, teletype=True, after=keyboard.enter):
        """enter(keys=None, teletype=True, after='Enter')
        Type ``keys``, then press :kbd:`Enter`.

        By default, typing character-by-character is enabled with the
        ``teletype`` parameter.

        .. note:: |auto-advancing|

        :param keys: the keystroke to be sent to the to the session. These keys
            may only be literal keystrokes, not keynames to be looked up by
            tmux.
        :param teletype: whether to enable simulated typing
        :param after: additional keystrokes to send to the session with
            ``literal`` set to ``False`` (typically for appending a special
            keys from :mod:`oraide.keys`, like the default, :kbd:`Enter`)
        """

        if keys:
            if teletype:
                with self.auto_advance():
                    self.teletype(keys)
            else:
                self.send_keys(keys)

        if after:
            with self.auto_advance():
                self.send_keys(after, literal=False)

    @contextmanager
    def auto_advance(self):
        """auto_advance()
        Return a context manager that disables prompts before sending
        keystrokes to the session. For example:

        .. code-block:: python

           session.enter('vim some_file.txt')    # prompt first
           with session.auto_advance():          # disables prompts
               session.teletype('jjji')
               session.enter('Hello, World!', after=keys.escape)
           session.enter(':x')                   # prompt first
        """
        initial_auto_state = self.auto_advancing
        self.auto_advancing = True
        yield
        self.auto_advancing = initial_auto_state


__all__ = ['send_keys', 'Session']
