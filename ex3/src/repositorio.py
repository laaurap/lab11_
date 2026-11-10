import sqlite3


class EmailDuplicado(Exception):
    pass


class RepoSqlite:
    def __init__(self):
        self.conexao = sqlite3.connect(":memory:")
        self.conexao.execute(
            "CREATE TABLE usuarios (email TEXT PRIMARY KEY, nome TEXT)"
        )

    def salvar(self, email, nome):
        email = email.lower()

        try:
            self.conexao.execute(
                "INSERT INTO usuarios (email, nome) VALUES (?, ?)",
                (email, nome)
            )
            self.conexao.commit()
        except sqlite3.IntegrityError:
            raise EmailDuplicado(email)

    def buscar(self, email):
        email = email.lower()

        resultado = self.conexao.execute(
            "SELECT nome FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        return resultado[0] if resultado else None

class FakeIngenuo:
    def __init__(self):
        self.usuarios = {}

    def salvar(self, email, nome):
        self.usuarios[email] = nome

    def buscar(self, email):
        return self.usuarios.get(email)


class FakeFiel:
    def __init__(self):
        self.usuarios = {}

    def salvar(self, email, nome):
        email = email.lower()

        if email in self.usuarios:
            raise EmailDuplicado(email)

        self.usuarios[email] = nome

    def buscar(self, email):
        email = email.lower()
        return self.usuarios.get(email)