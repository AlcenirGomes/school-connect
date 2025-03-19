from flask import Flask, request, jsonify

app = Flask(__name__)

listas = {
    "alunos":[
         {'id': 1, 'nome': 'Alcenir Gomes da Costa', 'idade': 38, 'data_nascimento': '06/03/1987', 'nota_primeiro_semestre': 9, 'nota_segundo_semestre': 8, 'media_final': 8.5, 'turma_id': 1},   
    ],
    "professor":[
        {'id':1, 'nome': 'Fernando da silva', 'idade': 34},
    ],
    "turmas":[
        {'id': 1, 'nome':'turma A'},
    ]
}

class AlunoNaoExiste(Exception):
    pass


@app.route('/alunos', methods=['GET'])  
def get_alunos():
    dados = listas['alunos']
    return jsonify(dados)

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    novo = request.json
    alunos = listas['alunos']
    alunos.append(novo)

    for aluno in alunos:
        if aluno['id'] == novo['id']:
            return jsonify({'erro': 'id ja utilizado'}), 400
        
    return jsonify(novo), 200

@app.route('/alunos/<int:id>', methods=['POST'])
def id_existente(id):
    for aluno in listas['alunos']:
        if aluno['id'] == id:
            return jsonify({'erro': 'aluno ja cadastrado'}), 400

@app.route('/alunos/<int:id>', methods=['GET'])
def localizar_aluno(id):
    for aluno in listas['alunos']:
        if aluno['id'] == id:
            return jsonify(aluno)
    return jsonify({'erro': 'aluno nao encontrado'}), 404

@app.route('/alunos/<int:id>', methods=['PUT'])
def editar_aluno(id):
    for aluno in listas['alunos']:
        if aluno['id'] == id:
            novo = request.json

            aluno['nome'] = novo.get('nome', aluno['nome']) 
            aluno['idade'] = novo.get('idade', aluno['idade'])
            aluno['data_nascimento'] = novo.get('data_nascimento', aluno['data_nascimento'])
            aluno['nota_primeiro_semestre'] = novo.get('nota_primeiro_semestre', aluno['nota_primeiro_semestre'])
            aluno['nota_segundo_semestre'] = novo.get('nota_segundo_semestre', aluno['nota_segundo_semestre'])
            aluno['media_final'] = novo.get('media_final', aluno['media_final'])
            aluno['turma_id'] = novo.get('turma_id', aluno['turma_id'])
            return jsonify(aluno), 200
    return jsonify({'erro': 'aluno nao encontrado'}),404

@app.route('/reseta_alunos', methods=['POST'])
def reseta():
    listas['alunos'] = [] 
    return jsonify({'mensagem': 'Dados resetados com sucesso'})

@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    for aluno in listas['alunos']:
        if aluno['id'] == id:
            listas['alunos'].remove(aluno)
            return jsonify({'mensagem': 'Aluno removido com sucesso'})
    return jsonify({'erro': 'aluno nao encontrado'}), 404

@app.route('/professores', methods=['GET'])  
def get_professores():
    dados = listas['professor']
    return jsonify(dados)

@app.route('/professores', methods=['POST'])
def cadastrar_professor():
    novo = request.json
    professores = listas['professor']
    professores.append(novo)  
    return jsonify(novo)

@app.route('/professores/<int:id>', methods=['GET'])
def localizar_professor(id):
    for professor in listas['professor']:
        if professor['id'] == id:
            return jsonify(professor)
    return jsonify({'erro': 'professor nao encontrado'}), 400


@app.route('/reseta_professores', methods=['POST'])
def reset_professores():
    listas['professor'] = []
    return jsonify({'mensagem': 'Professores resetados com sucesso'})

@app.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    for professor in listas['professor']:
        if professor['id'] == id:
            listas['professor'].remove(professor)
            return jsonify({'mensagem': 'Professor removido com sucesso'})
    return jsonify({'erro': 'professor nao encontrado'}), 400


@app.route('/professores/<int:id>', methods=['PUT'])
def editar_professor(id):
    for professor in listas['professor']:
        if professor['id'] == id:
            novo = request.json
            professor['nome'] = novo.get('nome', professor['nome']) 
            return jsonify(professor), 200
    return jsonify({'erro': 'professor nao encontrado'}),400

#----------------------------------------------TURMAS-------------------------------------------------------#

@app.route('/turmas', methods=['GET'])  
def get_turmas():
    dados = listas['turmas']
    return jsonify(dados)

@app.route('/turmas', methods=['POST'])
def cadastrar_turmas():
    novo = request.json
    turmas = listas['turmas']

    for turma in turmas:
        if turma['id'] == novo['id']:
            return jsonify({'erro': 'id ja utilizado'}), 400
        
    turmas.append(novo)
    return jsonify(novo), 200

@app.route('/turmas/<int:id>', methods=['POST'])
def id_existente_turma(id):
    for turma in listas['turmas']:
        if turma['id'] == id:
            return jsonify({'erro': 'turma ja cadastrado'}), 400

@app.route('/turmas/<int:id>', methods=['GET'])
def localizar_turma(id):
    for turma in listas['turmas']:
        if turma['id'] == id:
            return jsonify(turma)
    return jsonify({'erro': 'turma nao encontrado'}), 404

@app.route('/turmas/<int:id>', methods=['PUT'])
def editar_turmas(id):
    for turma in listas['turmas']:
        if turma['id'] == id:
            novo = request.json
            turma['nome'] = novo.get('nome', turma['nome']) 
            return jsonify(turma), 200
    return jsonify({'erro': 'professor nao encontrado'}),400

@app.route('/reseta_turmas', methods=['POST'])
def reseta_turmas():
    listas['turmas'] = []
    return jsonify({'mensagem': 'Dados das turmas resetados com sucesso'}), 200

@app.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turmas(id):
    for turma in listas['turmas']:
        if turma['id'] == id:
            listas['turmas'].remove(turma)
            return jsonify({'mensagem': 'turma removida com sucesso'})
    return jsonify({'erro': 'turma nao encontrada'}), 404




if __name__ == '__main__':
    app.run(debug=True)