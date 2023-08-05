"""
Este é o modulo "nester_hmeso.py", e fornece uma função chamada
imprimir_la() que imprimi itens de uma lista que podem ou não
estar aninhdas
"""

def imprimir_la(lista):

    """
    Essa função requer um argumento posicional chamadado lista,
    que é qualquer lista python. Cada item da lista é (recursivamente)
    impresso na tela em sua própria linha.
    """

    for item in lista:
        if isinstance(item, list):
            imprimir_la(item)
        else:
            print(item)
