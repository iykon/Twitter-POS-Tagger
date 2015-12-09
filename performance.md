##Performance
####POS with preprocessor
1. emission.py MLE, with preprocessor

		python run.py -t ../data/POS/ptrain 
		-i ../data/POS/dev.in 
		-o ../data/POS/dev.p4.out 
		--algorithm 0
	
Error rate: 0.305203938115

2. viterbi, best 1, with preprocessor
		python run.py -t ../data/POS/ptrain 
		-i ../data/POS/dev.in 
		-o ../data/POS/dev.p4.out 
		--algorithm 1
Error rate: 0.325246132208

3. viterbi, best 10, with preprocessor
 		
 		python run.py -t ../data/POS/ptrain 
		-i ../data/POS/dev.in 
		-o ../data/POS/dev.p4.out 
		--algorithm 2 
		-b 10
Error rate: 

		
		0.310829817159
		0.313291139241
		0.322784810127
		0.318213783404
		0.323839662447
		0.32876230661
		0.331575246132
		0.32876230661
		0.32841068917
		0.329465541491

####NPC with preprocessor
1. emission.py MLE, with preprocessor

		python run.py -t ../data/NPC/ptrain 
		-i ../data/NPC/dev.in 
		-o ../data/NPC/dev.p2.out 
		--algorithm 0
		
Error rate:0.296279505546

2. viterbi, best 1, with preprocessor

		python run.py -t ../data/NPC/ptrain 
		-i ../data/NPC/dev.in 
		-o ../data/NPC/dev.p3.out 
		--algorithm 1

Error rate: 0.214767129084
3. viterbi, best 10 with preprocessor
		
		python run.py -t ../data/NPC/ptrain 
		-i ../data/NPC/dev.in 
		-o ../data/NPC/dev.p4.out 
		--algorithm 2 
		-b 10
Error rate: 

		0.214767129084
		0.235711911022
		0.240638317164
		0.254813068577
		0.256505576208
		0.264726327561
		0.268232236226
		0.275425393659
		0.266962855502
		0.257142857143
