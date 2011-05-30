#!/usr/bin/env python2.7

from __future__ import print_function
import argparse
import functools
import re
import subprocess


CMD_REGEX = re.compile(r'(?!#)((?P<index>\d+):){0,1}(?P<command>.*)')


def parse_args():
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description='Run an Oraide script.')
    parser.add_argument('script', metavar='SCRIPT',
        type=argparse.FileType('r'), help='path to an Oraide script')
    parser.add_argument('screen', metavar='SCREEN',
        help='name of a screen session')
    args = parser.parse_args()
    return args.script, args.screen


def send_command(session, window, command):
    """docstring for send_command"""
    args = ['screen',
            '-S', session,
            '-p', str(window),
            '-X', 'stuff', "%s" % command]
    proc = subprocess.Popen(args)
    proc.communicate()


def parse_script_line(line):
    """Parse a script line and return a tuple.

    For commands, the first element is a screen window and the second is the
    command string. For notes, the first element is None and the second element
    is the note string. For blank lines, both elements are None.
    """
    if line.strip() == '':
        return None, None
    elif line.startswith('#'):
        if line.startswith('# '):
            return None, line[2:].rstrip()
        else:
            return None, line[1:].rstrip()
    else:
        result = CMD_REGEX.search(line).groupdict()
        index, command = result['index'], result['command'].strip()
        if result['index'] is not None:
            return int(result['index']), command
        else:
            return 0, command


def parse_script(screen, lines):
    """Yields a callable for each command line of the script."""
    for line in lines:
        window, cmd = parse_script_line(line)
        if (window, cmd) == (None, None):   # blank line: noop
            pass
        elif window == None:    # note: print
            print(cmd)
        else:
            def _send():    # command: send to screen
                print("SENDING: %s ==> window %s" % (repr(cmd), window))
                send_command(screen, window, cmd)
                raw_input()
                send_command(screen, window, '\n')
                raw_input()
            yield _send


def main():
    """Run Oraide."""
    try:
        script, screen = parse_args()

        print('Starting %s. Press ENTER to advance script.\n' % script.name)
        for call in parse_script(screen, script.readlines()):
            call()
    except KeyboardInterrupt:
        pass
