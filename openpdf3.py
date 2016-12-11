import json, re, sys, glob, math
import subprocess
from collections import OrderedDict

def ordena_subdata(data):
	new_data = {}
	for i in range(0,len(data)):
		new_sub_data = {}
		k = i + 1
		txt = 'Pregunta' + str(k)
		tmp = data[txt]
		#print(tmp)
		sub_elementos = []
		for j in range(0,len(tmp)):
			txt2 = 'Resposta' + str(j+1)
			tmp2 = tmp[txt2]
			trocito = {}
			trocito['Resposta'] = int(j+1)
			trocito['coord_x1'] = tmp2['coord_x1']
			trocito['coord_y1'] = tmp2['coord_y1']
			sub_elementos.append(trocito)
		newlist = []
		if(len(tmp)>1):
			if(sub_elementos[0]['coord_y1'] == sub_elementos[1]['coord_y1']):
				#si coinciden las y, es que las respuestas van el horizontal
				newlist = sorted(sub_elementos, key=lambda k: k['coord_x1'])
			else:
				#si no coinciden las y, es que las respuestas van en vertical
				newlist = sorted(sub_elementos, key=lambda k: k['coord_y1'], reverse=True)
			subdatin = {}
			cont = 1
			miro_x = 1
			for g in range (0,len(newlist)):
				respord = newlist[g]
				for original in range (0,len(tmp)):
					text = 'Resposta' + str(original+1)
					resp = tmp[text]
					if(g == 0):
						if(newlist[g]['coord_x1'] == newlist[g+1]['coord_x1']):
							miro_x = 0
						else:
							miro_x = 1
					if(miro_x == 1):
						if(respord['coord_x1'] == resp['coord_x1']):
							textin = 'Resposta' + str(cont)
							cont = cont + 1
							subdatin[textin] = resp
					elif(miro_x == 0):
						if(respord['coord_y1'] == resp['coord_y1']):
							textin = 'Resposta' + str(cont)
							cont = cont + 1
							subdatin[textin] = resp
		new_data[txt] = subdatin
	result = new_data
	return result

def fill_json(coordsP,coordsR):
	data = {}
	k = 0
	for i in range(0,len(coordsP)):
		k = k + 1
		txt = "Pregunta" + str(k)
		l = 0
		sub_data = {}
		for j in range(0,len(coordsR)):
			if(i < len(coordsP) - 1):
				preg1 = coordsP[i]
				preg2 = coordsP[i+1]
				resp = coordsR[j]
				if((resp['coord_y1'] < preg1['coord_y3']) and (resp['coord_y3'] > preg2['coord_y1'])):
					l = l + 1
					txt2 = "Resposta" + str(l)
					sub_sub_data = {}
					sub_sub_data['num'] = int(l)
					sub_sub_data['coord_x1'] = float(resp['coord_x1'])
					sub_sub_data['coord_y1'] = float(resp['coord_y1'])
					sub_sub_data['coord_x2'] = float(resp['coord_x2'])
					sub_sub_data['coord_y2'] = float(resp['coord_y2'])
					sub_sub_data['coord_x3'] = float(resp['coord_x3'])
					sub_sub_data['coord_y3'] = float(resp['coord_y3'])
					sub_sub_data['coord_x4'] = float(resp['coord_x4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['centre_x'] = (( float(resp['coord_x1']) + float(resp['coord_x2']) )/2)
					sub_sub_data['centre_y'] = (( float(resp['coord_y1']) + float(resp['coord_y3']) )/2)
					sub_sub_data['Marcada'] = "NO"
					sub_data[txt2] = sub_sub_data
				elif((preg1['coord_y1']==resp['coord_y1']) and (resp['coord_x2'] > preg1['coord_x1'])):
					l = l + 1
					txt2 = "Resposta" + str(l)
					sub_sub_data = {}
					sub_sub_data['num'] = int(l)
					sub_sub_data['coord_x1'] = float(resp['coord_x1'])
					sub_sub_data['coord_y1'] = float(resp['coord_y1'])
					sub_sub_data['coord_x2'] = float(resp['coord_x2'])
					sub_sub_data['coord_y2'] = float(resp['coord_y2'])
					sub_sub_data['coord_x3'] = float(resp['coord_x3'])
					sub_sub_data['coord_y3'] = float(resp['coord_y3'])
					sub_sub_data['coord_x4'] = float(resp['coord_x4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['centre_x'] = (( float(resp['coord_x1']) + float(resp['coord_x2']) )/2)
					sub_sub_data['centre_y'] = (( float(resp['coord_y1']) + float(resp['coord_y3']) )/2)
					sub_sub_data['Marcada'] = "NO"
					sub_data[txt2] = sub_sub_data

				#para poner la coordenadas en las preguntas
				#sub_data['p-coord_x1'] = float(preg1['coord_x1'])
				#sub_data['p-coord_y1'] = float(preg1['coord_y1'])
				#sub_data['p-coord_x2'] = float(preg1['coord_x2'])
				#sub_data['p-coord_y2'] = float(preg1['coord_y2'])
				#sub_data['p-coord_x3'] = float(preg1['coord_x3'])
				#sub_data['p-coord_y3'] = float(preg1['coord_y3'])
				#sub_data['p-coord_x4'] = float(preg1['coord_x4'])
				#sub_data['p-coord_y4'] = float(preg1['coord_y4'])
				#sub_data['p-coord_y4'] = float(preg1['coord_y4'])
				#sub_data['numero_pregunta'] = k

			elif(i == len(coordsP) -1):
				#ultimo caso
				preg = coordsP[i]
				resp = coordsR[j]
				if(resp['coord_y1'] < preg['coord_y3']):
					l = l + 1
					txt2 = "Resposta" + str(l)
					sub_sub_data = {}
					sub_sub_data['num'] = int(l)
					sub_sub_data['coord_x1'] = float(resp['coord_x1'])
					sub_sub_data['coord_y1'] = float(resp['coord_y1'])
					sub_sub_data['coord_x2'] = float(resp['coord_x2'])
					sub_sub_data['coord_y2'] = float(resp['coord_y2'])
					sub_sub_data['coord_x3'] = float(resp['coord_x3'])
					sub_sub_data['coord_y3'] = float(resp['coord_y3'])
					sub_sub_data['coord_x4'] = float(resp['coord_x4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['centre_x'] = (( float(resp['coord_x1']) + float(resp['coord_x2']) )/2)
					sub_sub_data['centre_y'] = (( float(resp['coord_y1']) + float(resp['coord_y3']) )/2)
					sub_sub_data['Marcada'] = "NO"
					sub_data[txt2] = sub_sub_data
				elif((preg['coord_y1']==resp['coord_y1']) and (resp['coord_x2'] > preg['coord_x1'])):
					l = l + 1
					txt2 = "Resposta" + str(l)
					sub_sub_data = {}
					sub_sub_data['num'] = int(l)
					sub_sub_data['coord_x1'] = float(resp['coord_x1'])
					sub_sub_data['coord_y1'] = float(resp['coord_y1'])
					sub_sub_data['coord_x2'] = float(resp['coord_x2'])
					sub_sub_data['coord_y2'] = float(resp['coord_y2'])
					sub_sub_data['coord_x3'] = float(resp['coord_x3'])
					sub_sub_data['coord_y3'] = float(resp['coord_y3'])
					sub_sub_data['coord_x4'] = float(resp['coord_x4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['coord_y4'] = float(resp['coord_y4'])
					sub_sub_data['centre_x'] = (( float(resp['coord_x1']) + float(resp['coord_x2']) )/2)
					sub_sub_data['centre_y'] = (( float(resp['coord_y1']) + float(resp['coord_y3']) )/2)
					sub_sub_data['Marcada'] = "NO"
					sub_data[txt2] = sub_sub_data

				#para poner la coordenadas en las preguntas

				#sub_data['p-coord_x1'] = float(preg['coord_x1'])
				#sub_data['p-coord_y1'] = float(preg['coord_y1'])
				#sub_data['p-coord_x2'] = float(preg['coord_x2'])
				#sub_data['p-coord_y2'] = float(preg['coord_y2'])
				#sub_data['p-coord_x3'] = float(preg['coord_x3'])
				#sub_data['p-coord_y3'] = float(preg['coord_y3'])
				#sub_data['p-coord_x4'] = float(preg['coord_x4'])
				#sub_data['p-coord_y4'] = float(preg['coord_y4'])
				#sub_data['numero_pregunta'] = k

		data[txt] = sub_data
	tmp = ordena_subdata(data)
	return tmp

def getQuestions(fileName):
	comando = 'cat -v ' + fileName
	text = subprocess.check_output(comando, shell=True)
	text = text.decode('utf-8')

	#buscamos la coordenadas de los highlights
	array = []
	for m in re.finditer('/QuadPoints ', text):
		coords = {}
		coords['end'] = m.end()
		array.append(coords)

	#buscamos los colores
	array2 = []
	for m2 in re.finditer('/C ', text):
		coords2 = {}
		coords2['end2'] = m2.end()
		array2.append(coords2)

	#arrays para las coordenadas de ls preguntas y de las respuestas, respectivamente
	coordsP = []
	coordsR = []
	maximoOP = 10000000000
	for k in range(0,len(array)):
		#nos quedamos las coordenadas
		c1 = array[k]
		coordenadas = text[c1['end']+1:c1['end']+100]
		coordenadas = coordenadas.split(' ')

		point1 = text.find('/P ', c1['end']+100,len(text))
		point2 = text.find('R', point1,len(text))
		pagina = text[point1:point2]
		pagina = pagina.split(' ')

		#nos quedamos el color
		c2 = array2[k]
		color = text[c2['end2']+1:c2['end2']+6]

		sub_coord = {}
		sub_coord['coord_x1'] = coordenadas[0]
		sub_coord['coord_y1'] = float(coordenadas[1])+(maximoOP/float(pagina[1]))
		sub_coord['coord_x2'] = coordenadas[2]
		sub_coord['coord_y2'] = float(coordenadas[3])+(maximoOP/float(pagina[1]))
		sub_coord['coord_x3'] = coordenadas[4]
		sub_coord['coord_y3'] = float(coordenadas[5])+(maximoOP/float(pagina[1]))
		sub_coord['coord_x4'] = coordenadas[6]
		sub_coord['coord_y4'] = float(coordenadas[7])+(maximoOP/float(pagina[1]))

		color = color.replace(' ','')

		if(color == '110'):
			coordsR.append(sub_coord)
		elif(color == '011'):
			coordsP.append(sub_coord)
	print(array)
	#omplim json
	data = fill_json(coordsP,coordsR)

	text_file = open('json.json','w')
	text_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

	text_file.close()

def getAnswers():
	id = 1
	for filename in glob.glob('*.pdf'):
		s = "cat -v "
		s = s + filename
		text = subprocess.check_output(s, shell=True)
		text = text.decode('utf-8')
		array = []
		cords = []
		for m in re.finditer('/InkList', text):
			coords = {}
			coords['end'] = m.end()
			array.append(coords)
		for k in range(0,len(array)):
			#nos quedamos las coordenadas
			c1 = array[k]
			coordenadas = text[c1['end']+3:]
			c = coordenadas.find(']')
			cor = coordenadas[:c-1]
			cor = cor.split(' ')

			point1 = coordenadas.find('/P ', c,len(coordenadas))
			point2 = coordenadas.find('R', point1,len(coordenadas))
			pagina = coordenadas[point1:point2]
			pagina = pagina.split(' ')

			c_x = abs(float(cor[0]) + float(cor[len(cor)-2])) /2
			c_y = abs((float(cor[1])+(10000000000/float(pagina[1]))) + float((cor[len(cor)-1]))+(10000000000/float(pagina[1]))) /2
			cor_prov = {}
			cor_prov['x'] = c_x
			cor_prov['y'] = c_y
			cords.append(cor_prov)

		for m in re.finditer('/QuadPoints', text):
			coords = {}
			coords['end'] = m.end()
			array.append(coords)
		for k in range(0,len(array)):
			#nos quedamos las coordenadas
			c1 = array[k]
			coordenadas = text[c1['end']+3:]
			c = coordenadas.find(']')
			cor = coordenadas[:c-1]
			cor = cor.split(' ')

			point1 = coordenadas.find('/P ', c,len(coordenadas))
			point2 = coordenadas.find('R', point1,len(coordenadas))
			pagina = coordenadas[point1:point2]
			pagina = pagina.split(' ')

			c_x = abs(float(cor[0]) + float(cor[len(cor)-2])) /2
			c_y = abs((float(cor[1])+(10000000000/float(pagina[1]))) + float((cor[len(cor)-1]))+(10000000000/float(pagina[1]))) /2
			cor_prov = {}
			cor_prov['x'] = c_x
			cor_prov['y'] = c_y
			cords.append(cor_prov)

		with open('json.json') as text_file:
			data = json.load(text_file)
		resultat = {}
		for x in cords:
			#print (x)
			min= 99999999999999999999999999999999999999
			pregunta = "no"
			respuesta = "se sae"
			for p in data:
				for r in data[p]:
					if(data[p]["Resposta1"]["coord_y1"]!=data[p]["Resposta2"]["coord_y1"]):
						yses = abs(float(data[p][r]["centre_y"])-float(x['y']))
						if(abs(yses) < min):
							min = abs(yses)
							pregunta = p
							respuesta = r
					else:
						xses = abs(float(data[p][r]["centre_x"])-float(x['x']))
						yses = abs(float(data[p][r]["centre_y"])-float(x['y']))
						if(abs(xses+yses) < min):
							min = abs(xses+yses)
							pregunta = p
							respuesta = r
			resultat[pregunta] = respuesta

		filename = filename.replace('.pdf','')
		stringo = str(id) + '.-' + filename + '.json'
		text_file = open(stringo,'w')
		text_file.write(json.dumps(resultat, sort_keys=True, indent=4, separators=(',', ': ')))
		text_file.close()
		id = id + 1


op = input("Selecciona una opción( 1 para la primera pasada, 2 para escanear las respuestas): ")
if(op=='1'):
	fileName = input("Indica el nombre con la extensión del pdf con las preguntas y respuestas marcadas (ej: SLDSpreguntas.pdf): ")
	getQuestions(fileName)
elif(op == '2'):
	getAnswers()
