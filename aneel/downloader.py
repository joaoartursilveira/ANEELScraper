from conexao_sql import SQLite
from pathlib import Path
import os
import requests
import pandas as pd

def download(df):
    """Função de download do dataframe de entrada"""
    for arquivo, nome_padrao, link in df[['arquivo','nome_padrao','link']].to_numpy():
        path_arquivo = os.path.join(arquivo.lower(), nome_padrao)
        with open(path_arquivo, 'wb') as f:
            f.write(requests.get(link).content)
            f.flush()
            f.close()
        print(f'Arquivo: "{nome_padrao}" foi baixado com sucesso')
    print('Todos os arquivos foram baixados com sucesso')


def ler_pasta(path):
    """Cria o diretório destino dos arquivos, caso não exista
    Lê o conteundo da pasta dos arquivos e retorna um dataframe"""
    Path(path).mkdir(parents=True, exist_ok=True)
    dict_arquivos = {'nome_padrao': [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]}
    return pd.DataFrame(dict_arquivos)

def checkar_pasta(path_pasta):
    """Compara os dados dos arquivos no banco com os existentes na pasta
    Realiza o download dos arquivos faltantes na pasta"""
    df = SQLite().select_processos()
    df_banco = df.loc[df['arquivo']==path_pasta.upper(), :]
    df_pasta = ler_pasta(path=path_pasta)
    df_check = pd.merge(df_banco, df_pasta, on='nome_padrao', how='left', indicator=True)
    df_check = df_check.loc[df_check['_merge']=='left_only', :].drop(columns='_merge')
    if len(df_check)>0:
        print(df_check['nome_padrao'].values.tolist())
        while True:
            resposta = input('Deseja realizar o download dos arquivos printados acima? [y/n] ')
            if resposta == 'y':
                download(df_check)
                return None
            elif resposta == 'n':
                return None
        

if __name__ == '__main__':
    checkar_pasta('pcat')
    #checkar_pasta('sparta')