import httpx

from correios_plus.buscadores.buscador import Buscador
from correios_plus.filtros.filtro import Localidade, LocalidadeType, UFType
from correios_plus.modelos.endereco_ou_cep_model import Endereco


class CEPLocalidade(Buscador):
    """
    Classe para buscar CEPs e localidades pelo site do Correios.

    >>> CEPLocalidade(uf="RJ", localidade="Rio de Janeiro", logradouro="Santa Cruz").filtrar(Campo.UF, "RJ").enderecos
    [Endereco(logradouro='Santa Cruz', bairro='Pavuna', localidade='Rio de Janeiro', uf='RJ', cep='21521020', complemento='')]
    """

    def __init__(
        self,
        uf: UFType,
        localidade: str,
        logradouro: str,
        tipo: LocalidadeType = Localidade.DEFAULT,
        numero: str = "",
    ):
        self.uf = uf
        self.tipo = tipo
        self.localidade = localidade
        self.logradouro = logradouro
        self.numero = numero
        self.fields = ["logradouro", "bairro", "localidade", "uf", "cep"]
        self.pagini = 1
        self.pagfim = 50
        self.enderecos: list[Endereco] = []

    def __repr__(self) -> str:
        return (
            f"CEPLocalidade({self.uf=}, {self.localidade=}, "
            f"{self.tipo=}, {self.logradouro=}, {self.numero=})".replace("self.", "")
        )

    def requisicao(self) -> httpx.Response:
        """
        Realiza uma requisição para o site do Correios.

        Returns:
            httpx.Response: Resposta da requisição
        """
        data = {
            "UF": self.uf,
            "Localidade": self.localidade,
            "Tipo": self.tipo,
            "Logradouro": self.logradouro,
            "Numero": self.numero,
            "Pagini": self.pagini,
            "Pagfim": self.pagfim,
        }
        with httpx.Client() as client:
            return client.post(
                "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCep.cfm",
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
            uf=original_instance.uf,
            localidade=original_instance.localidade,
            logradouro=original_instance.logradouro,
            tipo=original_instance.tipo,
            numero=original_instance.numero,
        )
        instancia.enderecos = enderecos_filtrados
        return instancia
