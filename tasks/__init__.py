import os

from invoke import Collection, run, task

from . import docs
import oraide

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


@task
def increment(version):
    """Change the version number."""
    old_version = oraide.__version__

    version_file_path = os.path.join(PROJECT_ROOT, 'oraide/version.py')
    version_pattern = 's/^VERSION = .*$/VERSION = "{0}"/'.format(version)

    history_file_path = os.path.join(PROJECT_ROOT, 'docs/history.rst')
    history_pattern = ("s/.. NEXT_VERSION_HEADER_TARGET/&\\\n"
                       "\\\n\\\n"
                       "Version {0}\\\n"
                       "========{1}/").format(old_version,
                                              len(old_version) * '=')

    run("sed -Ei '.bak' '{0}' {1}".format(version_pattern, version_file_path))
    run("sed -Ei '.bak' '{0}' {1}".format(history_pattern, history_file_path))


ns = Collection()
ns.add_task(increment)
ns.add_collection(Collection.from_module(docs))
