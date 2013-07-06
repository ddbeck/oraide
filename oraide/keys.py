"""This module provides shortcuts for sending special keystrokes to tmux
sessions. The functions and constants are typically used with
:meth:`oraide.Session.send_keys`, or the ``after`` parameter on certain
:class:`oraide.Session` methods.

The constants of this module are provided as a Pythonic substitute for the
strings used in tmux's keyname lookup table. For example, to send a backspace
key, the string ``'BSpace'`` may be replaced with a reference to
``oraide.keys.backspace``. The following keys are provided:

* ``backspace``
* ``end``
* ``enter``
* ``escape``
* ``home``
* ``page_down``
* ``page_up``
* ``space``
* ``tab``
* ``up``
* ``down``
* ``left``
* ``right``

as well as the function keys ``f1`` through ``f20``.
"""

import sys


# Function keys (e.g., F1, F2, F3, and so on)
def _add_f_keys():
    for i in range(1, 20):
        setattr(sys.modules[__name__], 'f{}'.format(i), 'F{}'.format(i))
_add_f_keys()


# special keys
backspace = 'BSpace'
end = 'End'
enter = 'Enter'
escape = 'Escape'
home = 'Home'
page_down = 'PageDown'
page_up = 'PageUp'
space = 'Space'
tab = 'Tab'


# arrow keys
up = 'Up'
down = 'Down'
left = 'Left'
right = 'Right'


def control(key):
    """Make a string that tmux will parse as the control key (:kbd:`Ctrl`) and
    ``key`` pressed at the same time.

    .. note::

       The ``key`` parameter is case-sensitive. If ``key`` is uppercase, it's
       equivalent to entering :kbd:`Shift` and the key.

       .. doctest::

          >>> from oraide.keys import control
          >>> control('a')  # ctrl + a
          'C-a'
          >>> control('A')  # ctrl + shift + a
          'C-A'
       """
    return 'C-{}'.format(key)


def command(key):
    """Make a string that tmux will parse as the command key (also known as the
    meta, super, cmd, Apple, and Windows key) and ``key`` pressed at the same
    time.

    .. note::

       The ``key`` parameter is case-sensitive. If ``key`` is uppercase, it's
       equivalent to entering :kbd:`Shift` and the key.

       .. doctest::

          >>> from oraide.keys import command
          >>> command('a')  # command + a
          'M-a'
          >>> command('A')  # command + shift + a
          'M-A'
    """
    return 'M-{}'.format(key)


def alt(key):
    """Make a string that tmux will parse as the alt key (:kbd:`Alt`) and
    ``key`` pressed at the same time.

    .. note::

       The ``key`` parameter is case-sensitive. If ``key`` is uppercase, it's
       equivalent to entering :kbd:`Shift` and the key.

       .. doctest::

          >>> from oraide.keys import alt
          >>> alt('a')  # alt + a
          'A-a'
          >>> alt('A')  # alt + shift + a
          'A-A'
    """
    return 'A-{}'.format(key)
