import sqlite3

# Conectar ou criar o banco de dados
conexao = sqlite3.connect("meubanco.db")  # Isso cria o banco se não existir

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

# Criar a tabela Serviços
cursor.execute('''
CREATE TABLE IF NOT EXISTS Serviços (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serviço TEXT NOT NULL,
    preço_serviço REAL NOT NULL
)
''')

# Salvar (commit) as alterações
conexao.commit()

# Fechar a conexão
conexao.close()

print("Tabela Serviços criada com sucesso!")
