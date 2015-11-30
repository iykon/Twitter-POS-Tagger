# Order2 HMM
This part increases the order of Hidden Markov Model, but it seems doesn't work well to improve the correction rate, and is extremely slow:

result for best 1:

without preprocessor
POS,MLE: 0.340717299578
POS,MLE likelihood: 0.44939194816
runtime: 777.330067
1 :POS, DP2: 0.864978902954
1 :POS, DP2 likelihood: 0.324274524723
with preprocessor
POS, MLE: 0.322784810127
POS, MLE, likelihood: 0.424347590673
runtime: 1571.648573
1 :POS, DP2: 0.86005625879
1 :POS, DP2 likelihood: 0.286778644743
without preprocessor
NPC,MLE: 0.242995738508
NPC,MLE likelihood: 0.0923896897338
runtime: 4.595088
1 :NPC, DP2: 0.200924834527
1 :NPC, DP2 likelihood: 0.0889452344985
with preprocessor
NPC, MLE: 0.269259830145
NPC, MLE likelihood: 0.0597943008795
runtime: 6.736796
1 :NPC, DP2: 0.211714570677
1 :NPC, DP2 likelihood: 0.0550779326169