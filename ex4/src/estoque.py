class SemEstoque(Exception):
    pass


class Estoque:
    def __init__(self, itens):
        self.itens = dict(itens)

    def reservar(self, item, qtd):
        if self.itens.get(item, 0) < qtd:
            raise SemEstoque(item)

        self.itens[item] -= qtd