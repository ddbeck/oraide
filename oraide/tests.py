import locale
import logging
import os
import subprocess
import time
import unittest

from oraide import (ConnectionFailedError, prompt, send_keys, Session,
                    SessionNotFoundError)

SHELL_PROMPT = os.environ.get('ORAIDE_TEST_PROMPT', u'$')
SHELL_PROMPT = (SHELL_PROMPT.decode(locale.getdefaultlocale()[1])
                if hasattr(SHELL_PROMPT, 'decode')
                else SHELL_PROMPT)
TESTING_SESSION_NAME = 'oraide_test_session'


class TimeoutError(Exception):
    pass


def assert_after_timeout(fn, timeout_duration=2.0):
    timeout = time.time() + timeout_duration

    def wrapper():
        while True:
            try:
                return fn()
            except AssertionError:
                if time.time() > timeout:
                    raise
    return wrapper


class LiveSessionMixin(object):
    def start_tmux_session(self, timeout_duration=2.0):
        logging.info('Starting tmux session: {}'.format(self.session_name))

        subprocess.check_call(['tmux', 'new-session', '-d',
                               '-s{}'.format(self.session_name)])

        subprocess.check_call(['tmux', 'has-session',
                               '-t{}'.format(self.session_name)])

        timeout = time.time() + timeout_duration
        while time.time() < timeout:
            if SHELL_PROMPT in self.get_tmux_session_contents():
                break
        else:
            msg = ('tmux session failed to start before timeout; '
                   'expected to see shell prompt: {} '
                   '(set ORAIDE_TEST_PROMPT to look for something else)')
            raise TimeoutError(msg.format(SHELL_PROMPT))

    def get_tmux_session_contents(self):
        out = subprocess.check_output(
            ['tmux', 'capture-pane', '-p',
             '-t{}'.format(self.session_name)])
        out_decoded = out.decode(locale.getdefaultlocale()[1])
        return out_decoded

    def kill_tmux_session(self):
        proc = subprocess.Popen(['tmux', 'kill-session',
                                 '-t{}'.format(self.session_name)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        proc.communicate()


class TestSendKeys(LiveSessionMixin, unittest.TestCase):
    session_name = TESTING_SESSION_NAME
    verification_string = '7hh50zxnxj'

    def test_literal_keys_appear_in_session(self):
        self.start_tmux_session()
        send_keys(self.session_name, '\n' + self.verification_string)

        @assert_after_timeout
        def _assertion():
            self.assertIn(self.verification_string,
                          self.get_tmux_session_contents())
        _assertion()

    def test_lookup_keys_are_sent_to_session(self):
        self.start_tmux_session()
        send_keys(self.session_name,
                  'echo "Hello, {}"'.format(self.verification_string))
        send_keys(self.session_name, 'Enter', literal=False)

        @assert_after_timeout
        def _assertion():
            session_contents = self.get_tmux_session_contents()
            self.assertEqual(2,
                             session_contents.count(self.verification_string))
        _assertion()

    def test_wrong_session_raises_session_not_found_error(self):
        self.start_tmux_session()

        with self.assertRaises(SessionNotFoundError):
            send_keys(self.session_name + '__', self.verification_string)

    def test_no_server_raises_connection_failed_error(self):
        with self.assertRaises(ConnectionFailedError):
            send_keys(self.session_name, self.verification_string)

    def tearDown(self):
        self.kill_tmux_session()


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

        fn(Session('test'), 'test prompt with keys')

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
        s.teletype("echo 'this is the delay set on the method'", delay=10)
        s.send_keys('Enter', literal=False)

    def test_delay_set_by_session_attribute(self):
        s = Session(self.session_name, enable_auto_advance=True,
                    teletype_delay=10)
        s.teletype("echo 'this is the delay set on the session at-large'")
        s.send_keys('Enter', literal=False)

    def test_delay_default(self):
        s = Session(self.session_name, enable_auto_advance=True)
        s.teletype("echo 'this is the default delay'")
        s.send_keys('Enter', literal=False)

    def tearDown(self):
        self.kill_tmux_session()


class TestSessionEnter(LiveSessionMixin, unittest.TestCase):
    session_name = TESTING_SESSION_NAME

    def setUp(self):
        self.start_tmux_session()
        self.session = Session(self.session_name, enable_auto_advance=True)

    def test_noop(self):
        """Test some cases of calling Enter that don't actually do anything."""
        contents = self.get_tmux_session_contents()

        self.session.enter(after=None)
        self.session.enter(teletype=False, after=None)

        self.assertEqual(contents, self.get_tmux_session_contents())

    def test_enter_without_text(self):
        original_contents = self.get_tmux_session_contents()
        original_count = original_contents.count(SHELL_PROMPT)
        logging.debug("Before: %s", repr(original_contents))

        self.session.enter()
        self.session.enter(teletype=False)

        @assert_after_timeout
        def _assertion():
            contents = self.get_tmux_session_contents()
            logging.debug("After: %s", repr(contents))
            self.assertEqual(original_count + 2, contents.count(SHELL_PROMPT))
        _assertion()

    def test_keys_with_enter(self):
        self.session.enter("echo 'test_keys_with_enter'")

        output = self.get_tmux_session_contents()

        self.assertEqual(output.count('test_keys_with_enter'), 2)

    def test_keys_without_enter(self):
        self.session.enter("echo 'test_keys_without_enter'", after=None)

        output = self.get_tmux_session_contents()

        self.assertEqual(output.count('test_keys_without_enter'), 1)
        self.session.enter()

    def test_keys_without_teletype_without_after(self):
        self.session.enter("echo 'test_keys_without_teletype_without_after'",
                           teletype=False, after=None)

        self.assertIn(
            'test_keys_without_teletype_without_after',
            self.get_tmux_session_contents()
        )

    def test_keys_without_teletype_with_enter(self):
        self.session.enter("echo 'test_keys_without_teletype_with_enter'")

        output = self.get_tmux_session_contents()

        self.assertEqual(output.count('test_keys_without_teletype_with_enter'),
                         2)

    def tearDown(self):
        self.kill_tmux_session()
