.. module:: oraide

History
=======

Oraide was created by `Daniel D. Beck`_.
The library's name is a portmanteau of *orate* and *aide*.

.. _Daniel D. Beck: http://www.danieldbeck.com/

Release 0.4
-----------

- :issue:`8`: Added an explicit requirement of tmux 1.7 or greater.
  On import, a warning is raised when it cannot be confirmed that a supported version of tmux is available.
  Thanks to David Greisen for the feedback about this issue.
- Upgraded to Sphinx 1.2.
- Added a :ref:`seealso` document.
- Added a :ref:`whentouse` document.
- Improved the process for adding and updating version numbers.
- Fixed a PDF documentation build failure caused by the tutorial's animated GIF.
- Fixed various style and kwalitee problems.
- Changed the layout of the Git repository to use `git-flow`_.
- Added a bunch more tests.
- Added optional ``ORAIDE_TEST_PROMPT`` environment variable setting for test suite's prompt detection.
- Added polling and timeouts to improve the precision of tmux sessions in the test suite.
- Removed the part of the test suite that kills the tmux server. Now it only kills the test session.

.. _git-flow: https://github.com/nvie/gitflow


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
