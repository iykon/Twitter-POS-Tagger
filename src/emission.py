'''A simple and time consuming method of calculating emission probability'''
import string
import time
import toolbox as tool
import numpy as np
class emission(object):
    def __init__(self):
        self.matrix = {}
        self.labels = {}
    # compute:
    #1.the count(y->x) saved in the first returned value with key "x y" in hashing table
    #2. the count(y) save with key "y" in the second return value in hashing table
    def compute(self,infile) :
        try:
            # 'hello' 'tag'   matrix["hello tag"]= num
            # matrix[tag][hello] = n
            # labels["tag"] = n
            inf = open(infile,'r')
            inline = inf.readlines()
            self.matrix = {}
            self.labels = {}
            for line in inline:
                if line=='\n':
                    continue
                line = line.strip().split()
                word = line[0]
                label = line[1]
                if word in self.matrix:
                    if label in self.matrix[word]:
                        self.matrix[word][label] += 1
                    else :
                        self.matrix[word][label] = 1
                else:
                    self.matrix[word] = {}
                    self.matrix[word][label] = 1

                if label in self.labels:
                    self.labels[label] += 1
                else:
                    self.labels[label] = 1
        except IOError, e:
            print e
            exit(0)
        finally:
            if inf:
                inf.close()
    # compute the emission probability with the hashing tables get from function compute
    def emit(self,word, tag,p=True):
        if p:
            word = tool.processWord(word)

        numer = 0
        denom = 0
        if word in self.matrix:
            if tag in self.matrix[word]:
                numer = self.matrix[word][tag]
            else :
                # count zero under this tag
                numer = 0
        else :
            # new word
            numer = 1

        if tag in self.labels:
            denom = self.labels[tag]
        else:
            raise RuntimeError("Tag '"+tag+"' not found")

        return np.float64(numer*1.0)/np.float64(denom+1.0)
    # predict the labels of the input file
    def predict(self, infile, outfile, p=True):
        # start=time.clock()
        try:
            inf = open(infile,'r')
            outf = open(outfile, 'w')
            inline = inf.readlines()
            writeline = []
            for line in inline:
                if line == '\n':
                    writeline.append('\n')
                    continue
                line = line.strip()
                bestprob = 0
                besttag = ""
                for tag in self.labels.keys():
                    prob = self.emit(line,tag,p)
                    if prob>bestprob:
                        bestprob=prob
                        besttag=tag
                # print 'word:',line
                # print 'best tag:',besttag
                # print 'prob:',bestprob
                writeline.append(line+' '+besttag+'\n')
            outf.writelines(writeline)
        except IOError, e:
            print e
            exit(0)
        finally:
            if inf:
                inf.close()
            if outf:
                outf.close()
            # print 'time:',time.clock() - start
