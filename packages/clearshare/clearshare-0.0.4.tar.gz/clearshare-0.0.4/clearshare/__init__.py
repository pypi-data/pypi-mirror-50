# Auto-generated package module by :mod:`datakeeper`.
from os import path
reporoot = path.dirname(path.dirname(__file__))

from datacustodian.datacustodian_app import run, start, stop
from datacustodian.utility import relpath
appspecs = [relpath(s, reporoot) for s in ['docker/specs/api.yml']]
app = run(appspecs=appspecs, norun=True)