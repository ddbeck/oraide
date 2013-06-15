"""A demonstration of the simplest possible Oraide commands, without using the
``Session`` API.
"""

import oraide


def main():
    oraide.send_keys('oraide-example', "echo 'Hello, world!'")
    oraide.send_keys('oraide-example', oraide.keyboard.enter, literal=False)


if __name__ == '__main__':
    main()
