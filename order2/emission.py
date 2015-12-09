import string
import time
import toolbox as tool
class emission(object):
    def __init__(self):
        self.matrix = {}
        self.labels = {}
        self.freq = {}
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
            for word in self.matrix:
                for tag in self.matrix[word]:
                    if tag not in self.freq:
                        self.freq[tag]={}
                    if str(self.matrix[word][tag]) not in self.freq[tag]:
                        self.freq[tag][str(self.matrix[word][tag])] = 1
                    else:
                        self.freq[tag][str(self.matrix[word][tag])] += 1
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
        # if tag in self.matrix:
            # if word in self.matrix[tag]:
                # numer = self.matrix[tag][word]
                # return 1.0*numer / self.labels[tag]
            # elif str(1) in self.freq[tag]:
                # numer = self.freq[tag]["1"]
                # if numer == self.labels[tag]:
                    # return self.labels[tag]*1.0/(self.labels[tag]+1.0)
                # else:
                    # return 1.0*numer/self.labels[tag]
            # else:
                # return self.labels[tag]*1.0/(self.labels[tag]+1.0)

        if word in self.matrix:
            if tag in self.matrix[word]:
                numer = self.matrix[word][tag] - 0.75
            else :
                # count zero under this tag
                numer = 0
        else :
            # new word
            # self.new += 1
            # numer = self.labels[tag]
            if "1" in self.freq[tag]:
                numer = self.freq[tag]["1"]
            else:
                numer = 0

        if tag in self.labels:
            denom = self.labels[tag]
        else:
            raise RuntimeError("Tag '"+tag+"' not found")

        return numer*1.0/denom
    # predict the labels of the input file
    def predict(self, infile, outfile, p=True):
        # start=time.clock()
        try:
            inf = open(infile,'r')
            outf = open(outfile, 'w')
            inline = inf.readlines()
            writeline = []
            for line in inline:
                # print len(line)
                # print line
                if line == '\n' or line=='\r\n':
                    writeline.append('\n')
                    continue
                line = line.strip('\n')
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
    def newword(self,infile, outfile) :
        inf = open(infile, 'r')
        outf = open(outfile,'w')

        inline = inf.readlines()
        outline = []
        length = len(inline)
        new = 0
        for i in range(length) :
            word = inline[i]
            if(word=='\n'):
                continue
            else:
                word = word.strip()
                if word not in self.matrix:
                    new = new +1
                    outline.append(str(i))
        outf.writelines(outline)
        inf.close()
        outf.close()
        return new, outline


