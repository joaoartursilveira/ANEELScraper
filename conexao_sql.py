import sqlite3
import pandas as pd
import os

class SQLite():
    def __init__(self):
        path_db = r'D:\python_projects\cpfl\db_sqlite'
        db_name = 'central_dist_new.db'
        self.os_path = os.path.join(path_db, db_name)

    def select_processos(self):
        """Seleciona todos os processos do banco de dados"""
        conn = sqlite3.connect(self.os_path)
        conn.execute("PRAGMA foreign_keys = 1")
        query = """select distribuidora, data_processo, processo, arquivo, link from processo_tarifario pt 
        inner join processo_arquivamento pa on pt.chave_processo=pa.chave_processo"""
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def info_agente(self, agente: str):
        """Seleciona o nome padrão aneel das distribuidoras na tabela distribuidora"""
        conn = sqlite3.connect(self.os_path)
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        with conn:
            query = """select nome_aneel from distribuidora 
            where nome_aneel = (?) or nome1 = (?) or nome2 = (?)"""
            holder = (agente, agente, agente)
            sigla = cursor.execute(query, holder).fetchone()[0]
        conn.close()
        return sigla

    def inserir_sqlite(self, df_novos, tabela):
        """Insere os novos processos encontrados na varredura"""
        try:
            conn = sqlite3.connect(self.os_path)
            conn.execute("PRAGMA foreign_keys = 1")
            df_novos.to_sql(tabela, conn, if_exists='append', index=False)
            conn.close()
            print(f'Dados inseridos com sucesso na tabela: {tabela}')

        except sqlite3.Error as error:
            print(f'Conexao falhou, erro reportado "{error}"')
            conn.close()

    
if __name__ == '__main__':
    df = SQLite().select_processos()
    print(df)