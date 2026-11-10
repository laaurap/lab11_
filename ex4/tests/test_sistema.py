from pedido import fechar
from estoque import Estoque
from frete import calcular


def test_tres_pedidos_em_sequencia():
    estoque = Estoque({"livro": 3})

    # Primeiro pedido: reserva 2 livros
    pedido1 = fechar(
        "livro", 2, 4000, 1, "SP",
        estoque, calcular
    )

    assert pedido1 == {
        "status": "fechado",
        "total": 9700
    }
    assert estoque.itens["livro"] == 1

    # Segundo pedido: reserva o ultimo livro
    pedido2 = fechar(
        "livro", 1, 4000, 1, "SP",
        estoque, calcular
    )

    assert pedido2 == {
        "status": "fechado",
        "total": 5700
    }
    assert estoque.itens["livro"] == 0

    # Terceiro pedido: estoque esgotado
    pedido3 = fechar(
        "livro", 1, 4000, 1, "SP",
        estoque, calcular
    )

    assert pedido3 == {"status": "sem estoque"}
    assert estoque.itens["livro"] == 0