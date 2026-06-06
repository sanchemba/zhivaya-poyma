import sys, os

INTERP = os.path.expanduser("~/.venv/python313/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'zhivaya_poyma'))
from zhivaya_poyma.wsgi import application