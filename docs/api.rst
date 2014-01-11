.. _api_reference:

API reference
=============

Oraide provides a set of conveniences around tmux's ``send-keys`` command.
For more information about how tmux actually works, please see tmux's `man page`_.

.. _man page: http://www.openbsd.org/cgi-bin/man.cgi?query=tmux


``oraide``
----------

.. |auto-advancing| replace:: If auto-advancing is disabled,
                              then a confirmation prompt appears before keystrokes are sent to the session.


.. module:: oraide

.. autofunction:: send_keys

.. autoclass:: Session
   :members:
   :member-order: bysource


Exceptions
^^^^^^^^^^

If tmux's ``send-keys`` command ends with an error status code, an exception is raised.

.. autoexception:: oraide.TmuxError

.. autoexception:: oraide.ConnectionFailedError
   :show-inheritance:

.. autoexception:: oraide.SessionNotFoundError(returncode, cmd, output=None, session=None)
   :show-inheritance:
   :members:


``oraide.keys``
---------------

.. automodule:: oraide.keys
   :members:
   :undoc-members:
