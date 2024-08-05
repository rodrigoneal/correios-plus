import httpx

from correios_plus.buscadores.buscador import Buscador
from correios_plus.filtros.filtro import Tipo, TipoType
from correios_plus.modelos.endereco_ou_cep_model import Endereco


class EnderecoOuCep(Buscador):
    """
    Classe para buscar endereços e CEPs pelo site do Correios.

    Não utilize nº de casa/apto/lote/prédio ou abreviação

    >>> EnderecoOuCep("Alameda Santa Cruz").buscar()
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
    @classmethod
    def from_filtered(cls, original_instance, enderecos_filtrados):
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