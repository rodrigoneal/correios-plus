from abc import ABC
from copy import deepcopy

import httpx
from bs4 import BeautifulSoup

from correios_plus.filtros.filtro import CampoType
from correios_plus.modelos.endereco_ou_cep_model import Endereco


class Buscador(ABC):
    fields: list[str]
    pagini: int
    pagfim: int
    enderecos: list[Endereco]

    @classmethod
    def from_filtered(cls, *args, **kwargs) -> "Buscador":
        raise NotImplementedError
    def requisicao(self) -> httpx.Response:
        """
        Realiza uma requisição para o site do Correios.

        Returns:
            httpx.Response: Resposta da requisição
        """
        raise NotImplementedError

    def buscar(self) -> "Buscador":
        """
        Busca os dados no site do Correios.

        Returns:
            Buscador: Retorna uma instância da classe.
        """
        response = self.requisicao()
        enderecos = self.extrair_dados(response)
        self.enderecos = [Endereco(**e) for e in enderecos]
        return self

    def extrair_dados(self, response) -> list[dict]:
        """
        Extrai os dados da resposta da requisição.

        Arguments:
            response -- Resposta da requisição

        Returns:
            list[dict] -- Lista de dicionários com os dados
        """
        dados: list[dict] = []
        soup = BeautifulSoup(response.content, "html.parser")
        content_page = soup.find("div", {"class": "ctrlcontent"})
        if (
            not content_page
            or content_page.find("p").get_text(strip=True) == "Dados não encontrado"  # type: ignore
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

    def _tr_to_dict(self, tr) -> dict:
        """
        Transforma uma linha da tabela HTML em um dicionário.

        Arguments:
            tr -- Tabela HTML

        Returns:
            dict -- Dicionário com os dados
        """
        cidade_estado = tr[2].split("/")
        tr[2] = cidade_estado[0]
        tr.insert(3, cidade_estado[1])
        return dict(zip(self.fields, tr))

    def __getitem__(self, index) -> Endereco:
        """
        Retorna o item pelo indice.

        Arguments:
            index -- Indice

        Returns:
            Endereco -- Objeto Endereco
        """
        return self.enderecos[index]

    def __len__(self) -> int:
        """
        Retorna o tamanho da lista de endereços.

        Returns:
            int -- Tamanho da lista de endereços
        """
        return len(self.enderecos)

    def to_dict(self) -> dict:
        """
        Retorna um dicionário com os dados.

        Returns:
            dict -- Dicionário com os dados
        """
        return {"enderecos": [e.dict() for e in self.enderecos]}

    def proximar_pagina(self) -> "Buscador":
        """
        Retorna uma instância da classe com os dados da proxima pagina.

        Returns:
            EnderecoOuCep: Retorna uma instância da classe.
        """
        self.pagini += 50
        self.pagfim += 50
        cls = deepcopy(self)
        cls.pagini = self.pagini
        cls.pagfim = self.pagfim
        cls.enderecos = []
        return cls.buscar()

    def filtrar(self, campo: CampoType, valor: str):
        """
        Filtra os dados pelo campo e valor.

        Arguments:
            campo -- Campo a ser filtrado
            valor -- Valor a ser filtrado

        Returns:
            EnderecoOuCep -- Instância da classe
        """
        if not self.enderecos:
            self.buscar()
        campo_lower = campo.lower()
        enderecos_filtrados = [
            e for e in self.enderecos if getattr(e, campo_lower) == valor
        ]
        return self.from_filtered(self, enderecos_filtrados)
