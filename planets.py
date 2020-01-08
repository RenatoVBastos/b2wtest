from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'star'
app.config['MONGO_URI'] = 'mongodb+srv://renatovbastos:1123581321a@starwarsplanet-g4ewa.gcp.mongodb.net/test?retryWrites=true&w=majority'


mongo = PyMongo(app)


#Lista de planetas
@app.route('/planet', methods=['GET'])
def get_all_planets():
	planets = mongo.db.planets

	output = []

	for q in planets.find():
		output.append ({ 'Nome' : q['Nome'], 'Clima' : q['Clima'], 'Terreno' : q['Terreno'], 'Aparicoes' : q['Aparicoes']})
	return jsonify({'Resultado' : output})	


#Pesquisar por planeta
@app.route('/planet/<nome>' , methods = ['GET'])
def get_one_planet(nome):
	planets = mongo.db.planets

	query = planets.find_one({'Nome' : nome} )


	if query:

		output = ({'Nome' : query['Nome'], 
			'Clima' : query['Clima'], 
			'Terreno' : query['Terreno'], 
			'Aparicoes' : query['Aparicoes']
				})

	else:
		output = 'Nenhum resultado encontrado'	

	return jsonify({'Resultado' : output})



#Pesquisar por ID
@app.route('/<planetid>' , methods = ['GET'])
def get_one_id(planetid):
	planets = mongo.db.planets

	query = planets.find_one({'_id' : ObjectId(planetid)})


	if query:

		output = ({'Nome' : query['Nome'], 
		'Clima' : query['Clima'], 
		'Terreno' : query['Terreno'], 
		'Aparicoes' : query['Aparicoes']})

	
		
	return jsonify({'Resultado' : output})


#Cadastrar planeta
@app.route('/planet', methods=['POST'])
def add_planet():
	planet = mongo.db.planets

	Nome = request.json['Nome']
	Clima = request.json['Clima']
	Terreno = request.json['Terreno']
	Aparicoes = request.json['Aparicoes']

	planet_id = planet.insert({'Nome' : Nome, 'Clima' : Clima, 'Terreno' : Terreno, 'Aparicoes' : Aparicoes })
	new_planet = planet.find_one({'_id' : planet_id})

	output = {'Nome' : new_planet['Nome'], 
	'Clima' : new_planet['Clima'], 
	'Terreno' : new_planet['Terreno'], 
	'Aparicoes' : new_planet['Aparicoes']}

	return jsonify({'Resultado' : output})

#Apagar planeta
@app.route('/planet/<nome>', methods = ['DELETE'])
def remove_planet(nome):
	planets = mongo.db.planets

	query = planets.find_one({'Nome' : nome})

	if query:

		output = ({'Nome' : query['Nome'], 
			'Clima' : query['Clima'], 
			'Terreno' : query['Terreno'], 
			'Aparicoes' : query['Aparicoes']
				})
		planets.remove(query)
	else:
		output = 'Nenhum resultado encontrado'	

	
	return ('Apagado com sucesso!')




 

if __name__ == '__main__':
	app.run(debug=True)