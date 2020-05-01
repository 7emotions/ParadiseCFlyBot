from utilities import *
from random import random
import os
info("[ProgramRunning] module loaded")

def execute(cmd) :
    '''
    run a command
    '''
    info('Running :'+cmd)
    return os.popen(cmd).read()

def pyExec(py_cmd):
    '''
    run a python command
    '''
    info('Running python: '+py_cmd)
    f_name = str(random()) + '.py'
    py_cmd = py_cmd.replace("\"", '\\"')#.replace("'", "\\'")
    run_cmd = '''
echo """
''' + py_cmd + '''
""" > ''' + f_name + '''
python ''' + f_name + '''
rm ''' + f_name + '''
    '''
    return execute(run_cmd)
