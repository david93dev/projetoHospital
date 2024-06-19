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

    elif opcao == 2:

        crm = int(input('\nDigite o crm do Médico: '))
        sql_valida_medico = f"SELECT crm FROM medico WHERE crm = {crm}"
        medicoExistente = banco_dados1.listarUmValorBancoDados(conexao,sql_valida_medico)

        if medicoExistente:
            print('\nJá existe um Médico com esse CRM no sistema.')

        else:
            nome = input('Digite o nome do Médico: ')
            especialidade = input('Digite a especialidade do Médico: ')
            telefone = input('Digite o telefone do Médico: ')
            insert_medico = (crm,nome,especialidade,telefone)

            sql_inserir_medico = "INSERT INTO medico (crm, nome, especialidade,telefone) VALUES (%s, %s, %s, %s)"
            banco_dados1.insertNaTabela(conexao, sql_inserir_medico, insert_medico)
            print('\nMédico adicionado com sucesso!')

