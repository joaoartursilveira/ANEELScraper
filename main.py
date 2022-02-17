#pacotes utilizados
from coletor import coletor_tr
from conexao_sql import SQLite
from seletor import PainelAneel
import pandas as pd
import tratamento_dados_aneel as tda
pd.options.display.max_columns = 500
pd.options.mode.chained_assignment = None


def iniciar_selecao():
    aneel = PainelAneel()
    aneel.escolha_agentes()
    aneel.escolha_processo()
    aneel.escolha_ano()
    aneel.clicar_procurar()
    tabela_aneel = coletor_tr(aneel.driver)
    return tabela_aneel


def iniciar_tratamento(tabela, data_corte):
    df_aneel = tda.criar_df_aneel(tabela)
    df_aneel_corte = tda.filtrar_data_processo(df_aneel, data_corte=data_corte)
    df_aneel_padrao = tda.nome_padrao_arquivo(df_aneel_corte)
    return df_aneel_padrao


def relacao_arquivos_novos(df_padrao):
    df_banco = SQLite().select_processos()
    df_novos = pd.merge(df_padrao, df_banco, on=list(df_banco.columns), indicator=True)
    df_novos = df_novos.loc[df_novos['_merge']=='left_only', :]
    return df_novos

def main():
    tabela_aneel = iniciar_selecao()
    df_aneel_padrao = iniciar_tratamento(tabela_aneel, data_corte='2021-12-31')
    df_novos = relacao_arquivos_novos(df_padrao=df_aneel_padrao)
    if len(df_novos) == 0:
        print('Nenhum processo novo foi encontrado')
        print(f'Ultimo processo mapeado: {df_aneel_padrao.iloc[0, :].values.tolist()}')
        return None
    print(df_novos.values.tolist())
    SQLite().inserir_sqlite(df_novos)


if __name__ == '__main__':
    #iniciar_selecao()
    main()
