import re
import string

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
    # if hasURL(word) :
        # return word
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
# evaluate the error rate of our prediction
def evaluate(testfile,answerfile,col=1, pr = False):
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
            word = test[i].strip().split()[0]
            t = test[i].strip().split()[col]
            a = answer[i].strip().split()[1]
            # print 't:',t
            # print 'a:',a
            if t != a :
                error += 1
                if pr:
                    print "i:",i
                    print "word:",word
                    print "t:",t
                    print "a:",a
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
