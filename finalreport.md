##instruction
This package consists of four python modules:

1. **emission.py:**This module computes emission probability with given training text.
2. **transition.py:**This module computes transition probability with given training text.
3. **viterbi.py:** This module implements viterbi algorithm to predict the tag of given test text
4. **toolbox.py:**This module is a box of tools, providing functionalities and optimization for three modules above, including preprocessor, evaluation of a prediction

##How to run the code


##emission.py
This module contains the class *emission* which maintains the emission probabilty of text given in a file.
#### Algorithm Specification
This class computes emission probability of the given text with the Maximal Likelihood Estimator (MLE) introduced in Hidden Markov Model.

The general case formula is:
$$ e(word|tag) = \frac{count(word,tag)}{count(tag)+1}$$

As we can hardly learn all possible *"word"*s in the given text file, for a word that has never appeared in the corpus, we provide a special case formula to estimate it's emission probability:
$$e(new|tag) = \frac{1}{count(tag)+1}$$

Internally, this class maintains two Python dictionaries, named *matrix* and *labels*, which has:

	matrix[word][tags] = count(word, tag)
	labels[tag] = count(tag)
####import the module and initialization
	# import the module
	import emission
	# initialization
	e = emission.emission()
This step provides an "empty" emission object whose two internal dictionaries mentioned above are empty.
####compute the parameters with a given corpus
	e.compute("training file name")
After this step the *matrix* and *labels* in emission classes is computed with the training file provided.
####compute emission probability
	e.emit(word, tag, p=True)
	# attention: tag must appear in the given training corpus
	# or it would raise a runtime error
***word*** is the word to be emitted from ***tag***. Parameter *p* stands for "process", when *p* is set True, the object would process *word* (with the tools in toolbox) before computing the emission probability.

This function returns a floating number specifying the emission probability of the given ***word*** and ***tag***.
####guess the most probable tag
	e.mostprob()
It happens in Hidden Markov Model that at some points in a sentence, all possible tags score 0. One enhacement is to tag this position as the most probable label among all possible labels, which could improve the result to some degree.

####MLE predictor:
With the emission probability, one way to predict labels of a given corpus is to use Maximal Likelihood, that is, to find out the most probable tag for the word under emission probability.

	e.predict("input filename","output filename", p=True)
Then the object labels the input file with emission probability MLE and writes the labeled corpus into output file. 

When *p* is set True, the word would be processed with toolbox before computing emission probability.

##transition.py
This module provides a class similar to emission.py, which also maintains four internal dictionaries ***start***, ***stop***, ***matrix*** and ***states*** to compute the transition probability with the MLE in Hidden Markov Model, where:
$$T(y_{i-1}->y_i) = \frac{count(y_{i-1},y{i})}{count(y_{i-1})}$$
In particular, i=1 or i=n respectively denotes that this word is the first or last word of the sentence, under such case the transition probability is:
$$T(y_0->y_1)= \frac{count(START,y_1)}{count(START)}$$
$$T(y_n->y_{n+1}) = \frac{count(y_n,STOP)}{count(STOP)}$$

	matrix[front][current] = count(front, current)
	states[tag] = count(tag)
	start[tag] = count(START,tag)
	stop[tag] = count(tag,STOP)

###import and initialization
	
	import transition
	t = transition.transition()
Similarly to that in emission.py, this procedure give an empty transition object with empty dictioinaries.

###compute the transition probability

	t.compute(training file name)
Also similarly to that in emission.py, this procedure computes the values in the four dictionaries mentioned above

###transit

	t.transit(front, current)
This procedure returns a single floating number denoting the transition probability of transitioning from ***front*** to ***current***, which respective denoting the front tag and current tag.

###startwith
	
	t.startwith(tag)
This method returns a single floating number, that is the value of $T(START,tag)$, denoting the probability of the sentence starts with ***tag***.

###stopwith
	t.stopwith(tag)
Similarly to ***startwith()***, it returns the probability that one sentence stops with ***tag***.

##viterbi.py
This part is the core of our viterbi algorithm, it has two classes and two methods.

####methods: viterbi_best()

	viterbi_best(emission, transition, inputfile, outputfile, p=True)
This function runs the dynamic programming to find the best tag sequence for given observation of word sequence.


