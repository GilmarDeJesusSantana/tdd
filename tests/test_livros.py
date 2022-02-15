from colecao.livros import consultar_livros
from unittest.mock import patch

def test_consultar_livros_retorna_resultado_formato_sting():
    resultado = consultar_livros('Agatha Christie')
    assert type(resultado) == str

def test_consultar_livros_chama_preparar_dados_para_requisicao_uma_vez_e_com_os_mesmos_parametros_de_consultar_livros():
    with patch('colecao.livros.preparar_dados_para_requisicao') as duble:
        consultar_livros('Agatha Christie')
        duble.assert_called_once_with('Agatha Christie')
