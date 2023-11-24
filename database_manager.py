# database_manager.py
import sqlite3
from datetime import datetime

idMunicipe = None
nomeMunicipe = ''
data_hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

def create_database():
    try:
        connection = sqlite3.connect("appprotoon.db")
        connection.close()
    except sqlite3.Error as e:
        print(f"Erro ao criar o banco de dados: {e}")

def create_table():
    create_database()
    connection = sqlite3.connect("appprotoon.db")
    cursor = connection.cursor()

    # Criação da tabela reclamacoes se não existir
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reclamacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idMunicipe INTEGER,
                protocolo TEXT,
                nomeMunicipe TEXT,
                problema TEXT,
                bairro TEXT,
                rua TEXT,
                descricao TEXT,
                status TEXT,
                data_hora TEXT
            );
        """)
        
        # Criação da tabela municipes se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS municipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,                
                nome TEXT,
                email TEXT,
                senha TEXT,
                data_hora TEXT
            );
        """)
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
        
    connection.commit()
    connection.close()
    
def validar_login(email, senha):
    try:
        conn = sqlite3.connect('appprotoon.db')
        cursor = conn.cursor()

        # Use placeholders (?) para evitar SQL injection
        cursor.execute('SELECT * FROM municipes WHERE email = ? AND senha = ?', (email, senha))
        
        # Obtém o resultado da consulta
        resultado = cursor.fetchall()

        conn.close()

        # Verifica se há algum registro retornado pela consulta
        if resultado:
            nomeMunicipe = resultado[0][1]
            idMunicipe = resultado[0][0]            
            # Retorna o idMunicipe
            return idMunicipe, nomeMunicipe
        else:
            # Retorna None se não houver correspondência
            return None
    except sqlite3.Error as e:
        print(f"Erro ao validar login no banco de dados: {e}")
        return None    

def save_municipe(nome, email, senha, validate):
    
    if validate:    
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Senha: {senha}")
        print(f"Data e hora: {data_hora_atual}")
        
        try:
            # Criação do banco de dados e da tabela se não existirem
            create_database()
            create_table()
        
            # Estabeleça a conexão com o banco de dados (ou crie o banco se não existir)
            conn = sqlite3.connect('appprotoon.db')

            # Crie um cursor para executar operações no banco de dados
            cursor = conn.cursor()
            
            
            
            cursor.execute("INSERT INTO municipes (nome, email, senha, data_hora) VALUES (?, ?, ?, ?)",
                        (nome, email, senha, data_hora_atual))
            
            # Commit para salvar as alterações no banco de dados
            conn.commit()

            # Feche a conexão
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            
def save_reclamacao(idMunicipe, nomeMunicipe, problema, bairro, rua, descricao, validate):
    
    if validate:
        
        try:
            create_database()
            create_table()
        
            conn = sqlite3.connect('appprotoon.db')

            cursor = conn.cursor()
            
            # Obtém o último ID
            cursor.execute('SELECT MAX(id) FROM reclamacoes')
            ultimo_id = cursor.fetchone()[0]

            # Verifica se há algum ID na tabela
            if ultimo_id is not None:
                # Calcula o próximo ID
                novo_id = ultimo_id + 1
            else:
                # Se não houver nenhum ID na tabela, comece do primeiro ID (por exemplo, 1)
                novo_id = 1

            # Obtém o ano atual
            ano_atual = datetime.now().year

            # Gera o protocolo
            protocolo = f'{19000 + novo_id}/{ano_atual}'
            
            cursor.execute("INSERT INTO reclamacoes (idMunicipe, protocolo, nomeMunicipe, problema, bairro, rua, descricao, status, data_hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (idMunicipe, protocolo, nomeMunicipe, problema, bairro, rua, descricao, 'Em Análise', data_hora_atual))
            
            conn.commit()

            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao salvar no banco de dados: {e}")
            
def get_reclamacoes(idMunicipe):
    try:

        conn = sqlite3.connect('appprotoon.db')
        cursor = conn.cursor()

        # Verifica se há reclamações para o idMunicipe
        cursor.execute("SELECT * FROM reclamacoes WHERE idMunicipe = ?", (idMunicipe,))
        reclamacoes = cursor.fetchall()

        conn.close()

        return reclamacoes
    except sqlite3.Error as e:
        print(f"Erro ao obter reclamações do banco de dados: {e}")
        return []
