import pandas as pd
from unidecode import unidecode


def criar_df_aneel(tabela_aneel):
    """Cria o dataframe dos arquivos do site da ANEEL"""
    colunas_aneel = ['distribuidora', 'data_processo', 'processo', 'arquivo','link']
    return pd.DataFrame(tabela_aneel, columns=colunas_aneel)

def filtrar_data_processo(df_aneel, data_corte: str):
    """Filtra o dataframe do site da ANEEL baseado na data de corte declarada"""
    formato_data = '%Y-%m-%d'
    df_aneel['data_processo'] = pd.to_datetime(df_aneel['data_processo'], format=formato_data)
    filtro_data = df_aneel['data_processo'] >= pd.to_datetime(data_corte, format=formato_data)
    df_aneel_corte = df_aneel.loc[filtro_data, :]
    df_aneel_corte['data_processo'] = df_aneel_corte['data_processo'].dt.strftime(formato_data)
    return df_aneel_corte

def nome_padrao_arquivo(df):
    """Formato padrão definido para o dataframe do site da ANEEL"""
    formatar_string = lambda string: unidecode(''.join(char for char in string if char.isalnum())).replace(' ','').upper()
    df['identificador'] = df['link'].apply(lambda x: formatar_string(x.split('/')[-1].split('.')[0]))
    df['extensao'] = df['link'].apply(lambda x: x.split('.')[-1])
    df['chave_processo'] = df['distribuidora']+'_'+df['data_processo']+'_'+df['processo']
    df['nome_padrao'] = df['arquivo']+'_'+df['chave_processo']+'_('+df['identificador']+').'+df['extensao']
    return df.drop(columns=['identificador', 'extensao','chave_processo'])

