import textdistance
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import os

class Pesquisa:
    
    tipo_graduacao = 0
    tipo_mestrado = 1
    tipo_especialização = 2
    tipo_doutorado = 3
    
    """
Classe de pesquisa tem como função principal realizar a pesquisa da palavra de acordo com a chave de busca.
Tem como os atributos os tipos de graduação que será usado para filtrar a busca
    """
    def __init__(self):
        self.__quant_linhas = 0
        self.__quant_colunas = 0 
        self.__quant_bytes = 0
        self.__nome_arquivo = ''
        self.__ocorrencia = 0
        """
Método Construtor, não recebe argumento para instanciar e onde temos as seguintes propriedades:
self.__quant_linhas : Quantidade de linhas do csv carregado
self.__quant_colunas : Quantidade de colunas do csv carregado
self.__quant_bytes : Quantidade de bytes do csv carregado
self.__nome_arquivo : Nome do arquivo csv carregado
self.__ocorrencia : Quantidade de palavras encontradas durante a pesquisa
        """    
    def get_quant_linhas(self): 
        return self.__quant_linhas
    
    def get_quant_colunas(self):
        return self.__quant_colunas
    
    def get_quant_bytes(self):
        return self.__quant_bytes
    
    def get_nome_arquivo(self):
        return self.__nome_arquivo
    
    def get_ocorrencia(self):
        return self.__ocorrencia

        """
Métodos get para cada propriedade do construtor
        """
    def pesquisar(self, lista, chave, tipo):
        """
Método pesquisar, principal método desta classe que faz tudo funcionar.
Recebe como parametro a lista(list), chave de busca(str) e o tipo(int)( graduação,mestrado,doutorado,especialização)

É feito o processo de Tokenize tanto com a chave quanto na palavra buscada ( ambas em lower case). Esse processo
retira stopwords da língua portuguesa como artigos definidos e indefinidos, conectivos, bem como
carácteres que não sejam alfabéticos: (,/,'',[,] e etc. Portanto o que sobra é apenas uma lista
contendo as palavras chaves por exemplo:

    chave: Engenharia da computação
    palavra_buscada : Licenciatura em Matemática

    self.tokenize_elemento(chave.lower())
    self.tokenize_elemento(palavra_buscada.lower())
    chave = ["Engenharia","computação"]
    palavra_buscada = ["Licenciatura","Matemática"]


Então ele varre a lista buscando no campo de graduação quais palavras sinônimas
baseadas no algoritmo de Levenshtein. Caso, a chave buscada tenha resultados, cada um é alocado
numa lista de busca ( lista_resultado), contendo o nome do professor e sua referente graduação.
        """
        tipo_campo = self._filtrar_campo(tipo)
        print(tipo_campo)
        lista_resultado = []
        elemento_busca = ''
        elemento_chave = self._tokenize_elemento(chave.lower())
        self.__ocorrencia = 0
              
        for i in lista:
            contador = 0
            graduacao = i[tipo_campo]
            nome = i[0]
            elemento_busca = self._tokenize_elemento(graduacao.lower())
            graduacao = self._formatar_campo(i[tipo_campo])
            tamanho = len(elemento_chave)
            
            for k in elemento_chave:
                for j in elemento_busca:
                    if self._levenstein(k, j, 0.3):
                        
                        contador += 1
                        break

            if contador >= tamanho:
                self.__ocorrencia += 1
                lista_resultado.append([nome, graduacao, self.__ocorrencia])

        
        return lista_resultado
     
    
    
    def _levenstein(self, palavra1, palavra2, parametro):
        """
Método de levenstein, algoritmo oficialmente usado na aplicação, recebe como parâmetros
as duas palavras(str) que serão comparadas e o parâmetro de comparação.
No caso do Levenshtein ao realizar o cálculo abaixo, temos um valor entre 0 e 1, onde quanto
mais próximo de 0 maior é a similaridade da palavra, portanto o parâmetro serve para que possamos
comparar o resultado com ele e assim decidir se o sistema de busca será mais ou menos rígido.
Por exemplo, caso o parâmetro seja definido 0.3, qualquer valor que estiver entre 0 e 0.3, será capturado,
qualquer valor acima disso será descartado. Caso ele entre no parâmetro a flag que se inicia com False vai
para True e ela é retornada ao final.
        """
        flag = False
        valor_de = textdistance.damerau_levenshtein(palavra1.lower(), palavra2.lower())
        valor_max = max(len(palavra1), len(palavra2))
        valor_final = valor_de / valor_max
        if valor_final <= parametro:
            flag = True

        return flag
    
    def _sorensen(self, palavra1, palavra2, parametro):
        """
Outro algortimo de Busca que testamos... ( mesma explicação do método acima, sendo que
tanto nesse como no cosseno da similaridade ( método abaixo) quanto mais próximo de 1 mais similar é
a palavra.
        """
        flag = False
        valor_final = textdistance.sorensen(palavra1, palavra2)

        if valor_final >= parametro:
            flag = True
        
        return flag


    def _cossenoSim(self, palavra1, palavra2, parametro):
        flag = False
        valor_final = textdistance.cosine(palavra1.lower(), palavra2.lower())

        if valor_final >= parametro:
            flag = True
        
        return flag
    
    def estatistica(self, nome, lista):
        """
Estatística da aplicação recebe como parâmetro a lista(list) de dados e o nome do arquivo(str) que foi carregado.
Calcula a quantidade de linhas/colunas/bytes do arquivo carregado.        
        """
        self.__quant_linhas = len(lista)
        self.__quant_colunas = len(lista[0])
        self.__quant_bytes = os.stat(f'{nome}.csv').st_size
        self.__nome_arquivo = nome

    def _tokenize_elemento(self, texto):
        """
Recebe como parâmetro o texto(str)

É feito o processo de Tokenize tanto com a chave quanto na palavra buscada ( ambas em lower case). Esse processo
retira stopwords da língua portuguesa como artigos definidos e indefinidos, conectivos, bem como
carácteres que não sejam alfabéticos: (,/,'',[,] e etc. Portanto o que sobra é apenas uma lista
contendo as palavras chaves por exemplo:

    chave: Engenharia da computação
    palavra_buscada : Licenciatura em Matemática

    self.tokenize_elemento(chave.lower())
    self.tokenize_elemento(palavra_buscada.lower())
    chave = ["Engenharia","computação"]
    palavra_buscada = ["Licenciatura","Matemática"]
        """
        texto_elemento = texto
        stop_words = set(stopwords.words('portuguese'))
        word_tokens = word_tokenize(texto_elemento)
        filtered_sentence = [w for w in word_tokens if not w in stop_words and w.isalnum()] 
        return filtered_sentence

    def _formatar_campo(self, texto):
        """
Recebe como parâmetro o texto(str)
Formata o campo de gradução para ser mostrado na tela de forma limpa
        """
        texto = texto.replace('[','')
        texto = texto.replace(']','')
        texto = texto.replace('"','')
        return texto
    
    def _filtrar_campo(self, tipo):
        """
Recebe como parâmetro a list(list) e o tipo(int)
Filtra os campos da lista de acordo com tipo de graduação que o usuário pediu.
        """
        
        if tipo == Pesquisa.tipo_graduacao:
            tipo_campo = 2

        elif tipo == Pesquisa.tipo_mestrado:
            tipo_campo = 6
        
        elif tipo == Pesquisa.tipo_doutorado:
            tipo_campo = 8
        
        elif tipo == Pesquisa.tipo_especialização:
            tipo_campo = 4
        
        return tipo_campo

        

        
            


    


