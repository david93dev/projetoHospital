import mysql


def valida_cadastro(cadastro_valido):
    if bool(cadastro_valido.strip()):
        return cadastro_valido
    while not bool(cadastro_valido.strip()):
        cadastro_valido = input("Campo vazio, tente novamente: ")
    return cadastro_valido

def valida_cpf(cpf):
    # Removendo caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verificando se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verificando se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calculando o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0

    # Verificando o primeiro dígito verificador
    if digito1 != int(cpf[9]):
        return False

    # Calculando o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0

    # Verificando o segundo dígito verificador
    if digito2 != int(cpf[10]):
        return False

    # Se passou por todas as verificações, o CPF é válido
    return True





