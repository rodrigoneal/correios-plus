from typing import Literal


class Campo:
    UF: Literal["uf"] = "uf"
    BAIRRO: Literal["bairro"] = "bairro"
    LOGRADOURO: Literal["logradouro"] = "logradouro"
    LOCALIDADE: Literal["localidade"] = "localidade"
    CEP: Literal["cep"] = "cep"


class Tipo:
    TUDO: Literal["ALL"] = "ALL"
    LOCALIDADE: Literal["LOG"] = "LOG"
    LOGRADOURO: Literal["LOG"] = "LOG"
    CEP_PROMOCIONAL: Literal["PRO"] = "PRO"
    CAIXA_POSTAL_COMUNITARIA: Literal["CPC"] = "CPC"
    GRANDE_USUARIO: Literal["GRU"] = "GRU"
    UNIDADE_OPERACIONAL: Literal["UOP"] = "UOP"


TipoType = Literal["ALL", "LOG", "PRO", "CPC", "GRU", "UOP"]
CampoType = Literal["uf", "bairro", "logradouro", "localidade", "cep"]
