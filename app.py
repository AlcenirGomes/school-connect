from flask import Flask, jsonify, request
from professor import professores
from aluno import alunos

app = Flask(__name__)

# Consultar Professores.
# Metodo GET.
@app.route('/professores', methods=['GET'])
def consultar_professores():
  return professores

# Consultar professor por ID.
# Quando for consultar, prestar atenção na sintaxe.
# Metodo GET.
@app.route('/professores/<int:professor_id>', methods=['GET'])
def consultar_professor(professor_id):
  return professores.get(
    professor_id, {'error': 'Professor não encontrado.'}
  )

# Cadastrar Professores.
# Metodo POST.
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
  return {'message': 'Novo professor cadastrado com sucesso.'}

# Deletar Professores.
# Metodo DELETE.
@app.route('/professores/<int:professor_id>', methods=['DELETE'])
def deletar_professor(professor_id):
  if professor_id in professores.keys():
    del professores[professor_id]
    return {'message': 'Professor excluído com sucesso.'}
  else:
    return {'error': 'Professor não encontrado.'}

# Alterar ou atualizar Professores por ID.
# Metodo PUT.
@app.route('/professores/<int:professor_id>', methods=['PUT'])
def atualizar_professor(professor_id):
	if professor_id in professores.keys():
		professores[professor_id]['id']=request.json['id']
		professores[professor_id]['nome']=request.json['nome']
		professores[professor_id]['idade']=request.json['idade']
		professores[professor_id]['data_nascimento']=request.json['data_nascimento']
		professores[professor_id]['disciplina']=request.json['disciplina']
		professores[professor_id]['salario']=request.json['salario']
		return {'message': 'Professor atualizado com sucesso.'}
	else:
		return {'error': 'Professor não encontrado.'}
    
# Consultar Alunos.
# Metodo GET.
@app.route('/alunos', methods=['GET'])
def consultar_alunos():
  return alunos

# Consultar aluno por ID.
# Quando for consultar, prestar atenção na sintaxe.
# Metodo GET.
@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def consultar_aluno(aluno_id):
  return alunos.get(
    aluno_id, {'error': 'Aluno não encontrado.'}
  )

# Cadastrar Alunos.
# Metodo POST.
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
  id = sorted(alunos.keys())[-1] + 1
  novo_aluno = {
    'id':request.json['id'],
    'nome': request.json['nome'],
    'idade': request.json['idade'],
    'data_nascimento': request.json['data_nascimento'],
    'nota_primeiro_semestre': request.json['nota_primeiro_semestre'],
    'nota_segundo_semestre': request.json['nota_segundo_semestre'],
    'media_final': request.json['media_final'],
    'turma_id': request.json['turma_id']
  }
  alunos[id] = novo_aluno
  return {'message': 'Novo aluno cadastrado com sucesso.'}

# Deletar Alunos.
# Metodo DELETE.
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
	if aluno_id in alunos.keys():
		del alunos[aluno_id]
		return {'message': 'Aluno deletado com sucesso.'}
	else:
		return {'error': 'Aluno não encontrado.'}

# Alterar ou atualizar Alunos por ID.
# Metodo PUT.
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
	if aluno_id in alunos.keys():
		alunos[aluno_id]['id']=request.json['id']
		alunos[aluno_id]['nome']=request.json['nome']
		alunos[aluno_id]['idade']=request.json['idade']
		alunos[aluno_id]['data_nascimento']=request.json['data_nascimento']
		alunos[aluno_id]['nota_primeiro_semestre']=request.json['nota_primeiro_semestre']
		alunos[aluno_id]['nota_segundo_semestre']=request.json['nota_segundo_semestre']
		alunos[aluno_id]['media_final']=request.json['media_final']
		alunos[aluno_id]['turma_id']=request.json['turma_id']
		return {'message': 'Aluno atualizado com sucesso.'}
	else:
		return {'error': 'Aluno não encontrado.'}

if __name__ == '__main__':
  app.run(debug=True)
