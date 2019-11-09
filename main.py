import time
from subprocess import Popen
import sys


Popen([sys.executable, 'Parser.py']).wait()
Popen([sys.executable, 'SemantAnalisys.py']).wait()
Popen([sys.executable, 'run.py'])
timing = time.time()
while True:
    if time.time() - timing > 300.0:
        Popen([sys.executable, 'Parser.py']).wait()
        Popen([sys.executable, 'SemantAnalisys.py']).wait()
        timing = time.time()