ml-classifier-inbox
===================

Machine Learning - Email classifier - Inbox

---------------------------------------------------------------------

1) **CLASIFICADOR:** inbox_classifier.py
- Multiclass One Vs Rest Classifier
- Logistic Regression


Correos que entran en la bandeja de entrada. Clasificación:

- inbox     i   0
- carga     c   1
- barco     b   2

Ejemplo de ejecución:

	Número de correos TOTAL:
	23711

	Número de palabras (total):
	224113

	Número de indices:
	8120575

	============ EVALUATION ================

	Accuracy Score:
	0.967019526802

	=======================================

	Confusion matrix:
	[[ 4272     2     2]
	 [    2  2595   476]
	 [    2   298 16062]]


INPUT: 
- Necesita la carpeta 'output' donde están los correos en formato .txt

OUTPUT: 
- Tras crear el modelo, lo guarda en 'models/inbox_model.txt'.
- El conjunto de palabras se guarda en 'models/inbox_words.txt'.
- Accuracy y matriz de confusión.


---------------------------------------------------------------------


2) **PREDICCIÓN:** inbox_model.py

Función que recibe un correo y utilizando el modelo creado en (1) previamente, devuelve la clasificación + probabilidad.

Ejemplo de ejecución:

	Fichero DATA: ../Output/Inbox/_50.txt

	Número de ficheros:
	1

	Número de palabras (total):
	224113

	Probabilidad prediccion:
	[[  9.99999831e-01   1.05931510e-07   6.29447414e-08]]

	Class predicted:
	0

INPUT:
- Fichero recibido a clasificar.
- Carga el modelo de 'models/inbox_model.txt' y el conjunto de palabras de 'models/inbox_words.txt'.

OUTPUT:
- Clase predicha + probabilidades de las tres clases

	[Class predicted, [p0  p1  p2]]:
	[0, array([[  9.99999831e-01,   1.05931510e-07,   6.29447414e-08]])]


---------------------------------------------------------------------


3) **API REST PREDICCIÓN:** servicio_inbox.py
Servicio REST que devuelve JSON o string. 
Recibe un correo desde POST/GET:
* POST si viene de un formulario
* GET permite CORS usando JSNOP

INPUT: 
- Función de predicción creada en (2)
	from inbox_classifier import predictionInbox

OUTPUT:
- Clase predicha + probabilidades de las tres clases

	[Class predicted, [p0  p1  p2]]:
	[0, array([[  9.99999831e-01,   1.05931510e-07,   6.29447414e-08]])]