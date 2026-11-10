from estoque import SemEstoque


def fechar(item, qtd, preco, peso_kg, uf, estoque, frete):
    try:
        estoque.reservar(item, qtd)
    except SemEstoque:
        return {"status": "sem estoque"}

    total = preco * qtd + frete(peso_kg, uf)

    return {"status": "fechado", "total": total}