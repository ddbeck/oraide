.. module:: oraide

History
=======

Oraide was created by `Daniel D. Beck`_.
The library's name is a portmanteau of *orate* and *aide*.

.. _Daniel D. Beck: http://www.danieldbeck.com/

Release dev
-----------

- Improved the process for adding and updating version numbers.


Release 0.3
-----------

- :issue:`1`: Added Python 3 support.
- Calling :meth:`Session.teletype` with the default delay raised a ``TypeError`` exception.
  The bug was fixed and tests were added.
- Calling :meth:`Session.enter` without providing a ``keys`` argument raised a ``ValueError`` exception.
  The bug was fixed and tests were added.
- Cleaned up wording and formatting in prompt messages.
- Added a missing parameter to :meth:`Session.enter`'s documented parameter list.
- Added tests to cover prompts.
- Replaced meaningless "hello world" strings in the test suite with strings that at least pretend to be relevant.


Release 0.2
-----------

Complete rewrite, with all new API and documentation.


Release 0.1
-----------

Initial version.
