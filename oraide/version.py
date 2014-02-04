from datetime import datetime
import os
import subprocess

VERSION = '0.5'
DEV = True


def get_commit_time():
    """Get the timestamp of the last commit on the project."""
    try:
        cmd = ["git", "log", "-1", "--format=format:%ct",
               os.path.dirname(__file__)]
        proc = subprocess.check_output(cmd)
        time_str = datetime.fromtimestamp(float(proc)).strftime(
            '%Y%m%d%S')
        return time_str
    except Exception:
        return 0


def get_version():
    """Get the current version number."""
    if DEV:
        return "{}.dev{}".format(VERSION, get_commit_time())
    else:
        return VERSION
