.. _tutorial:

Tutorial
========

This tutorial will walk you through the process of installing and using Oraide
for the first time.


Prerequisites
-------------

Oraide requires tmux 1.7 or later.
Your system may already have tmux installed, or you may need to use your system's package manager to install it.
For example, to install tmux with APT, run ``apt-get install tmux``.
On Mac OS X, you can install tmux with Homebrew_.
To install tmux with Homebrew, run: ``brew install tmux``.

.. _Homebrew: http://brew.sh/


Installation
------------

To install Oraide, run ``pip install oraide``, or download and install the latest release from PyPI_.

.. _PyPI: https://pypi.python.org/pypi/oraide/


Setting up
----------

First, get a tmux session up and running:

#. Start a terminal session.

#. Start a new tmux session.
   Enter :kbd:`tmux new-session -s 'my_session'` and press :kbd:`Enter`.
   You should find yourself in a terminal session, as if you had just started.
   It's a terminal session in a terminal session
   (yes, it's a little confusing, but it's easy to leave; run ``exit`` at the command line,
   or, by default, press :kbd:`Ctrl + b` followed by the the :kbd:`&` key).

   This is the session we'll be controlling with Oraide.

   .. note::

      Don't crane your neck!
      If your presentation is going to be on a large screen or projector
      that would be awkward for you to look at while you give your presentation,
      attach a second terminal to ``my_session`` with tmux's ``attach-session`` command.
      Put the second terminal on your screen (e.g., your laptop's built-in display) and give your neck a rest.

#. Start a separate terminal session.
   This is the session you will use to send keystrokes to ``my_session``.

#. Start the Python interactive interpreter.
   Enter :kbd:`python` and press :kbd:`Enter`.
   It will look something like this:

   .. code-block:: pycon

      $ python
      Python 2.7.5 (default, Jun  9 2013, 16:41:37)
      [GCC 4.2.1 Compatible Apple LLVM 4.2 (clang-425.0.28)] on darwin
      Type "help", "copyright", "credits" or "license" for more information.
      >>> _


.. _sending_keystrokes:

Sending keystrokes
------------------

.. currentmodule:: oraide

At it's simplest, Oraide is a wrapper around tmux's ``send-keys`` command.
Let's give it a try.


#. In the Python interactive session, import Oraide.
   Enter :kbd:`import oraide` and press :kbd:`Enter`. It'll look like this:

   .. code-block:: pycon

      >>> import oraide

#. Send some keys to the tmux session with the :func:`send_keys` function.
   It requires two parameters: a session name and a string of keys to send.
   Enter this:

   .. code-block:: pycon

      >>> oraide.send_keys('my_session', "echo 'Hello, World!'")

   and then press :kbd:`Enter`.
   If you look at your tmux session, you'll see the second parameter entered at the prompt, like this:

   .. code-block:: bash

      $ echo 'Hello, World!'

   Note that the command is unexecuted, because we haven't sent the :kbd:`Enter` key yet.

#. Next, send the :kbd:`Enter` key to ``my_session``. Type:

   .. code-block:: pycon

      >>> send_keys('my_session', 'Enter', literal=False)

   and then press :kbd:`Enter`.
   The :kbd:`Enter` key is sent to ``my_session``.

   The :func:`send_keys` function accepts an optional keyword argument, ``literal``.
   tmux can try to convert the names of keys into the keystrokes themselves (e.g., ``Escape`` to the :kbd:`Esc` key),
   but this can be quite surprising.
   Instead, Oraide defaults to treating the string literally.
   If you want to look up special keystrokes, set ``literal`` to ``False`` (or, at least, something falsy).

   .. seealso::

      Remembering which strings convert to which keystrokes is annoying,
      so you can use attributes of the :mod:`oraide.keys` module instead of literal strings.
      Then you can substitute ``Enter`` for ``oraide.keys.enter``.


Session management
------------------

While :func:`send_keys` is useful, it's tedious to re-enter the session name every time.
To alleviate that frustration, and introduce some more features, Oraide provides the :class:`Session` class.
Here's a simple script that demonstrates its use:

.. code-block:: python

   from oraide import keys, Session

   s = Session('my_session')

   s.send_keys("echo 'Hello, World!'")
   s.send_keys(keys.enter, literal=False)

The script is equivalent to the two ``send_keys`` calls made in the :ref:`previous section <sending_keystrokes>`.
The :meth:`Session.send_keys` method is just like the ``send_keys`` function, but the session name is no longer needed.

The ``Session`` class, by keeping the name of the session, allows for some special behavior,
including the :meth:`Session.teletype` and :meth:`Session.enter` methods.
Let's take a look:

.. code-block:: python

   from oraide import keys, Session

   s = Session('my_session')

   s.teletype("echo 'Hello, World!'")
   s.send_keys(keys.enter, literal=False)

   s.enter("echo 'Look Ma, no hands!'")

The ``teletype`` method works like ``send_keys`` with two differences:

#. Before the keys are sent, a prompt appears (in the terminal where the script is running, not the tmux session),
   so you can control the pacing of your presentation.

#. The keys are sent one at a time, with a short delay between each, to simulate typing.

   .. only:: html

      It looks something like this (slowed for dramatic effect):

      .. image:: no-hands.gif

The ``enter`` method does the same as ``teletype``, except the :kbd:`Enter` key is sent after the literal keys.


Auto-advancement
----------------

By default, the ``teletype`` and ``enter`` methods prompt before sending keys to the session.
Sometimes this is inconvenient.
For example, you may want to narrate a longer sequence of steps without stopping.
To suppress prompts, you can use the :meth:`Session.auto_advance` context manager, like this:

.. code-block:: python

   from oraide import keys, Session

   s = Session('my_session')

   with s.auto_advance():
      s.teletype("echo 'Hello, World!'")
      s.send_keys(keys.enter, literal=False)

   s.enter("echo 'Look Ma, no hands!'")

The commands inside the ``with`` statement are executed without prompting.

If you want to auto-advance all keys sent to a session,
you can instantiate a ``Session`` object with ``enable_auto_advance=True``.

.. note::

   It's unwise to auto-advance your entire presentation.
   Not only is it easier to practice shorter auto-advancing sequences,
   but you also give yourself room to respond to questions or repeat an important point.


Learning more
-------------

Now you're ready to start using Oraide.
For more detailed information about the API, see the :ref:`api_reference`.
If you'd like to see more examples, try the scripts in Oraide's :file:`examples` directory.
If you have problems, see Oraide's `GitHub issues`__.

.. __: https://github.com/ddbeck/oraide/issues

