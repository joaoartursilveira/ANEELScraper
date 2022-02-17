from bs4 import BeautifulSoup
from datetime import datetime
from unidecode import unidecode
from time import sleep
from conexao_sql import SQLite
import re


def formatar_data(raw_date) -> str:
    """Formatar a data em Y/M/d"""
    data_regex = re.compile(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}")
    data_formata = data_regex.findall(raw_date)[0].replace('/','-')
    return datetime.strptime(data_formata, "%d-%m-%Y").strftime("%Y-%m-%d")

def clear_string(string: str) -> str:
    """Retira caracteres especiais e espaços em branco"""
    limpado = unidecode(''.join(char for char in string)).replace(' ', '').upper()
    return ''.join(char for char in limpado if char.isalnum())

def localizar_arquivo(arquivo, agente, data_processo, processo, lista_link):
    """"Procura os links que contenham o arquivo procurado (SPARTA ou PCAT)"""
    if arquivo in lista_link['href'].upper():
        agente_padrao = SQLite().info_agente(agente)
        lista_processo = [arquivo, agente_padrao, data_processo, processo, lista_link['href']]
        return lista_processo

def coletor_tr(driver):
    """Varredura da página procurando-se pelas planilhas de SPARTA e PCAT"""
    sleep(2)
    soup = BeautifulSoup(driver.page_source, features='html.parser')
    driver.quit()
    style = {'style': "padding-left: 5px; padding-bottom: 5px; padding-right: 5px; padding-top: 5px;"}
    tabela_tr = soup.find_all('tr', style)[1::]
    td_css = {'valign': 'top', 'class': 'linha2'}
    lista_aneel = []
    for linha in tabela_tr:
        td = linha.find_all('td', td_css)
        processo = clear_string(td[2])
        if processo in ['REAJUSTE', 'REVISAO', 'REVISAOEXTRAORDINARIA']:
            agente = clear_string(td[0])
            data_processo = formatar_data(td[3].text)
            for links in linha('a', href=True):
                lista_sparta = localizar_arquivo('SPARTA', agente, data_processo, processo, links)
                lista_pcat = localizar_arquivo('PCAT', agente, data_processo, processo, links)
                if lista_sparta is not None:
                    lista_aneel.append(lista_sparta)
                if lista_pcat is not None:
                    lista_aneel.append(lista_pcat)
    return lista_aneel

