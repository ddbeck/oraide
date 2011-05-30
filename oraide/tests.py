import nose
from . import main


class TestParseScriptLine(object):
    def test_blank_line(self):
        assert main.parse_script_line('   \n') == (None, None)

    def test_note_with_space(self):
        r = main.parse_script_line('# test\n')
        assert r == (None, 'test'), r

    def test_note_without_space(self):
        r = main.parse_script_line('#test\n')
        assert r == (None, 'test'), r

    def test_implicit_window(self):
        assert main.parse_script_line('yes') == (0, 'yes')

    def test_explicit_window_with_space(self):
        r1 = main.parse_script_line('1: yes\n')
        r2 = main.parse_script_line('123: yes\n')
        assert r1 == (1, 'yes'), r1
        assert r2 == (123, 'yes'), r2

    def test_explicit_window_without_space(self):
        assert main.parse_script_line('1:yes\n') == (1, 'yes')
        assert main.parse_script_line('123:yes\n') == (123, 'yes')


def test_parse_script():
    s = ('# note\n'
         '\n'
         'yes\n'
         '1: yes')
    funcs = [f for f in main.parse_script('test_session', s.splitlines())]
    assert len(funcs) == 2, len(funcs)
    assert all(callable(f) for f in funcs), (callable(f) for f in funcs)
