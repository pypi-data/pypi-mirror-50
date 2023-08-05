# Auto-generated package module by :mod:`datakeeper`.
import logging
from os import path, environ
log = log = logging.getLogger(__name__)
reporoot = path.abspath(path.expanduser(environ.get("CLEARSHARE_HOME", '.')))
log.info("Using %s as the home directory for clearshare.", reporoot)

from datacustodian.datacustodian_app import run, start, stop
from datacustodian.utility import relpath
appspecs = [relpath(s, reporoot) for s in ['docker/specs/api.yml']]
log.info("Initializing API with specifications at %r", appspecs)
app = run(appspecs=appspecs, norun=True)
