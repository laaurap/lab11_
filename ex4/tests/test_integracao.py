import pytest

from pedido import fechar
from estoque import Estoque
from frete import calcular


def test_integracao_pedido():
    estoque = Estoque({"livro": 5})

    resultado = fechar(
        "livro", 2, 4000, 1, "SP",
        estoque, calcular
    )

    assert resultado == {
        "status": "fechado",
        "total": 9700
    }