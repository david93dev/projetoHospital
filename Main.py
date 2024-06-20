from projetoHospital.hospitalarbd import *
from util import *

endereco = "localhost"
usuario = "root"
senha = "David#2010"

conexao = criarConexaoInicial(endereco, usuario, senha)

sql_criar_bd = "CREATE DATABASE IF NOT EXISTS hospital"
criarBancoDados(conexao, sql_criar_bd)

sql_criar_tabela_paciente = """
        CREATE TABLE IF NOT EXISTS Paciente(
            CPF VARCHAR(15) NOT NULL PRIMARY KEY,
            Nome VARCHAR(50) NOT NULL,
            Idade INT NOT NULL,
            Endereco VARCHAR(150) NOT NULL,
            Telefone VARCHAR(50) NOT NULL
        );
    """
sql_criar_tabela_medico = """
        CREATE TABLE IF NOT EXISTS Medico(
            CRM VARCHAR(15) NOT NULL PRIMARY KEY,
            Nome VARCHAR(50) NOT NULL,
            Especialidade VARCHAR(50) NOT NULL,
            Telefone VARCHAR(50) NOT NULL
        );
    """

sql_criar_tabela_agendar_consulta = """
        CREATE TABLE IF NOT EXISTS agendarConsulta(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            CPF VARCHAR(15) NOT NULL,
            NomePaciente VARCHAR(50) NOT NULL,
            Consulta VARCHAR(100) NOT NULL,
            Datas VARCHAR(20) NOT NULL
        );
    """

sql_criar_tabela_agendar_procedimento_medico = """
        CREATE TABLE IF NOT EXISTS procedimentos(
            ID INT AUTO_INCREMENT PRIMARY KEY,
            CRM VARCHAR(15) NOT NULL,
            NomeMedico VARCHAR(50) NOT NULL,
            CPF VARCHAR(15) NOT NULL,
            NomePaciente VARCHAR(50) NOT NULL,
            Procedimento VARCHAR(100) NOT NULL,
            Datas VARCHAR(20) NOT NULL
        );
    """

criarTabela(conexao, "hospital", sql_criar_tabela_paciente)
criarTabela(conexao, "hospital", sql_criar_tabela_medico)
criarTabela(conexao, "hospital", sql_criar_tabela_agendar_consulta)
criarTabela(conexao, "hospital", sql_criar_tabela_agendar_procedimento_medico)

menu = 0
while menu != 9:
    try:
        menu = int(input('''
                    ╔═════════════════MENU════════════════╗
                    ║   1. Adicionar Novo Paciente        ║
                    ║   2. Adicionar Novo Médico          ║
                    ║   3. Pesquisar Paciente por CPF     ║
                    ║   4. Pesquisar Médico por CRM       ║ 
                    ║   5. Excluir Paciente pelo CPF      ║
                    ║   6. Excluir Médico pelo CRM        ║
                    ║   7. Agendar Consulta               ║
                    ║   8. Registrar Procedimento Médico  ║
                    ║   9. Sair do Sistema                ║                
                    ╚═════════════════════════════════════╝    
                        Digite o número da opção: '''))

    except ValueError:
        print('Tente novamente')

    if menu == 1:

        print('''
                    ╔══════════════════════════════╗
                    ║      Cadastro Paciente       ║
                    ╚══════════════════════════════╝ 
                    ''')

        cpf = input("CPF do paciente: ")
        cpf_valido = valida_cadastro(cpf)

        nome = input("Nome do paciente: ")
        nome_valido = valida_cadastro(nome)

        idade = input("Idade do paciente: ")
        idade_valido = valida_cadastro(idade)

        endereco = input("Endereço do paciente: ")
        endereco_valido = valida_cadastro(endereco)

        telefone = input("Telefone do paciente: ")
        telefone_valido = valida_cadastro(telefone)

        cursor = conexao.cursor()

        query = "SELECT * FROM paciente WHERE cpf = %s"
        cursor.execute(query, (cpf_valido,))
        resultado = cursor.fetchone()

        if resultado:
            print('Operação falhou: CPF já cadastrado!')

        else:
            sql_inserir_paciente = "INSERT INTO Paciente (cpf, nome, idade, endereco, telefone) VALUES (%s, %s, %s, %s, %s)"
            dados_insert = (cpf_valido, nome_valido, idade_valido, endereco_valido, telefone_valido)
            insertNaTabela(conexao, sql_inserir_paciente, dados_insert)
            print('Paciente cadastrado com sucesso!')

    elif menu == 2:

        print('''
                    ╔══════════════════════════════╗
                    ║       Cadastro Médico        ║
                    ╚══════════════════════════════╝ 
                            ''')

        crm = input("CRM do médico: ")
        crm_valido = valida_cadastro(crm)

        nome = input("Nome do médico: ")
        nome_valido = valida_cadastro(nome)

        especialidade = input("Especialidade do médico: ")
        especialidade_valida = valida_cadastro(especialidade)

        telefone = input("Telefone do médico: ")
        telefone_valido = valida_cadastro(telefone)

        cursor = conexao.cursor()

        query = "SELECT * FROM medico WHERE crm = %s"
        cursor.execute(query, (crm_valido,))
        resultado = cursor.fetchone()

        if resultado:
            print('Operação falhou: CRM já cadastrado!')

        else:
            sql_inserir_medico = "INSERT INTO Medico (crm, nome, especialidade, telefone) VALUES (%s, %s, %s, %s)"
            dados_insert = (crm_valido, nome_valido, especialidade_valida, telefone_valido)
            insertNaTabela(conexao, sql_inserir_medico, dados_insert)
            print('Médico cadastrado com sucesso!')

    elif menu == 3:

        print('''
                    ╔══════════════════════════════╗
                    ║      Pesquisa Paciente       ║
                    ╚══════════════════════════════╝ 
                    ''')

        cursor = conexao.cursor()
        cpf_pesquisado = input("Digite o CPF do paciente que deseja pesquisar: ")

        query = "SELECT * FROM paciente WHERE cpf = %s"
        cursor.execute(query, (cpf_pesquisado,))
        resultado = cursor.fetchone()

        if resultado:
            print(
                f'CPF: {resultado[0]}\nNome: {resultado[1]}\nIdade: {resultado[2]}\nEndereço: {resultado[3]}\nTelefone: {resultado[4]}')
        else:
            print(f'Nenhum paciente encontrado com esse CPF: {cpf_pesquisado}.')


    elif menu == 4:

        print('''
                    ╔══════════════════════════════╗
                    ║       Pesquisa Médico        ║
                    ╚══════════════════════════════╝ 
                    ''')

    cursor = conexao.cursor()
    crm_pesquisado = input("Digite o crm do médico que deseja pesquisar: ")

    query = "SELECT * FROM medico WHERE crm = %s"
    cursor.execute(query, (crm_pesquisado,))
    resultado = cursor.fetchone()

    if resultado:
        print(
            f'CRM: {resultado[0]}\nNome: {resultado[1]}\nEspecialidade: {resultado[2]}\nTelefone: {resultado[3]}')
    else:
        print("Nenhum médico encontrado com esse CRM.")

    elif menu == 5:

        print('''
                    ╔══════════════════════════════╗
                    ║       Excluir Paciente       ║
                    ╚══════════════════════════════╝ 
                            ''')
    cursor = conexao.cursor()
    cpf_excluir = input("Digite o CPF do paciente que deseja excluir: ")

    query = "SELECT cpf FROM paciente WHERE cpf = %s"
    cursor.execute(query, (cpf_excluir,))
    resultado = cursor.fetchone()

    if not resultado:
        print(f"Nenhum paciente encontrado com CPF: {cpf_excluir}.")

    else:
        delete_query = "DELETE FROM paciente WHERE cpf = %s"
        cursor.execute(delete_query, (cpf_excluir,))
        conexao.commit()
        print(f"Paciente excluído com sucesso.")
