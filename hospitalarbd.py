import mysql.connector

# Função para iniciar conexão com o mysql
def criarConexaoInicial(endereco, usuario, senha):
    return mysql.connector.connect(
        host=endereco,
        user=usuario,
        password=senha
    )

# Função para finalizar conexão com o mysql
def encerrarBancoDados(connection):
    connection.close()

def criarBancoDados(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()


def criarTabela(connection, nome_banco_dados, sql):
    cursor = connection.cursor()
    cursor.execute(f"USE {nome_banco_dados}")
    cursor.execute(sql)
    cursor.close()
    print(f"Tabela criada ou já existente.")


def listarTabelas(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    tabelas = cursor.fetchall()
    cursor.close()
    return tabelas

# Função para inserir dados na tabela
def insertNaTabela(connection, sql, dados):
    cursor = connection.cursor()
    cursor.execute(sql, dados)
    connection.commit()
    cursor.close()

# Função para listar dados da tabela
def listarBancoDados(connection, sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return results

# Função para atualizar dados na tabela
def atualizarBancoDados(connection, sql, dados):
    cursor = connection.cursor()
    cursor.execute(sql, dados)
    connection.commit()
    cursor.close()

# Função para excluir dados da tabela
def excluirDadosTabela(connection, sql, dados):
    cursor = connection.cursor()
    cursor.execute(sql, dados)
    connection.commit()
    cursor.close()

# Função para excluir um banco de dados
def excluirBancoDados(connection, nome_banco):
    cursor = connection.cursor()
    cursor.execute(f"DROP DATABASE {nome_banco}")
    connection.commit()
    cursor.close()

# Função para excluir uma tabela
def excluirTabela(connection, nome_tabela):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE {nome_tabela}")
    connection.commit()
    cursor.close()
