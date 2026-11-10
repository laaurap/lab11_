import pytest
from repositorio import RepoSqlite, FakeIngenuo, FakeFiel, EmailDuplicado


@pytest.fixture(
    params=[RepoSqlite, FakeIngenuo, FakeFiel]
)
def repo(request):
    if request.param is FakeIngenuo:
        if request.node.name.startswith(
            ("test_email_maiusculo_minusculo", "test_email_duplicado")
        ):
            pytest.xfail("FakeIngenuo nao respeita o contrato")

    return request.param()


def test_salvar_e_buscar(repo):
    repo.salvar("teste@email.com", "Maria")

    assert repo.buscar("teste@email.com") == "Maria"


def test_buscar_inexistente(repo):
    assert repo.buscar("inexistente@email.com") is None


def test_email_maiusculo_minusculo(repo):
    repo.salvar("TESTE@EMAIL.COM", "Maria")

    assert repo.buscar("teste@email.com") == "Maria"


def test_email_duplicado(repo):
    repo.salvar("teste@email.com", "Maria")

    with pytest.raises(EmailDuplicado):
        repo.salvar("TESTE@EMAIL.COM", "Ana")