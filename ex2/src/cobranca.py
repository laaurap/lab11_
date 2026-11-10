def confirmar(pedido, centavos, gateway, email, tentativas=3):
    if tentativas < 1:
        raise ValueError("Tentativas deve ser maior ou igual a 1")

    for tentativa in range(tentativas):
        try:
            status = gateway.cobrar(pedido, centavos)

            if status == "aprovado":
                email.enviar(pedido, "pedido confirmado")

            return status

        except ConnectionError:
            if tentativa == tentativas - 1:
                email.enviar(pedido, "falha na cobranca")
                raise

