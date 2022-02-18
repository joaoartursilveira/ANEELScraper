import pandas as pd
from unidecode import unidecode


def criar_df_aneel(tabela_aneel):
    colunas_aneel = ['distribuidora', 'data_processo', 'processo', 'arquivo','link']
    return pd.DataFrame(tabela_aneel, columns=colunas_aneel)

def filtrar_data_processo(df_aneel, data_corte: str):
    formato_data = '%Y-%m-%d'
    df_aneel['data_processo'] = pd.to_datetime(df_aneel['data_processo'], format=formato_data)
    filtro_data = df_aneel['data_processo'] >= pd.to_datetime(data_corte, format=formato_data)
    df_aneel_corte = df_aneel.loc[filtro_data, :]
    df_aneel_corte['data_processo'] = df_aneel_corte['data_processo'].dt.strftime(formato_data)
    return df_aneel_corte

def nome_padrao_arquivo(df):
    formatar_string = lambda string: unidecode(''.join(char for char in string if char.isalnum())).replace(' ','').upper()
    df['identificador'] = df['link'].apply(lambda x: formatar_string(x.split('/')[-1].split('.')[0]))
    df['extensao'] = df['link'].apply(lambda x: x.split('.')[-1])
    df['chave_processo'] = df['distribuidora']+'_'+df['data_processo']+'_'+df['processo']
    df['nome_padrao'] = df['arquivo']+'_'+df['chave_processo']+'_('+df['identificador']+').'+df['extensao']
    return df.drop(columns=['identificador', 'extensao'])

def normalizar_dados(df_padrao):
    df_pt_colunas = ['distribuidora','data_processo','processo','chave_processo']
    df_arquivamento_colunas = ['arquivo', 'chave_processo', 'link', 'nome_padrao']
    df_pt = df_padrao.loc[:, df_pt_colunas].drop_duplicates()
    df_arquivamento = df_padrao.loc[:, df_arquivamento_colunas]
    return {'processo_tarifario': df_pt,
            'processo_arquivamento': df_arquivamento}


if __name__ == '__main__':
    exemplos = {'link': ['https://www2.aneel.gov.br/aplicacoes/tarifa/arquivo/CVA ERO 2021.xlsx', 
    'https://www2.aneel.gov.br/aplicacoes/tarifa/arquivo/SPARTA Novo Contrato - Energisa Acre.xlsx',
    "https://www2.aneel.gov.br/aplicacoes/tarifa/arquivo/SPARTA Cooperaliança v13 versão final.xlsx"]}
    df_exemplo = pd.DataFrame(exemplos)
    nome_padrao_arquivo(df_exemplo)