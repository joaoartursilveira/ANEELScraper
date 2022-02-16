import sqlite3
import pandas as pd
import os

class SQLite():
    def __init__(self, path: str, db_name: str):
        self.os_path = os.path.join(path, db_name)

    def select_processos(self):
        conn = sqlite3.connect(self.os_path)
        conn.execute("PRAGMA foreign_keys = 1")
        df = pd.read_sql_query("SELECT * FROM processos_tarifarios", conn, index_col='id')
        conn.close()
        return df

    def info_agente(self, agente: str):
        """Seleciona o nome padrão definido para às distribuidoras na tabela info_concessionarias."""
        conn = sqlite3.connect(self.os_path)
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        with conn:
            query = """select distribuidora from info_concessionarias 
            where distribuidora = (?) or nome1 = (?) or nome2 = (?)"""
            holder = (agente, agente, agente)
            sigla = cursor.execute(query, holder).fetchone()[0]
        conn.close()
        return sigla

    def inserir_sqlite(self, df_novos):
        try:
            conn = sqlite3.connect(self.os_path)
            conn.execute("PRAGMA foreign_keys = 1")
            df_novos.to_sql('processos_tarifarios', conn, if_exists='append', index=False)
            conn.close()
            print('dados acima foram inseridos')

        except sqlite3.Error as error:
            print('Conexao falhou', error)

    
if __name__ == '__main__':
    df_banco = SQLite()
    print(df_banco.info_agente('RORAIMAENERGIASA'))