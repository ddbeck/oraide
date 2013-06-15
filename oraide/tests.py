import logging
import subprocess
import time
import unittest

from oraide import send_keys, ConnectionFailedError, SessionNotFoundError


class TestSendKeys(unittest.TestCase):
    session_name = 'oraide_test_session'
    verification_string = '7hh50zxnxj'

    def start_tmux_session(self):
        logging.info('Starting tmux session: {}'.format(self.session_name))
        subprocess.check_call(['tmux', 'new-session', '-d',
                               '-s{}'.format(self.session_name)])
        time.sleep(0.5)  # wait for the session to start
                         # TODO: find a way to determine whether the session is
                         #       ready, instead of waiting and hoping

    def get_tmux_session_contents(self):
        return subprocess.check_output(
            ['tmux', 'capture-pane', '-p',
             '-t{}'.format(self.session_name)])

    def test_literal_keys_appear_in_session(self):
        self.start_tmux_session()

        send_keys(self.session_name, self.verification_string)
        session_output = self.get_tmux_session_contents()

        self.assertIn(self.verification_string, session_output)

    def test_lookup_keys_appear_in_session(self):
        self.start_tmux_session()

        send_keys(self.session_name,
                  'echo "Hello, {}"'.format(self.verification_string))
        send_keys(self.session_name, 'Enter', literal=False)
        session_output = self.get_tmux_session_contents()
        count = session_output.count(self.verification_string)

        self.assertEquals(count, 2)

    def test_wrong_session_raises_session_not_found_error(self):
        self.start_tmux_session()

        with self.assertRaises(SessionNotFoundError):
            send_keys(self.session_name + '__', self.verification_string)

    def test_no_server_raises_connection_failed_error(self):
        with self.assertRaises(ConnectionFailedError):
            send_keys(self.session_name, self.verification_string)

    def tearDown(self):
        subprocess.call(['tmux', 'kill-server'])
