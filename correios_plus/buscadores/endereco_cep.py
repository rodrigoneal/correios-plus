import httpx

from correios_plus.buscadores.buscador import Buscador



class EnderecoCEP(Buscador):

    fields = ["logradouro", "bairro", "localidade", "uf", "cep"]

    def __init__(self, cep: str):
        self.cep = cep

    def requisicao(self) -> httpx.Response:
        data = {"CEP": self.cep}
        return httpx.post(
            "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaEndereco.cfm",
            data=data,
        )
