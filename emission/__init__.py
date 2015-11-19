'''A simple and time consuming method of calculating emission probability'''
import numpy as np
import scipy as scp
import string
import time
import re
# judge whether a sentence has URL
def hasURL(word):
    rt = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',word)
    if rt is not None:
        return True
    else :
        return False
# process words:
# words having only punctuations stay the same
# other words, erase the punctuations
def processWord(word):
# if word has URL, return the word it self
    if hasURL(word) :
        return word
    pword = ''.join(ch for ch in word if ch not in string.punctuation)
    if pword == '':
        pword = word
    return pword.lower()
# process Sentences, separate the sentence into word & tag
def processSentence(line) :
    pline = line.strip().split()
    p0 = processWord(pline[0])
    p1 = pline[1]
    return p0, p1
# preprocess one file with the rule given above, it could improve the result of MLE by 2%
def preprocess(infile,outfile) :
    try:
        inf = open(infile,'r')
        outf = open(outfile, 'w')

        inline = inf.readlines()
        outline = []
        for i in inline:
            if i == '\n' :
                outline.append('\n')
            else :
                i0, i1 = processSentence(i)
                outline.append(i0+' '+i1+'\n')
        outf.writelines(outline)
    except IOError, e:
        print e
        exit(0)
    finally:
        if inf:
            inf.close()
        if outf:
            outf.close()
        return outline
# compute:
#1.the count(y->x) saved in the first returned value with key "x y" in hashing table
#2. the count(y) save with key "y" in the second return value in hashing table
def compute(infile) :
    try:
        # 'hello' 'tag'   matrix["hello tag"]= num
        # matrix[tag][hello] = n
        # labels["tag"] = n
        inf = open(infile,'r')
        inline = inf.readlines()
        matrix = {}
        labels = {}
        for line in inline:
            if line=='\n':
                continue
            line = line.strip().split()
            word = line[0]
            label = line[1]
            if word in matrix:
                if label in matrix[word]:
                    matrix[word][label] += 1
                else :
                    matrix[word][label] = 1
            else:
                matrix[word] = {}
                matrix[word][label] = 1

            if label in labels:
                labels[label] += 1
            else:
                labels[label] = 1
    except IOError, e:
        print e
        exit(0)
    finally:
        if inf:
            inf.close()
        return matrix, labels
# compute the emission probability with the hashing tables get from function compute
def emit(word, tag, matrix, labels,p = True):
    if p:
        word = processWord(word)
    numer = 0
    denom = 0
    if word in matrix:
        if tag in matrix[word]:
            numer = matrix[word][tag]
        else :
            # count zero under this tag
            numer = 0
    else :
        # new word
        numer = 1

    if tag in labels:
        denom = labels[tag]
    else:
        raise RuntimeError("Tag '"+tag+"' not found")

    return numer*1.0/(denom+1.0)
# predict the labels of the input file
def predict(infile, outfile, matrix, labels,p=True):
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
            for tag in labels.keys():
                prob = emit(line,tag,matrix, labels, p)
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
# evaluate the error rate of our prediction
def evaluate(testfile,answerfile):
    # start = time.clock()
    try:
        testf = open(testfile,'r')
        ansf = open(answerfile, 'r')

        test = testf.readlines()
        answer = ansf.readlines()
        i = 0
        error = 0
        total = 0
        if len(answer) != len(test):
            raise RuntimeError("File length different")
        while i<len(answer) and i<len(test):
            # print i,'-th loop\n'
            if test[i]=='\n' and answer[i]=='\n':
                i += 1
                continue
            total += 1
            t = test[i].strip().split()[1]
            a = answer[i].strip().split()[1]
            # print 't:',t
            # print 'a:',a
            if t != a :
                error += 1
            i += 1
    except IOError, e:
        print e
        exit(0)
    finally:
        if testf:
            testf.close()
        if ansf:
            ansf.close()
        # print 'time:',time.clock()-start
        return error*1.0/total
