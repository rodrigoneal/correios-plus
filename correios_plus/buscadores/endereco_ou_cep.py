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

    def requisicao(self) -> httpx.Response:
        """
        Realiza uma requisição para o site do Correios.

        Returns:
            httpx.Response: Resposta da requisição
        """
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

    def buscar(self) -> "EnderecoOuCep":
        """
        Busca os dados no site do Correios.

        Returns:
            EnderecoOuCep: Retorna uma instância da classe.
        """
        response = self.requisicao()
        enderecos = self.extrair_dados(response)
        self.enderecos = [Endereco(**e) for e in enderecos]
        return self

    def proximar_pagina(self) -> "EnderecoOuCep":
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
        cls.tipo = self.tipo
        return cls.buscar()

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

    @classmethod
    def from_filtered(cls, original_instance, enderecos_filtrados) -> "EnderecoOuCep":
        """
        Cria uma instância da classe com os dados filtrados.

        Arguments:
            original_instance -- Instância da classe original
            enderecos_filtrados -- Lista de endereços filtrados

        Returns:
            EnderecoOuCep -- Instância da classe
        """
        instancia = cls(
            endereco_ou_cep=original_instance.endereco_ou_cep,
            tipo=original_instance.tipo,
        )
        instancia.enderecos = enderecos_filtrados
        return instancia

    def filtrar(self, campo: CampoType, valor: str) -> "EnderecoOuCep":
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

    def __getitem__(self, index) -> Endereco:
        """
        Retorna o item pelo indice.

        Arguments:
            index -- Indice

        Returns:
            Endereco -- Objeto Endereco
        """
        return self.enderecos[index]

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
        """
        Retorna o tamanho da lista de endereços.

        Returns:
            int -- Tamanho da lista de endereços
        """
        return len(self.enderecos)
