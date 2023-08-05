#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json
from ikabot.helpers.recursos import *

def borrar(texto, ocurrencias):
	for ocurrencia in ocurrencias:
		texto = texto.replace(ocurrencia, '')
	return texto

def getCiudadanosDisponibles(html):
	ciudadanosDisp = re.search(r'js_GlobalMenu_citizens">(.*?)</span>', html).group(1)
	return int(ciudadanosDisp.replace(',', ''))

def enVenta(html):
	rta = re.search(r'branchOfficeResources: JSON\.parse\(\'{\\"resource\\":\\"(\d+)\\",\\"1\\":\\"(\d+)\\",\\"2\\":\\"(\d+)\\",\\"3\\":\\"(\d+)\\",\\"4\\":\\"(\d+)\\"}\'\)', html)
	if rta:
		return [ int(rta.group(1)), int(rta.group(2)), int(rta.group(3)), int(rta.group(4)), int(rta.group(5))]
	else:
		return [0, 0, 0, 0, 0]

def getIsla(html):
	isla = re.search(r'\[\["updateBackgroundData",([\s\S]*?),"specialServerBadges', html).group(1) + '}'

	isla = isla.replace('buildplace', 'empty')
	isla = isla.replace('xCoord', 'x')
	isla = isla.replace('yCoord', 'y')
	isla = isla.replace(',"owner', ',"')
	isla = isla.replace(',"tradegoodLevel',',"goodLv')
	isla = isla.replace(',"tradegood', ',"good')
	isla = isla.replace(',"resourceLevel', ',"woodLv')
	isla = isla.replace(',"wonderLevel', ',"wonderLv')
	isla = isla.replace('avatarScores', 'scores')

	remove = []

	sub = re.search(r',"type":\d', isla).group()
	remove.append(sub)

	quitar = re.search(r'(,"barbarians[\s\S]*?),"scores"', isla).group(1)

	remove.append(quitar)
	remove.append(',"goodTarget":"tradegood"')
	remove.append(',"name":"Building ground"')
	remove.append(',"name":"Terreno"')
	remove.append(',"actions":[]')
	remove.append('"id":-1,')
	remove.append(',"level":0,"viewAble":1')
	remove.append(',"empty_type":"normal"')
	remove.append(',"empty_type":"premium"')
	remove.append(',"hasTreaties":0')
	remove.append(',"hasTreaties":1')
	remove.append(',"infestedByPlague":false')
	remove.append(',"infestedByPlague":true')
	remove.append(',"viewAble":0')
	remove.append(',"viewAble":1')
	remove.append(',"viewAble":2')
	isla = borrar(isla, remove)

	# {"id":idIsla,"name":nombreIsla,"x":,"y":,"good":numeroBien,"woodLv":,"goodLv":,"wonder":numeroWonder, "wonderName": "nombreDelMilagro","wonderLv":"5","cities":[{"type":"city","name":cityName,"id":cityId,"level":lvIntendencia,"Id":playerId,"Name":playerName,"AllyId":,"AllyTag":,"state":"vacation"},...}}
	isla = json.loads(isla, strict=False)
	tipo = re.search(r'"tradegood":"(\d)"', html).group(1)
	isla['tipo'] = tipo
	return isla

def getCiudad(html):
	ciudad = re.search(r'"updateBackgroundData",([\s\S]*?),"(?:beachboys|spiesInside)', html).group(1) + '}'

	ciudad = ciudad.replace(',"owner', ',"')
	ciudad = ciudad.replace('islandXCoord','x')
	ciudad = ciudad.replace('islandYCoord','y')
	ciudad = '{"cityName"' + ciudad[len('{"name"'):]

	remove = []

	sub = re.search(r',"buildingSpeedupActive":\d', ciudad)
	remove.append(sub.group())

	sub = re.search(r',"showPirateFortressBackground":\d', ciudad)
	remove.append(sub.group())

	sub = re.search(r',"showPirateFortressShip":\d', ciudad)
	remove.append(sub.group())

	ciudad = borrar(ciudad, remove)

	for elem in ['sea', 'land', 'shore', 'wall']:
		ciudad = ciudad.replace('"building":"buildingGround {}"'.format(elem),'"name":"empty","building":"empty"')
	ciudad = ciudad.replace('"isBusy":true,','"isBusy":false,')

	ampliando = re.findall(r'(("name":"[\w\s\\]*","level":"\d*","isBusy":false,"canUpgrade":\w*,"isMaxLevel":\w*,"building":"\w*?)\sconstructionSite","(?:completed|countdownText|buildingimg).*?)}',ciudad)
	for edificio in ampliando:
		viejo = edificio[1]+'"'
		nuevo = viejo.replace('"isBusy":false,', '"isBusy":true,')
		ciudad = ciudad.replace(edificio[0], nuevo)

	# {'cityName': '', 'id': 'idCiudad', 'phase': 5, 'isCapital': True|False, 'Id': 'idJugador', 'Name': 'nombreJugador', 'islandId': 'idIsla', 'islandName': 'NombreIsla', 'x': 'Coordx', 'y': 'Coordy', 'underConstruction': -1, 'endUpgradeTime': -1, 'startUpgradeTime': -1, 'position': [{'name': 'nombreEdificio', 'level': 'nivel', 'isBusy': True|False, 'canUpgrade': True|False, 'isMaxLevel': True|False, 'building': 'nombreEnIngles'}, ...]}
	ciudad = json.loads(ciudad, strict=False)
	ciudad['propia'] = True
	ciudad['recursos'] = getRecursosDisponibles(html, num=True)
	ciudad['capacidad'] = getCapacidadDeAlmacenamiento(html)
	ciudad['ciudadanosDisp'] = getCiudadanosDisponibles(html)
	ciudad['consumo'] = getConsumoDeVino(html)
	ciudad['enventa'] = enVenta(html)
	ciudad['libre'] = []
	for i in range(5):
		ciudad['libre'].append( ciudad['capacidad'] - ciudad['recursos'][i] - ciudad['enventa'][i] )
	return ciudad
