import emission as em
import transition as tr
import toolbox as tool
import viterbi as viterbi
import argparse

parser = argparse.ArgumentParser(description="twitter POS tagger implemented with hidden markov model")

parser.add_argument("-t",dest='trainfile',required=True,help='path of training file')
parser.add_argument("-i",dest='infile',required=True,help='path of input file')
parser.add_argument("-o",dest='outfile',required=True,help='path of output file')
parser.add_argument("--algorithm",dest="algorithm",type=int,choices=[0,1,2],required=True,help="0:MLE with emission probability\n1:viterbi_best,top 1 sequence\n2:viterbi_Nbest,top 1 or 10 best sequence")
parser.add_argument('-b',dest='best',type=int,choices=[1,10],default=1,help='number of best tags to generate')
parser.add_argument('-p',dest='process',type=bool,default=True,help='whether do process or not')
args = parser.parse_args()
print args
if args.algorithm==0:
	e = em.emission()
	e.compute(args.trainfile)
	e.predict(args.infile,args.outfile,args.process)
	# print tool.evaluate('../data/POS/dev.out',args.outfile,col=1)

elif args.algorithm==1:
	if args.best != 1:
		print "Error: best must be 1 with algorithm 1"
		exit(0)
#run original version of viterbi
	e = em.emission()
	e.compute(args.trainfile)
	t = tr.transition()
	t.compute(args.trainfile)
	viterbi.viterbi_best(e,t,args.infile,args.outfile,args.process)
	# print tool.evaluate('../data/POS/dev.out',args.outfile,col=1)
elif args.algorithm==2:
	e = em.emission()
	e.compute(args.trainfile)
	t = tr.transition()
	t.compute(args.trainfile)

	viterbi.viterbi_Nbest(e,t,args.infile,args.outfile,args.best, args.process)
	# c = 1
	# while c<=args.best:
		# print tool.evaluate(args.outfile,'../data/POS/dev.out',col=c)
		# c = c+1