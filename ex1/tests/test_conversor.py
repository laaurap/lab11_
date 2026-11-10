import pytest
from conversor import ConversorFrete
from unittest.mock import Mock
from conversor import CotacaoIndisponivel

class CotacaoStub:
    def __init__(self, taxa):
        self.taxa = taxa

    def dolar(self):
        return self.taxa


@pytest.mark.parametrize(
    "centavos, taxa, esperado",
    [
        (100, 5.0, 500),
        (200, 5.0, 1000),
        (150, 4.0, 600),
        (1, 2.5, 2),
        (3, 2.5, 8),
    ]
)
def test_conversao(centavos, taxa, esperado):
    cotacao = CotacaoStub(taxa)
    conversor = ConversorFrete(cotacao)

    resultado = conversor.em_centavos_de_real(centavos)

    assert resultado == esperado

@pytest.mark.parametrize("taxa", [0, -1, -5])
def test_taxa_invalida(taxa):
    cotacao = CotacaoStub(taxa)
    conversor = ConversorFrete(cotacao)

    with pytest.raises(ValueError):
        conversor.em_centavos_de_real(100)

def test_cotacao_indisponivel():
    cotacao = Mock()
    cotacao.dolar.side_effect = TimeoutError

    conversor = ConversorFrete(cotacao)

    with pytest.raises(CotacaoIndisponivel):
        conversor.em_centavos_de_real(100)

    cotacao.dolar.assert_called_once_with()