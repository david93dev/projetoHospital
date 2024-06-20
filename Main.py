from hospitalarbd import *
from util import *

endereco = "localhost"
usuario = "root"
senha = "981276"

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
            Datas VARCHAR(20) NOT NULL,
            FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
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
            Datas VARCHAR(20) NOT NULL,
            FOREIGN KEY (CRM) REFERENCES Medico(CRM),
            FOREIGN KEY (CPF) REFERENCES Paciente(CPF)
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
        cpf_validado = valida_cpf(cpf_valido)

        if cpf_validado:

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
        else:
            print('CPF inválido! Informe o cpf da seguinte forma: 000.000.000-00')

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

    elif menu == 6:

        print('''
                    ╔══════════════════════════════╗
                    ║       Excluir Médico         ║
                    ╚══════════════════════════════╝ 
                    ''')

        cursor = conexao.cursor()
        crm_excluir = input("Digite o CRM do médico que deseja excluir: ")

        query = "SELECT crm FROM medico WHERE crm = %s"
        cursor.execute(query, (crm_excluir,))
        resultado = cursor.fetchone()

        if not resultado:
            print(f"Nenhum médico encontrado com esse CRM: {crm_excluir}.")

        else:
            delete_query = "DELETE FROM medico WHERE crm = %s"
            cursor.execute(delete_query, (crm_excluir,))
            conexao.commit()
            print(f"Médico excluído com sucesso.")

    elif menu == 7:
        menu2 = 0
        while menu2 != 4:
            try:
                menu2 = int(input('''
                    ╔═══════Menu Agendamento═══════╗
                    ║   1. Agendar consulta        ║
                    ║   2. Listar consultas        ║
                    ║   3. Cancelar agendamento    ║
                    ║   4. Voltar                  ║
                    ╚══════════════════════════════╝ 
                        Digite o número da opção: '''))

            except ValueError:
                print('Tente novamente')

            if menu2 == 1:

                cpf = input("CPF do paciente: ")
                cpf_valido = valida_cadastro(cpf)
                cpf_validado = valida_cpf(cpf_valido)

                if cpf_validado:
                
                    consulta = input("O que deseja agendar: ")
                    consulta_valido = valida_cadastro(consulta)

                    data = input("Digite a data do agendamento (DD-MM-YYYY): ")
                    data_valido = valida_cadastro(data)

                    cursor = conexao.cursor()

                    query = "SELECT * FROM paciente WHERE cpf = %s"
                    cursor.execute(query, (cpf_valido,))
                    resultado = cursor.fetchone()

                    

                    if resultado:
                        nome = resultado[1]

                        sql_inserir_agendamento = "INSERT INTO agendarconsulta (cpf, nomepaciente, consulta, datas) VALUES (%s, %s, %s, %s)"
                        dados_insert = (cpf_valido, nome, consulta_valido, data_valido)
                        insertNaTabela(conexao, sql_inserir_agendamento, dados_insert)
                        print("Consulta agendada com sucesso!")

                    else:
                        print(f"Nenhum paciente encontrado com CPF: {cpf_valido}.")
                        print("Volte ao menu principal e realize seu cadastro!")

                else:
                    print('CPF inválido! Informe o cpf da seguinte forma: 000.000.000-00')


            elif menu2 == 2:

                cursor = conexao.cursor()

                query = "SELECT * FROM agendarconsulta"
                cursor.execute(query)
                resultado = cursor.fetchall()

                if not resultado:
                    print("Nenhuma consulta encontrada.")

                else:
                    print('\nCONSULTAS AGENDADAS:\n\n')
                    for row in resultado:
                        print(
                            f"ID: {row[0]} \nCPF: {row[1]} \nNome: {row[2]} \nConsulta: {row[3]} \nData: {row[4]}")
                        print(
                            "--------------------------------------------------------------------------------")

            elif menu2 == 3:

                cursor = conexao.cursor()

                query = "SELECT * FROM agendarconsulta"
                cursor.execute(query)
                resultado = cursor.fetchall()

                if not resultado:
                    print("Nenhuma consulta encontrada.")

                else:
                    for row in resultado:
                        print(
                            f"ID: {row[0]} \nCPF: {row[1]} \nNome: {row[2]} \nConsulta: {row[3]} \nData: {row[4]}")
                        print(
                            "--------------------------------------------------------------------------------")

                    cursor = conexao.cursor()
                    id_excluir = input("Digite o Código ou ID da consulta agendada que deseja excluir: ")

                    query = "SELECT id FROM agendarconsulta WHERE id = %s"
                    cursor.execute(query, (id_excluir,))
                    resultado = cursor.fetchone()

                    if not resultado:
                        print(f"Nenhum agendamento encontrado com essa ID: {id_excluir}.")

                    else:
                        delete_query = "DELETE FROM agendarconsulta WHERE id = %s"
                        cursor.execute(delete_query, (id_excluir,))
                        conexao.commit()
                        print(f"Agendamento excluído com sucesso.")

            elif menu2 != 4:
                print("Opção invalida!.")

    elif menu == 8:
        menu3 = 0
        while menu3 != 3:
            try:
                menu3 = int(input('''
                    ╔═══════Menu Procedimentos Médico══════╗
                    ║   1. Adicionar Procedimento Médico   ║
                    ║   2. Pesquisar Procedimento Médico   ║
                    ║   3. Voltar                          ║
                    ╚══════════════════════════════════════╝ 
                        Digite o número da opção: '''))

            except ValueError:
                print('Tente novamente!')

            if menu3 == 1:

                crm = input("Digite seu CRM: ")
                crm_valido = valida_cadastro(crm)

                cpf = input("CPF do paciente: ")
                cpf_valido = valida_cadastro(cpf)
                cpf_validado = valida_cpf(cpf_valido)

                if cpf_validado:

                    procedimento = input("Registre o procedimento médico realizado: ")
                    procedimento_valido = valida_cadastro(procedimento)

                    data = input("Digite a data desse procedimento (DD-MM-YYYY): ")
                    data_valido = valida_cadastro(data)

                    cursor = conexao.cursor()

                    query = "SELECT * FROM medico WHERE crm = %s"
                    cursor.execute(query, (crm_valido,))
                    resultado_medico = cursor.fetchone()


                    query = "SELECT * FROM paciente WHERE cpf = %s"
                    cursor.execute(query, (cpf_valido,))
                    resultado_paciente = cursor.fetchone()


                    if resultado_medico and resultado_paciente:
                        nome_medico = resultado_medico[1]
                        nome_paciente = resultado_paciente[1]

                        sql_inserir_procedimentos = "INSERT INTO procedimentos (crm, nomemedico, cpf, nomepaciente, procedimento, datas) VALUES (%s, %s, %s, %s, %s, %s)"
                        dados_insert = (crm_valido, nome_medico, cpf_valido, nome_paciente, procedimento_valido, data_valido)
                        insertNaTabela(conexao, sql_inserir_procedimentos, dados_insert)
                        print("Cadastrado realizado com sucesso!")

                    else:
                        print(f"Paciente ou médico não cadastrados")
                        print("Volte ao menu principal e realize os cadastros!")

                else:
                    print('CPF inválido! Informe o cpf da seguinte forma: 000.000.000-00')

            elif menu3 == 2:
                cursor = conexao.cursor()

                query = "SELECT * FROM procedimentos"
                cursor.execute(query)
                resultado = cursor.fetchall()

                if not resultado:
                    print("Nenhuma consulta encontrada.")

                else:
                    print('\nPROCEDIMENTOS REALIZADOS:\n\n')
                    for row in resultado:
                        print(
                            f"ID: {row[0]} \nCRM: {row[1]} \nNome do médico: {row[2]} \nCPF: {row[3]} \nNome do paciente: {row[4]} \nProcediemnto: {row[5]} \nData: {row[6]}")
                        print(
                            "--------------------------------------------------------------------------------")
            elif menu3 != 3:
                print("Opção invalida!.")

    elif menu == 9:
        print("Saindo do sistema...")
        print("Obrigado!")

    else:
        print('Opção invalida!')


encerrarBancoDados(conexao)
