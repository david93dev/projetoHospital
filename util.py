import mysql


def valida_cadastro(cadastro_valido):
    if bool(cadastro_valido.strip()):
        return cadastro_valido
    while not bool(cadastro_valido.strip()):
        cadastro_valido = input("Campo vazio, tente novamente: ")
    return cadastro_valido





