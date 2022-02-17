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
    with urlopen(url, timeout=10) as resposta:
        resultado = resposta.read().decode("utf-8")
    return resultado
