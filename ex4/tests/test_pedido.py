from unittest.mock import Mock
from pedido import fechar
from estoque import SemEstoque


def test_fecha_com_frete():
    estoque = Mock()
    estoque.reservar.return_value = None

    frete = Mock(return_value=1700)

    resultado = fechar(
        "livro", 2, 4000, 1, "SP", estoque, frete
    )

    assert resultado == {
        "status": "fechado",
        "total": 9700
    }

    estoque.reservar.assert_called_once_with("livro", 2)
    frete.assert_called_once_with(1, "SP")


def test_sem_estoque():
    estoque = Mock()
    estoque.reservar.side_effect = SemEstoque("livro")

    frete = Mock()

    resultado = fechar(
        "livro", 2, 4000, 1, "SP", estoque, frete
    )

    assert resultado == {"status": "sem estoque"}

    estoque.reservar.assert_called_once_with("livro", 2)
    frete.assert_not_called()