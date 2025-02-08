from flask import Flask, jsonify, request
from professor import professores
from aluno import alunos

app = Flask(__name__)

# Consultar Professores
# Metodo GET
@app.route('/professores', methods=['GET'])
def consultar_professores():
  return professores

# Consultar professor por ID.
# Quando for consultar, prestar atenção na sintaxe.
# Metodo GET
@app.route('/professores/<int:professor_id>', methods=['GET'])
def consultar_professor(professor_id):
  return professores.get(
    professor_id, {'error': 'Professor não encontrado'}
  )

# Consultar Alunos
# Metodo GET
@app.route('/alunos', methods=['GET'])
def consultar_alunos():
  return alunos

# Consultar aluno por ID.
# Quando for consultar, prestar atenção na sintaxe.
# Metodo GET
@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def consultar_aluno(aluno_id):
  return alunos.get(
    aluno_id, {'error': 'Professor não encontrado'}
  )

if __name__ == '__main__':
  app.run(debug=True)
