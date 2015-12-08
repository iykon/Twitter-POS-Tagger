import time
import string
class tri_transition(object):
    def __init__(self):
        self.matrix = {}
        self.states = {}
    def add(self, llword, lword, tag):
        if llword not in self.matrix:
            self.matrix[llword]={}
        if lword not in self.matrix[llword]:
            self.matrix[llword][lword] = {}
        if tag not in self.matrix[llword][lword]:
            self.matrix[llword][lword][tag] = 1
        else :
            self.matrix[llword][lword][tag] += 1

        if llword not in self.states:
            self.states[llword] = {}
        if lword not in self.states[llword]:
            self.states[llword][lword] = 1
        else :
            self.states[llword][lword] += 1
# compute the parameters within the given file
    def compute(self,infile):
        try:
            inf = open(infile,'r')
            inlines = inf.readlines()
            self.matrix = {}
            self.states = {}
            llword = ""
            lword = ""

            START = True
            SECSTART = True
            linenum = len(inlines)
            for i in range(linenum):
                line = inlines[i]
                if START is True and SECSTART is True:
                    tag = line.strip().split()[1]
                    self.add('START','START',tag)
                    lword = tag
                    START = False
                elif START is False and SECSTART is True:
                    tag = line.strip().split()[1]
                    self.add('START',lword,tag)
                    llword = lword
                    lword = tag
                    SECSTART = False
                elif line == '\n':
                    self.add(llword,lword,'STOP')
                    START = True
                    SECSTART = True
                else :
                    tag = line.strip().split()[1]
                    self.add(llword,lword,tag)
                    llword = lword
                    lword = tag
        except IOError, e:
            print e
            exit(0)
        finally :
            if inf:
                inf.close()
# within a sentence, calculate the probability that nword is transitioned from fword
    def transit(self,llword,lword,word) :
        if llword not in self.matrix:
            # print "transit 0:", llword,",",lword, "-->", word
            return 0
        if lword not in self.matrix[llword]:
            # print "transit 0:", llword,",",lword,"-->",word
            return 0
        if word not in self.matrix[llword][lword]:
            # print "transit 0:", llword,",",lword,"-->",word
            return 0
        else:
            # print "transit ", self.matrix[llword][lword][word]*1.0/self.states[llword][lword],llword,",",lword,"-->",word
            return self.matrix[llword][lword][word]*1.0/self.states[llword][lword]
