# -*- coding: utf-8 -*-
import json
from os import system, remove

with open('questions.json') as data_file:
	questions = json.load(data_file)

with open('answers.json') as data_file:
	answers = json.load(data_file)

questions = questions['questions']
answers = answers['answers']

for question in questions:
	#Generar el tsv con los datos
	for answer in answers:
		if answer['questionId'] == question['id']:
			respuestas = answer['answers']
			yrange = max(answer['answers'])

	respuestastsv = ''
	cont = 0
	for res in question['answers']:
		respuestastsv += str(respuestas[res['id']-1]) + ' ' + res['text'].encode('utf-8')
		cont+=1

	file = open('respuestas.tsv', 'w+')
	file.write(respuestastsv) # python will convert \n to os.linesep
	file.close()

	gnuplot = "\
	# ______________________________________________________________________\n\
	#Setting output\n\
	set term png\n\
	set output \"./Plots/plot"+str(question['id'])+".png\"\n\
	# For the next graph, we want a histogram.\n\
	set style data boxes\n\
	# set xrange [0:"+str(question['numAnswers'])+"]\n\
	# set yrange [0:"+str(yrange)+"]\n\
	# set xtics rotate by -45\n\
	\n\
	# We want a small gap between solid (filled-in) bars.\n\
	set boxwidth 0.8 relative\n\
	set style fill solid 1.0\n\
	\n\
	# Plot the histogram (one curve).\n\
	plot 'respuestas.tsv' using 1:xtic(2) with boxes title '"+question['text'].strip('\n').encode('utf-8')+"'\n\
	"
	file = open('tmp.gp', 'w+')
	file.write(gnuplot) # python will convert \n to os.linesep
	file.close()
#
#
#
#
	system('gnuplot tmp.gp')
	remove('respuestas.tsv')
	remove('tmp.gp')
