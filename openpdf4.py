import json, re, sys, glob, math
import subprocess
from collections import OrderedDict

def getQuestions(fileName):
	comando = 'cat -v ' + fileName
	text = subprocess.check_output(comando, shell=True)
	text = text.decode('utf-8')
	
	#buscamos la coordenadas de los highlights
	pcoordenadas = []
	for m in re.finditer('/QuadPoints ', text):
		marca = {}
		#puntero al texto despues de la marca /QuadPoints 
		marca['end'] = m.end()
		pcoordenadas.append(marca)
		
	#buscamos los colores	
	pcolores = []
	for m2 in re.finditer('/C ', text):
		valor = {}
		#puntero al texto despues de la marca /C
		valor['end2'] = m2.end()
		pcolores.append(valor)
		
	coordsPreguntas = []
	coordsRespuestas = []
	coordenadas = []
	print(len(pcoordenadas))
	for k in range(0,len(pcoordenadas)):
		#nos quedamos las coordenadas
		firstPoint = pcoordenadas[k]
		secondPoint = text.find(']', firstPoint['end'], len(text))
		cs = text[firstPoint['end']+1:secondPoint]
		print('cs: ',cs)
		#coordenadas = cs.split(' ')
		
	
i = 0
while(i < 2):
	op = input("Selecciona una opción( 1 para la primera pasada, 2 para escanear las respuestas): ")
	if(op=='1'):
		getQuestions('Vander.pdf')
	elif(op == '2'):
		getAnswers()
	i = i+1
	
