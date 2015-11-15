'''A simple and time consuming method of calculating emission probability'''
import numpy as np
import scipy as scp
import string
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
                i = i.strip().split()
                i0 = ''.join(ch for ch in i[0] if ch not in string.punctuation)
                i0 = i0.lower()
                i1 = i[1]
                if i0 == '':
                    i0 = i[0]
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

def emission(pfile, word, label):
    pword = ''.join(ch for ch in word if ch not in string.punctuation)
    if pword == '':
        pword = word
    pword = pword.lower()
    numer = 0
    denom = 0

    try:
        pf = open(pfile,'r')
        pline = pf.readlines()
        for i in pline:
            if i == '\n':
                continue
            i = i.split()
            w = i[0]
            l = i[1]
            if l == label:
                denom +=1
                if w == pword:
                    numer += 1
    except IOError, e:
        print e
        exit(0)
    finally:
        if numer == 0:
            return 1.0/(denom+1.0)
        else :
            return numer*1.0/(denom+1.0)
