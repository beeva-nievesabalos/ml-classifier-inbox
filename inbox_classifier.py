# -*- coding: utf-8 -*-
import numpy as np
from scipy import sparse as sp
from sklearn import multiclass
from sklearn.cross_validation import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import os
from sklearn.externals import joblib

#import pylab as pl
pathDataI = '../Output/Inbox/'         
pathDataC = '../Output/Cargas/'    
pathDataB1 = '../Output/Posiciones/Posiciones Coasters/'
pathDataB2 = '../Output/Posiciones/Posiciones Handies/'     
pathDataB3 = '../Output/Posiciones/Posiciones Panamax/'

# CLASIFICADOR por correos que entran en INBOX:
# se quedan en inbox, son barcos, son cargas interesantes...
# inbox     i   0
# carga     c   1
# barco     b   2

# PARTE 1: input de datos
# Matriz X
files=[]
tag_array=[]
for messagefile in os.listdir(pathDataI):
    print("\nFichero DATA inbox: " + pathDataI + messagefile)
    # Abro el fichero a voy a leer
    f = open(pathDataI + messagefile, 'r')
    files.append(f.read())
    tag_array.append(0)

for messagefile in os.listdir(pathDataC):
    print("\nFichero DATA carga (Bergeshipbrokers): " + pathDataC + messagefile)
    # Abro el fichero a voy a leer
    f = open(pathDataC + messagefile, 'r')
    files.append(f.read())
    tag_array.append(1)

for messagefile in os.listdir(pathDataB1):
    print("\nFichero DATA barcos (Posiciones): " + pathDataB1 + messagefile)
    # Abro el fichero a voy a leer
    f = open(pathDataB1 + messagefile, 'r')
    files.append(f.read())
    tag_array.append(2)

for messagefile in os.listdir(pathDataB2):
    print("\nFichero DATA barcos (Posiciones): " + pathDataB2 + messagefile)
    # Abro el fichero a voy a leer
    f = open(pathDataB2 + messagefile, 'r')
    files.append(f.read())
    tag_array.append(2)
    
for messagefile in os.listdir(pathDataB3):
    print("\nFichero DATA barcos (Posiciones): " + pathDataB3 + messagefile)
    # Abro el fichero a voy a leer
    f = open(pathDataB3 + messagefile, 'r')
    files.append(f.read())
    tag_array.append(2)    

# Vector Y (ver leyenda arriba)
Y=np.array(tag_array) 
#joblib.dump(Y,'models/inbox/vector_y.txt')


print("\n=======================================")   
print("\nNúmero de correos TOTAL:")   
print len(files)
   
filess=[f.split() for f in files]


# PARTE 2: procesamiento de datos, conteo de palabras
words={}
indcount=0
for f in filess:
    for w in f:
        if w not in words:
            words[w]=indcount
            indcount+=1

print("\nNúmero de palabras (total):")    
print len(words)            
joblib.dump(words,'models/inbox_words.txt')

indices=[]
indptr=[0]
c=0
for iemail,f in enumerate(filess):
     d=[words[w] for w in f]
     c+=len(d)
     indptr.append(c)
     indices.extend(d)

print("\nNúmero de indices:") 
print len(indices)
  
# Vector X: matriz con las palabras   
X=sp.csr_matrix((np.ones(len(indices)),indices,indptr),shape=(len(files),len(words)))
#joblib.dump(X,'models/inbox/vector_x.txt')
#print("\nCompressed Sparse Row matrix:") 
#print X

# PARTE 3: training
skf = StratifiedKFold(Y, 5) # era antes 5

# Calculo sólo
y_true=[]
y_predT=[]
# Calculo Y predicción
for indtrain, indtest in skf:
    xTrain=X[indtrain,:]
    yTrain=Y[indtrain]
    xTest=X[indtest,:]    
    yTest=Y[indtest]
    
    y_true.extend(yTest)
#    y_pred = multiclass.OneVsRestClassifier(LinearSVC(random_state=0)).fit(xTrain,yTrain).predict(xTest)
    y_pred = multiclass.OneVsRestClassifier(LogisticRegression()).fit(xTrain,yTrain).predict(xTest)
    y_predT.extend(y_pred)



# PARTE 3B: guardar el modelo
model = multiclass.OneVsRestClassifier(LogisticRegression()).fit(X,Y)

joblib.dump(model,'models/inbox_model.txt')

# PARTE 4: evaluacion: y (real) vs ŷ (estimada)
print("\n============ EVALUATION ================")
print("\nAccuracy Score:") 
print accuracy_score(y_true, y_predT, normalize=True)

#print("\nY estimada:")
#print y_predT
print("\n=======================================")     
    
from sklearn.metrics import f1_score

#f1= f1_score(y_true, y_predT, average='macro')
#print(f1)
#print("\n=======================================") 
#f2= f1_score(y_true, y_predT, average='micro')
#print(f2)
print("\n=======================================") 
f3= f1_score(y_true, y_predT, average='weighted')
print(f3)
print("\n=======================================") 
#f4= f1_score(y_true, y_predT, average=None)
#print(f4)
#print("\n=======================================") 

# Compute confusion matrix
cm = confusion_matrix(y_true, y_predT)
print("\nConfusion matrix:") 
print(cm)

# Show confusion matrix in a separate window
#pl.matshow(cm)
#pl.title('Confusion matrix')
#pl.colorbar()
#pl.ylabel('True label')
#pl.xlabel('Predicted label')
#pl.show()
    
        
    

        

