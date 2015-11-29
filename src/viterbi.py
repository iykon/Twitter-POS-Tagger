import emission as em
import toolbox as tool
import transition as tr
import time
# This class could maintain the N-best route to one possible tag at one position
class worditem(object):
    def __init__(self, word, prob, m):
        self.word = word
        self.score = prob
        self.path = m
class NBest(object):
    def __init__(self, n):
        self.elements=[None,]
        self.N = n
# add new tag, its probability and number into the array
# maintain this entire array with a heap
    def add(self, word, prob, m):
        a = worditem(word,prob,m)
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
# get the first i-th label in the array
    def pop(self,i):
        return self.elements.pop(i)
# the algorithm to get the best 1 path, deprecated, there exists one more general method, see viterbi_NBest
def viterbi_best(e, t, infile, outfile, p=True):
    try:
        inf = open(infile, 'r')
        outf = open(outfile, 'w')
        inlines = inf.readlines()
        START = True

        matrix = []
        path = []

        rg = range(len(inlines))
        for i in rg:
            # print "loop:",i
            line = inlines[i]
            tags = {}
            if START:
                # print "START"
                word = line.strip()
                for tag in e.labels.keys():
                    tags[tag] = t.startwith(tag) * e.emit(word, tag, p)
                # print tags
                matrix.append(tags)
                path.append(None)
                START = False
            elif line == '\n':
                # print "STOP"
                bestprob = 0
                endtag = ""
                for tag in e.labels.keys():
                    tags[tag] = t.stopwith(tag) * matrix[i - 1][tag]
                    if tags[tag] >= bestprob:
                        bestprob = tags[tag]
                        endtag = tag
                # print "endsentence:",endtag," score:",bestprob
                # print i,":",bestprob
                # print endtag,":",bestprob
                # print "best score of this sentence:", bestprob
                # print bestprob.hex()
                # print "type:",type(bestprob)
                matrix.append(tags)
                path.append(endtag)
                START = True
            else:
                # print "in sentence"
                word = line.strip()
                # print "word:",word
                fromtag = {}
                for tag in e.labels.keys():
                    for ftag in e.labels.keys():
                        prob = matrix[i - 1][ftag] * t.transit(ftag, tag) * e.emit(word, tag, p)
                        # print ftag,"-->",tag,":",prob
                        if tag not in tags:
                            tags[tag] = prob
                            fromtag[tag] = ftag
                        elif tags[tag] <= prob:
                            tags[tag] = prob
                            fromtag[tag] = ftag
                    # print "after compute:"
                    # print "*****chosen:",fromtag[tag],"-->",tag,":",tags[tag] 
                # print tags
                # print fromtag
                matrix.append(tags)
                path.append(fromtag)

        rg.reverse()
        finalpath = []
        lasttag = ""
        for i in rg:
            if inlines[i] == '\n':
                if isinstance(path[i], str):
                    lasttag = path[i]
                    # print "i:",i
                    # print "end sentence:"
                    # print "tag:", lasttag
                    # print "score:",matrix[i][lasttag]
                    # print "endsentence:",lasttag, "   score:", matrix[i][lasttag]
                    # print "score:",matrix[i][lasttag].hex()
                    # print "type:", type(matrix[i][lasttag])
                    finalpath.append(lasttag)
                else:
                    raise RuntimeError("endtag must be determined")
            elif path[i] is not None:
                word = inlines[i].strip()
                if isinstance(path[i], dict):
                    lasttag = path[i][lasttag]
                    # print "within sentence:", lasttag, "   score:",matrix[i][lasttag]
                    # print "in sentence:"
                    # print "tag: ", lasttag
                    # print "score:", matrix[i][lasttag]
                    # print "score: ", matrix[i][lasttag].hex()
                    # print "type:" , type(matrix[i][lasttag])
                    finalpath.append(lasttag)
                else:
                    raise RuntimeError("in text must correspond to a dict")
        outlines = []
        for line in inlines:
            if line == '\n':
                outlines.append('\n')
                continue
            else:
                word = line.strip()
                tag = finalpath.pop()
                outlines.append(word + " " + tag + "\n")
        outf.writelines(outlines)
    except IOError, e:
        print e
        exit(0)
    finally:
        if inf:
            inf.close()
        if outf:
            outf.close()

# this algorihtm calculates first N best paths
def viterbi_Nbest(e, t, infile, outfile, best=10, p=True):
    try:
        inf = open(infile, 'r')
        outf = open(outfile, 'w')
        START = True
        inlines = inf.readlines()
        count = range(len(inlines))
        matrix = []
        outlines = []
        for i in count:
            line = inlines[i]
            # calculate all possible tags and its score and which path of previous tag this path comes from
            if START is True:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = 1.0*t.startwith(tag) * e.emit(word, tag, p)
                matrix.append(tags)
                START = False
            elif line == '\n':
                START = True
                nb = NBest(best)
                for tag in e.labels:
                    if isinstance(matrix[i - 1][tag], float):
                        raise RuntimeError("Sentence has no words")
                    else:
                        b = matrix[i - 1][tag]
                        for j in range(len(b.elements)):
                            prob = b.elements[j].score * t.stopwith(tag)
                            nb.add(tag, prob,j)
                nb.best()
                # print "end sentence:",nb.elements[0].word,"score:",nb.elements[0].score, "from:",nb.elements[0].path
                matrix.append(nb)
            else:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    nb = NBest(best)
                    for ftag in e.labels:
                        # case 1
                        # the second word in the sentence
                        if isinstance(matrix[i - 1][ftag], float):
                            prob = matrix[i - 1][ftag] * t.transit(ftag, tag) * e.emit(word, tag, p)
                            nb.add(ftag, prob,-1)
                        # case 2
                        # from the third word of the sentence
                        else:
                            b = matrix[i - 1][ftag]
                            for j in range(len(b.elements)):
                                prob = b.elements[j].score * t.transit(ftag, tag) * e.emit(word, tag, p)
                                # print ftag,"-->",tag,":", prob
                                nb.add(ftag, prob,j)
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
                    lw = lastelement[j].word
                    nm = lastelement[j].path
                    scr = lastelement[j].score
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
    viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out',p=False)
    print "POS,DP:", tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
    start = time.clock()
    viterbi_Nbest(e0, t0, '../data/POS/dev.in', '../data/POS/dev.p4.out', best=10, p=False)
    print "runtime:",time.clock()-start
    c = 1
    while c<=10:
        print c,":POS, DP2:", tool.evaluate('../data/POS/dev.p4.out', '../data/POS/dev.out',col=c)
        c+=1

    print "with preprocessor"
    e0.compute('../data/POS/ptrain')
    t0.compute('../data/POS/ptrain')
    e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out')
    print "POS, MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
    viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out')
    print "POS, DP:",tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
    start = time.clock()
    viterbi_Nbest(e0, t0, '../data/POS/dev.in', '../data/POS/dev.p4.out', best=10)
    print "runtime:",time.clock() - start
    c = 1
    while c <= 10:
        print c,":POS, DP2:", tool.evaluate('../data/POS/dev.p4.out', '../data/POS/dev.out',col=c)
        c += 1

    e1 = em.emission()
    t1 = tr.transition()
    print "without preprocessor"
    e1.compute('../data/NPC/train')
    t1.compute('../data/NPC/train')
    e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out',p=False)
    print "NPC,MLE:", tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out',p=False)
    print "NPC,DP:", tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    start = time.clock()
    viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=10, p=False)
    print "runtime:",time.clock() - start
    c = 1
    while c <= 10:
        print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        c += 1

    print "with preprocessor"
    e1.compute('../data/NPC/ptrain')
    t1.compute('../data/NPC/ptrain')
    e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out')
    print 'NPC, MLE:', tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out')
    print 'NPC, DP:',tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    start = time.clock()
    viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=10)
    print "runtime:",time.clock()-start
    c = 1
    while c <= 10:
        print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        c += 1
if __name__ == '__main__':
    main()
