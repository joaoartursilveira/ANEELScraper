from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


class PainelAneel():
    def __init__(self):
        site = 'https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/'
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
        self.wait = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions)
        self.driver.get(site)
        

    # concessionarias: option[4]
    def escolha_distribuidoras(self):
        """Escolha Categoria do Agente: 'concessionária de distribuição'"""
        xpath_distribuidora = '//select[@name="CategoriaAgente"]/option[4]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_distribuidora)))
        self.driver.find_element(By.XPATH, xpath_distribuidora).click()
        
    def escolha_agentes(self):
        """Escolha Agente: 'Todos'"""
        xpath_agentes = '//select[@name="Agentes"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'{xpath_agentes}/option[3]')))
        agentes = Select(self.driver.find_element(By.XPATH, xpath_agentes))
        agentes.select_by_value('0')

    def escolha_processo(self):
        """Escolha Processo: 'Todos'"""
        xpath_processo = '//select[@name="TipoProcesso"]/option[@value="0"]'
        self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_processo)))
        processos = Select(self.driver.find_element(By.NAME, 'TipoProcesso'))
        processos.select_by_value('0')

    def escolha_ano(self):
        """Escolha Ano: 'Todos'"""
        xpath_ano = '//select[@name="Ano"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, f'{xpath_ano}/option[2]')))
        selecao_anos = Select(self.driver.find_element(By.XPATH, xpath_ano))
        selecao_anos.select_by_value('0')

    def clicar_procurar(self):
        """Clique no botão de procura"""
        xpath_botao = '//input[@type="Submit"]'
        self.driver.find_element(By.XPATH, xpath_botao).click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//tbody/tr[4]')))