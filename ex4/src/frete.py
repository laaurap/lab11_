def calcular(peso_kg, uf):
    """Devolve o frete em centavos."""
    base = 1500 + 200 * peso_kg
    return base if uf == "SP" else base + 1000