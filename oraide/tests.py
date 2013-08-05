import locale
import logging
import subprocess
import time
import unittest

from oraide import (prompt, send_keys, Session, ConnectionFailedError,
                    SessionNotFoundError)

TESTING_SESSION_NAME = 'oraide_test_session'


class LiveSessionMixin(object):
    def start_tmux_session(self):
        logging.info('Starting tmux session: {}'.format(self.session_name))
        subprocess.check_call(['tmux', 'new-session', '-d',
                               '-s{}'.format(self.session_name)])
        time.sleep(0.5)  # wait for the session to start
                         # TODO: find a way to determine whether the session is
                         #       ready, instead of waiting and hoping

    def get_tmux_session_contents(self):
        out = subprocess.check_output(
            ['tmux', 'capture-pane', '-p',
             '-t{}'.format(self.session_name)])
        return out.decode(locale.getdefaultlocale()[1])

    def kill_tmux_server(self):
        proc = subprocess.Popen(['tmux', 'kill-server'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.communicate()


class TestSendKeys(LiveSessionMixin, unittest.TestCase):
    session_name = TESTING_SESSION_NAME
    verification_string = '7hh50zxnxj'

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

        self.assertEqual(count, 2)

    def test_wrong_session_raises_session_not_found_error(self):
        self.start_tmux_session()

        with self.assertRaises(SessionNotFoundError):
            send_keys(self.session_name + '__', self.verification_string)

    def test_no_server_raises_connection_failed_error(self):
        with self.assertRaises(ConnectionFailedError):
            send_keys(self.session_name, self.verification_string)

    def tearDown(self):
        self.kill_tmux_server()


class TestSession(unittest.TestCase):
    session_name = TESTING_SESSION_NAME

    def test_auto_advance_context_manager_restores_state(self):
        s1 = Session(self.session_name, enable_auto_advance=True)
        s2 = Session(self.session_name)

        self.assertTrue(s1.auto_advancing)
        with s1.auto_advance():
            self.assertTrue(s1.auto_advancing)
        self.assertTrue(s1.auto_advancing)

        self.assertFalse(s2.auto_advancing)
        with s2.auto_advance():
            self.assertTrue(s1.auto_advancing)
        self.assertFalse(s2.auto_advancing)


class TestPrompt(unittest.TestCase):
    def fake_input(*args, **kwargs):
        pass

    def test_prompt_with_keys(self):
        def test_fn(*args, **kwargs):
            pass
        fn = prompt(test_fn, input_func=self.fake_input)

        fn(Session('test'), 'hargle bargle')

    def test_prompt_without_keys(self):
        def test_fn(*args, **kwargs):
            pass
        fn = prompt(test_fn, input_func=self.fake_input)

        fn(Session('test'))


class TestTeletypeDelay(LiveSessionMixin, unittest.TestCase):
    session_name = TESTING_SESSION_NAME

    def setUp(self):
        self.start_tmux_session()

    def test_delay_set_by_argument(self):
        s = Session(self.session_name, enable_auto_advance=True)
        s.teletype("echo 'Hello, World!'", delay=10)
        s.enter()

    def test_delay_set_by_session_attribute(self):
        s = Session(self.session_name, enable_auto_advance=True,
                    teletype_delay=10)
        s.teletype("echo 'Hello, World!'")
        s.enter()

    def test_delay_default(self):
        s = Session(self.session_name, enable_auto_advance=True)
        s.teletype("echo 'Hello, World!'")
        s.enter()

    def tearDown(self):
        self.kill_tmux_server()


class TestSessionEnter(LiveSessionMixin, unittest.TestCase):
    session_name = TESTING_SESSION_NAME

    def setUp(self):
        self.start_tmux_session()
        self.session = Session(self.session_name, enable_auto_advance=True)

    def test_enter_with_keys(self):
        self.session.enter("echo 'testing enter() with keys string'")

    def test_enter_without_keys(self):
        self.session.enter()

    def tearDown(self):
        self.kill_tmux_server()
