import emission as em
import toolbox as tool
import transition as tr
import time
# This class could maintain the N-best route to one possible tag at one position
class worditem(object):
    def __init__(self, llword ,lword, score, path):
        self.llword = llword
        self.lword = lword
        self.score = score
        self.path = path

class NBest(object):
    def __init__(self, n):
        self.elements=[None,]
        self.N = n
# add new tag, its probability and number into the array
# maintain this entire array with a heap
    def add(self,llword , lword, score, path):
        a = worditem(llword, lword, score, path)
        self.elements.append(a)
        i = len(self.elements)-1
        while self.elements[i/2] is not None and self.elements[i/2].score<a.score:
            self.elements[i] = self.elements[i/2]
            i = i/2
        self.elements[i] = a
    def deleteMax(self) :
        a = self.elements[1]
        b = self.elements.pop()
        i = 1;
        while i*2<len(self.elements):
            child = i*2
            if child+1<len(self.elements) and self.elements[child+1].score>self.elements[child].score:
                child+=1
            if self.elements[child].score > b.score:
                self.elements[i] = self.elements[child]
            else:
                break;
            i = child
# avoid indexing zero
        if i<len(self.elements):
            self.elements[i] = b
        return a
# get the first N from them
    def best(self):
        belement = []
        i = 1
        while i<=self.N and len(self.elements)>1:
            belement.append(self.deleteMax())
            i+=1
        self.elements = belement
        while len(self.elements) < self.N:
            self.elements.append(self.elements[-1])
# get the first i-th label in the array
    def pop(self,i):
        return self.elements.pop(i)

# this algorihtm calculates first N best paths
def viterbi_Nbest(e, t, infile, outfile, best=10, p=True):
    try:
        inf = open(infile, 'r')
        outf = open(outfile, 'w')
        START = True
        SECSTART = True
        inlines = inf.readlines()
        count = range(len(inlines))
        matrix = []
        outlines = []
        for i in count:
            line = inlines[i]
            # calculate all possible tags and its score and which path of previous tag this path comes from
            if START is True and SECSTART is True:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = 1.0*t.transit('START','START',tag) * e.emit(word, tag, p)
                matrix.append(tags)
                START = False
            elif START is False and SECSTART is True:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = {}
                    for lword in e.labels:
                        tags[tag][lword] = 1.0*t.transit('START',lword,tag) * e.emit(word,tag,p)
                matrix.append(tags)
                SECSTART = False
            elif line == '\n':
                START = True
                SECSTART = True
                nb = NBest(best)
                for lword in e.labels:
                    # sentence having no words
                    if isinstance(matrix[i-1],NBest):
                        raise RuntimeError("Sentence has no words")
                    # sentence havine only one word
                    elif isinstance(matrix[i-1][lword],float):
                        prob = 1.0 * matrix[i-1][lword]*t.transit('START',lword,'STOP')
                        nb.add('START',lword,prob,-1)
                    # more than one word
                    else :
                        for llword in e.labels:
                            # sentence has only two words
                            if isinstance(matrix[i-1][lword][llword],float):
                                prob = 1.0*matrix[i-1][lword][llword]*t.transit(llword,lword,'STOP')
                                nb.add(llword,lword,prob,-1)
                            # sentence has more than two words
                            else :
                                b = matrix[i-1][lword][llword]
                                for j in range(len(b.elements)):
                                    prob = 1.0*b.elements[j].score * t.transit(llword,lword,'STOP')
                                    nb.add(llword,lword,prob,j)
                nb.best()
                matrix.append(nb)
                # print "end sentence:",nb.elements[0].word,"score:",nb.elements[0].score, "from:",nb.elements[0].path
                matrix.append(nb)
            else:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    nb = NBest(best)
                    for lword in e.labels:
                        for llword in e.labels:
                            # third word in the sentence
                            if isinstance(matrix[i-1][lword][llword],float) :
                                prob = 1.0*matrix[i-1][lword][llword]*t.transit(llword,lword,tag)*e.emit(word,tag,p)
                                nb.add(llword,lword,prob,-1)
                            # after the third word in the sentence
                            else :
                                b = matrix[i-1][lword][llword]
                                for j in range(len(b.elements)):
                                    prob = 1.0*b.elements[j].score*t.transit(llword,lword,tag)*e.emit(word,tag,p)
                                    nb.add(llword, lword, prob, j)
                    nb.best()
                    # print "******chosen:",nb.elements[0].word,"-->",tag,":",nb.elements[0].score
                    tags[tag] = nb
                matrix.append(tags)
        # decode the sentence
        # print "DECODING"
        count.reverse()
        lastelement = []
        for i in count:
            line = inlines[i]
            # end of a sentence, get all the final tags
            if line == '\n':
                nb = matrix[i]
                lastelement = nb.elements
                outlines.append('\n')

                # print "endsentence:",lastelement[0].word, "score:",lastelement[0].score, "from:" ,lastelement[0].path
            # in the sentence, extract all current tags from the result stored in the position behind
            else:
                currentlastelement = []
                word = line.strip()
                cnt = range(len(lastelement))
                for j in cnt:
                    llw = lastelement[j].llword
                    lw = lastelement[j].lword
                    nm = lastelement[j].path
                    scr = lastelement[j].score
                    if isinstance(matrix[i-1][lw],float)
                    if scr == 0:
                        lw = e.mostprob()
                    word = word + ' ' + lw

                    # print "word:",word
                    nb = matrix[i][lw]
                    if isinstance(nb, float):
                        # the first word in a sentence, do nothing
                        continue
                    else:
                        # get the tags of previous position
                        currentlastelement.append(nb.elements[nm])
                        # print j,"-th, within sentence:",currentlastelement[0].word, "score:",currentlastelement[0].score, "from:", currentlastelement[0].path
                lastelement = currentlastelement
                word += '\n'
                outlines.append(word)
        outlines.reverse()
        outf.writelines(outlines)
    except IOError, error:
        print error
        exit(0)
    finally:
        if inf:
            inf.close()
        if outf:
            outf.close()
def main():
    tool.preprocess('../data/POS/train', '../data/POS/ptrain')
    tool.preprocess('../data/NPC/train', '../data/NPC/ptrain')

    e0 = em.emission()
    t0 = tr.transition()
    print "without preprocessor"
    e0.compute('../data/POS/train')
    t0.compute('../data/POS/train')
    e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out',p=False)
    print "POS,MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
    print "POS,MLE likelihood:", e0.filelikelihood("../data/POS/dev.p2.out",p=False)
    viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out',p=False)
    print "POS,DP:", tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
    print "POS,DP likelihood:", e0.filelikelihood("../data/POS/dev.p3.out", p=False)
    start = time.clock()
    viterbi_Nbest(e0, t0, '../data/POS/dev.in', '../data/POS/dev.p4.out', best=10, p=False)
    print "runtime:",time.clock()-start
    c = 1
    while c<=10:
        print c,":POS, DP2:", tool.evaluate('../data/POS/dev.p4.out', '../data/POS/dev.out',col=c)
        print c,":POS, DP2 likelihood:", e0.filelikelihood("../data/POS/dev.p4.out",p=False, col=c)
        c+=1

    print "with preprocessor"
    e0.compute('../data/POS/ptrain')
    t0.compute('../data/POS/ptrain')
    e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out')
    print "POS, MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
    print "POS, MLE, likelihood:",e0.filelikelihood("../data/POS/dev.p2.out")
    viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out')
    print "POS, DP:",tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
    print "POS, DP likelihood:", e0.filelikelihood("../data/POS/dev.p3.out")
    start = time.clock()
    viterbi_Nbest(e0, t0, '../data/POS/dev.in', '../data/POS/dev.p4.out', best=10)
    print "runtime:",time.clock() - start
    c = 1
    while c <= 10:
        print c,":POS, DP2:", tool.evaluate('../data/POS/dev.p4.out', '../data/POS/dev.out',col=c)
        print c,":POS, DP2 likelihood:", e0.filelikelihood("../data/POS/dev.p4.out",col=c)
        c += 1

    e1 = em.emission()
    t1 = tr.transition()
    print "without preprocessor"
    e1.compute('../data/NPC/train')
    t1.compute('../data/NPC/train')
    e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out',p=False)
    print "NPC,MLE:", tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    print "NPC,MLE likelihood:", e1.filelikelihood("../data/NPC/dev.p2.out",p=False)
    viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out',p=False)
    print "NPC,DP:", tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    print "NPC,DP likelihood:", e1.filelikelihood("../data/NPC/dev.p3.out",p=False)
    start = time.clock()
    viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=10, p=False)
    print "runtime:",time.clock() - start
    c = 1
    while c <= 10:
        print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        print c,":NPC, DP2 likelihood:", e1.filelikelihood("../data/NPC/dev.p4.out",p=False, col=c)
        c += 1

    print "with preprocessor"
    e1.compute('../data/NPC/ptrain')
    t1.compute('../data/NPC/ptrain')
    e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out')
    print 'NPC, MLE:', tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    print "NPC, MLE likelihood:", e1.filelikelihood("../data/NPC/dev.p2.out")
    viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out')
    print 'NPC, DP:',tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    print "NPC, DP likelihood:", e1.filelikelihood("../data/NPC/dev.p3.out")
    start = time.clock()
    viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=10)
    print "runtime:",time.clock()-start
    c = 1
    while c <= 10:
        print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        print c,":NPC, DP2 likelihood:", e1.filelikelihood("../data/NPC/dev.p4.out",col=c)
        c += 1
if __name__ == '__main__':
    main()
