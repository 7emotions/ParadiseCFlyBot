from utilities import *
from random import random
import os
info("[ProgramRunning] module loaded")

'''
cmd_dic={}
n=0
def AddCmd(cmd):
    '''
    Add a command to .py file
    '''
    n += 1
    info('Add cmd: ' + cmd + 'at line ' + str(n))
    global n
    cmd_dic[n] = cmd

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
    n = 0
    os.system('del '+f_name)
    os.system('del '+f_name+'.txt')
    return data
'''

class ProgramRunning(object):
    '''
    Program Running
    '''

    # file content
    content = []

    # number of lines
    line = 0

    def __init__(self, content = ''):
        super(ProgramRunning, self).__init__()
        if content :
            self.content = [content]
            self.flush()

    def flush(self) :
        '''
        Flush content

        Returns:
            {list} : content after flush
        '''
        self.line = len(self.content)
        for ind in range(len(self.content)):
            line = ind + 1
            if "\n" in self.getLine(line) :
                con = self.getLine(line).split("\n")
                self.delLine(line, False)
                for x in range(len(con)) :
                    self.insLine(con[x], line + x, False)
            self.line = len(self.content)
        return self.content

    def getLine(self, line = -1):
        if line == -1 :
            line = self.line
        return self.content[line-1]

    def insLine(self, content = '', line = -1, flush = True) :
        '''
        insert code at someline
        '''
        if line == -1 :
            line = self.line + 1

        self.content.insert(line - 1, content)
        if flush :
            self.flush()
        return self.content

    def delLine(self, line = -1, flush = True) :
        '''
        Delete code at some line

        Args:
            line {int} : line of command, if not given, the last line will be deleted
        Returns:
            {bool|list} : delete status

        '''
        if line > self.line or line == -1 :
            return False

        # contents that before the line
        before = self.content[0: line]
        # contents that after the line
        after = self.content[line: self.line]
        before.pop()
        self.content = before + after
        if flush :
            self.flush()
        return self.content

    def edtLine(self, line, content = '') :
        '''
        edit the content of a line
        '''
        self.delLine(line)
        self.insLine(content, line)
        return self.content

    def run(self) :
        '''
        TODO : run code
        '''
