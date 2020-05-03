from utilities import *
from random import random
import os
import re
info("[ProgramRunning] module loaded")

class PyExec(object):
    """run python"""
    def __init__(self, qid):
        self.f_name = str(qid)
        self.cmd_list=[]
        self.pcmds={
            '/a':'AddCmd',
            '/d':'DelCmd',
            '/v':'GetCode',
            '/c':'ChangeCode',
            '/r':'RunCmd',
            '/l':'Clear'
        }

    def exe(self, msg) :
        catch = catch.command(msg)
        if catch in self.pcmds :
            cmd = re.sub(r'^\w *', '', msg)
            if catch == '/c':
                pass
            elif catch == '/a' or catch == '/d':
                cmd = 'self.' + self.pcmds[catch] + '(r"' + re.sub('\"', '\\"', cmd) + '")'
            else:
                cmd = 'self.' + self.pcmds[catch] + '(' + str(re.sub('\"', '\\"', cmd)) + ')'
            data = eval(cmd)
            print(self.cmd_list)
            print(data)
            self.save()
            return data
        else:
            return ''

    def save(self):
        with open('./../db/'+self.f_name,'w') as fileObj:
            for cmd in self.cmd_list:
                print(cmd)
                fileObj.write(cmd+'\n')

    def AddCmd(self, cmd):
        '''
        Add a command to .py file
        '''
        info('Add cmd: ' + cmd)
        self.cmd_list.append(cmd)

    def DelCmd(self, m):
        '''
        Delete a command
        '''
        if m < len(self.cmd_list):
            info('Delete cmd at line '+str(m)+':'+self.cmd_list[m])
            self.cmd_list.pop(m)
            return True
        else:
            return False

    def GetCode(self):
        '''
        Get command dictionary
        '''
        info('Get Python Code')
        with open('./../db/'+self.f_name,'rb') as fileObj:
            data=fileObj.read()
        return data

    def ChangeCode(self, m,cmd):
        '''
        Change command at line m
        '''
        if m <len(self.cmd_list):
            info('Change Command:' + self.cmd_list[m] + ' line:'+str(m)+' to ' + cmd)
            self.cmd_list.pop(m)
            self.cmd_list.insert(m,cmd)
            return True
        else:
            return False

    def RunCmd(self):
        '''
        Run python
        '''
        info('Running python')
        info('Creating python file:'+self.f_name)
        os.system('python {f} >> {f}.txt'.format(f='./../db/'+self.f_name))
        with open('./../db/'+self.f_name+'.txt','rb') as fileObj:
            data=fileObj.read()
        return data

    def Clear(self):
        self.cmd_list=[]
        os.remove(self.f_name)
        os.remove(self.f_name+'.txt')
