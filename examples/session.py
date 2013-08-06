"""A demonstration of the ``Session`` API."""

from __future__ import print_function

import oraide


EARNESTNESS = """\
ALGERNON: Well, that is exactly what dentists always do. Now, go on!
          Tell me the whole thing. I may mention that I have always
          suspected you of being a confirmed and secret Bunburyist; and
          I am quite sure of it now.

JACK: Bunburyist? What on earth do you mean by a Bunburyist?

ALGERNON: I'll reveal to you the meaning of that incomparable expression
          as soon as you are kind enough to inform me why you are Ernest
          in town and Jack in the country.

JACK: Well, produce my cigarette case first.

ALGERNON: Here it is. Now produce your explanation, and pray make it
          improbable.
"""


def main():
    s = oraide.Session('oraide-example')
    s.enter("vim")
    s.enter('i')

    with s.auto_advance():
        print("Typing {} characters".format(len(EARNESTNESS)))
        for line in EARNESTNESS.splitlines():
            s.enter(line)

    s.send_keys(oraide.keys.escape, literal=False)
    s.enter(':q!')
    s.enter('exit')

if __name__ == '__main__':
    main()
