import os

class CONTEUDOS:

    def __init__(self, num):
        self.num = num

    def get_conteudo(self):
        return self.num

    def set_conteudo(self, novo_num):
        self.x = novo_num

def ler():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(script_dir, "PEU1.txt")
    
    conteudo = 0
    with open(file_path, "r") as arquivo:   
            arquivo.seek(0)
            conteudo = arquivo.read()
    elementos = []
    linhas = conteudo.split('\n')
    for linha in linhas:
        if linha.strip():
            itens = linha.split('\t')
            for item in itens:
                if item.strip():
                    elementos.append(item.strip())

    elementos = list(map(int, elementos))    

    tamanho_tubo = elementos.pop(0)
    quantidade_de_conteudo = elementos.pop(0)
    conteudo_lido2 = elementos.copy()
    
    vetor_de_recipientes = []
    
    for i in range(quantidade_de_conteudo):
        novo_conteudo = CONTEUDOS(elementos[0])
        recipiente = []
        recipiente.append(novo_conteudo)
        vetor_de_recipientes.append(recipiente)
        elementos.remove(elementos[0])
    

    return vetor_de_recipientes, tamanho_tubo, conteudo_lido2

def gerar_vizinho(vetor):
    vizinho = []
    for i in vetor:
        vizinho.append(i.copy())
    return vizinho

def verificar_tubo(tubo_verificar):
    i = 0
    for conteudo in tubo_verificar:
        i += conteudo.get_conteudo()
    return i

def achar_diferenca(vetoratual, novo):
    diferenca = 0
    for i in range(len(vetoratual)):
        if len(vetoratual[i]) > len(novo[i]): #saiu um conteudo
            for conteudo in vetoratual[i]:
                if conteudo not in novo[i]:
                    diferenca = conteudo
                    return diferenca
        elif len(vetoratual[i]) < len(novo[i]): #entrou um conteudo
            for conteudo in novo[i]:
                if conteudo not in vetoratual[i]:
                    diferenca = conteudo
                    return diferenca

def gerar_vizinhos(vetor_de_recipientes, lista_tabu):
    vizinhos = []

    for index_tubo, tubo in enumerate(vetor_de_recipientes):
        for conteudo in tubo:
            if conteudo in lista_tabu:
                continue
            tubo.remove(conteudo)

            for index_vizinho, vizinho in enumerate(vetor_de_recipientes):
                if index_vizinho == index_tubo and index_tubo != len(vetor_de_recipientes) - 1:
                    continue
                vizinho = gerar_vizinho(vetor_de_recipientes)
                vizinho[index_vizinho].append(conteudo)
                if verificar_tubo(vizinho[index_vizinho]) > tamanho_tubo:
                    continue
                vizinhos.append(vizinho)
            tubo.append(conteudo)

    return vizinhos

def verificar_custo(vetor_de_tubos):
    i = 0
    for tubos in vetor_de_tubos:
        if len(tubos) > 0:
            i += 1
    return i

def menor_custo(vetor):
    menor_elemento = vetor[0]
    for i in range(len(vetor)):
        if verificar_custo(menor_elemento) > verificar_custo(vetor[i]):
            menor_elemento = vetor[i]

    #i = vetor.index(menor_elemento)
    return menor_elemento

def remover_vazios(vetor_remover):
    lista = []
    for tubos in vetor_remover:
        if len(tubos) == 0:
            lista.append(tubos)
    for tubo in lista:
        vetor_remover.remove(tubo)
    return vetor_remover

def busca_tabu(itens):
    melhor_solucao = itens
    solucao_atual = itens
    lista_tabu = []
    for i in range(tamanho_lista_tabu):
        lista_tabu.append(0)
    
    for k in range(1000):
        vetor_de_vizinhos = gerar_vizinhos(solucao_atual, lista_tabu)
        
        melhor_vizinho = menor_custo(vetor_de_vizinhos)
        lista_tabu.append(achar_diferenca(solucao_atual, melhor_vizinho))
        lista_tabu.remove(lista_tabu[0])
        #print(k)
        
        if verificar_custo(melhor_vizinho) < verificar_custo(melhor_solucao):
            melhor_solucao = melhor_vizinho
        
        solucao_atual = melhor_vizinho


    melhor_solucao = remover_vazios(melhor_solucao)        
    return melhor_solucao

vetor_de_recipientes, tamanho_tubo, conteudo_lido = ler()
tamanho_lista_tabu = int(len(conteudo_lido) / 2)
melhor_solucao = busca_tabu(vetor_de_recipientes)

print("\n\nConteudos: ", end=' ')
for i in range(len(conteudo_lido)):
    print(conteudo_lido[i], end=' ')

print(f"\nTamanho do Tubo: {tamanho_tubo}")

print("Melhor solução encontrada: ")
for i in range(len(melhor_solucao)):
    print(f" Tubo {i+1}: [", end=' ')
    for conteudo in melhor_solucao[i]:
        print(conteudo.get_conteudo(), end=' ')
    print("]")

print(f"Tubos utilizados: {len(melhor_solucao)}")