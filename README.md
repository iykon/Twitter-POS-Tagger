# SUTD Machine Learning Project 2015
Machine Learning Project at SUTD, 2015

This project is to consists of four different files:

1. **emission.py:**This part calculates emission probability for a given file.
2. **transition.py:**This  part computes transition probability
3. **viterbi.py:**This part generates the best N routes with viterbi algorithm
4. **toolbox.py:**This part is a box of tools for more general use to facilitate above 3 parts

##Result:
POS:

without preprocessor
POS,MLE: 0.399085794655
POS,DP: 0.409282700422
runtime: 183.357277
1 :POS, DP2: 0.385372714487
2 :POS, DP2: 0.386779184248
3 :POS, DP2: 0.388537271449
4 :POS, DP2: 0.389240506329
5 :POS, DP2: 0.393108298172
6 :POS, DP2: 0.39099859353
7 :POS, DP2: 0.398030942335
8 :POS, DP2: 0.392405063291
9 :POS, DP2: 0.396624472574
10 :POS, DP2: 0.395218002813
with preprocessor
POS, MLE: 0.373769338959
POS, DP: 0.354430379747
runtime: 308.317963
1 :POS, DP2: 0.339310829817
2 :POS, DP2: 0.341420534459
3 :POS, DP2: 0.347046413502
4 :POS, DP2: 0.346694796062
5 :POS, DP2: 0.348452883263
6 :POS, DP2: 0.350914205345
7 :POS, DP2: 0.351617440225
8 :POS, DP2: 0.348452883263
9 :POS, DP2: 0.349156118143
10 :POS, DP2: 0.353023909986

NPC:

without preprocessor
NPC,MLE: 0.299996977665
NPC,DP: 0.223622570798
runtime: 17.605402
1 :NPC, DP2: 0.223622570798
2 :NPC, DP2: 0.24311663191
3 :NPC, DP2: 0.244325565932
4 :NPC, DP2: 0.256173119352
5 :NPC, DP2: 0.258016743736
6 :NPC, DP2: 0.264726327561
7 :NPC, DP2: 0.263910297096
8 :NPC, DP2: 0.271224347931
9 :NPC, DP2: 0.267325535709
10 :NPC, DP2: 0.271428571429
with preprocessor
NPC, MLE: 0.296672409103
NPC, DP: 0.215673829601
runtime: 23.08525
1 :NPC, DP2: 0.215673829601
2 :NPC, DP2: 0.236739504942
3 :NPC, DP2: 0.240849880618
4 :NPC, DP2: 0.255780215795
5 :NPC, DP2: 0.25714026657
6 :NPC, DP2: 0.265361017922
7 :NPC, DP2: 0.268111342823
8 :NPC, DP2: 0.275425393659
9 :NPC, DP2: 0.267144195606
10 :NPC, DP2: 0.257142857143
##toolbox.py
This module provides the tools that facilitates other modules, including preprocessor and evaluation methods:
####Preprocessor
	toolbox.preprocess("input file", "output file")
This method preprocesses the input file and write the results into output file. It achieves this by using following two methods:

	#sentence processing
	pword, ptag = toolbox.processSentence(sentence)
This method processes one sentence into one processed word and one processed tag. Temporarily, no modifications are done to tag except extracting it from the sentence.
	
	#word processing
	pword = toolbox.processWord(word)
This method processes a word with the following rule:

  *  when one word contains only punctuations, for example ":)", ":(", remains the same
  *  for other words with not only punctuations like "hello!", remove the punctuations in them and modify into lower case. This generalization procedure could slightly improve the results.
  *  [deprecated]exception is URL, initially URL are retained, but in terms of the error rate there were not improvements, so deprecated:

		hasURL(word) #judge whether one sentence has URL
		
####Evaluation
This tool is to evaluate the prediction with the answer, and return the error rate:

	evaluate("test file","answer file",col=1, pr=False)
The *test file* contains our prediction, *answer file* contains the correct anser, *col* specifies which column of prediction is to be tested (in case there are multiple predictions like in Top-10 predictions), when *pr* is set True, the function would print in which line the prediction differs from the answer.

##emission.py
This module contains the class which maintains the emission probabilty of text given in a file.
#### Algorithm Specification
This class computes emission probability of the given text with the Maximal Likelihood Estimator introduced in Hidden Markov Model.

The general case formula is:
$$ e(word|tag) = \frac{count(word,tag)}{count(tag)}$$
As we can hardly enumerate all possible *"word"*s in the given text file, for a word that has never appeared in the corpus, we provide a special case formula to estimate it's emission probability:
$$e(new|tag) = \frac{1}{count(tag)+1}$$
Internally, this class maintains two Python dictionaries, named *matrix* and *labels*, which has:

	matrix[word][tags] = count(word, tag)
	labels[tag] = count(tag)
####import the module and initialization
	# import the module
	import emission
	# initialization
	e = emission.emission()
This step provides an "empty" emission object.
####compute the parameters with a given corpus
	e.compute("file name")
After this step the *matrix* and *labels* in emission classes is computed. 
####compute emission probability
	e.emit(word, tag, p=True)
	# attention: tag must appear in the given training corpus
	# or it would raise a runtime error
*word* is the word we want to emit, *tag* is the tentative tag to emit, and *p* stands for "process", when *p* is set true, the object would process *word* before computing the emission probability.
####guess the most probable tag
	e.mostprob()
It occurs in Hidden Markov Model that at some points in a sentence, all possible tags score 0. When it occurs such scenario one enhacement is tag this position as the most probable label among all possible labels.

####MLE predictor:
With the emission probability, one way to predict labels of a given corpus is to use Maximal Likelihood, that is, to find out the most probable tag for the word under emission probability.

	e.predict("input filename","output filename", p=True)
Then the object labels the input file with emission probability MLE and writes the labeled corpus into output file. 

When *p* is set True, the word would be processed with toolbox before computing emission probability.


 
	