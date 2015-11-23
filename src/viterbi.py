import emission as em
import toolbox as tool
import transition as tr
import time
import numpy as np

class NBest(object):
    def __init__(self, n):
        self.label = []
        self.score = []
        self.args = []
        self.num = []
        self.N = n

    def add(self, word, prob, m):
        self.label.append(word)
        self.score.append(prob)
        self.num.append(m)

    def best(self):

        # print "when compute"
        # print "label:",self.label
        # print "score:",self.score

        # temp = np.array(self.score)
        # print "temp:",temp
        # print "args:",self.args
        # print "temp argsort", temp.argsort()
        self.args = np.argsort(self.score)[-self.N:]
        # print "args:",self.args

        blabel = []
        bscore = []
        bnum = []
        for i in self.args:
            # print i,"-th loop when compute"
            # print 'label:',self.label[i]
            # print 'score:',self.score[i]
            blabel.append(self.label[i])
            bscore.append(self.score[i])
            bnum.append(self.num[i])
        blabel.reverse()
        bscore.reverse()
        bnum.reverse()
        self.label = blabel
        self.score = bscore
        self.num = bnum
        # print 'labels:',self.label
        # print 'scores:',self.score

    def pop(self,i):
        return self.label.pop(i)


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
                bestprob = np.float64(0)
                endtag = ""
                for tag in e.labels.keys():
                    tags[tag] = t.stopwith(tag) * matrix[i - 1][tag]
                    if tags[tag] >= bestprob:
                        bestprob = tags[tag]
                        endtag = tag
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
                    # print fromtag[tag],"-->",tag,":",tags[tag]
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
                    # print "score:",matrix[i][lasttag].hex()
                    # print "type:", type(matrix[i][lasttag])
                    finalpath.append(lasttag)
                else:
                    raise RuntimeError("endtag must be determined")
            elif path[i] is not None:
                word = inlines[i].strip()
                if isinstance(path[i], dict):
                    lasttag = path[i][lasttag]
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


def viterbi_Nbest(e, t, infile, outfile, best=10, p=True):
    try:
        inf = open(infile, 'r')
        outf = open(outfile, 'w')
        START = True
        inlines = inf.readlines()
        count = range(len(inlines))
        matrix = []
        outlines = []
        sen = 1
        start = 0
        for i in count:
            # print "the", i, "-th loop"
            line = inlines[i]
            if START is True:
                # print "START"
                print "START:",sen
                start = time.clock()
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = 1.0*t.startwith(tag) * e.emit(word, tag, p)
                matrix.append(tags)
                # print tags
                START = False
            elif line == '\n':
                # print "End Sentence"
                print "END:",sen
                sen += 1
                print "Time:", time.clock() - start
                START = True
                nb = NBest(best)
                for tag in e.labels:
                    if isinstance(matrix[i - 1][tag], float):
                        raise RuntimeError("Sentence has no words")
                    else:
                        b = matrix[i - 1][tag]
                        for j in range(len(b.label)):
                            prob = b.score[j] * t.stopwith(tag)
                            nb.add(tag, prob,j)
                nb.best()
                # print i,":",nb.score
                # print "best score at this sentence:", nb.score[0]
                # print nb.score[0].hex()
                # print "type:",type(nb.score[0])
                # print nb.label,"-->STOP:",nb.score
                matrix.append(nb)
            else:
                # print "In sentence"
                tags = {}
                word = line.strip()
                # print "word:",word
                for tag in e.labels:
                    nb = NBest(best)
                    for ftag in e.labels:
                        # case 1
                        # the second word in the sentence
                        if isinstance(matrix[i - 1][ftag], float):
                            # print "second word of the sentence"
                            prob = matrix[i - 1][ftag] * t.transit(ftag, tag) * e.emit(word, tag, p)
                            # print ftag,"-->",tag,":",prob
                            nb.add(ftag, prob,-1)
                        # case 2
                        # from the third word of the sentence
                        else:
                            # print "within sentence"
                            b = matrix[i - 1][ftag]
                            for j in range(len(b.label)):
                                prob = b.score[j] * t.transit(ftag, tag) * e.emit(word, tag, p)
                                # print ftag,"-->",tag,":",prob
                                nb.add(ftag, prob,j)
                    nb.best()
                    # print "after compute"
                    # print nb.label,"-->",tag,":",nb.score
                    tags[tag] = nb
                matrix.append(tags)

        count.reverse()
        lastword = []
        lastnum = []
        lastscore = []
        for i in count:
            line = inlines[i]
            if line == '\n':
                nb = matrix[i]
                lastword = nb.label
                lastnum = nb.num
                lastscore = nb.score
                # print "endsentence"
                # print "word:",lastword
                # print "number:",lastnum
                # print "score:", nb.score[0]
                # print "score:", nb.score[0].hex()
                # print "type:",type(nb.score[0])
                outlines.append('\n')
            else:
                currentlastword = []
                currentlastnum = []
                currentlastscore = []
                word = line.strip()
                cnt = range(len(lastword))
                for j in cnt:
                    lw = lastword[j]
                    nm = lastnum[j]
                    word = word + ' ' + lw
                    nb = matrix[i][lw]
                    if isinstance(nb, float):
                        # the first word in a sentence
                        continue
                    else:
                        # print "in sentence for :", lw
                        # print "number:", nm
                        # print "from words:",nb.label
                        # print "from numbers:",nb.num
                        # print "respective scores:",nb.score
                        # print "select words:",nb.label[nm]
                        # print "select number:", nb.num[nm]
                        currentlastword.append(nb.label[nm])
                        currentlastnum.append(nb.num[nm])
                        currentlastscore.append(nb.score[nm])
                lastword = currentlastword
                lastnum = currentlastnum
                lastscore = currentlastscore
                # print "within sentence:"
                # print "word:",lastword
                # print "number:",lastnum
                # if len(lastscore) > 0:
                    # print "score:", lastscore[0]
                    # print "score:",lastscore[0].hex()
                    # print "type:",type(lastscore[0])
                word += '\n'
                outlines.append(word)
        # print "outlines:",outlines
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
