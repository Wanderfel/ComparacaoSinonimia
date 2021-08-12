import csv


class EtlException(Exception):
    """
Classe que herda as exceções do Python usada para tratamento de erros da classe Etl 
    """
    def __init__(self, mensagem, metodo=''):
        super().__init__(mensagem)
        self.metodo = metodo


class Etl:


    def __init__(self):
        self.lista = []
    """
Construtor não recebe parâmetro e tem como único atributo público uma lista vazia
    """
    
    def load(self, nome_arquivo, lista_colunas=[]):
        """
Método load, usado para carregar os arquivos e coloca-los em um list.
Recebe como parâmetro o nome do arquivo csv(str) a ser carregado e opcionalmente
a lista das colunas(list) que o usuário deseja deletar.
        """
        lista = []
        try:
            arq = open(f'{nome_arquivo}.csv', 'r', encoding='utf8')
        except FileNotFoundError:
            raise EtlException(f'{nome_arquivo} não existe')    
        linhas = csv.reader(arq)      
        for linha in linhas:
            if len(lista_colunas) != 0:
                for coluna in lista_colunas:            
                    del linha[coluna]
            lista.append(linha)
        arq.close()
        lista = [x for x in lista if x != []]
        self.lista = lista

    def save(self, nome_arquivo):
        """
Método Save salva os arquivos persistindo-os em disco como csv a partir da lista que foi carregado no load.
Recebe como argumento o nome do arquivo de saida(str).
        """
        arq = open(f'{nome_arquivo}', 'w', encoding='utf8')
        novo = csv.writer(arq)
        novo.writerows(self.lista)
        arq.close()
    
    def transforma_bool(self, lista, lista_colunas):
        """
Método para transformar valores binários como "Sim" e "Não", em True e False respectivamente
Recebe como argumento a lista em questão(list) e uma lista(list) contendo as colunas onde esses valores existem.
        """
        for i in range(len(lista)):
            if i != 0:
                for j in lista_colunas:
                    if lista[i][j] == 'SIM':
                        lista[i][j] = True
                    else:
                        lista[i][j] = False
