from copy import deepcopy

import httpx
from bs4 import BeautifulSoup

from correios_plus.filtros.filtro import CampoType, Tipo, TipoType
from correios_plus.modelos.endereco_ou_cep_model import Endereco


class EnderecoOuCep:
    """
    Classe para buscar endereços e CEPs pelo site do Correios.

    Não utilize nº de casa/apto/lote/prédio ou abreviação

    >>> EnderecoOuCep("Alameda Santa Cruz").buscar().enderecos
    [Endereco(logradouro='Alameda Santa Cruz', bairro='Santa Cruz', localidade='Rio de Janeiro', uf='RJ', cep='21521020', complemento='')]

    >>> EnderecoOuCep("21521020").filtrar(Campo.UF, "RJ").enderecos
    [Endereco(logradouro='Alameda Santa Cruz', bairro='Santa Cruz', localidade='Rio de Janeiro', uf='RJ', cep='21521020', complemento='')]


    """

    def __init__(
        self,
        endereco_ou_cep: str,
        tipo: TipoType = Tipo.TUDO,
    ):
        self.endereco_ou_cep = endereco_ou_cep
        self.tipo = tipo
        self.fields = ["logradouro", "bairro", "localidade", "uf", "cep"]
        self.pagini = 1
        self.pagfim = 50
        self.enderecos: list[Endereco] = []

    def __repr__(self) -> str:
        return f"EnderecoOuCep({self.endereco_ou_cep=}, {self.tipo=})".replace(
            "self.", ""
        )

    def requisicao(self):
        data = {
            "relaxation": self.endereco_ou_cep,
            "tipoCEP": self.tipo,
            "semelhante": "N",
            "exata": "S",
            "qtrows": "50",
            "pagini": self.pagini,
            "pagfim": self.pagfim,
        }
        with httpx.Client() as client:
            return client.post(
                "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm",
                data=data,
            )

    def buscar(self):
        response = self.requisicao()
        enderecos = self.extrair_dados(response)
        self.enderecos = [Endereco(**e) for e in enderecos]
        return self

    def proximar_pagina(self):
        self.pagini += 50
        self.pagfim += 50
        cls = deepcopy(self)
        cls.pagini = self.pagini
        cls.pagfim = self.pagfim
        cls.enderecos = None
        cls.tipo = self.tipo
        return cls.buscar()

    def _tr_to_dict(self, tr):
        cidade_estado = tr[2].split("/")
        tr[2] = cidade_estado[0]
        tr.insert(3, cidade_estado[1])
        return dict(zip(self.fields, tr))

    @classmethod
    def from_filtered(cls, original_instance, enderecos_filtrados) -> "EnderecoOuCep":
        instancia = cls(
            endereco_ou_cep=original_instance.endereco_ou_cep,
            tipo=original_instance.tipo,
        )
        instancia.enderecos = enderecos_filtrados
        return instancia

    def filtrar(self, campo: CampoType, valor: str) -> "EnderecoOuCep":
        if not self.enderecos:
            self.buscar()
        campo_lower = campo.lower()
        enderecos_filtrados = [
            e for e in self.enderecos if getattr(e, campo_lower) == valor
        ]
        return self.from_filtered(self, enderecos_filtrados)

    def __getitem__(self, index) -> Endereco:
        return self.enderecos[index]

    def extrair_dados(self, response) -> list[dict]:
        dados: list[dict] = []
        soup = BeautifulSoup(response.content, "html.parser")
        content_page = soup.find("div", {"class": "ctrlcontent"})
        if (
            not content_page
            or content_page.find("p").get_text(strip=True) == "Dados não encontrado"
        ):
            return dados
        for tag in soup.find_all("tr"):
            dados_tr = []
            for td in tag.find_all("td"):
                dado = td.get_text(strip=True)
                dados_tr.append(dado)
            if dados_tr:
                endereco = self._tr_to_dict(dados_tr)
                dados.append(endereco)
        return dados

    def __len__(self) -> int:
        return len(self.enderecos)
