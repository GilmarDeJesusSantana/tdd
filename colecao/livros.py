import logging
import os
from urllib.error import HTTPError
from urllib.request import urlopen


def consultar_livros(autor):
    dados = preparar_dados_para_requisicao(autor)
    url = obter_url('https://buscador', dados)
    retorno = executar_requisicao(url)
    return retorno


def preparar_dados_para_requisicao(autor):
    pass


def obter_url(url, dados):
    pass


def executar_requisicao(url):
    try:
        with urlopen(url, timeout=10) as resposta:
            resultado = resposta.read().decode("utf-8")
    except HTTPError as error:
        logging.exception(f'Ao acessar {url} : {error}')
    else:
        return resultado


def escrever_em_arquivo(arquivo, conteudo):
    diretorio = os.path.dirname(arquivo)
    try:
        os.makedirs(diretorio)
    except OSError:
        logging.exception(f'Não foi possível criar diretório {diretorio}')

    try:
        with open(arquivo, 'w') as file_open:
            file_open.write(conteudo)
    except OSError as error:
        logging.exception(f'Não foi possível criar arquivo {arquivo}')
