import string
import time
import toolbox as tool
class emission(object):
    def __init__(self):
        self.matrix = {}
        self.labels = {}
        self.most = None
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
            numer = self.labels[tag]

        if tag in self.labels:
            denom = self.labels[tag]
        else:
            raise RuntimeError("Tag '"+tag+"' not found")

        return numer*1.0/(denom+1.0)
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
# get the label that is most probably to appear, useful when some labels at some point are uncertain (scoreing 0)
    def mostprob(self) :
        if self.most is None:
            prob = 0
            highest = ""
            for i in self.labels:
                if self.labels[i] > prob:
                    prob = self.labels[i]
                    highest = i
            self.most = highest
        return self.most
# compute the likelihood of a prediction:
    def likelihood(self,lines,p=True,col=1):
        total = 0
        sentence = 0
        num = 0
        for i in lines:
            if i=='\n':
                total+= sentence
                sentence = 0
            else:
                num += 1
                i = i.strip()
                lst = i.split()
                word = lst[0]
                tag = lst[col]
                sentence += self.emit(word, tag, p)
        return 1.0*total/num
    def filelikelihood(self,infile,p=True, col=1):
        try:
            inf = open(infile,"r")
            line = inf.readlines()
            total = self.likelihood(line, p, col)
        except IOError, e:
            print e
            exit(0)
        finally:
            if inf:
                inf.close()
            return total