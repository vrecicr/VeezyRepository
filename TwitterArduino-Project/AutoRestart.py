import subprocess
from subprocess import *
import os
while True:
    try:
        call(["python", "TwitterBrewWifiv2.py"])
        print('Running the Twitter script')
    except:
        print('Something happened, re-running...')
        call(["python", "TwitterBrewWifiv2.py"])