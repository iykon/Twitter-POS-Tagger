import time
import string
import numpy as np
class transition(object):
    def __init__(self):
        self.start = {}
        self.stop = {}
        self.matrix = {}
        self.states = {}
    def compute(self,infile):
        try:
            inf = open(infile,'r')
            inlines = inf.readlines()
            self.start = {}
            self.stop = {}
            self.matrix = {}
            self.states = {}

            START = True
            linenum = len(inlines)
            for i in range(linenum):
                line = inlines[i]
                if START is True:
                    nline = line.strip().split()[1]
                    if nline in self.start:
                        self.start[nline] += 1
                    else :
                        self.start[nline] = 1

                    if 'START' in self.states:
                        self.states['START'] += 1
                    else :
                        self.states['START'] = 1
                    START = False

                if line == '\n':
                    START = True
                else :
                    nnline = line.strip().split()[1]
                    if nnline in self.states:
                        self.states[nnline] += 1
                    else :
                        self.states[nnline] = 1

                    nextline = inlines[i+1]
                    if nextline == '\n':
                        if nnline in self.stop:
                            self.stop[nnline] += 1
                        else :
                            self.stop[nnline] = 1
                    else:
                        ntline = nextline.strip().split()[1]
                        if nnline in self.matrix:
                            if ntline in self.matrix[nnline]:
                                self.matrix[nnline][ntline] += 1
                            else:
                                self.matrix[nnline][ntline] = 1
                        else :
                            self.matrix[nnline] = {}
                            self.matrix[nnline][ntline] = 1
        except IOError, e:
            print e
            exit(0)
        finally :
            if inf:
                inf.close()
    def transit(self,fword,nword) :
        if fword in self.matrix:
            if nword in self.matrix[fword]:
                if fword in self.states:
                    return np.float64(self.matrix[fword][nword]*1.0)/np.float64(self.states[fword])
                else :
                    raise RuntimeError("current tag:"+fword+"\n never occurred in train data")
            else :
                return np.float64(0)
        else :
            return np.float64(0)
    def startwith(self, word) :
        if word in self.start:
            return np.float64(self.start[word]*1.0) / np.float64(self.states['START'])
        else:
            return np.float64(0)
    def stopwith(self, word) :
        if word in self.stop:
            return np.float64(self.stop[word]*1.0)/np.float64(self.states[word])
        else :
            return np.float64(0)
