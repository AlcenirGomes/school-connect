from flask import Flask, jsonify, request

app = Flask(__name__)

#Dicionario de professores
@app.route('/',methods=['GET'])
def index():
  return jsonify()

#Consultar Professor por ID.
#Quando for consultar, prestar atencao na sintaxe.
@app.route('/',methods=['GET'])
def index():
  return jsonify({'error': 'Professor não encontrado'})

@app.route('/',methods=['PUT'])
def index():
  return jsonify({'error': 'Professor nao encontrado'})

