# Instalação do Python
Antes de qualquer coisa, precisa-se do python instalado na maquina do usuário. Para tanto, recomenda-se o guia [Python YouTube](https://www.youtube.com/watch?v=KeDLsBmi3JA) com todos os passos. A instalação é bem simples e rápida.

## Download do módulo
Caso o usuário for familiar com o github, prossiga normalmente com a clonagem do repositório ou download do zip. Para os não familiares, o zip pode ser feito [aqui](https://github.com/joaoartursilveira/ANEEL/archive/refs/heads/master.zip). Extraia a pasta zipada no local escolhido para abrigar o módulo.

## Setup do ambiente
Após a instalação do python e a extração do zip, é necessário criar um ambiente virtual para hospedar todas as dependências utilizadas na produção deste módulo, para isso:
1. Navegue até a pasta escolhida para abrigar o módulo.
2. Digite "cmd" (sem aspas) na barra do explorador de arquivos da pasta e a janela de comandos aparecerá.
3. Digite o comando "python -m venv venv" (sem as aspas) e... pronto, seu ambiente virtual foi criado com sucesso.
4. Ative o ambiente virtual com o comando "venv\scripts\activate" (sem as aspas)
5. O termo (venv) irá aparecer no começo da linha, indicando que o ambiente foi ativado.
6. Instale todas as dependencias do módulo com o comando "pip install -r requirements.txt" (sem as aspas) e... pronto, o ambiente virtual foi configurado com sucesso.
7. Para executar o código, digite, com o ambiente virtual ainda ativado, o comando "python main.py" (sem as aspas).

**Detalhe: a instalação e configuração do ambiente virtual são feitos uma única vez. Sempre que desejar executar o código, repita os passos 1, 2, 4 e 7.**

# Scraper em python do site dos resultados tarifários da ANEEL para as SPARTA e PCAT
## URL:  https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/

###### Comentário sobre o módulo
O processo é feito com base no site da ANEEL e todas as informações estão abertas ao público. Dito isso, esse módulo pode ser aprimorado para incluir novos arquivamentos, como as notas técnicas, resoluções homologatórias, dentre outros. Fique à vontade para clonar o repositório e explorar todas as funcionalidades.
###### Armazenamento: sqlite3 - processo_tarifario_aneel.db
###### Atualização dos dados: Coleta atualizada no dia 20/02/2022


O usuário deve executar apenas o main.py, como explicado [anteriormente](#instala%C3%A7%C3%A3o-do-python), englobando os processos:
- As pastas de arquivamento da SPARTA e PCAT são criadas automaticamente, caso não existam.
- O links já armazenados no banco podem ser baixados para as pastas, caso o usuário desejar.
- O scraper inicializa a seleção dos menus do site da aneel.
- O scraper varre o html do site coletando as informações dos processos tarifários e os arquivos SPARTA e PCAT.
- Caso um processo novo for encontrado, o usuário pode incluí-lo no banco e realizar o download em pasta, com o nome padrão gerado, seguindo a regra: ARQUIVO_DISTRIBUIDORA_DATAPROCESSO_PROCESSO_(NOMEORIGINAL).extensão (normalmente xlsx ou xlsm).

Além do mapeamento dos arquivos citados, o banco de dados vem com a extração das tarifas (soma das abas TUSD e TE) e do efeito consumidor médio das PCAT, feitos em outro projeto, para que o usuário possa interagir diretamente com o banco, sem a necessidade do download de todos os arquivos. Abaixo pode-se ver o diagrama do banco de dados, bem como a relação entre as tabelas. <br/>
<p align="center">
  <img src="/db/diagrama_aneel.png" width="750">
</p>

