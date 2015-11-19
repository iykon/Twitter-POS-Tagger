import time
import string

def compute(infile):
    try:
        inf = open(infile,'r')
        inlines = inf.readlines()
        start = {}
        stop = {}
        matrix = {}
        states = {}
        START = True
        linenum = len(inlines)
        print 'linenum:',linenum
        print 'range:', range(linenum)
        for i in range(linenum):
            print 'loop:', i
            line = inlines[i]
            print 'start:',START
            if START is True:
                print 'is True'
                nline = line.strip().split()[1]
                print 'nline:',nline
                if nline in start:
                    start[nline] += 1
                else :
                    start[nline] = 1

                if 'START' in states:
                    states['START'] += 1
                else :
                    states['START'] = 1
                START = False

            if line == '\n':
                print 'line is \\n'
                START = True
            else :
                print 'line is not \\n'
                nnline = line.strip().split()[1]
                print 'nnline:',nnline
                if nnline in states:
                    states[nnline] += 1
                else :
                    states[nnline] = 1

                nextline = inlines[i+1]
                print 'nextline:',nextline
                if nextline == '\n':
                    print 'nextline is \\n'
                    if nnline in stop:
                        stop[nnline] += 1
                    else :
                        stop[nnline] = 1
                else:
                    print 'nextline is not \\n'
                    ntline = nextline.strip().split()[1]
                    print 'ntline:',ntline
                    if nnline in matrix:
                        if ntline in matrix[nnline]:
                            matrix[nnline][ntline] += 1
                        else:
                            matrix[nnline][ntline] = 1
                    else :
                        matrix[nnline] = {}
                        matrix[nnline][ntline] = 1
    except IOError, e:
        print e
        exit(0)
    finally :
        if inf:
            inf.close()
        return start, stop, matrix, states

