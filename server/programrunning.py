from utilities import *
from random import random
import os
info("[ProgramRunning] module loaded")

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
            if type(content) == list :
                self.content = content
            elif type(content) == str :
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

    def getLine(self, line = -1) :
        if line == -1 :
            line = self.line
        return self.content[line-1]

    def shwCode(self) :
        lined_content = self.content.copy()
        for ind in range(len(lined_content)) :
            line = ind + 1
            lined_content[ind] = str(line) + ' | ' + lined_content[ind]
        return "\n".join(lined_content)

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
        f_name = str(random()) + '.py'
        with open(f_name,'w+') as fileObj:
            fileObj.write("\n".join(self.content))
        data = os.popen('python '+ f_name).read()
        self.content.clear()
        self.flush
        os.remove(f_name)
        return data
