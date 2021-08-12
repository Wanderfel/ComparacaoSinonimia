from etl import *
from pesquisa import *
"""
Importando as classes
"""
pesquisa = Pesquisa()
etl = Etl()
"""
Instanciando Objetos
"""

verificar_carregado = False
lista_colunas = [1,3,5,7,9]
"""
Declarando variável de controle "verificar_carregado" que será usado para verificar se o usuário
digitou um caminho válido. Caso sim, a seguinte flag é mudada para True e ele pode acessar outras áreas
do menu como Busca e Estatística da Base.

Declarando variável "lista_Colunas" onde vai conter as colunas onde estão os valores "Sim" e "Não", para que sejam
trocadas por valores booleanos ( True e False)
"""

while (True):

    print(''' 
    (c) Carregar Dados
    (e) Estatística da Base
    (i) Busca
    (s) Sobre
    (q) Sair
    ''')
    opcao = input('Opção:').lower()

    if opcao == 'c':
        nome = input('Digite o nome do arquivo que deseja carregar(.csv):')
        try:
            etl.load(f'{nome}')
            pesquisa.estatistica(nome, etl.lista)
            verificar_carregado = True
            print('Arquivo carregado com Sucesso !')
        except EtlException as tl:
            print(tl)
        
        etl.transforma_bool(etl.lista,lista_colunas)
        
        
    
    elif opcao == 's':
        print('sobre')
        print('''
FRAMEWORK DE DETECÇÃO DE SINONIMIA

Integrantes:
Ismael Jônatas dos Santos Silva
Marcos Antonio Grisi Filho
--------------------------------
Metodologia de trabalho:
Durante todo o trabalho usamos a metodologia de programação em pares,que
consiste em programar juntos e reversar, ora um codificava e o outro observava
apontando algum erro ou bug e vice versa. Portanto, cada um contribuiu igualmente
com o  trabalho.

Escolhas,algoritmos e etc:
Na fase de ETL, observamos os dados e tiramos as colunas da base que achamos inconveniente
para a aplicação, como por exemplo a coluna referente a data de atualização e a de ID.

Depois disso decidimos que ao carregar os dados em alguma estrutura ( coleção), mudar os valores
de sim e não dentro da tabela para True e False, pois julgamos que ficaria mais leve e com menos strings.

Optamos usar uma simples lista para carregar os dados. Em uma única varrida, ele encontra os valores que
correspondam a sinonimia da chave e então retorna na tela.

Durante o processo testamos diversos algoritmos de comparação : Levenshtein, Cosseno da similaridade,
Sorensen. Usando cada um separadamente ou mesclando-os de diversas formas. Depois disso optamos por usar apenas
o Levenshtein. Por conseguinte, depois de muitos testes percebemos que dependendo do parâmetro colocado, ou capturávamos
bastante lixo ( palavras não tão sinônimas assim) ao mesmo tempo que aparecia palavras bem parecidas. Ao diminuir demais,
o sistema de busca ficava mais rígido dando valores bem parecidos porem se perdia um pouco da sinonimia então por exemplo,
ao usar "Biologia" como chave de busca, não se via palavras como " Biológicas". Então tentamos calibrar e encontrar um meio
termo. No nosso caso, foi colocar como parâmetro 0.3. Dessa forma teríamos resultados errados como por exemplo,
"Biologia" = "Geologia", porém com poucas ocorrências erradas desse tipo ao mesmo tempo que iria capturar palavras iguais
ou sinônimas.

Nossa aplicação depende de dois módulos: TextDistance e o nltk. Como sabemos que isso iria causar uma dependência,
criamos um arquivo chamado requiriments.txt onde ao usar o comando pip install -r requirements.txt os módulos são
baixados sem problema. Isso é uma padronização para usuários que costumam usar módulos do python. As instruções
de como utilizar esse comando está no arquivo README.txt.

''')
        input('Enter para continuar...')
        
    elif opcao == 'q':
        print('sair')
        break
    
    elif (verificar_carregado) and (opcao == 'i' or opcao == 'e'):
        if opcao == 'i':
            while True:
                print('''
Tipos:
(0) Graduação
(1) Mestrado
(2) Especialização
(3) Doutorado
''')

                tipo = int(input('Por qual campo deseja pesquisar ?'))
                chave = input('Chave de busca (Enter para retornar ao menu):')
                if chave == '':
                    break
                resultado = pesquisa.pesquisar(etl.lista, chave, tipo)
                for i in range(len(resultado)):
                    nome = resultado[i][0]
                    graduacao = resultado[i][1]
                    ocorrencia = resultado[i][2]

                    print(
f'''
{ocorrencia}
Nome: {nome}
Área de formação: {graduacao}''')

                print(
f'''{pesquisa.get_ocorrencia()}''')
                input('\nEnter para continuar...')
                

        elif opcao == 'e':
            print(f''' 
Informações sobre a base:
Nome do arquivo: {pesquisa.get_nome_arquivo()}
Quantidade de Linhas: {pesquisa.get_quant_linhas()}
Quantidade de Colunas: {pesquisa.get_quant_colunas()}
Quantidade de Bytes: {pesquisa.get_quant_bytes()}

            ''')
            input('Enter para continuar...')
                  
    
    else:
        print('É necessário carregar a base')
       
    
