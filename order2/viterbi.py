import emission as em
import toolbox as tool
import bi_transition as bitr
import tri_transition as tritr
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
            # print "loop:",i, "line:",inlines[i]
            line = inlines[i]
            tags = {}
            if START and line!='\n' and line!='\r\n':
                # print "START"
                word = line.strip().split()[0]
                # print word
                for tag in e.labels.keys():
                    tags[tag] = t.startwith(tag) * e.emit(word, tag, p)
                # print tags
                matrix.append(tags)
                path.append(None)
                START = False
            elif line == '\n' or line=='\r\n':
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
                word = line.strip().split()[0]
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
            print "decode:",i
            print "word:",inlines[i]
            if inlines[i] == '\n' or inlines[i]=='\r\n':
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
                word = inlines[i].strip().split()[0]
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
                word = line.strip().split()[0]
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
def viterbi_Nbest(e, bt, tt, infile, outfile,lambda0=0.4, lambda1=0.5, lambda2=0.1, best=10, p=True):
    try:
        inf = open(infile, 'r')
        outf = open(outfile, 'w')
        START = True
        SECSTART = True
        inlines = inf.readlines()
        count = range(len(inlines))
        matrix = []
        outlines = []
        start = time.clock()
        for i in count:
            print "i:",i
            # print "i:",i,"time", time.clock() - start
            # start = time.clock()
            # print "START:",START
            # print "SECSTART:", SECSTART
            line = inlines[i]
            # calculate all possible tags and its score and which path of previous tag this path comes from
            if START is True and SECSTART is True:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = 1.0*(lambda0+lambda1*bt.startwith(tag)+lambda2*tt.transit('START','START',tag) )* e.emit(word, tag, p)
                matrix.append(tags)
                START = False
            elif START is False and SECSTART is True:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    tags[tag] = {}
                    for lword in e.labels:
                        tags[tag][lword] = 1.0*matrix[i-1][lword]*(lambda0+lambda1*bt.transit(lword,tag)+lambda2*tt.transit('START',lword,tag))* e.emit(word,tag,p)
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
                        prob = 1.0 * matrix[i-1][lword]*(lambda0+lambda1*bt.stopwith(lword)+lambda2*tt.transit('START',lword,'STOP'))
                        nb.add('START',lword,prob,-1)
                    # more than one word
                    else :
                        for llword in e.labels:
                            # sentence has only two words
                            if isinstance(matrix[i-1][lword][llword],float):
                                prob = 1.0*matrix[i-1][lword][llword]*(lambda0+lambda1*bt.stopwith(lword)+lambda2*tt.transit(llword,lword,'STOP'))
                                nb.add(llword,lword,prob,-1)
                            # sentence has more than two words
                            else :
                                b = matrix[i-1][lword][llword]
                                for j in range(len(b.elements)):
                                    prob = 1.0*b.elements[j].score *(lambda0+lambda1*bt.stopwith(lword)+lambda2*tt.transit(llword,lword,'STOP'))
                                    nb.add(llword,lword,prob,j)
                nb.best()
                print "score:", nb.elements[0].score
                matrix.append(nb)
                # print "end sentence:",nb.elements[0].word,"score:",nb.elements[0].score, "from:",nb.elements[0].path
            else:
                tags = {}
                word = line.strip()
                for tag in e.labels:
                    for lword in e.labels:
                        nb = NBest(best)
                        for llword in e.labels:
                            # third word in the sentence
                            if isinstance(matrix[i-1][lword][llword],float) :
                                # print "third word in a sentence"
                                prob = 1.0*matrix[i-1][lword][llword]*(lambda0 + lambda1*bt.transit(lword,tag) + lambda2*tt.transit(llword,lword,tag))*e.emit(word,tag,p)
                                nb.add(llword,lword,prob,-1)
                            # after the third word in the sentence
                            else :
                                b = matrix[i-1][lword][llword]
                                for j in range(len(b.elements)):
                                    prob = 1.0*b.elements[j].score*(lambda0+lambda1*bt.transit(lword,tag)+lambda2*tt.transit(llword,lword,tag))*e.emit(word,tag,p)
                                    nb.add(llword, lword, prob, j)
                        nb.best()
                    # print "******chosen:",nb.elements[0].word,"-->",tag,":",nb.elements[0].score
                        if tag not in tags:
                            tags[tag] = {}
                        tags[tag][lword] = nb
                matrix.append(tags)
        # decode the sentence
        # print "DECODING"
        count.reverse()
        lastelement = []
        SECHEAD = False
        HEAD = False
        ONEHEAD = False
        for i in count:
            line = inlines[i]
            # end of a sentence, get all the final tags
            if line == '\n':
                nb = matrix[i]
                lastelement = nb.elements
                outlines.append('\n')
                tlw = nb.elements[0].lword
                tllw = nb.elements[0].llword
                if tlw == 'START' and tllw == 'START':
                    raise RuntimeError("Sentence appears START->STOP")
                elif tllw == 'START':
                    #this sentence has only one word
                    ONEHEAD = True
                elif isinstance(matrix[i-1][tlw][tllw],float) and isinstance(matrix[i-2][tllw],float):
                    SECHEAD = True
                    HEAD = False
                # print "endsentence:",lastelement[0].word, "score:",lastelement[0].score, "from:" ,lastelement[0].path
            elif SECHEAD is True and HEAD is False:
                word = line.strip()
                for j in range(len(lastelement)):
                    word= word +' '+lastelement[j].lword
                word += '\n'
                outlines.append(word)
                SECHEAD = False
                HEAD = True
            elif SECHEAD is False and HEAD is True:
                word = line.strip()
                for j in range(len(lastelement)):
                    word = word + ' ' + lastelement[j].llword
                word += '\n'
                outlines.append(word)
                SECHEAD = False
                HEAD = False
            elif ONEHEAD is True:
                word = line.strip()
                for j in range(len(lastelement)):
                    word = word + ' '+lastelement[j].lword
                word += '\n'
                outlines.append(word)
                ONEHEAD = False
            # in the sentence, extract all current tags from the result stored in the position behind
            else:
                currentlastelement = []
                word = line.strip()
                for j in range(len(lastelement)):
                    llw = lastelement[j].llword
                    lw = lastelement[j].lword
                    nm = lastelement[j].path
                    scr = lastelement[j].score
                    if scr == 0:
                        word = word + ' '+e.mostprob()
                    # else :
                    word = word + ' '+ lw
                    # print "word:",word
                    nb = matrix[i][lw][llw]
                    # get the tags of previous position
                    currentlastelement.append(nb.elements[nm])
                    # print j,"-th, within sentence:",currentlastelement[0].word, "score:",currentlastelement[0].score, "from:", currentlastelement[0].path
                lastelement = currentlastelement
                tlw = lastelement[0].lword
                tllw = lastelement[0].llword
                if isinstance(matrix[i-1][tlw][tllw],float) and isinstance(matrix[i-2][tllw],float):
                    SECHEAD = True
                    HEAD = False
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
    bt0 = bitr.bi_transition()
    tt0 = tritr.tri_transition()
    # print "without preprocessor"
    # e0.compute('../data/POS/train')
    # t0.compute('../data/POS/train')
    # e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out',p=False)
    # print "POS,MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
    # print "POS,MLE likelihood:", e0.filelikelihood("../data/POS/dev.p2.out",p=False)
    # viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out',p=False)
    # print "POS,DP:", tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
    # print "POS,DP likelihood:", e0.filelikelihood("../data/POS/dev.p3.out", p=False)
    # start = time.clock()
    # viterbi_Nbest(e0, t0, '../data/POS/dev.in', '../data/POS/dev.p4.out', best=1, p=False)
    # print "runtime:",time.clock()-start
    # c = 1
    # while c<=1:
        # print c,":POS, DP2:", tool.evaluate('../data/POS/dev.p4.out', '../data/POS/dev.out',col=c)
        # print c,":POS, DP2 likelihood:", e0.filelikelihood("../data/POS/dev.p4.out",p=False, col=c)
        # c+=1

    print "with preprocessor"
    e0.compute('../data/POS/ptrain')
    bt0.compute('../data/POS/ptrain')
    tt0.compute('../data/POS/ptrain')
    # e0.predict('../data/POS/test.in','../data/POS/test.p1.out')
    # era,eno= tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out',col=1,pr=True)
    # print "error rate:",era
    # print "POS, MLE, likelihood:",e0.filelikelihood("../data/POS/dev.p2.out")
    # with new smoothing 0.27637
    # viterbi_best(e0,bt0,'../data/POS/dev.in','../data/POS/dev.p2.out')
    # era,eno = tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out',pr=True)
    # print "POS, DP:", era
    # print "POS, DP likelihood:", e0.filelikelihood("../data/POS/dev.p3.out")
    # start = time.clock()
    # 0.5 1.5 0: 0.2574
    # 1 10 1: 0.2422
    # 1 15 1: 0.2422
    # 1 20 1: 0.239
    # 1 25 1: 0.2369
    # 1 30 1: 0.235
    # 1 35 1: 0.2334
    # viterbi_Nbest(e0, bt0, tt0, '../data/POS/dev.in', '../data/POS/dev.p5.out',lambda0=1.0, lambda1=30.0, lambda2=1.0, best=1)
    # print "runtime:",time.clock() - start
    c = 1
    while c <= 1:
        era, eno = tool.evaluate('../data/POS/dev.p5.out', '../data/POS/dev.out',col=c,pr=True)
        print c,":POS, DP2:",era       # print c,":POS, DP2 likelihood:", e0.filelikelihood("../data/POS/dev.p4.out",col=c)
        c += 1

    # e1 = em.emission()
    # t1 = tr.transition()
    # print "without preprocessor"
    # e1.compute('../data/NPC/train')
    # t1.compute('../data/NPC/train')
    # e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out',p=False)
    # print "NPC,MLE:", tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    # print "NPC,MLE likelihood:", e1.filelikelihood("../data/NPC/dev.p2.out",p=False)
    # viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out',p=False)
    # print "NPC,DP:", tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    # print "NPC,DP likelihood:", e1.filelikelihood("../data/NPC/dev.p3.out",p=False)
    # start = time.clock()
    # viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=1, p=False)
    # print "runtime:",time.clock() - start
    # c = 1
    # while c <= 1:
        # print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        # print c,":NPC, DP2 likelihood:", e1.filelikelihood("../data/NPC/dev.p4.out",p=False, col=c)
        # c += 1

    # print "with preprocessor"
    # e1.compute('../data/NPC/ptrain')
    # t1.compute('../data/NPC/ptrain')
    # e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out')
    # print 'NPC, MLE:', tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
    # print "NPC, MLE likelihood:", e1.filelikelihood("../data/NPC/dev.p2.out")
    # viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out')
    # print 'NPC, DP:',tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
    # print "NPC, DP likelihood:", e1.filelikelihood("../data/NPC/dev.p3.out")
    # start = time.clock()
    # viterbi_Nbest(e1, t1, '../data/NPC/dev.in', '../data/NPC/dev.p4.out', best=1)
    # print "runtime:",time.clock()-start
    # c = 1
    # while c <= 1:
        # print c,":NPC, DP2:", tool.evaluate('../data/NPC/dev.p4.out', '../data/NPC/dev.out',col=c)
        # print c,":NPC, DP2 likelihood:", e1.filelikelihood("../data/NPC/dev.p4.out",col=c)
        # c += 1
if __name__ == '__main__':
    main()
