import os
import requests

def download(df):
    path_root =  r'D:\python_projects\cpfl\arquivos_aneel'
    for arquivo, nome_padrao, link in df[['arquivo','nome_padrao','link']].to_numpy():
        path_arquivo = os.path.join(path_root, arquivo.lower(), nome_padrao)
        with open(path_arquivo, 'wb') as f:
            f.write(requests.get(link).content)
            f.flush()
            f.close()
        print(f'Arquivo: "{nome_padrao}" foi baixado com sucesso')
    print('Todos os arquivos foram baixados com sucesso')

