# ANEEL
## Site de coleta:  https://www2.aneel.gov.br/aplicacoes_liferay/tarifa/
## Tipo de arquivos: SPARTA e PCAT
## Armazenamento: sqlite3 - processo_tarifario_aneel.db 

Scraper em python do site da ANEEL para a extração dos arquivos SPARTA e PCAT. O código faz a seleção dos menus, coletando-se a distribuidora, data processo, processo, o link do arquivo e gera um nome padrão para o arquivamento em pasta.
O usuário deve apenas executar o main.py que o código baixará os dados armazenados em uma pasta para cada tipo de arquivo (SPARTA ou PCAT).
