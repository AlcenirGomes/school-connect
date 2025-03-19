import requests
import unittest

class TestStringMethods(unittest.TestCase):


    def test_000_alunos_retorna_lista(self):
        #pega a url /alunos, com o verbo get
        r = requests.get('http://localhost:5000/alunos')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /alunos no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado),type([]))

    def test_001_adiciona_alunos(self):
        #criar dois alunos (usando post na url /alunos)
        r = requests.post('http://localhost:5000/alunos',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5000/alunos',json={'nome':'roberto','id':2})
        
        #pego a lista de alunos (do mesmo jeito que no teste 0)
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei aparecem
        achei_fernando = False
        achei_roberto = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'fernando':
                achei_fernando = True
            if aluno['nome'] == 'roberto':
                achei_roberto = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_fernando:
            self.fail('aluno fernando nao apareceu na lista de alunos')
        if not achei_roberto:
            self.fail('aluno roberto nao apareceu na lista de alunos')

    def test_002_alunos_por_id(self):
        #cria um aluno 'mario', com id 20
        r = requests.post('http://localhost:5000/alunos',json={'nome':'mario','id':20})

        #consulta a url /alunos/20, pra ver se o aluno está lá
        resposta = requests.get('http://localhost:5000/alunos/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado),dict)
        self.assertIn('nome',dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'],'mario') # no dic, o nome tem que ser o que eu mandei tem que ser mario


    #adiciona um aluno, mas depois reseta o servidor e o aluno deve desaparecer
    def test_003_reseta_alunos(self):
        #criei um aluno, com post
        r = requests.post('http://localhost:5000/alunos',json={'nome':'cicero','id':29})
        #peguei a lista
        r_lista = requests.get('http://localhost:5000/alunos')
        #no momento, a lista tem que ter mais de um aluno
        self.assertTrue(len(r_lista.json()) > 0)

        #POST na url reseta: deveria apagar todos os dados do servidor
        r_reset = requests.post('http://localhost:5000/reseta_alunos')

        #estou verificando se a url reseta ou nao se voce ainda nao definiu ela, esse cod status nao vai ser 200
        self.assertEqual(r_reset.status_code,200)

        #pego de novo a lista
        r_lista_depois = requests.get('http://localhost:5000/alunos')
        
        #e agora tem que ter 0 elementos
        self.assertEqual(len(r_lista_depois.json()),0)

    #esse teste adiciona 2 alunos, depois deleta 1 e verifica que o numero de alunos realmente diminuiu
    def test_004_deleta_alunos(self):
        #apago tudo
        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        self.assertEqual(r_reset.status_code,200)
   
        #crio 3 alunos
        requests.post('http://localhost:5000/alunos',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5000/alunos',json={'nome':'lucas','id':28})
        requests.post('http://localhost:5000/alunos',json={'nome':'marta','id':27})
   
        #pego a lista completa
        r_lista = requests.get('http://localhost:5000/alunos')
        lista_retornada = r_lista.json()
        
        #a lista completa tem que ter 3 elementos
        self.assertEqual(len(lista_retornada),3)
        
        #faço um request com delete, pra deletar o aluno de id 28
        requests.delete('http://localhost:5000/alunos/28')
        
        #pego a lista de novo
        r_lista2 = requests.get('http://localhost:5000/alunos')
        lista_retornada2 = r_lista2.json()
        
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada2),2) 

        acheiMarta = False
        acheiCicero = False
        for aluno in lista_retornada:
            if aluno['nome'] == 'marta':
                acheiMarta=True
            if aluno['nome'] == 'cicero':
                acheiCicero=True
        if not acheiMarta or not acheiCicero:
            self.fail("voce parece ter deletado o aluno errado!")

        requests.delete('http://localhost:5000/alunos/27')

        r_lista3 = requests.get('http://localhost:5000/alunos')
        lista_retornada3 = r_lista3.json()
       
        #e vejo se ficou só um elemento
        self.assertEqual(len(lista_retornada3),1) 

        if lista_retornada3[0]['nome'] == 'cicero':
            pass
        else:
            self.fail("voce parece ter deletado o aluno errado!")


    #cria um usuário, depois usa o verbo PUT para alterar o nome do usuário
    def test_005_edita_alunos(self):
        #resetei
        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        
        #verifiquei se o reset foi
        self.assertEqual(r_reset.status_code,200)

        #criei um aluno
        requests.post('http://localhost:5000/alunos',json={'nome':'lucas','id':28})
        
        #e peguei o dicionario dele
        r_antes = requests.get('http://localhost:5000/alunos/28')
        
        #o nome enviado foi lucas, o nome recebido tb
        self.assertEqual(r_antes.json()['nome'],'lucas')
        
        #vou editar. Vou mandar um novo dicionario p/ corrigir o dicionario que já estava no 28 (note que só mandei o nome) para isso, uso o verbo PUT
        requests.put('http://localhost:5000/alunos/28', json={'nome':'lucas mendes'})
        
        #pego o novo dicionario do aluno 28
        r_depois = requests.get('http://localhost:5000/alunos/28')
        
        #agora o nome deve ser lucas mendes
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')
        
        #mas o id nao mudou
        self.assertEqual(r_depois.json()['id'],28)

    #tenta fazer GET, PUT e DELETE num aluno que nao existe
    def test_006a_id_inexistente_no_put_alunos(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        
        #estou tentando EDITAR um aluno que nao existe (verbo PUT)
        r = requests.put('http://localhost:5000/alunos/15',json={'nome':'bowser','id':15})
        
        #tem que dar erro 400 ou 404 ou seja, r.status_code tem que aparecer na lista [400,404]
        self.assertIn(r.status_code,[400,404])

        #qual a resposta que a linha abaixo pede? um json, com o dicionario {"erro":"aluno nao encontrado"}
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
    
    def test_006b_id_inexistente_no_get_alunos(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        
        #agora faço o mesmo teste pro GET, a consulta por id
        r = requests.get('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        
        #olhando pra essa linha debaixo, o que está especificado que o servidor deve retornar
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')
        # ----------------------------
        # string json
        # ----------------------------
        # que representa um dicionario
        # ---------------------------- 
        # o dict tem a chave erro
        # ----------------------------
        # o valor da chave erro
        
    def test_006c_id_inexistente_no_delete_alunos(self):
        #reseto
        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        
        #vejo se nao deu pau resetar
        self.assertEqual(r_reset.status_code,200)
        r = requests.delete('http://localhost:5000/alunos/15')
        self.assertIn(r.status_code,[400,404])
        self.assertEqual(r.json()['erro'],'aluno nao encontrado')

        #404 usuário tentou acessar um recurso inexistente
        #400 usuário fez alguma besteira
        #toda vez que o servidor retorna 404, ele
        #poderia, se quisesse, retornar o erro MENOS INFORMATIVO
        #400. Talvez fosse sacanagem com o programador do outro
        #lado, mas nao seria mentira

#------------------------------------TESTES PROFESSOR----------------------------------------#    

    def test_007_professor_retorna_lista(self):
        r = requests.get('http://localhost:5000/professores')
        self.assertEqual(type(r.json()),type([]))
    
    def test_008_adiciona_professor(self):
        r = requests.post('http://localhost:5000/professores',json={'nome':'fernando','id':1})
        r = requests.post('http://localhost:5000/professores',json={'nome':'roberto','id':2})
        r_lista = requests.get('http://localhost:5000/professores')
        achei_fernando = False
        achei_roberto = False
        for professor in r_lista.json():
            if professor['nome'] == 'fernando':
                achei_fernando = True
            if professor['nome'] == 'roberto':
                achei_roberto = True
        if not achei_fernando:
            self.fail('professor fernando nao apareceu na lista de professores')
        if not achei_roberto:
            self.fail('professor roberto nao apareceu na lista de professores')

    def test_009_professores_por_id(self):
        r = requests.post('http://localhost:5000/professores',json={'nome':'mario','id':20})
        r_lista = requests.get('http://localhost:5000/professores/20')
        self.assertEqual(r_lista.json()['nome'],'mario')
 
    def test_010_adiciona_e_reseta_professor(self):
        r = requests.post('http://localhost:5000/professores',json={'nome':'cicero','id':29})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertTrue(len(r_lista.json()) > 0)
        r_reset = requests.post('http://localhost:5000/reseta_professores')
        self.assertEqual(r_reset.status_code,200)
        r_lista_depois = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista_depois.json()),0)

    def test_011_deleta_professor(self):
        r_reset = requests.post('http://localhost:5000/reseta_professores')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={'nome':'cicero','id':29})
        requests.post('http://localhost:5000/professores',json={'nome':'lucas','id':28})
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        requests.delete('http://localhost:5000/professores/28')
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),1)
    
    def test_012_edita_professor(self):
        r_reset = requests.post('http://localhost:5000/reseta_professores')
        self.assertEqual(r_reset.status_code,200)
        requests.post('http://localhost:5000/professores',json={'nome':'lucas','id':28})
        r_antes = requests.get('http://localhost:5000/professores/28')
        self.assertEqual(r_antes.json()['nome'],'lucas')
        requests.put('http://localhost:5000/professores/28', json={'nome':'lucas mendes'})
        r_depois = requests.get('http://localhost:5000/professores/28')
        self.assertEqual(r_depois.json()['nome'],'lucas mendes')

    def test_013_id_inexistente_professor(self):
        r_reset = requests.post('http://localhost:5000/reseta_professores')
        self.assertEqual(r_reset.status_code,200)
        r = requests.put('http://localhost:5000/professores/15',json={'nome':'bowser','id':15})
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.get('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')
        r = requests.delete('http://localhost:5000/professores/15')
        self.assertEqual(r.status_code,400)
        self.assertEqual(r.json()['erro'],'professor nao encontrado')

    def test_014_nao_confundir_professor_e_aluno(self):

        r_reset = requests.post('http://localhost:5000/reseta_alunos')
        r = requests.post('http://localhost:5000/professores',json={'nome':'fernando','id':1})
        self.assertEqual(r.status_code,200)
        r = requests.post('http://localhost:5000/professores',json={'nome':'roberto','id':2})
        self.assertEqual(r.status_code,200)
        r_lista = requests.get('http://localhost:5000/professores')
        self.assertEqual(len(r_lista.json()),2)
        r_lista_alunos = requests.get('http://localhost:5000/alunos')
        self.assertEqual(len(r_lista_alunos.json()),0)


#------------------------------------TESTES TURMAS----------------------------------------------------------#

    def test_015_turmas_retorna_lista(self):
        #pega a url /turmas, com o verbo get
        r = requests.get('http://localhost:5000/turmas')

        #o status code foi pagina nao encontrada?
        if r.status_code == 404:
            self.fail("voce nao definiu a pagina /turmas no seu server")

        try:
            obj_retornado = r.json()
            #r.json() é o jeito da biblioteca requests
            #de pegar o arquivo que veio e transformar
            #em lista ou dicionario.
            #Vou dar erro se isso nao for possivel
        except:
            self.fail("queria um json mas voce retornou outra coisa")

        #no caso, tem que ser uma lista
        self.assertEqual(type(obj_retornado), type([]))

    def test_016_adiciona_turmas(self):
        #criar duas turmas (usando post na url /turmas)
        r = requests.post('http://localhost:5000/turmas',json={'id': 2, 'nome': 'Turma B'})
        r = requests.post('http://localhost:5000/turmas',json={'id': 3, 'nome': 'Turma C'})
        
        #verifica se as turmas foram adicionadas corretamente
        r_lista = requests.get('http://localhost:5000/turmas')
        lista_retornada = r_lista.json()#le o arquivo que o servidor respondeu
                                        #e transforma num dict/lista de python

        #faço um for para garantir que as duas pessoas que eu criei 
        #aparecem
        achei_Turma_B = False
        achei_Turma_C = False
        for turma in lista_retornada:
            if turma['nome'] == 'Turma B':
                achei_Turma_B = True
            if turma['nome'] == 'Turma C':
                achei_Turma_C = True
        
        #se algum desses "achei" nao for True, dou uma falha
        if not achei_Turma_B:
            self.fail('turma B nao apareceu na lista de turmas')
        if not achei_Turma_C:
            self.fail('turma C nao apareceu na lista de turmas')

    def test_017_turmas_por_id(self):
        #cria uma turma 'turma D', com id 20
        r = requests.post('http://localhost:5000/turmas',json={'nome':'Turma D','id':20})

        #consulta a url /turmas/20, pra ver se a turma está lá
        resposta = requests.get('http://localhost:5000/turmas/20')
        dict_retornado = resposta.json() #pego o dicionario retornado
        self.assertEqual(type(dict_retornado), dict)
        self.assertIn('nome', dict_retornado)#o dicionario dict_retornado, que veio do servidor, 
        #tem que ter a chave nome
        self.assertEqual(dict_retornado['nome'], 'Turma D') # no dic, o nome tem que ser o que eu mandei tem que ser Turma D

    def test_018_edita_turmas(self):
        # reseta a lista de turmas
        r_reset = requests.post('http://localhost:5000/reseta_turmas')
        self.assertEqual(r_reset.status_code, 200)

        # cria uma turma com o nome "Turma A" e ID 1
        requests.post('http://localhost:5000/turmas', json={'nome': 'Turma A', 'id': 1})

        # verifica se o nome da turma criada é "Turma A"
        r_antes = requests.get('http://localhost:5000/turmas/1')
        self.assertEqual(r_antes.json()['nome'], 'Turma A')

        # edita o nome da turma para "Turma B"
        requests.put('http://localhost:5000/turmas/1', json={'nome': 'Turma B'})

        # verifica se o nome da turma editada é "Turma B"
        r_depois = requests.get('http://localhost:5000/turmas/1')
        self.assertEqual(r_depois.json()['nome'], 'Turma B')


    def test_019_reseta_turmas(self):
        # cria uma turma usando POST
        r = requests.post('http://localhost:5000/turmas', json={'nome': 'Turma A', 'id': 1})

        # pega a lista turmas
        r_lista = requests.get('http://localhost:5000/turmas')

        # verifica se a lista tem mais de um elemento
        self.assertTrue(len(r_lista.json()) > 0)

        # chama a rota /reseta_turmas para resetar a lista de turmas
        r_reset = requests.post('http://localhost:5000/reseta_turmas')

        # verifica se a rota /reseta_turmas retornou status code 200
        self.assertEqual(r_reset.status_code, 200)

        # pega a lista turmas novamente
        r_lista_depois = requests.get('http://localhost:5000/turmas')

        # verifica se a lista esta vazia apos o reset
        self.assertEqual(len(r_lista_depois.json()), 0)

    def test_020_deleta_turmas(self):
        # reseta a lista de turmas
        r_reset = requests.post('http://localhost:5000/reseta_turmas')
        self.assertEqual(r_reset.status_code, 200)

        # cria duas turmas
        requests.post('http://localhost:5000/turmas', json={'nome': 'Turma A', 'id': 1})
        requests.post('http://localhost:5000/turmas', json={'nome': 'Turma B', 'id': 2})

        # verifica se a lista de turmas tem 2 elementos
        r_lista = requests.get('http://localhost:5000/turmas')
        self.assertEqual(len(r_lista.json()), 2)

        # deleta a turma com ID 2
        requests.delete('http://localhost:5000/turmas/2')

        # verifica se a lista de turmas tem 1 elemento apos a exclusao
        r_lista_depois = requests.get('http://localhost:5000/turmas')
        self.assertEqual(len(r_lista_depois.json()), 1)



                    
def runTests():
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStringMethods)
        unittest.TextTestRunner(verbosity=2,failfast=True).run(suite)


if __name__ == '__main__':
    runTests()