#pacotes utilizados
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from coletor import coletor_tr
from conexao_sql import SQLite
import pandas as pd
import tratamento_dados_aneel as tda
pd.options.display.max_columns = 500
pd.options.mode.chained_assignment = None


class PainelAneel():
    def __init__(self, service, site):
        self.lista_aneel = []
        self.driver = webdriver.Chrome(service=service)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.wait = WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions)
        self.driver.get(site)
        self.escolha_distribuidoras()

    # concessionarias: option[4]
    def escolha_distribuidoras(self):
        xpath_distribuidora = '//select[@name="CategoriaAgente"]/option[4]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_distribuidora)))
        self.driver.find_element(By.XPATH, xpath_distribuidora).click()
        
    # Escolha de processo: 'Todos'
    def escolha_processo(self):
        xpath_processo = '//select[@name="TipoProcesso"]/option[@value="0"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_processo)))
        processos = Select(self.driver.find_element(By.NAME, 'TipoProcesso'))
        processos.select_by_value('0')

    def escolha_agentes(self):
        xpath_agentes = '//select[@name="Agentes"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'{xpath_agentes}/option[3]')))
        agentes = Select(self.driver.find_element(By.XPATH, xpath_agentes))
        agentes.select_by_value('0')

    def escolha_ano(self):
        xpath_ano = '//select[@name="Ano"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'{xpath_ano}/option[2]')))
        selecao_anos = Select(self.driver.find_element(By.XPATH, xpath_ano))
        selecao_anos.select_by_value('0')

    def clicar_procurar(self):
        xpath_botao = '//input[@type="Submit"]'
        self.driver.find_element(By.XPATH, xpath_botao).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//tbody/tr[4]')))


def iniciar_selecao():
    site = 'https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/'
    service = Service(ChromeDriverManager().install())
    aneel = PainelAneel(service, site)
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


def main():
    tabela_aneel = iniciar_selecao()
    df_aneel_padrao = iniciar_tratamento(tabela_aneel, data_corte='2021-12-31')
    banco = SQLite()
    df_banco = banco.select_processos()
    df_novos = pd.merge(df_aneel_padrao, df_banco, on=list(df_banco.columns), indicator=True)
    df_novos = df_novos.loc[df_novos['_merge']=='left_only', :]
    if len(df_novos) != 0:
        print(df_novos.values.tolist())
        banco.inserir_sqlite(df_novos)
    else:
        print('Nenhum processo novo foi encontrado')
        print(f'Ultimo processo mapeado: {df_aneel_padrao.iloc[0, :].values.tolist()}')


if __name__ == '__main__':
    iniciar_selecao()
    #main()
