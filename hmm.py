
#forward algorithm

H = {'A': 0.2, 'C': 0.3, 'G': 0.3, 'T': 0.2}
L = {'A': 0.3, 'C': 0.2, 'G': 0.2, 'T': 0.3}
trProb = {     ('S', 'H'): 0.5, 
               ('S', 'L'): 0.5, 
               ('H', 'H'): 0.5, 
               ('L', 'L'): 0.6, 
               ('L', 'H'): 0.4, 
               ('H', 'L'): 0.5
         }
seq = 'GGCA'
P = []

for i in seq:
    if len(P) == 0:
        p = [trProb[('S', 'H')] * H[i], trProb[('S', 'L')] * L[i]]
    else:
        p = []
        # H
        # (H -> H) + (L -> H)
        p.append(P[-1][0] * trProb[('H', 'H')] * H[i] + P[-1][1] * trProb[('L', 'H')] * H[i])
        # L
        # (L -> L) + (H -> L)
        p.append(P[-1][1] * trProb[('L', 'L')] * L[i] + P[-1][0] * trProb[('H', 'L')] * L[i])
    P.append(p)

print("probability table : ", P)
print("total probability: ", P[-1][0] + P[-1][1])


#-------------------------------------------------------------

#viterbi backward algorithm
seqn="GGCACTGAA"

startH=0.5
startT=0.5

trProb=[0.5,0.4,0.5,0.6]

hDict={"A":0.2,"C":0.3,"G":0.3,"T":0.2}
tDict={"A":0.3,"C":0.2,"G":0.2,"T":0.3}

hVals=[]
tVals=[]
for i in range(0,2):
    temp=[]
    for j in range(0,9):
        temp.append(0)
    hVals.append(temp)
    tVals.append(temp)
    
hVals[0][0]=startT * hDict[seqn[0]]
hVals[1][0]=startH * tDict[seqn[0]]

tVals[0][0]=startT * hDict[seqn[0]]
tVals[1][0]=startH * tDict[seqn[0]]

for i in range(1,len(seqn)):
    hVals[0][i]=hVals[0][i-1]*trProb[2]*hDict[seqn[i]]+hVals[1][i-1]*trProb[1]*hDict[seqn[i]]
    hVals[1][i]=hVals[1][i-1]*trProb[3]*tDict[seqn[i]]+hVals[0][i-1]*trProb[0]*tDict[seqn[i]]
    

if(tVals[0][0]>tVals[1][0]):
    print("H",end="")
else:
    print("L",end="")
        
for i in range(1,len(seqn)):
    tVals[0][i]=hDict[seqn[i]]* max(hVals[0][i-1]*trProb[2],hVals[1][i-1]*trProb[1])
    tVals[1][i]=tDict[seqn[i]]* max(hVals[1][i-1]*trProb[3],hVals[0][i-1]*trProb[0])
    if(tVals[0][i]>tVals[1][i]):
        print("H",end="")
    else:
        print("L",end="")
        
#-------------------------------------------------------------


#viterbi algorithm given raw probability

H = {'A': -2.322, 'C': -1.737, 'G': -1.737, 'T': -2.322}
L = {'A': -1.737, 'C': -2.322, 'G': -2.322, 'T': -1.737}
trProb = {('S', 'H'): -1, ('S', 'L'): -1, ('H', 'H'): -1, ('L', 'L'): -0.737, ('L', 'H'): -1.322, ('H', 'L'): -1}
seq = 'GGCACTGAA'
P = []
parent = []

for i in seq:
    if len(P) == 0:
        p = [trProb[('S', 'H')] + H[i], trProb[('S', 'L')] + L[i]]
    else:
        p = []
        par = []
        # H
        p.append(H[i] + max(P[-1][0] + trProb[('H', 'H')], P[-1][1] + trProb[('L', 'H')]))
        if P[-1][0] + trProb[('H', 'H')] > P[-1][1] + trProb[('L', 'H')]:
            par.append('H')
        else:
            par.append('L')
        # L
        p.append(L[i] + max(P[-1][0] + trProb[('H', 'L')], P[-1][1] + trProb[('L', 'L')]))
        if P[-1][0] + trProb[('H', 'L')] > P[-1][1] + trProb[('L', 'L')]:
            par.append('H')
        else:
            par.append('L')

        parent.append(par)
        
    P.append(p)

# Backtracking
path = []
if P[-1][0] > P[-1][1]:
    path.extend([par[0] for par in parent])
    path.append('H')
else:
    path.extend([par[1] for par in parent])
    path.append('L')

print(path)
