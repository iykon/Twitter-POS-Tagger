import emission as em
import toolbox as tool
import transition as tr
import types
def viterbi_best(e, t, infile,outfile,p=True):
	try:
		inf = open(infile,'r')
		outf = open(outfile,'w')
		inlines = inf.readlines()
		START = True

		matrix = []
		path = []

		rg = range(len(inlines))
		for i in rg:
			line = inlines[i]
			tags = {}
			if START:
				word = line.strip()
				for tag in e.labels.keys():
					tags[tag] = t.startwith(tag) * e.emit(word,tag,p)
				matrix.append(tags)
				path.append(None)
				START = False
			elif line == '\n':
				bestprob = 0
				endtag = ""
				for tag in e.labels.keys():
					tags[tag] = t.stopwith(tag) * matrix[i-1][tag]
					if tags[tag] >= bestprob:
						bestprob = tags[tag]
						endtag = tag
				matrix.append(tags)
				path.append(endtag)
				START = True
			else :
				word = line.strip()
				fromtag = {}
				for tag in e.labels.keys():
					for ftag in e.labels.keys():
						prob = matrix[i-1][ftag] * t.transit(ftag,tag) * e.emit(word,tag,p)
						if tag not in tags:
							tags[tag] = prob
							fromtag[tag] = ftag
						elif tags[tag] <= prob:
							tags[tag] = prob
							fromtag[tag] = ftag
				matrix.append(tags)
				path.append(fromtag)

		rg.reverse()
		finalpath = []
		lasttag = ""
		for i in rg:
			if inlines[i] == '\n':
				if isinstance(path[i],str):
					lasttag = path[i]
					finalpath.append(lasttag+' '+str(matrix[i][lasttag]))
				else :
					raise RuntimeError("endtag must be determined")
			elif path[i] is not None:
				word = inlines[i].strip()
				if isinstance(path[i],dict):
					lasttag = path[i][lasttag]
					finalpath.append(lasttag)
				else :
					raise RuntimeError("in text must correspond to a dict")
		outlines = []
		for line in inlines:
			if line == '\n':
				outlines.append('\n')
				continue
			else:
				word = line.strip()
				tag = finalpath.pop()
				outlines.append(word+" "+tag+"\n")
		outf.writelines(outlines)
	except IOError, e:
		print e
		exit(0)
	finally:
		if inf:
			inf.close()
		if outf:
			outf.close()

def main() :
	tool.preprocess('../data/POS/train','../data/POS/ptrain')
	tool.preprocess('../data/NPC/train','../data/NPC/ptrain')

	e0 = em.emission()
	t0 = tr.transition()
	print "without preprocessor"
	e0.compute('../data/POS/train')
	t0.compute('../data/POS/train')
	e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out',p=False)
	print "POS,MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
	viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out',p=False)
	print "POS,DP:", tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')
	print "with preprocessor"
	e0.compute('../data/POS/ptrain')
	t0.compute('../data/POS/ptrain')
	e0.predict('../data/POS/dev.in','../data/POS/dev.p2.out')
	print "POS, MLE:", tool.evaluate('../data/POS/dev.p2.out','../data/POS/dev.out')
	viterbi_best(e0,t0,'../data/POS/dev.in','../data/POS/dev.p3.out')
	print "POS, DP:",tool.evaluate('../data/POS/dev.p3.out','../data/POS/dev.out')


	e1 = em.emission()
	t1 = tr.transition()
	print "without preprocessor"
	e1.compute('../data/NPC/train')
	t1.compute('../data/NPC/train')
	e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out',p=False)
	print "NPC,MLE:", tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
	viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out',p=False)
	print "NPC,DP:", tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')
	print "with preprocessor"
	e1.compute('../data/NPC/ptrain')
	t1.compute('../data/NPC/ptrain')
	e1.predict('../data/NPC/dev.in','../data/NPC/dev.p2.out')
	print 'NPC, MLE:', tool.evaluate('../data/NPC/dev.p2.out','../data/NPC/dev.out')
	viterbi_best(e1,t1,'../data/NPC/dev.in','../data/NPC/dev.p3.out')
	print 'NPC, DP:',tool.evaluate('../data/NPC/dev.p3.out','../data/NPC/dev.out')

if __name__ == '__main__':
	main()
