#!/usr/bin/python
# -*- coding:utf8 -*-
from utilities import *
from random import random
import re
import os
import json
info("[ProgramRunning] module loaded")

pcmds = [
    '/get',
    '/flush',
    '/del',
    '/ist',
    '/edt',
    '/run',
    '/fetch',
    '/clear'
]


def command(msg) :
    catch = re.match(r'\/\w+', msg)
    if catch :
        catch = catch.group()
        info('Catched command: ' + catch)
        if catch in pcmds :
            return catch
    return False


def _(qid, msg) :
    qid = str(qid)
    program = ProgramRunning(qid)
    cmd = command(msg)
    data = analyze(msg)
    if cmd == '/flush' :
        program.flush()
    elif cmd == '/get' :
        return program.getLine(data['line'])
    elif cmd == '/ist' :
        program.insLine(data['content'], data['line'])
    elif cmd == '/del' :
        program.delLine(data['line'])
    elif cmd == '/edt' :
        program.edtLine(data['line'], data['content'])
    elif cmd == '/run' :
        return program.run()
    elif cmd == '/fetch' :
        return program.fetch()
    elif cmd == '/clear' :
        program.clear()
    return program.shwCode()
    program.store()

def analyze(msg) :
    '''
    analyzing command

    Returns:
        {dict} : {'line': {int}|False, 'content': {string}}
    '''
    line = re.search(r'(?<=\/\w{3,3} )[0-9]+(?= .*)?', msg)
    if not line :
        line = False
        content = re.sub(r'^\/\w+ ', '', msg)
    else :
        line = int(line.group())
        content = re.sub(r'^\/\w+ %s '%(line), '', msg)
    return {'line': line, 'content': content}

class ProgramRunning(object):
    '''
    Program Running
    '''

    # file content
    content = []

    # number of lines
    line = 0

    #file name
    fname = 'null'

    def __init__(self, fname = 'null', content = ''):
        super(ProgramRunning, self).__init__()
        self.fname = './../db/' + fname + '.json'
        if content :
            if type(content) == str :
                self.content = [content]
            elif type(content) == list :
                self.content = content
        else :
            old_data = self.fetch()
            if old_data :
                self.content = old_data
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
        self.store()
        return self.content

    def getLine(self, line = False) :
        if not line :
            line = self.line
        if line == 0 :
            return ''
        return self.content[line-1]

    def shwCode(self, format = True) :
        lined_content = self.content.copy()
        if format :
            for ind in range(len(lined_content)) :
                line = ind + 1
                lined_content[ind] = str(line) + ' | ' + lined_content[ind]
        return "\n".join(lined_content)

    def insLine(self, content = '', line = False, flush = True) :
        '''
        insert code at someline
        '''
        if not line :
            line = self.line + 1

        self.content.insert(line - 1, content)
        if flush :
            self.flush()
        return self.content

    def delLine(self, line = False, flush = True) :
        '''
        Delete code at some line

        Args:
            line {int} : line of command, if not given, the last line will be deleted
        Returns:
            {bool|list} : delete status

        '''
        if line > self.line :
            return False
        elif not line :
            line = self.line

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
        run code
        '''
        f_name = self.fname + '.py'
        with open(f_name,'w+') as fileObj:
            fileObj.write("\n".join(self.content))
        data = execute('python '+ f_name)
        if os.path.exists(f_name) :
            os.remove(f_name)
        self.flush()
        return data

    def store(self) :
        '''
        storing data
        '''
        f = open(self.fname, 'w+')
        f.write(json.dumps(self.content))
        f.close()

    def fetch(self) :
        fname = self.fname
        if os.path.exists(fname) :
            f = open(fname, 'r')
            return json.loads(f.read())
        else :
            return False

    def clear(self) :
        fname = self.fname
        self.content = []
        if os.path.exists(fname) :
            os.remove(fname)
        return self.flush()
