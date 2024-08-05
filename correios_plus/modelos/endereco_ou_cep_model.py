from typing import NamedTuple


class Endereco(NamedTuple):
    logradouro: str
    bairro: str
    localidade: str
    uf: str
    cep: str
    complemento: str = ""

    def dict(self) -> dict:
        return self._asdict()
