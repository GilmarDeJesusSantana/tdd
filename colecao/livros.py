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
    pass
