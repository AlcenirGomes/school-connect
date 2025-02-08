from flask import Flask, request
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

# Cadastrar Professores
# Metodo POST
@app.route('/professores', methods=['POST'])
def cadastrar_professor():
  id = sorted(professores.keys())[-1] + 1
  novo_professor = {
    'id': request.json['id'],
    'nome': request.json['nome'],
    'idade': request.json['idade'],
    'data_nascimento': request.json['data_nascimento'],
    'disciplina': request.json['disciplina'],
    'salario': request.json['salario']
  }
  professores[id] = novo_professor
  return novo_professor
    
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
