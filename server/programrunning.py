from utilities import *
from random import random
import os
info("[ProgramRunning] module loaded")

cmd_dic={}
n=0
def AddCmd(cmd):
    '''
    Add a command to .py file
    '''
    info('Add cmd: ' + cmd)
    global n
    cmd_dic[n]=cmd
    n+=1

def DelCmd(m):
    '''
    Delete a command
    '''
    if m in cmd_dic:
        info('Delete cmd at line '+str(m)+':'+cmd_dic[m])
        del cmd_dic[m]
        return True
    else:
        return False

def GetCode():
    '''
    Get command dictionary
    '''
    info('Get Python Code')
    return cmd_dic

def ChangeCode(m,cmd):
    '''
    Change command at line m
    '''
    if m in cmd_dic:
        info('Change Command:' + cmd_dic[m] +' to ' + cmd)
        cmd_dic[m]=cmd
        return True
    else:
        return False

def RunCmd():
    '''
    Run python
    '''
    info('Running python')
    f_name = str(random()) + '.py'
    info('Creating python file:'+f_name)
    with open(f_name,'w') as fileObj:
        for key in cmd_dic:
            fileObj.write(cmd_dic[key]+'\n')
    os.system('python {f} >> {f}.txt'.format(f=f_name))
    with open(f_name+'.txt','rb') as fileObj:
        data=fileObj.read()
    cmd_dic.clear()
    n=0
    os.system('del '+f_name)
    os.system('del '+f_name+'.txt')
    return data