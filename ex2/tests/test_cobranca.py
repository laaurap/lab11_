import pytest
from unittest.mock import Mock, call
from cobranca import confirmar


def test_cobranca_aprovada():
    gateway = Mock()
    email = Mock()
    gateway.cobrar.return_value = "aprovado"

    resultado = confirmar("pedido1", 5000, gateway, email)

    assert resultado == "aprovado"
    gateway.cobrar.assert_called_once_with("pedido1", 5000)
    email.enviar.assert_called_once_with(
        "pedido1", "pedido confirmado"
    )


def test_cobranca_negada():
    gateway = Mock()
    email = Mock()
    gateway.cobrar.return_value = "negado"

    resultado = confirmar("pedido1", 5000, gateway, email)

    assert resultado == "negado"
    gateway.cobrar.assert_called_once_with("pedido1", 5000)
    email.enviar.assert_not_called()


def test_cobranca_aprovada_apos_falha():
    gateway = Mock()
    email = Mock()

    gateway.cobrar.side_effect = [
        ConnectionError("Falha"),
        "aprovado"
    ]

    resultado = confirmar("pedido1", 5000, gateway, email)

    assert resultado == "aprovado"
    assert gateway.cobrar.call_count == 2
    assert gateway.cobrar.call_args_list == [
        call("pedido1", 5000),
        call("pedido1", 5000)
    ]
    email.enviar.assert_called_once_with(
        "pedido1", "pedido confirmado"
    )


def test_todas_tentativas_falham():
    gateway = Mock()
    email = Mock()
    gateway.cobrar.side_effect = ConnectionError("Falha")

    with pytest.raises(ConnectionError):
        confirmar("pedido1", 5000, gateway, email)

    assert gateway.cobrar.call_count == 3
    assert gateway.cobrar.call_args_list == [
        call("pedido1", 5000)
    ] * 3
    email.enviar.assert_called_once_with(
        "pedido1", "falha na cobranca"
    )


def test_tentativas_personalizadas():
    gateway = Mock()
    email = Mock()
    gateway.cobrar.side_effect = ConnectionError("Falha")

    with pytest.raises(ConnectionError):
        confirmar("pedido1", 5000, gateway, email, tentativas=2)

    assert gateway.cobrar.call_count == 2
    email.enviar.assert_called_once_with(
        "pedido1", "falha na cobranca"
    )


def test_tentativa_invalida():
    gateway = Mock()
    email = Mock()

    with pytest.raises(ValueError):
        confirmar("pedido1", 5000, gateway, email, tentativas=0)

    gateway.cobrar.assert_not_called()
    email.enviar.assert_not_called()


def test_cobranca_negada_apos_falha():
    gateway = Mock()
    email = Mock()

    gateway.cobrar.side_effect = [
        ConnectionError("Falha"),
        "negado"
    ]

    resultado = confirmar("pedido1", 5000, gateway, email)

    assert resultado == "negado"
    assert gateway.cobrar.call_count == 2
    email.enviar.assert_not_called()