from urllib.error import HTTPError

import pytest

from colecao.livros import consultar_livros, executar_requisicao, escrever_em_arquivo
from unittest.mock import patch, mock_open, Mock, MagicMock
from unittest import skip


class StubHTTPResponse:
    def read(self):
        return b''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@patch('colecao.livros.urlopen', return_value=StubHTTPResponse())
def test_consultar_livros_retorna_resultado_formato_string(stub_urlopen):
    resultado = consultar_livros('Agatha Christie')
    assert type(resultado) == str


@patch('colecao.livros.urlopen', return_value=StubHTTPResponse())
def test_consultar_livros_chama_preparar_dados_para_requisicao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros(
        stub_urlopen):
    with patch('colecao.livros.preparar_dados_para_requisicao') as spy_preparar_dados:
        consultar_livros('Agatha Christie')
        spy_preparar_dados.assert_called_once_with('Agatha Christie')


@patch('colecao.livros.urlopen', return_value=StubHTTPResponse())
def test_consultar_livros_chama_obter_url_usando_como_parametro_o_retorno_de_preparar_dados_para_requisicao(
        stub_urlopen):
    with patch('colecao.livros.preparar_dados_para_requisicao') as stub_preparar:
        dados = {'autor': 'Agatha Christie'}
        stub_preparar.return_value = dados
        with patch('colecao.livros.obter_url') as spy_obter_url:
            consultar_livros('Agatha Christie')
            spy_obter_url.assert_called_once_with('https://buscador', dados)


@patch('colecao.livros.urlopen', return_value=StubHTTPResponse())
def test_consultar_livros_chama_executar_requisicao_usando_retorno_obter_url(stub_urlopen):
    with patch('colecao.livros.obter_url') as stub_obter_url:
        stub_obter_url.return_value = 'https://buscador'
        with patch('colecao.livros.executar_requisicao') as spy_executar_requisicao:
            consultar_livros('Agatha Christie')
            spy_executar_requisicao.assert_called_once_with('https://buscador')


def stub_de_urlopen(url, timeout):
    return StubHTTPResponse()


def test_executar_requisicao_retorna_tipo_string():
    with patch('colecao.livros.urlopen', stub_de_urlopen):
        print(stub_de_urlopen)
        resultado = executar_requisicao('https://buscarlivros?author=JK+Rowlings')
        assert type(resultado) == str


def test_executar_requisicao_retorna_resultado_tipo_str():
    with patch('colecao.livros.urlopen') as dube_de_urlopen:
        print(dube_de_urlopen)
        dube_de_urlopen.return_value = StubHTTPResponse()
        resultado = executar_requisicao('https://buscarlivros?autor=JK+Rowlings')
        assert type(resultado) == str


def test_executar_requisicao_retorna_resultado_tipo_str_com_return():
    with patch('colecao.livros.urlopen', return_value=StubHTTPResponse()):
        resutado = executar_requisicao('https://buscarlivros?autor=JK+Rowlings')
        assert type(resutado) == str


@patch('colecao.livros.urlopen', return_value=StubHTTPResponse())
def test_executar_requisicao_retorna_resultado_tipo_str_com_decorator(duble_de_urlopen):
    resutado = executar_requisicao('https://buscarlivros?autor=JK+Rowlings')
    assert type(resutado) == str


@patch('colecao.livros.urlopen')
def test_executar_requisicao_retorna_resultado_tipo_str_com_decorator_sem_return_value(duble_de_urlopen):
    duble_de_urlopen.return_value = StubHTTPResponse()
    resutado = executar_requisicao('https://buscarlivros?autor=JK+Rowlings')
    assert type(resutado) == str


class Dummy:
    pass


def stub_de_urlopen_que_levanta_execao_http_error(url, timeout):
    fp = mock_open
    fp.close = Mock
    raise HTTPError(Mock(), Mock(), 'Mensagem de Error', Mock(), fp)


# def test_executar_requisicao_levanta_excecao_do_tipo_http_error():
#     with patch('colecao.livros.urlopen', stub_de_urlopen_que_levanta_execao_http_error):
#         with pytest.raises(HTTPError) as excecao:
#             executar_requisicao('http://')
#         assert 'Mensagem de Error' in str(excecao.value)
#
#
# @patch('colecao.livros.urlopen')
# def test_executar_requisicao_levanta_excecao_do_tipo_http_error_com_decorator(duble_de_urlopen):
#     fp = mock_open
#     fp.close = Mock()
#     duble_de_urlopen.side_effect = HTTPError(Mock(), Mock(), 'Mensagem de Error', Mock(), fp)
#     with pytest.raises(HTTPError) as excecao:
#         executar_requisicao('http://')
#         assert 'Mensagem de Error' in str(excecao.value)


def test_executar_requisicao_levanta_excecao_do_tipo_http_error_com_caplog(caplog):
    with patch('colecao.livros.urlopen',
               stub_de_urlopen_que_levanta_execao_http_error):
        resultado = executar_requisicao('http://')
        mensagem_de_erro = 'Mensagem de Error'
        assert len(caplog.records) == 1
        for registro in caplog.records:
            assert mensagem_de_erro in registro.message


@patch('colecao.livros.urlopen')
def test_executar_requisicao_loga_mensagem_de_erro_de_http_error(stub_urlopen, caplog):
    fp = mock_open
    fp.close = Mock()
    stub_urlopen.side_effect = HTTPError(Mock(), Mock(), 'Mensagem de Error', Mock(), fp)

    executar_requisicao('http://')
    assert len(caplog.records) == 1
    for registro in caplog.records:
        assert 'Mensagem de Error' in registro.message


class DubleLogging:
    def __init__(self):
        self._mensagens = []

    def exception(self, mensagem):
        self._mensagens.append(mensagem)

    @property
    def mensagens(self):
        return self._mensagens


def duble_makedirs(diretorio):
    raise OSError(f'Não foi possível criar diretório {diretorio}')


def test_escrever_em_arquivo_registra_excecao_que_nao_foi_possivel_criar_diretorio():
    arquivo = '/tmp/arquivo'
    conteudo = 'dados de livros'
    duble_logging = DubleLogging()
    with patch('colecao.livros.os.makedirs', duble_makedirs):
        with patch('colecao.livros.logging', duble_logging):
            escrever_em_arquivo(arquivo, conteudo)
            assert 'Não foi possível criar diretório /tmp' in duble_logging.mensagens


@patch('colecao.livros.os.makedirs')
@patch('colecao.livros.logging.exception')
@patch('colecao.livros.open', side_effect=OSError)
def teste_escrever_em_arquivo_registra_erro_ao_criar_o_arquivo(stub_open, spy_exception, stub_makedirs):
    arquivo = '/bla/arquivo.json'
    escrever_em_arquivo(arquivo, 'Dados do livros')
    spy_exception.assert_called_once_with(f'Não foi possível criar arquivo {arquivo}')


class SpyFileOpen:
    def __init__(self):
        self._conteudo = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def write(self, conteudo):
        self._conteudo = conteudo

@skip
@patch('colecao.livros.open')
def test_escrever_em_arquivo_chama_write(stub_de_open):
    arquivo = '/tmp/arquivo'
    conteudo = 'Conteudo do arquivo'
    spy_de_file_open = SpyFileOpen()
    stub_de_open.return_value = spy_de_file_open

    escrever_em_arquivo(arquivo, conteudo)
    assert spy_de_file_open._conteudo == conteudo \


@patch('colecao.livros.open')
def test_escrever_em_arquivo_chama_write(stub_de_open):
    arquivo = '/tmp/arquivo'
    conteudo = 'Conteudo do arquivo'
    spy_de_file_open = MagicMock()
    spy_de_file_open.__enter__.return_value = spy_de_file_open
    spy_de_file_open.__exit__.return_value = None

    stub_de_open.return_value = spy_de_file_open

    escrever_em_arquivo(arquivo, conteudo)
    spy_de_file_open.write.assert_called_once_with(conteudo)
